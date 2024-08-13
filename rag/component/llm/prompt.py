from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableLambda

translation_prompt_template = """
You are an assistant for {user_lang}-{source_lang} translation tasks.

I will give you a sentence.
If the sentence is already written in {source_lang}, just copy the sentence.
If not, please translate the sentence from {user_lang} to {source_lang}.

You should say only the translation of the sentence, and do not say any additional information.

<sentence>
{sentence}
</sentence>

Translation:
"""
translation_prompt = ChatPromptTemplate.from_template(translation_prompt_template).partial(user_lang="Korean", source_lang="English")

rewrite_prompt_template = """
You are an assistant for question-revision tasks.
Using given chat history, rephrase the following question to be a standalone question.
The standalone question must have main words of the original question.
Write the revised question in {lang}.

<chat-history>
{history}
</chat-history>

<question>
{query}
</question>

Revised question:
"""
rewrite_prompt = ChatPromptTemplate.from_template(rewrite_prompt_template).partial(lang="English")

expansion_prompt_template = """
Your task is to expand the given query, considering the chat history.
Generate {n} queries that are related to the given query and chat history.

You should provide the queries in {lang}.

All the queries should be separated by a newline.
Do not include any additional information. Only provide the queries.

<chat-history>
{history}
</chat-history>

<question>
{query}
</question>

Queries:
"""
expansion_prompt = ChatPromptTemplate.from_template(expansion_prompt_template).partial(n=3, lang="English")

# restrict the number of sentences to 3, to improve response latency
hyde_prompt_template = """
You are an assistant for question-answering tasks.
Please write a passage to answer the question, considering the given chat history.
Even though you cannot find the context in the chat history, you should generate a passage to answer the question.
Write the answer in {lang}.

Use up to {n} sentences to answer the question.

<chat-history>
{history}
</chat-history>

<question>
{query}
</question>

Answer:
"""
hyde_prompt = ChatPromptTemplate.from_template(hyde_prompt_template).partial(n=3, lang="English")

generation_prompt_template = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question considering the chat history.

Context can have specific features that are related to the question.
You should consider the context features to answer the question.
If context features are not given, you can ignore them.

Think step by step to find the answer.

If you don't know the answer, just say that you don't know.

You can answer in descriptive form or paraphrased form if you want, and keep the answer concise.

You should answer with the reference to the documents.
When you reference the documents, you should provide the exact title of the document.
Feel free to use markdown to format your answer.

You should answer in {lang}. Keep proper nouns, or any other specialized terms as they are.

<context-features>
{context_features}
</context-features>

<context>
{context}
</context>

<chat-history>
{history}
</chat-history>

<question>
{query}
</question>

Answer (in {lang}):
"""
generation_prompt = ChatPromptTemplate.from_template(generation_prompt_template).partial(lang="English", context_features="")

few_shot_example_prompt = PromptTemplate(
    input_variables=["history", "query", "answer"],
    template="<example>\n<chat-history>{history}</chat-history>\n<question>{query}</question>\n<answer>{answer}</answer>\n</example>"
)

few_shot_prompt_prefix = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question considering the chat history.

Context can have specific features that are related to the question.
You should consider the context features to answer the question.
If context features are not given, you can ignore them.

Think step by step to find the answer.

If you don't know the answer, just say that you don't know.

You can answer in descriptive form or paraphrased form if you want, and keep the answer concise.

You should answer with the reference to the documents.
When you reference the documents, you should provide the exact title of the document.
Feel free to use markdown to format your answer.

You should answer in {lang}. Keep proper nouns, or any other specialized terms as they are.

---------------------------------------
<examples>
<context>
{example_context}
</context>

"""

few_shot_prompt_suffix = """

</examples>
---------------------------------------

<context-features>
{context_features}
</context-features>

<context>
{context}
</context>

<chat-history>
{history}
</chat-history>

<question>
{query}
</question>

Answer (in {lang}):
"""

def generate_few_shot_prompt_from(
    example_context: str, context_features: str, examples: list[dict]
) -> FewShotPromptTemplate:
    few_shot_prompt = FewShotPromptTemplate(
        examples = examples,
        example_prompt = few_shot_example_prompt,
        prefix = few_shot_prompt_prefix,
        suffix = few_shot_prompt_suffix,
        input_variables = ["context", "example_context", "context_features", "history", "query", "lang"]
    )
    return few_shot_prompt.partial(example_context=example_context, context_features=context_features)



verification_prompt_template = """
Given context, verify the fact in the response.
You should also provide the reasoning for the verification.
Write the response in json format, with the following keys: "verification", "reasoning".
"verification" should be a boolean value that indicates whether the response is correct or not.
"reasoning" should be a string that explains the reason for the verification.

Write the reasoning in {lang}. Keep proper nouns, or any other specialized terms as they are.

Context: {context}
Answer: {response}

Verification:
{{
    "verification": "<true/false>",
    "reasoning": "<reasoning>"
}}
"""
verification_prompt = ChatPromptTemplate.from_template(verification_prompt_template).partial(lang="English")