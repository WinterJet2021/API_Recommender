import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from geopy.distance import geodesic

# Load dataset
file_path = "user_interests_1000_dataset.csv"  # Ensure the file is in the project folder
df_users = pd.read_csv(file_path)

# Define columns for activities
activity_columns = ["Basketball", "Yoga", "Hiking", "Cycling", "Gym", "Swimming", "Dancing", "Running", "Music", "Photography"]

# Normalize user interests and user scores
scaler = MinMaxScaler()
df_users_scaled = df_users.copy()
df_users_scaled[activity_columns] = scaler.fit_transform(df_users[activity_columns])
df_users_scaled["User Score"] = scaler.fit_transform(df_users[["User Score"]])

# Convert past matches from string representation to lists
df_users_scaled["Past Matches"] = df_users_scaled["Past Matches"].apply(lambda x: eval(x) if isinstance(x, str) else [])

def recommend_users(user_id, top_n=5, location_filter=None):
    """
    Recommend top_n users similar to the given user_id based on activity similarity.
    - Filters out past matches.
    - Optionally filters by location.
    """
    
    if user_id not in df_users_scaled["User_ID"].values:
        return {"error": "User ID not found"}
    
    # Get the user’s data
    user_row = df_users_scaled[df_users_scaled["User_ID"] == user_id]
    user_vector = user_row[activity_columns].values.reshape(1, -1)
    user_past_matches = user_row["Past Matches"].values[0]
    
    # Get other users
    other_users = df_users_scaled[df_users_scaled["User_ID"] != user_id]
    
    # Apply location filter if provided
    if location_filter:
        other_users = other_users[other_users["Location"] == location_filter]
    
    # Compute cosine similarity
    similarities = cosine_similarity(user_vector, other_users[activity_columns])
    other_users["Similarity"] = similarities[0]
    
    # Sort users by similarity & filter out past matches
    recommended_users = (
        other_users[~other_users["User_ID"].isin(user_past_matches)]
        .sort_values(by="Similarity", ascending=False)
        .head(top_n)
    )

    return {
        "user_id": user_id,
        "recommendations": recommended_users[["User_ID", "Location", "Similarity"]].to_dict(orient="records")
    }
