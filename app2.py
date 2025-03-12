from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from match_users import recommend_users
from typing import Optional
import os
import uvicorn

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://digitalnomadsync.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class MatchUsersRequest(BaseModel):
    user_id: int = Field(..., description="The unique ID of the user requesting matches")
    top_n: int = Field(5, ge=1, le=10, description="The number of matches to return (between 1 and 10)")
    location_filter: Optional[str] = Field(None, description="Optional filter to match users from a specific location")

# Define response model
class MatchUsersResponse(BaseModel):
    user_id: int
    matches: list
    message: str

@app.get("/")
def home():
    return {"message": "Welcome to the NomadSync Matchmaking API!"}

@app.post("/match-users/", response_model=MatchUsersResponse)
def match_users(request: MatchUsersRequest):
    try:
        result = recommend_users(request.user_id, request.top_n, request.location_filter)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return MatchUsersResponse(
            user_id=request.user_id,
            matches=result,
            message="Matches found successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Ensure Heroku Port Binding (Fixes R10 Boot Timeout)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, workers=1)
