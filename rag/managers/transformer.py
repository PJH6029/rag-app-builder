from typing import Optional
from wasabi import msg

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnablePassthrough, RunnableParallel, RunnableLambda

from rag.component import llm, prompt
from rag.managers.base import BasePipelineManager
from rag.type import *

def split_lambda(x: str) -> list[str]:
    return list(filter(lambda x: bool(x), x.split("\n")))

class TransformerManager(BasePipelineManager):       
    def __init__(self) -> None:
        super().__init__()
        self.transformer_name = None
        self.enable = {}
        self.lang = "English"
     
    def set_config(self, config: dict):
        self.transformer_name = config.get("model")
        self.enable = config.get("enable", {})
        self.lang = config.get("language", "English")
        
        msg.info(f"Setting TRANSFORMER to {self.transformer_name}")
        
    def translate(self, sentence: str) -> str:
        if self.lang == "English":
            msg.warn("Translation not needed. Skipping translation.")
            return sentence
        
        transformer = llm.get_model(self.transformer_name)
        if transformer is None:
            return sentence
        
        chain = prompt.translation_prompt.partial(lang=self.lang) | transformer | StrOutputParser()
        return chain.invoke({"sentence": sentence})
    
    def transform(self, sentence: str, history: list[ChatLog]=None) -> TransformationResult:
        if self.transformer_name is None:
            msg.warn("Transformer not set. Skipping transformation.")
            return [sentence]

        history = history or []
        sentences: TransformationResult = {}
        
        chains = {}
        
        if self.enable.get("translation", False):
            sentence = self.translate(sentence)
            sentences["translation"] = sentence
        else:
            sentences["translation"] = sentence
        
        for key in ["rewriting", "expansion", "hyde"]:
            if not self.enable.get(key, False):
                continue
            
            chain = self.build_chain(key, temperature=0.9)
            
            if chain is not None:
                if key == "expansion":
                    chain = chain | RunnableLambda(split_lambda)
                chains[key] = chain
        
        parallel_chain = RunnableParallel(**chains)
        transformed_sentences = parallel_chain.invoke({"query": sentence, "history": history})
        for key, _sentence in transformed_sentences.items():
            sentences[key] = _sentence

        return sentences

    def build_chain(self, key: str, **model_kwargs: dict) -> Optional[Runnable]:
        prompts = {
            "rewriting": prompt.rewrite_prompt.partial(lang=self.lang),
            "expansion": prompt.expansion_prompt.partial(lang=self.lang),
            "hyde": prompt.hyde_prompt.partial(lang=self.lang),
        }
        transformer = llm.get_model(self.transformer_name, **model_kwargs)
        if transformer is None:
            return None
        
        chain = prompts[key] | transformer | StrOutputParser()
        
        return chain
    