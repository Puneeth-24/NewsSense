import google.generativeai as genai
from webScraping import get_text_content

class SummaryGenerator:
    def __init__(self):
        self.configured = False
        
    def configure_api(self):
        try:
            api_key = "AIzaSyCVKGAOgmBiHXS3yKaC4oAff5_TF-zF8EI"
            genai.configure(api_key=api_key)
            self.configured = True
            return True
        except Exception as e:
            print(f"Error configuring API: {e}")
            return False

    def generate_summary(self, company_name, content):
        if not self.configured and not self.configure_api():
            return "API configuration failed"

        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            prompt = f"""
            Provide a concise summary about {company_name} stock covering:
            1. Key factors affecting price movement
            2. Potential timing for upward trends
            3. Impact on related stocks
            
            {content}
            """
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 350
                }
            )
            return response.text if response.text else "No summary generated"
        
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Summary generation failed"

    def get_summary(self, company_name):
        content = get_text_content(company_name)
        if not content:
            return "No content available"
        return self.generate_summary(company_name, content)

# Create a module-level instance
summary_generator = SummaryGenerator()

# Alias for backward compatibility
get_summary = summary_generator.get_summary
