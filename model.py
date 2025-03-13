import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity
from geopy.distance import geodesic
from sklearn.preprocessing import MinMaxScaler

# Load dataset
file_path = "user_interests_1000_dataset.csv"  # Adjust the path if needed
df_users = pd.read_csv(file_path)

# Normalize user interest data
activity_columns = ["Basketball", "Yoga", "Hiking", "Cycling", "Gym", "Swimming", "Dancing", "Running", "Music", "Photography"]
scaler = MinMaxScaler()
df_users_scaled = df_users.copy()
df_users_scaled[activity_columns] = scaler.fit_transform(df_users[activity_columns])

# Define recommendation function
def recommend_users(user_id, top_n=5, location_filter=None):
    # Ensure the user_id is valid
    if user_id not in df_users_scaled["UserID"].values:
        return {"error": "User ID not found"}

    # Filter users based on location if provided
    if location_filter:
        df_users_filtered = df_users_scaled[df_users_scaled["Location"] == location_filter]
    else:
        df_users_filtered = df_users_scaled

    # Get the user data and exclude the current user
    user_data = df_users_filtered[df_users_filtered["UserID"] == user_id][activity_columns]
    other_users = df_users_filtered[df_users_filtered["UserID"] != user_id][activity_columns]
    
    # Calculate similarity scores using cosine similarity
    similarity_scores = cosine_similarity(user_data, other_users)
    similar_users_indices = similarity_scores.argsort()[0][-top_n:][::-1]

    recommended_users = df_users_filtered.iloc[similar_users_indices]["UserID"].tolist()

    return {"user_id": user_id, "recommendations": recommended_users}
