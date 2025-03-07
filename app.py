from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model import recommend_users

app = FastAPI()

# Allow cross-origin requests from your WordPress site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or you can specify your WordPress domain here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define the request model
class RecommendRequest(BaseModel):
    user_id: int
    top_n: int = 5
    location_filter: str = None  # Optional location filter

@app.get("/")
def home():
    return {"message": "Welcome to the Recommendation API!"}

@app.post("/recommend/")
def recommend(request: RecommendRequest):
    return recommend_users(request.user_id, request.top_n, request.location_filter)
