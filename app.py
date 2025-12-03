from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Gemini API with key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Warning: GEMINI_API_KEY not found in .env file.")
else:
    genai.configure(api_key=api_key)

def get_gemini_prediction(text):
    """
    Sends text to Gemini AI to determine if it's real or fake news.
    Returns a tuple: (result_dict, error_message)
    """
    if not api_key:
        return None, "API Key missing"
        
    try:
        # Initialize the Gemini Pro model
        model = genai.GenerativeModel('gemini-pro')
        
        # Construct the prompt for the AI
        prompt = f"""
        Analyze the following news text and determine if it is Real or Fake.
        Provide a confidence score between 0 and 1 (where 1 is very confident).
        
        Text: "{text}"
        
        Respond ONLY with a JSON object in this format:
        {{
            "prediction": 0 or 1, (0 for Real, 1 for Fake)
            "probability": float (confidence that it is Fake, e.g. 0.95 for very likely Fake, 0.05 for very likely Real)
        }}
        """
        print(f"Sending request to Gemini for text: {text[:50]}...")
        
        # Get response from Gemini
        response = model.generate_content(prompt)
        print(f"Raw Gemini response: {response.text}")
        
        # Clean up response text to ensure it's valid JSON (remove markdown code blocks)
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
        elif response_text.startswith("```"):
            response_text = response_text[3:-3]
            
        # Parse the JSON response
        import json
        result = json.loads(response_text)
        print(f"Parsed result: {result}")
        return result, None
    except Exception as e:
        print(f"Error in get_gemini_prediction: {e}")
        return None, str(e)

@app.route('/')
def home():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to handle prediction requests."""
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Get prediction from Gemini
    result, error = get_gemini_prediction(text)
    
    if error:
        return jsonify({'error': error}), 500
        
    return jsonify(result)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
