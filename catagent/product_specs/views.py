from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers

import json
import requests
import urllib.request
from PIL import Image
#from statsmodels.sandbox.distributions.examples.matchdist import categ

from .utils import call_openai, extract_title_from_image, get_top_duckduckgo_images, fetch_html, extract_relevant, google_search, find_customer_questions


class GetSpecsView(APIView):
    """Single title/category endpoint"""
    def post(self, request):
        title = request.data.get('title')
        category = request.data.get('category')
        if not title or not category:
            return Response({'error': 'Both title and category are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch HTML content from DuckDuckGo
        # url = f"https://duckduckgo.com/html/?q={title}+{category}"
        # query = f'"{title} {category} product specifications"'
        # try:
        #     results = google_search(query, num_results=5)
        #     print(results)
        #     html_content = []
        #     for r in results:
        #         html_content += extract_relevant(fetch_html(r))
        #
        #     print(html_content[0])

            # prompt = (
            #     "You are a product-specs extraction assistant.\n"
            #     "Given these HTML snippet from some product pages, return a JSON object of the specs which buyers care when purchasing.\n"
            #     "The specs should be relevant to the category and title provided.\n"
            #     "You should not include professional specs such number of cores of cou. Instead focus on features like screen size, battery capacity, etc.\n"
            #     "Use snake_case keys, and only output JSON (no commentary).\n\n"
            #     f"{html_content}"
            # )

        # except requests.RequestException as e:
        #     return Response({'error': f'Failed to fetch HTML content: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        prompt = (f"""
                Given category "${category}", list the top 10 features buyers care about when purchasing a ${category}
                you should not include some features like price or wifi and Bluetooth standard, return features
                like screen size or battery capacity for mobile phones category, then provide values for "${title}".
                Output JSON: feature: value pairs only.
            """
        )
        specs = call_openai(prompt, system_prompt='You extract product specifications.', model='gpt-4.1-nano')

        desc_prompt = f"""
                        You are a helpful assistant. Summarize the for the following product into a clear, concise paragraph suitable for an online catalog.
                        Include key features, functionality, and important specifications. Avoid marketing or promotional language.
                        
                        Product: {title}
                        category: {category}
                        """
        desc = call_openai(desc_prompt, model='gpt-4.1-nano', system_prompt='You are a product description generator.')
        specs_json = json.loads(specs)
        images_url = get_top_duckduckgo_images({'find': 1, 'category': category, 'model': title})
        questions = find_customer_questions({'category': category, 'model': title})
        return Response({'title': title, 'category': category, 'specs': specs_json, 'images': images_url, 'description': desc, 'questions': questions}, status=status.HTTP_200_OK)


class ImageSpecsView(APIView):
    def post(self, request):
        url = request.data.get('url')
        json = extract_title_from_image(url)
        print(json)
        title = json.title
        category = json.category
        if not title or not category:
            return Response({'error': 'Could not extract title from image.'}, status=status.HTTP_400_BAD_REQUEST)

        body = {
            'title': title,
            'category': category
        }
        # Call GetSpecsView
        response = requests.request(url='http://localhost:8000/api/get-specs/', json=body, method='POST')
        return Response(response.json(), status=response.status_code)
