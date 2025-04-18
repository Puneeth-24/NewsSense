# --- Prerequisites ---
# Install necessary libraries:
# pip install selenium webdriver-manager transformers torch # or tensorflow instead of torch
# You might need to install Google Chrome if you don't have it.

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from transformers import pipeline # Hugging Face library

# --- Configuration ---

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Reduce verbosity of underlying libraries
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('transformers').setLevel(logging.ERROR) # Use ERROR or WARNING

# --- Functions ---

def get_rendered_page_text(url: str, wait_time: int = 5) -> str | None:
    """
    Fetches a URL using Selenium, waits for dynamic content,
    and extracts visible text from the body tag.

    Args:
        url: The URL of the webpage to scrape.
        wait_time: Seconds to wait for the page to render dynamic content.

    Returns:
        The extracted text content as a string, or None if an error occurs.
    """
    logging.info(f"Setting up headless Chrome browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without opening a browser window
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox") # Often needed in Linux environments
    chrome_options.add_argument("--window-size=1920,1080") # Set a reasonable window size
    # Use a common user agent to avoid basic bot detection
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Automatically download and manage the ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = None # Initialize driver

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info(f"Navigating to: {url}")
        driver.get(url)

        logging.info(f"Waiting {wait_time} seconds for JavaScript rendering...")
        time.sleep(wait_time) # Wait for dynamic content loading

        logging.info("Extracting text content from page body...")
        # Find the body element and get all text within it
        # NOTE: This grabs ALL text, including menus, footers, etc.
        # For better results, inspect the target page and use a more specific selector
        # e.g., driver.find_element(By.TAG_NAME, 'article').text
        # e.g., driver.find_element(By.ID, 'main-content').text
        body_element = driver.find_element(By.TAG_NAME, 'body')
        page_text = body_element.text
        logging.info(f"Successfully extracted text (length: {len(page_text)} chars).")
        return page_text

    except Exception as e:
        logging.error(f"An error occurred during Selenium operation: {e}")
        return None
    finally:
        if driver:
            logging.info("Closing browser.")
            driver.quit()

def summarize_text(text: str, model_name: str = "facebook/bart-large-cnn", max_input_length: int = 1024) -> str | None:
    """
    Summarizes the provided text using a Hugging Face transformer model.

    Args:
        text: The text content to summarize.
        model_name: The name of the pre-trained summarization model to use.
                    Examples: "facebook/bart-large-cnn", "google/pegasus-cnn_dailymail", "t5-small", "t5-base"
        max_input_length: The maximum number of tokens the model can handle (truncates if longer).

    Returns:
        The summarized text as a string, or None if an error occurs.
    """
    if not text or text.isspace():
        logging.warning("Input text is empty or whitespace. Cannot summarize.")
        return "Input text was empty."

    try:
        logging.info(f"Loading summarization pipeline with model '{model_name}'...")
        # device=0 uses GPU if available and configured, -1 uses CPU
        summarizer = pipeline("summarization", model=model_name, device=-1)
        logging.info("Summarization pipeline loaded.")

        # Handle potential model input length limits by truncating
        # For very long texts, more sophisticated chunking might be needed
        if len(text) > max_input_length * 4: # Rough estimate char to token
             logging.warning(f"Input text very long ({len(text)} chars). Truncating for summarization.")
             text_to_summarize = text[:max_input_length * 4] # Adjust multiplier as needed
        else:
             text_to_summarize = text

        logging.info("Generating summary...")
        # Adjust max_length and min_length for desired summary size
        summary_result = summarizer(text_to_summarize, max_length=200, min_length=50, do_sample=False)

        if summary_result and isinstance(summary_result, list):
            summary = summary_result[0]['summary_text']
            logging.info("Summary generated successfully.")
            return summary
        else:
            logging.error("Summarization pipeline did not return expected result format.")
            return None

    except Exception as e:
        logging.error(f"An error occurred during text summarization: {e}")
        # Provide more specific feedback if possible
        if "out of memory" in str(e).lower():
            return "Error: Summarization failed due to memory constraints. Try a smaller model or ensure sufficient RAM/VRAM."
        return f"Error: Could not generate summary. ({type(e).__name__})"


# --- Main Execution ---
if __name__ == "__main__":
    # ===> SET YOUR TARGET URL HERE <===
    target_url = "https://www.moneycontrol.com/news/" # Example URL

    print(f"--- Starting Process for URL: {target_url} ---")

    # 1. Get the rendered page text using Selenium
    page_content = get_rendered_page_text(target_url, wait_time=5) # Adjust wait_time if needed

    if page_content:
        # print("\n--- Extracted Text (First 500 Chars) ---")
        # print(page_content[:500] + "...\n") # Display a snippet

        # 2. Summarize the extracted text
        print("\n--- Generating Summary ---")
        summary = summarize_text(page_content)

        if summary:
            print("\n--- Generated Summary ---")
            print(summary)
        else:
            print("\n--- Failed to generate summary ---")
    else:
        print("\n--- Failed to retrieve content from the page ---")

    print(f"\n--- Process Finished for URL: {target_url} ---")