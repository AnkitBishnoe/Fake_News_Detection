import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_gemini_connection():
    print("Loading environment variables...")
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env file.")
        print("Please ensure you have created a .env file with GEMINI_API_KEY=your_key")
        return

    # Mask key for display
    masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "****"
    print(f"Found API Key: {masked_key}")

    print("Configuring Gemini...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        print("Sending test request...")
        response = model.generate_content("Say 'Hello, World!' if you can hear me.")
        
        print("\nSUCCESS! Gemini API responded:")
        print("-" * 20)
        print(response.text)
        print("-" * 20)
        
    except Exception as e:
        print("\nERROR: Failed to connect to Gemini API.")
        print(f"Details: {e}")

if __name__ == "__main__":
    test_gemini_connection()
