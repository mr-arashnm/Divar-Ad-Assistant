# Divar Ad Assistant

Divar Ad Assistant is an intelligent assistant for extracting and collecting product information from images, product names, and Excel files. It uses AI models and various APIs to identify products and gather their specifications. The assistant is designed to be easily integrated into any classified ads system via API.

## Supported Input Modes

1. **Image**: Upload a product image. The assistant analyzes the image, identifies the product type, brand, and model, and fetches detailed specifications.
2. **Product Name**: Provide a product name or title. The assistant searches for the product online and extracts its features and specifications.
3. **Excel File**: Upload an Excel file containing a list of product names or codes. The assistant processes each entry and returns structured product information.

## Input Formats

- **Image**: JPEG/PNG file or image URL.
- **Product Name**: Plain text string (e.g., "Galaxy A55").
- **Excel File**: XLSX file with a column for product names or codes.

## Main Workflow

1. **Receive Input**: Accepts image, product name, or Excel file.
2. **Product Identification**: Uses AI models (Gemini, GPT) to identify product details.
3. **Data Enrichment**: Searches the web and APIs for additional product specifications.
4. **Output**: Returns structured product information in JSON format, including category, brand, model, and key features.

## Integration

Divar Ad Assistant is designed to be API-friendly and can be integrated with any classified ads platform or system. You can use it to automate product listing, enrich ads with detailed specs, or assist users in posting accurate product information.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mr-arashnm/divar-ad-assistant.git
   cd divar_ad_assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your `.env` file with API keys:
   ```
   DIVAR_API_KEY=...
   METIS_API_KEY=...
   GOOGLE_API_KEY=...
   CSE_API_KEY=...
   ```


## Dependencies

- Python 3.9+
- [OpenAI](https://pypi.org/project/openai/)
- [google-generativeai](https://pypi.org/project/google-generativeai/)
- [ddgs](https://pypi.org/project/ddgs/)
- [requests](https://pypi.org/project/requests/)
- [Pillow](https://pypi.org/project/Pillow/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## License

This project is licensed under the MIT License.

