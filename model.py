from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from model import recommend_users
from typing import Optional
import os

app = FastAPI()

# CORS Configuration - Allowing requests from your domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://digitalnomadsync.com"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Define the request model
class RecommendRequest(BaseModel):
    user_id: int = Field(..., description="The unique ID of the user requesting recommendations")
    top_n: int = Field(5, ge=1, le=10, description="The number of recommendations to return (between 1 and 10)")
    location_filter: Optional[str] = Field(None, description="Optional filter to recommend users from a specific location")

# Define a response model to standardize the responses
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
        # Call the recommend_users function to get recommendations
        result = recommend_users(request.user_id, request.top_n, request.location_filter)

        # Check if there was an error in the result from the model
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        # Construct a successful response
        recommendations = result.get("recommendations", [])
        message = "Successfully retrieved recommendations" if recommendations else "No recommendations found"
        return RecommendResponse(
            user_id=request.user_id,
            recommendations=recommendations,
            message=message
        )
    except Exception as e:
        # Catch any unforeseen errors and return a generic error message
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Ensure Heroku Port Binding
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
