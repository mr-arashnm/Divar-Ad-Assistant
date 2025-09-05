import google.generativeai as genai
import base64
from google.generativeai import types
import time
from PIL import Image
import io

query = []
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()


def extract_json_object(text):
    # Step 1: Remove json and ending
    cleaned = re.sub(r'^```json\s*|\s*```$', '', text.strip(), flags=re.MULTILINE)

    # Step 2: Convert the cleaned string to a Python dictionary
    try:
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return None


image_path = 'catagent/product_specs/image.jpg'

with open(image_path, "rb") as img_file:
    image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    query.append(image_base64)

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
        model="gemini-2.0-flash-lite",
        contents=[problem,
                  types.Part.from_bytes(data=q, mime_type="image/jpeg")])
    print(result := extract_json_object(response.text))
    print("-------------")
    time.sleep(1)