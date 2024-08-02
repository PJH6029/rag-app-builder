example_context = """
John and Mary are in the house.
In the kitchen, there is a cup.
John went to the bathroom.
Mary went to the kitchen.
Mary went to the garden.
John went to the kitchen.
Mary went to the bathroom.
They have a dog named Spot who is in the garden.
"""

context_features = """
People went around the house.

You should think step by step.
You first summarize who went where in time order.
And then you answer the question.
"""

examples = [
    {
        "query": "Who went bathroom first?",
        "history": "",
        "answer": """John first went to the bathroom, then Mary went to the bathroom. So, John went to the bathroom first."""
    },
    {
        "query": "If John didn't see the cup in the kitchen, who took it?",
        "history": "",
        "answer": """Mary went to the kitchen before John. So, Mary took the cup."""
    }
]