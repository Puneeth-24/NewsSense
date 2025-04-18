from flask import Flask, send_file, jsonify, url_for, request
import os
import io
import random
import string
from PIL import Image, ImageDraw
from flask_cors import CORS
import base64

# Import specific functions to avoid circular imports
from extract_company_name import (
    extract_company_name,
    get_ticker_yahoo,
    show_yesterdays_stock_change,
    plot_5_day_trend
)
from summarize_new import get_summary
from web_scraper import get_text_content

app = Flask(__name__)
# --- Initialize CORS ---
# This enables CORS for all domains on all routes.
# For production, you might want more specific origins: CORS(app, resources={r"/generate-image-data": {"origins": "http://your-frontend-domain.com"}})
CORS(app)

@app.route('/generate-image-and-data') # Changed route name for clarity
def generate_image_and_data_endpoint():
    try:
        # Get company data
        query = request.args.get('query', '')  # Get query from request
        company = extract_company_name(query)
        name, ticker = get_ticker_yahoo(company) if company else (None, None)
        percent = show_yesterdays_stock_change(ticker, name) if ticker else None

        # --- Prepare your dictionary ---
        my_dictionary = {
            "Name": name or "N/A",
            "ticker": ticker or "N/A",
            "percent": percent or "N/A", 
             "summary": get_summary(name) if name else "N/A",
            "status": "success" if ticker else "no_ticker_found"
        }

        # --- Generate the image object ---
        # Assuming plot_5_day_trend returns a PIL Image object or similar
        image_object = plot_5_day_trend(ticker,name) # Pass necessary data

        if image_object is None:
             raise ValueError("Image generation function returned None")

        # --- Save image to buffer and encode as Base64 ---
        buf = io.BytesIO()
        image_object.save(buf, format='PNG')
        # No plt.close() needed if image_object is PIL Image,
        # but if plot_5_day_trend uses plt directly, ensure plt.close() is called inside it.
        buf.seek(0)
        image_bytes = buf.getvalue()
        base64_image_string = base64.b64encode(image_bytes).decode('utf-8')

        # --- Combine dictionary and image string in JSON response ---
        response_data = {
            "success": True,
            "dictionaryData": my_dictionary,
            "imageData": base64_image_string # Include Base64 string here
        }
        return jsonify(response_data)

    except Exception as e:
        print(f"Error generating image and data: {e}")
        # It's good practice to return JSON even for errors
        return jsonify({"success": False, "error": f"Internal server error: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)