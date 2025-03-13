import pandas as pd

# Load dataset
df = pd.read_csv("user_interests_1000_dataset.csv")

def recommend_users(user_id: int, top_n: int = 5, location_filter: str = None):
    """
    Generate recommendations based on user interests.

    Args:
    - user_id (int): The ID of the user requesting recommendations.
    - top_n (int): The number of recommendations to return.
    - location_filter (str): Optional location-based filter.

    Returns:
    - dict: A dictionary with recommendations or an error message.
    """
    if user_id not in df['user_id'].values:
        return {"error": "User ID not found in the dataset"}

    # Filter by location if provided
    if location_filter:
        filtered_df = df[df['location'] == location_filter]
    else:
        filtered_df = df

    # Recommend users with the most similar interests (simple matching)
    user_interests = df[df['user_id'] == user_id].iloc[0, 1:]  # Exclude user_id column
    filtered_df['similarity'] = filtered_df.iloc[:, 1:].apply(lambda row: (user_interests == row).sum(), axis=1)

    # Get top N recommendations excluding the user themselves
    recommendations = filtered_df[filtered_df['user_id'] != user_id].nlargest(top_n, 'similarity')['user_id'].tolist()

    return {"recommendations": recommendations}
