import google.generativeai as genai
import pandas as pd
import json  # Import JSON for proper parsing

# Configure Google Gemini API
genai.configure(api_key="AIzaSyATtsrK61pPdCSpUeZRXlTee5TAePM6--M")  # Ensure this is valid

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
    """
    Recommend users with similar interests using Google Gemini API.

    Args:
        user_id (int): The ID of the user requesting recommendations.
        top_n (int): The number of recommendations to return.
        location_filter (str, optional): Filter recommendations by location.

    Returns:
        dict: A dictionary containing recommended users or an error message.
    """

    # Get the user's profile
    user_profile = get_user_profile(user_id)
    if not user_profile:
        return {"error": "User not found"}

    # Correct model name (Gemini API)
    model_name = "gemini-1.5-pro"  # ✅ Fixed model name

    # Generate a recommendation prompt
    prompt = f"""
    Given the following user profile, find the top {top_n} most compatible users.

    User Profile:
    {user_profile}

    Consider shared interests, availability, and compatibility.
    If location filtering is provided, prioritize users from {location_filter}.

    Return a JSON object with:
    - List of top {top_n} recommended users.
    - Compatibility scores (1-100).
    - A short explanation for each match.
    """

    try:
        # Use Gemini API
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        if response and response.text:
            try:
                # Try parsing response as JSON
                recommendations_json = json.loads(response.text)

                # Check if the response contains a list of recommendations
                if isinstance(recommendations_json, dict) and "recommendations" in recommendations_json:
                    recommendations = recommendations_json["recommendations"]
                elif isinstance(recommendations_json, list):
                    recommendations = recommendations_json
                else:
                    recommendations = []  # Default to empty list if unexpected format

                return {"recommendations": recommendations}

            except json.JSONDecodeError:
                return {"error": "Invalid JSON response from Gemini API."}
        else:
            return {"error": "No recommendations generated."}

    except Exception as e:
        return {"error": f"Gemini API error: {str(e)}"}
