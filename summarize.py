
import google.generativeai as genai
import os
import webScraping as ws

# Configure the API key
def configure_api():
    try:
        api_key = "AIzaSyCVKGAOgmBiHXS3yKaC4oAff5_TF-zF8EI"  # Store your API key in environment variable
        if not api_key:
            raise ValueError("API key not found. Please set GEMINI_API_KEY environment variable.")
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Error configuring API: {e}")
        exit(1)

# Read content from text file
# def read_text_file(file_path):
#     try:
#         with open(file_path, 'r', encoding='cp1252') as file:
#             content = file.read()
#         if not content.strip():
#             raise ValueError("The input file is empty.")
#         return content
#     except FileNotFoundError:
#         print(f"Error: File '{file_path}' not found.")
#         exit(1)
#     except Exception as e:
#         print(f"Error reading file: {e}")
#         exit(1)



# Summarize content using Gemini API
def summarize_content(content,name):
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Create prompt for summarization
        prompt = (
            "just start with the summarization directly and dont mention about starting the summary and  give the below asked in bullets points with appropriate headings"
            "summarize me all the below information 200 words"
            f"what is affecting the {name} stock to go up or down "
            "when can we expect it the stock to go up "
            "what other stocks will be affected by this positively or negetively\n\n"
            f"{content}"
        )
        
        # Generate summary
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 350
            }
        )
        
        # Check if response is valid
        if not response.text:
            raise ValueError("No summary generated by the model.")
        
        return response.text
    
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None

# Main function
def main_summarizer(name):
    # Configure API
    configure_api()
    
    # Specify the input text file
    
    # image,name,ticker=ecn.main_flow_extract_name()
    # Read the file
    content = ws.get_text_content(name)
    
    # Generate summary
    
    summary = summarize_content(content,name)
    
    # Output the summary
    if summary:
        print("Summary generated successfully.")
        print(summary)
    else:
        print("Failed to generate summary.")
    
    return summary


