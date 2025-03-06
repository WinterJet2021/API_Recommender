# recommendation_app.py
from fastapi import FastAPI
from user_management_app import users  # Import user data from the User Management App

app = FastAPI()

@app.post("/recommend/")
def recommend(user_id: int, top_n: int = 5, location_filter: str = None):
    user = users.get(user_id)
    if not user:
        return {"message": "User not found"}
    
    # Filter users based on location
    recommended_users = [
        u for u in users.values() if u["location"] == location_filter or location_filter is None
    ]
    
    return {"recommendations": recommended_users[:top_n]}
