import os
from dotenv import load_dotenv
from ddgs import DDGS
import requests
import re
import json
from googleapiclient.discovery import build
import google.generativeai as genai
import base64
from google.generativeai import types
from PIL import Image
import io

load_dotenv()

METIS_URL = "https://api.tapsage.com/openai/v1"
METIS_API_KEY = os.getenv('METIS_API_KEY')

import google.generativeai as genai
import base64
from google.generativeai import types
import time
from PIL import Image
import io
import requests
from io import BytesIO
import json
import re

def extract_title_from_image(image_url):
    query=[]

    def download_and_encode_image(url):
        response = requests.get(url)
        response.raise_for_status()
        return base64.b64encode(response.content).decode("utf-8")

    query=[download_and_encode_image(image_url)]

    def extract_json_object(text):
        # Step 1: Remove ```json and ending
        cleaned = re.sub(r'^```json\s*|\s*```$', '', text.strip(), flags=re.MULTILINE)

        # Step 2: Convert the cleaned string to a Python dictionary

        try:
            print(cleaned)
            data = json.loads(cleaned)
            return data
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return None


    # image_path = '6-2.jpg'

    # with open(image_path, "rb") as img_file:

    #         image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    #         query.append(image_base64)


    kalas = ["tv-projection", 'camera', 'phone']
    problem = f'''what is product type exactly search its models and brand from photo if need send the company and product id.
        seach in net and send all property from this product in persian and sefrence od data (site) return json like {{
          "find":1,
          "category":"phone",
          "brand":"panasonic",
          "model":"KX-TS16754",
          "comment":""
        }} 
        if dont find this product in net find=0 and strings be empty just json no more sentence if you not find just put find 0 
        and send json and put other sentence in comment and just return a json file. 
        if the model isnt in {kalas} set find=0 we dont whant to find kalas are not in list'''
    client = genai.Client(api_key="AIzaSyBq3zjZ5zum11mJG6YN-oTdPS3znhJ51jE")

    for q in query:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[problem,
                      types.Part.from_bytes(data=q, mime_type="image/jpeg")])
        return extract_json_object(response.text)


def call_openai(prompt, system_prompt, model):
    from openai import OpenAI

    client = OpenAI(base_url=METIS_URL, api_key=METIS_API_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()


def get_top_duckduckgo_images(product_data: dict, max_images: int = 5) -> list:
    if product_data.get("find") != 1:
        print("Search not requested.")
        return []

    category = product_data.get("category", "")
    brand = product_data.get("brand", "")
    model = product_data.get("model", "")

    search_query = f"{brand} {model} {category}".strip()

    images = []
    with DDGS() as ddgs:
        results = ddgs.images(search_query, max_results=20)  # Fetch more to sort from

        for result in results:
            try:
                width = int(result.get("width", 0))
                height = int(result.get("height", 0))
                resolution = width * height
                images.append({
                    "url": result["image"],
                    "width": width,
                    "height": height,
                    "resolution": resolution
                })
            except (TypeError, ValueError):
                continue

    # Sort images by resolution in descending order
    sorted_images = sorted(images, key=lambda x: x["resolution"], reverse=True)

    # Return top N image URLs
    return [img["url"] for img in sorted_images[:max_images]]


def fetch_html(url):
    return requests.get(url, timeout=5).text


def google_search(query: str, num_results: int = 5):
    """Return top result URLs for a given query."""
    service = build("customsearch", "v1", developerKey=os.getenv('GOOGLE_API_KEY'))
    res = service.cse().list(
        q=query,
        cx=os.getenv('CSE_API_KEY'),
        num=num_results,
    ).execute()
    return [item["link"] for item in res.get("items", [])]



def extract_relevant(html):
    # crude way to grab the specs table
    match = re.search(r'(<table[^>]+specs[^>]*>.*?</table>)', html, re.S)
    return match.group(1) if match else html[:50000]  # fallback to first 50k chars

def find_customer_questions(product_json: dict) -> list:
    prompt = f"""
You are a market research assistant. Your task is to find the top 5 real customer questions that people ask online about this product.

Product details:
- Category: {product_json.get("category", "")}
- Model: {product_json.get("model", "")}

Return the result in this JSON format:

{{
  "customer_questions": [
    "Question 1?",
    "Question 2?",
    "Question 3?",
    "Question 4?",
    "Question 5?"
  ]
}}
"""

    content = call_openai(prompt, model='gpt-4.1-nano', system_prompt='You are a customer questions generator.')

    try:
        import json
        data = json.loads(content)
        return data["customer_questions"]
    except Exception as e:
        print("Failed to parse response as JSON:", e)
        return content