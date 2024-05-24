## Start Hadoop
Start Hadoop Cluster
```
start-all.sh

```
![Start Hadoop Cluster](img/start-all.png)

Check if Hadoop Cluster is running
```
jps

```
![Check if Hadoop Cluster is running](img/jps.png)

Hadoop is now running
![localhost:8088](img/localhost:8088.png)
![localhost:9870](img/localhost:9870.png)

## Start Hive
```
hive --service metastore
```
![metastore](img/hive-metastore.png)
```
 hive --service hiveserver2
```
![hiveserver2](img/hiveserver2.png)

Hive is now running at `localhost:10002`: 
![web-hive-running](img/web-hive-running.png)

## Start Spark
![Screenshot from 2024-05-23 19-57-43](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/c37eb3ed-ef67-41af-b822-153712f6cb62)

## Create database
![img/put-csv.png](img/put-csv.png)
![Screenshot from 2024-05-20 15-19-46](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/436ee464-24cd-4467-a084-0677663bfef7)

Create tables: 
```mysql
# Movies table
CREATE EXTERNAL TABLE movies (
  movieId INT,
  title STRING,
  genres STRING

)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = "\"",
  "escapeChar" = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/movielens/movies'
TBLPROPERTIES ("skip.header.line.count"="1");
```
```mysql
CREATE EXTERNAL TABLE ratings (
  userId INT,
  movieId INT,
  rating DOUBLE,
  rating_timestamp BIGINT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = "\"",
  "escapeChar" = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/movielens/ratings'
TBLPROPERTIES ("skip.header.line.count"="1");
```
```mysql
CREATE EXTERNAL TABLE tags (
  userId INT,
  movieId INT,
  tag STRING,
  tag_timestamp BIGINT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = "\"",
  "escapeChar" = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/movielens/tags'
TBLPROPERTIES ("skip.header.line.count"="1");
```
```mysql
CREATE EXTERNAL TABLE links (
  movieId INT,
  imdbId INT,
  tmdbId INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = "\"",
  "escapeChar" = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/movielens/links'
TBLPROPERTIES ("skip.header.line.count"="1");
```
![img/tables1.png](img/tables1.png)
![Screenshot from 2024-05-20 15-42-33](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/c07c4402-290f-4990-8577-4c71a27eb9ff)

## Running MAP-REDUCE queries
<!--
Simple Query example:
```mysql
SELECT movieId, AVG(rating) as avg_rating
FROM ratings
GROUP BY movieId
ORDER BY avg_rating DESC
LIMIT 10;
```
![Screenshot from 2024-05-23 18-54-56](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/2160008c-4d77-4967-a762-93681f6435a1)

![Screenshot from 2024-05-23 18-57-28](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/54363326-cfb5-46dc-a49c-fd115d19f23e)

![Screenshot from 2024-05-23 18-58-10](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/6101e03d-43d9-4e68-9870-d3f66d9d6a31)

-->
```mysql
CREATE TABLE avg_movie_ratings AS
SELECT movieId, AVG(rating) as avg_rating
FROM ratings
GROUP BY movieId;
```
![Screenshot from 2024-05-23 20-14-45](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/469c98e1-211d-45a9-8c75-dedcd263b954)

```mysql
CREATE TABLE top_movies AS
SELECT movieId, avg_rating
FROM avg_movie_ratings
ORDER BY avg_rating DESC;
```
![Screenshot from 2024-05-23 20-17-46](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/cff63dea-3bdc-4442-a4cd-4100c6ffde27)

```mysql
CREATE TABLE top_movies_by_genre AS
SELECT g.genre, m.movieId, m.title, AVG(r.rating) AS avg_rating
FROM movies m
JOIN movies_by_genre g ON m.movieId = g.movieId
JOIN ratings r ON m.movieId = r.movieId
GROUP BY g.genre, m.movieId, m.title
ORDER BY g.genre, avg_rating DESC;
```

```mysql
CREATE TABLE movies_by_genre AS
SELECT movieId, genre
FROM movies
LATERAL VIEW explode(split(genres, '[|]')) genreTable AS genre;
```
![Screenshot from 2024-05-23 21-10-04](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/4014fc9f-7283-4ba9-bc46-904b09d73969)

```mysql
CREATE TABLE user_activity AS
SELECT userId, COUNT(*) as rating_count, AVG(rating) as avg_rating
FROM ratings
GROUP BY userId;
```
![Screenshot from 2024-05-23 20-24-40](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/a21d7c8a-d689-45c5-839a-5373a5d1e2a4)
```mysql
CREATE TABLE genre_popularity AS
SELECT genre, COUNT(*) as count
FROM movies_by_genre
JOIN ratings ON movies_by_genre.movieId = ratings.movieId
GROUP BY genre;
```
![Screenshot from 2024-05-24 18-50-21](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/2396654f-b3b9-4bd0-81e7-535481cc6d55)

## Movie Recommendation System: Collaborative Filtering
```mysql
CREATE TABLE user_movie_matrix AS
SELECT userId, movieId, rating
FROM ratings;
```

