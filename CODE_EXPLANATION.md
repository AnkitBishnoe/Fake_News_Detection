# Fake News Detection Project Explanation

This project uses **Google's Gemini AI** to analyze news articles and determine if they are Real or Fake.

## How It Works

### 1. The Backend (`app.py`)
This is the core of the application, built with **Flask** (a Python web framework).

-   **Setup**: It loads the API key from the `.env` file and configures the Google Gemini library.
-   **`get_gemini_prediction(text)`**:
    -   This function takes the news text as input.
    -   It creates a **prompt** for Gemini, asking it to classify the text and provide a confidence score.
    -   It specifically asks for the response in **JSON format** so the code can easily read it.
    -   It cleans up the response (removing any markdown formatting) and parses it into a Python dictionary.
-   **Routes**:
    -   `/`: Serves the `index.html` page (the user interface).
    -   `/predict`: An API endpoint that accepts POST requests. It receives the text from the frontend, calls `get_gemini_prediction`, and returns the result as JSON.

### 2. The Frontend (`templates/index.html`)
This is the user interface where you paste the news.

-   **HTML**: Provides a text area for input and a button to check the news.
-   **JavaScript**:
    -   When you click "Check News", the `predict()` function runs.
    -   It sends the text to the backend (`/predict`) using the `fetch` API.
    -   It waits for the response and then updates the page to show "FAKE NEWS" (in red) or "REAL NEWS" (in green) along with the confidence score.
    -   It also includes error handling to alert you if something goes wrong (like an invalid API key).

### 3. Configuration (`.env`)
-   This file stores your sensitive **API Key**. It is kept separate from the code for security.
-   **Important**: You must replace `your_api_key_here` with your actual key from Google AI Studio.

### 4. Dependencies (`requirements.txt`)
-   Lists all the Python libraries needed to run the project (`flask`, `google-generativeai`, `python-dotenv`).

---

## Summary of Flow
1.  User pastes text in Browser -> Click "Check News".
2.  Browser sends text to Flask Server (`app.py`).
3.  Flask Server sends text + Prompt to Google Gemini API.
4.  Gemini AI analyzes text and returns JSON (Prediction + Probability).
5.  Flask Server sends JSON back to Browser.
6.  Browser displays the result to the User.
