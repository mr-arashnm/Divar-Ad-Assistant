from requests import request
from dotenv import load_dotenv
import os
from openai import OpenAI
from selenium.webdriver.common.devtools.v85.debugger import restart_frame

load_dotenv()

api_key = os.getenv('DIVAR_API_KEY')

def fetch_tags(category) -> list[str]:
    url = 'https://open-api.divar.ir/v2/open-platform/finder/post'
    headers = {'x-api-key': api_key}
    payload = {
        'city': 'tehran',
        'category': category
        # 'query': {k: v for k, v in query.items() if v is not None}
    }
    # remove keys with None values
    payload = {k: v for k, v in payload.items() if v is not None}

    response = request('POST', url, headers=headers, json=payload)
    if response.status_code == 200:
        items = response.json().get('posts')
        result = []
        for item in items:
            result.append(item.get('token'))
        return result[0]
    response.raise_for_status()

def get_features(tag, blacklist=['description', 'images', 'price', 'title', 'status']):
    url = f'https://open-api.divar.ir/v1/open-platform/finder/post/{tag}'
    headers = {'x-api-key': api_key}
    response = request('GET', url, headers=headers)
    features = response.json().get('data')
    for item in blacklist:
        if item in features.keys():
            del features[item]
    result = []
    for feature, value in features.items():
        result.append((feature, type(value)))
    return result

print(get_features('gZwrhVbU', ['description', 'images', 'price', 'title', 'status']))
# print(fetch_tags('mobile-phones'))
