import os
from dotenv import load_dotenv
import json

from openai import OpenAI
from sympy.codegen.cnodes import struct

from divar_api import get_features, fetch_tags, api_key

load_dotenv()

# llm = ChatOpenAI(
#     base_url='https://api.metisai.ir/openai/v1',
#     api_key=os.getenv('METIS_API_KEY'),
#     model_name="gpt-4o-mini",
#     temperature=0.1,
#     max_tokens=1000
# )
#
# def nothing():
#     pass
#
# tools = [
#     # Tool(
#     #     name='get products tags to search for products in divar',
#     #     func=fetch_tags,
#     #     description='Fetch tags for a given category. Returns a tag that can be used to search for products in Divar.',
#     # ),
#     # Tool(
#     #     name='get features key and their type, of a product by tag',
#     #     func=get_features,
#     #     description='Get features of a product by its tag. Returns a list of features and their type that can be used to describe the product.'
#     # )
#     Tool(
#         name='nothing',
#         func=nothing,
#         description='it does nothing'
#     )
# ]
#
# agent = initialize_agent(
#     # tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

agent = OpenAI(base_url='https://api.metisai.ir/openai/v1', api_key=os.getenv('METIS_API_KEY'))

title = 'Galaxy A55'
category = 'mobile-phones'
prompt = f"find the features of {title} in category {category}. You should trim those features that may be specific for just a product such as camera status or display status. Also, You may need to add some features that are not in the product but are common for all products in this category, such as battery capacity or RAM size. You should return a list of features and their type, such as (feature_name, feature_type) and title of the product. For example: title: {title}, features: ('battery_capacity', int), ('ram_size', int), .... You should return the result in a json format with keys 'title' and 'features'. Note that you don't have any tool and you should generate the result based on your knowledge and experience. You should not use any external tools or APIs to fetch the data. The result should be a valid json format."
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that provides product features based on the title and category."
    },
    {
        "role": "user",
        "content": prompt
    }
]

raw_prompt2 = agent.chat.completions.create(model='gpt-4.1-nano', messages=messages, temperature=0.5)
print(raw_prompt2)


# Set up client with your custom provider and API key
client = OpenAI(
    api_key=os.getenv('METIS_API_KEY'),
    base_url="https://api.tapsage.com/openai/v1"
)
#todo
def summarize_product_description(description: str) -> str:
    prompt = f"""
You are a helpful assistant. Summarize the following product description into a clear, concise paragraph suitable for an online catalog.
Include key features, functionality, and important specifications. Avoid marketing or promotional language.

Product description:
\"\"\"
{description}
\"\"\"

Summary:
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.5
    )

    return response.choices[0].message.content.strip()

#todo
def product_feautures(description: str) -> str:
    prompt = f"""
here are the feautrues I need to know for following product.
\"\"\"
{description}
\"\"\"
fill them for my online catalog, all features you get should be filled with a real value
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0
    )

    return response.choices[0].message.content.strip()

# Example usage
# if __name__ == "__main__":
#     raw_description = """
#     The Sony WH-1000XM5 wireless headphones silver.
#     """
#     req_feature = """
#     volume,
#     battery_life,
#     wirless
#     """
#     summary = summarize_product_description(raw_description)
#     feauture = product_feautures(raw_description, req_feature)
#     print(summary)
#     print(feauture)

print(product_feautures(raw_prompt2))
