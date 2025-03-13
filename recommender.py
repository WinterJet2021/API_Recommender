import google.generativeai as genai
import pandas as pd
import json

# Configure Google Gemini API
genai.configure(api_key="AIzaSyATtsrK61pPdCSpUeZRXlTee5TAePM6--M")

# Load user data from CSV
DATA_FILE = "user_interests_1000_dataset.csv"
df = pd.read_csv(DATA_FILE)

def get_user_profile(user_id):
    """Retrieve user profile from dataset based on user_id."""
    user_data = df[df["User_ID"] == user_id].to_dict(orient="records")
    if not user_data:
        return None
    return user_data[0]

def recommend_users(user_id, top_n=5, location_filter=None):
    """Recommend users with similar interests using Google Gemini API."""
    
    # Get the user's profile
    user_profile = get_user_profile(user_id)
    if not user_profile:
        return {"error": "User not found"}

    # Generate a recommendation prompt for Gemini API
    prompt = f"""
    Given the following user profile, find the top {top_n} most compatible users.

    User Profile:
    {json.dumps(user_profile, indent=2)}

    Consider shared interests, availability, and compatibility.
    If location filtering is provided, prioritize users from {location_filter}.

    Return a JSON object with:
    - List of top {top_n} recommended users.
    - Compatibility scores (1-100).
    - A short explanation for each match.
    """

    # Use Gemini API (Corrected)
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        # Ensure the response is valid
        if response and hasattr(response, "text") and response.text:
            try:
                recommendations = json.loads(response.text)
                return {"recommendations": recommendations}
            except json.JSONDecodeError:
                return {"error": "Invalid JSON response from Gemini API."}
        else:
            return {"error": "No recommendations generated."}

    except Exception as e:
        return {"error": f"Google Gemini API Error: {str(e)}"}
