from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from model import recommend_users  # Import the function from model.py
from typing import Optional

app = FastAPI()

# CORS Configuration - Allow all domains for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class RecommendRequest(BaseModel):
    user_id: int = Field(..., description="The unique ID of the user requesting recommendations")
    top_n: int = Field(5, ge=1, le=10, description="The number of recommendations to return (between 1 and 10)")
    location_filter: Optional[str] = Field(None, description="Optional filter to recommend users from a specific location")

# Define a response model
class RecommendResponse(BaseModel):
    user_id: int
    recommendations: list
    message: str

@app.get("/")
def home():
    return {"message": "Welcome to the Recommendation API!"}

@app.post("/recommend/", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    try:
        result = recommend_users(request.user_id, request.top_n, request.location_filter)

        # If the function returns an error
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        # Return recommendations
        return RecommendResponse(
            user_id=request.user_id,
            recommendations=result.get("recommendations", []),
            message="Successfully retrieved recommendations"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