### Movie Similarities (Collaborative Filtering)
```mysql
CREATE TABLE movie_similarities AS
SELECT m1.movieId AS movieId1, m2.movieId AS movieId2, 
       SUM(m1.rating * m2.rating) / (SQRT(SUM(m1.rating * m1.rating)) * SQRT(SUM(m2.rating * m2.rating))) AS similarity
FROM user_movie_matrix m1
JOIN user_movie_matrix m2 ON m1.userId = m2.userId AND m1.movieId != m2.movieId
GROUP BY m1.movieId, m2.movieId;
```
![Screenshot from 2024-05-24 18-46-48](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/e3183052-949e-4a8f-9130-3fd824ae2c44)

### Genre Similarities (Content-Based Filtering)
```mysql
CREATE TABLE genre_similarities AS
SELECT m1.movieId AS movieId1, m2.movieId AS movieId2, 
       COUNT(*) AS similarity
FROM movies_by_genre m1
JOIN movies_by_genre m2 ON m1.genre = m2.genre AND m1.movieId != m2.movieId
GROUP BY m1.movieId, m2.movieId;
```
![Screenshot from 2024-05-24 22-16-28](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/7d43671b-bfb3-4859-9fc7-9392eb85a896)

### Hybrid Similarities
```mysql
CREATE TABLE hybrid_similarities AS
SELECT c.movieId1, c.movieId2, (c.similarity + g.similarity) / 2 AS hybrid_similarity
FROM movie_similarities c
JOIN genre_similarities g ON c.movieId1 = g.movieId1 AND c.movieId2 = g.movieId2;
```
![Screenshot from 2024-05-24 22-17-16](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/a147d9a3-1147-4761-9cf6-f6e705f3450e)


### Trend Analysis
```mysql
CREATE TABLE movie_trends AS
SELECT YEAR(FROM_UNIXTIME(timestamp)) AS year, genre, COUNT(*) AS count
FROM ratings r
JOIN movies m ON r.movieId = m.movieId
JOIN movies_by_genre g ON m.movieId = g.movieId
GROUP BY year, genre;
```
![Screenshot from 2024-05-24 22-17-43](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/ed6a81e1-7649-46a8-9287-6d2842a97bc8)

### Seasonal Effects
```mysql
CREATE TABLE seasonal_effects AS
SELECT MONTH(FROM_UNIXTIME(CAST(rating_timestamp AS BIGINT))) AS month, COUNT(*) AS count
FROM ratings
GROUP BY MONTH(FROM_UNIXTIME(CAST(rating_timestamp AS BIGINT)));
```
![Screenshot from 2024-05-24 22-18-05](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/e2e36fd2-45a2-4adf-855d-5707b895af27)

###  User Clustering and Profiling
```mysql
CREATE TABLE user_profiles AS
SELECT userId, genre, AVG(rating) AS avg_rating
FROM ratings r
JOIN movies m ON r.movieId = m.movieId
JOIN movies_by_genre g ON m.movieId = g.movieId
GROUP BY userId, genre;
```
![Screenshot from 2024-05-24 22-18-24](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/4a3a9653-4acd-44c6-acda-f416300d87d4)

### User Engagement
```mysql
CREATE TABLE user_engagement AS
SELECT userId, COUNT(*) AS num_ratings, AVG(rating) AS avg_rating
FROM ratings
GROUP BY userId;
```
![Screenshot from 2024-05-24 22-18-53](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/31fb0562-4573-4eef-a098-1cf84ec26d05)

### Genre Recommendations
```mysql
CREATE TABLE genre_recommendations AS
SELECT userId, genre, movieId, AVG(rating) AS predicted_rating
FROM user_profiles p
JOIN movies_by_genre g ON p.genre = g.genre
LEFT JOIN ratings r ON g.movieId = r.movieId
GROUP BY userId, genre, movieId
ORDER BY predicted_rating DESC;
```
![Screenshot from 2024-05-24 22-19-36](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/56a77072-1008-4b16-a769-68f28cab98b1)


## Display as a dashboard
```python
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
```
![Screenshot from 2024-05-24 22-59-58](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/c34e5ad2-275f-463e-b768-57982e78c91c)
![Screenshot from 2024-05-24 23-00-40](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/f23da163-428a-499c-9d5f-73ecc79628df)
![Screenshot from 2024-05-24 23-01-08](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/ed882d17-5f84-4ac7-bf3d-0f7ae509da05)
![Screenshot from 2024-05-24 23-01-22](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/a612fa33-e11e-406a-b516-fc8e2e5d9d89)
![Screenshot from 2024-05-24 23-01-44](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/6dd605cf-c67c-46b3-94a6-a86d97eb3680)
![Screenshot from 2024-05-24 23-02-00](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/687229b5-79cb-4437-ad59-03e41e8bab8d)
![Screenshot from 2024-05-24 23-02-15](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/7f0931e7-a967-41a9-9d5d-5956f527d328)
![Screenshot from 2024-05-24 23-02-26](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/409ea4ca-6b31-4fc7-979e-717c37054b81)


