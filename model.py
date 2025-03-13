def recommend_users(user_id, top_n=5, location_filter=None):
    # Ensure the user_id is valid
    if user_id not in df_users_scaled["User_ID"].values:  # Update 'UserID' to 'User_ID'
        return {"error": "User ID not found"}

    # Filter users based on location if provided
    if location_filter:
        df_users_filtered = df_users_scaled[df_users_scaled["Location"] == location_filter]
    else:
        df_users_filtered = df_users_scaled

    # Get the user data and exclude the current user
    user_data = df_users_filtered[df_users_filtered["User_ID"] == user_id][activity_columns]  # Update 'UserID' to 'User_ID'
    other_users = df_users_filtered[df_users_filtered["User_ID"] != user_id][activity_columns]  # Update 'UserID' to 'User_ID'
    
    # Calculate similarity scores using cosine similarity
    similarity_scores = cosine_similarity(user_data, other_users)
    similar_users_indices = similarity_scores.argsort()[0][-top_n:][::-1]

    recommended_users = df_users_filtered.iloc[similar_users_indices]["User_ID"].tolist()  # Update 'UserID' to 'User_ID'

    return {"user_id": user_id, "recommendations": recommended_users}
