import google.generativeai as genai
import pandas as pd
import os

# ✅ Secure API Key Handling (Read from Environment Variable)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Google Gemini API key is missing. Set GEMINI_API_KEY in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Ensure Correct File Path for Heroku Deployment
DATA_FILE = os.path.join(os.path.dirname(__file__), "user_interests_1000_dataset.csv")

# ✅ Load Dataset Safely
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    raise FileNotFoundError(f"Dataset file '{DATA_FILE}' not found. Ensure it is included in the project.")

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

    # ✅ Get User Profile
    user_profile = get_user_profile(user_id)
    if not user_profile:
        return {"error": "User not found"}

    # ✅ Generate Recommendation Prompt for Gemini API
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

    # ✅ Call Gemini API
    try:
        response = genai.chat(model="gemini-pro", messages=[{"role": "user", "content": prompt}])
        return response.last
    except Exception as e:
        return {"error": f"Google Gemini API request failed: {str(e)}"}
