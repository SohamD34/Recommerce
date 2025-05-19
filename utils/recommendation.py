import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_rating_based_recommendations(train_data, top_n=10):
    """
    Generates a rating-based recommendation system.

    Parameters:
        train_data (pd.DataFrame): DataFrame containing training data with columns:
        top_n (int): Number of top-rated items to recommend. Default is 10.

    Returns:
        pd.DataFrame: DataFrame containing the top-rated items.
    """
    # Calculate average ratings grouped by relevant columns
    average_ratings = train_data.groupby(['Name', 'ReviewCount', 'Brand', 'ImageURL'])['Rating'].mean().reset_index()
    top_rated_items = average_ratings.sort_values(by='Rating', ascending=False)
    rating_base_recommendation = top_rated_items.head(top_n)

    # Convert Rating and ReviewCount to integers
    rating_base_recommendation['Rating'] = rating_base_recommendation['Rating'].astype(int)
    rating_base_recommendation['ReviewCount'] = rating_base_recommendation['ReviewCount'].astype(int)

    # Return the final recommendation DataFrame
    return rating_base_recommendation[['Name', 'Rating', 'ReviewCount', 'Brand', 'ImageURL']]




def get_content_based_recommendations(train_data, item_name, top_n=10):
    """
    Generates a content-based recommendation system using TF-IDF and cosine similarity.

    Parameters:
        train_data (pd.DataFrame): DataFrame containing training data with a 'Tags' column.
        item_name (str): Name of the item for which recommendations are to be generated.
        top_n (int): Number of similar items to recommend. Default is 10.

    Returns:
        pd.DataFrame: DataFrame containing the recommended items.
    """
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])

    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    item_index = train_data[train_data['Name'] == item_name].index[0]
    similar_items = list(enumerate(cosine_similarities_content[item_index]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)

    top_similar_items = similar_items[1:top_n + 1]
    recommended_items_indices = [x[0] for x in top_similar_items]

    return train_data.iloc[recommended_items_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL']]




def get_collaborative_filtering_recommendations(train_data, target_user_id, top_n=10):
    """
    Generates a collaborative filtering recommendation system using user-item interactions.

    Parameters:
        train_data (pd.DataFrame): DataFrame containing training data with columns:
        target_user_id (int): ID of the target user for whom recommendations are to be generated.
        top_n (int): Number of similar items to recommend. Default is 10.

    Returns:
        pd.DataFrame: DataFrame containing the recommended items.
    """

    user_item_matrix = train_data.pivot_table(index='ID', columns='ProdID', values='Rating', aggfunc='mean').fillna(0)
    user_similarity = cosine_similarity(user_item_matrix)

    target_user_index = user_item_matrix.index.get_loc(target_user_id)
    user_similarities = user_similarity[target_user_index]

    similar_users_indices = user_similarities.argsort()[::-1][1:]


    recommended_items = []

    for user_index in similar_users_indices:
        rated_by_similar_user = user_item_matrix.iloc[user_index]
        not_rated_by_target_user = (rated_by_similar_user == 0) & (user_item_matrix.iloc[target_user_index] == 0)

        recommended_items.extend(user_item_matrix.columns[not_rated_by_target_user][:top_n])


    recommended_items_details = train_data[train_data['ProdID'].isin(recommended_items)][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]

    return recommended_items_details.head(10)




def hybrid_recommendations(train_data,target_user_id, item_name, top_n=10):
    """
    Generates hybrid recommendations by combining content-based and collaborative filtering methods.

    Parameters:
        train_data (pd.DataFrame): DataFrame containing training data with columns:
        target_user_id (int): ID of the target user for whom recommendations are to be generated.
        item_name (str): Name of the item for which recommendations are to be generated.
        top_n (int): Number of similar items to recommend. Default is 10.

    Returns:
        pd.DataFrame: DataFrame containing the recommended items.
    """

    content_based_rec = get_content_based_recommendations(train_data,item_name, top_n)
    collaborative_filtering_rec = get_collaborative_filtering_recommendations(train_data,target_user_id, top_n)

    hybrid_rec = pd.concat([content_based_rec, collaborative_filtering_rec]).drop_duplicates()
    
    return hybrid_rec.head(10)