from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from model import recommend_users as demo_recommend_users  # Import demo model
from recommender import recommend_users as gemini_recommend_users  # Import Gemini-based recommender
from typing import Optional
import os

app = FastAPI()

# CORS Configuration - Restricting to specific domains for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://digitalnomadsync.com"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# -------------------------
# /recommend/ - Uses model.py (Demo Model)
# -------------------------

class RecommendRequest(BaseModel):
    user_id: int = Field(..., description="The unique ID of the user requesting recommendations")
    top_n: int = Field(5, ge=1, le=10, description="The number of recommendations to return (between 1 and 10)")
    location_filter: Optional[str] = Field(None, description="Optional filter to recommend users from a specific location")

class RecommendResponse(BaseModel):
    user_id: int
    recommendations: list
    message: str

@app.post("/recommend/", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    try:
        result = demo_recommend_users(request.user_id, request.top_n, request.location_filter)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        recommendations = result.get("recommendations", [])
        message = "Successfully retrieved recommendations" if recommendations else "No recommendations found"
        return RecommendResponse(
            user_id=request.user_id,
            recommendations=recommendations,
            message=message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# -------------------------
# /match-users/ - Uses recommender.py (Gemini API)
# -------------------------

class MatchUsersRequest(BaseModel):
    user_id: int = Field(..., description="The unique ID of the user requesting matches")
    top_n: int = Field(5, ge=1, le=10, description="The number of matches to return (between 1 and 10)")
    location_filter: Optional[str] = Field(None, description="Optional filter to match users from a specific location")

class MatchUsersResponse(BaseModel):
    user_id: int
    matches: list
    message: str

@app.post("/match-users/", response_model=MatchUsersResponse)
def match_users(request: MatchUsersRequest):
    try:
        result = gemini_recommend_users(request.user_id, request.top_n, request.location_filter)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        matches = result.get("recommendations", [])
        message = "Matches found successfully" if matches else "No matches found"
        return MatchUsersResponse(
            user_id=request.user_id,
            matches=matches,
            message=message
        )
    except ModuleNotFoundError as e:
        return {"error": "Google Gemini API module is missing. Ensure `google-generativeai` is installed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def home():
    return {"message": "Welcome to the NomadSync API!"}

# -------------------------
# Ensure Heroku Port Binding (Fixes R10 Boot Timeout)
# -------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
