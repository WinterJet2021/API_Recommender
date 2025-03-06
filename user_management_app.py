# user_management_app.py
from fastapi import FastAPI

app = FastAPI()

# Fake user data for demonstration
users = {
    1: {"name": "John", "location": "Bangkok", "preferences": "Music, Travel"},
    2: {"name": "Alice", "location": "Phuket", "preferences": "Travel, Food"},
    # Add more users
}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return users.get(user_id, {"message": "User not found"})

@app.post("/users/")
def create_user(user_id: int, name: str, location: str, preferences: str):
    users[user_id] = {"name": name, "location": location, "preferences": preferences}
    return {"message": "User created successfully"}
