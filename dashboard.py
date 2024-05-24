import streamlit as st
import pandas as pd
from pyhive import hive
import plotly.express as px

# Function to get data from Hive
@st.cache_data
def get_data(query):
    conn = hive.Connection(host='localhost', port=10000, username='hive')
    cursor = conn.cursor()
    cursor.execute('USE movie_db')  # Set the database
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    conn.close()
    return df

# Streamlit App
st.title('MovieLens Dashboard')

# Top Movies
st.header('Top Movies')
top_movies_query = "SELECT movieid, title, avg_rating FROM top_movies LIMIT 10"
top_movies_df = get_data(top_movies_query)
st.write(top_movies_df)

# Genre Popularity
st.header('Genre Popularity')
genre_popularity_query = "SELECT genre AS genre, count AS count FROM genre_popularity"
genre_popularity_df = get_data(genre_popularity_query)
fig = px.bar(genre_popularity_df, x='genre', y='count', title='Genre Popularity')
st.plotly_chart(fig)

# Top Movies by Genre
st.header('Top Movies by Genre')
selected_genre = st.selectbox('Select Genre', genre_popularity_df['genre'].unique())
top_movies_by_genre_query = f"""
SELECT movieid, title, avg_rating 
FROM top_movies_by_genre 
WHERE genre = '{selected_genre}'
LIMIT 10
"""
top_movies_by_genre_df = get_data(top_movies_by_genre_query)
st.write(top_movies_by_genre_df)

# User Activity
st.header('User Activity')
user_activity_query = "SELECT userId, rating_count, avg_rating FROM user_activity ORDER BY rating_count DESC LIMIT 10"
user_activity_df = get_data(user_activity_query)
fig = px.bar(user_activity_df, x='userid', y='rating_count', title='Top Active Users')
st.plotly_chart(fig)

# Show top users with number of ratings given
st.header('Top Users by Ratings Given')
top_users_query = "SELECT userid, rating_count FROM user_activity ORDER BY rating_count DESC LIMIT 10"
top_users_df = get_data(top_users_query)
st.write(top_users_df)

# User Profiles
st.header('User Profiles')
user_profiles_query = "SELECT userId, genre, avg_rating FROM user_profiles ORDER BY userId, genre"
user_profiles_df = get_data(user_profiles_query)
st.write(user_profiles_df)

# Movie Trends
st.header('Movie Trends Over Time')
movie_trends_query = "SELECT year, genre, count FROM movie_trends"
movie_trends_df = get_data(movie_trends_query)
fig = px.line(movie_trends_df, x='year', y='count', color='genre', title='Movie Trends Over Time')
st.plotly_chart(fig)

# Seasonal Effects
st.header('Seasonal Effects on Ratings')
seasonal_effects_query = "SELECT month, count FROM seasonal_effects"
seasonal_effects_df = get_data(seasonal_effects_query)
fig = px.bar(seasonal_effects_df, x='month', y='count', title='Seasonal Effects on Ratings')
st.plotly_chart(fig)


# Genre Recommendations
st.header('Genre Recommendations')
user_id = st.number_input('Enter User ID for Recommendations', min_value=1)
if st.button('Get Recommendations'):
    genre_recommendations_query = f"""
    SELECT genre, movieId, predicted_rating 
    FROM genre_recommendations 
    WHERE userId = {user_id}
    ORDER BY predicted_rating DESC
    LIMIT 10
    """
    genre_recommendations_df = get_data(genre_recommendations_query)
    st.write(genre_recommendations_df)

# Start Streamlit app
# if __name__ == '__main__':
#     st.run()
