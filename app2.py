from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from recommender import recommend_users  # Import your recommend_users function
from typing import Optional
import os

app = FastAPI()

# CORS Configuration - Restricting to specific domains for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://digitalnomadsync.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class MatchUsersRequest(BaseModel):
    user_id: int = Field(..., description="The unique ID of the user requesting matches")
    top_n: int = Field(5, ge=1, le=10, description="The number of matches to return")
    location_filter: Optional[str] = Field(None, description="Optional filter to recommend users from a specific location")

# Define the response model
class MatchUsersResponse(BaseModel):
    user_id: int
    matches: list
    message: str

@app.post("/match-users/", response_model=MatchUsersResponse)
def match_users(request: MatchUsersRequest):
    try:
        # Call the recommend_users function to get recommendations from recommender.py
        result = recommend_users(request.user_id, request.top_n, request.location_filter)

        # Check if there was an error in the result from the model
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        # Return the successful response
        matches = result.get("recommendations", [])
        message = "Successfully retrieved matches" if matches else "No matches found"
        return MatchUsersResponse(
            user_id=request.user_id,
            matches=matches,
            message=message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def home():
    return {"message": "Welcome to the NomadSync Matchmaking API!"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))  # Use Heroku's dynamically assigned port
    uvicorn.run(app, host="0.0.0.0", port=port, workers=1)
