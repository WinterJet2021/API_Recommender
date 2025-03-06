# matchmaking_app.py
from fastapi import FastAPI
from recommendation_app import recommend

app = FastAPI()

@app.post("/match/")
def match(user_id: int, top_n: int = 5, location_filter: str = None):
    recommendations = recommend(user_id, top_n, location_filter)
    matched_users = recommendations["recommendations"]
    
    # Example logic for grouping users
    if len(matched_users) > 1:
        group = matched_users[:top_n]
        return {"message": f"Matched Group: {group}"}
    else:
        return {"message": "Not enough users to match!"}
