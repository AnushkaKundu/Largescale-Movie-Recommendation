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

### Hybrid Similarities
```mysql
CREATE TABLE hybrid_similarities AS
SELECT c.movieId1, c.movieId2, (c.similarity + g.similarity) / 2 AS hybrid_similarity
FROM movie_similarities c
JOIN genre_similarities g ON c.movieId1 = g.movieId1 AND c.movieId2 = g.movieId2;
```

### Trend Analysis
```mysql
CREATE TABLE movie_trends AS
SELECT YEAR(FROM_UNIXTIME(timestamp)) AS year, genre, COUNT(*) AS count
FROM ratings r
JOIN movies m ON r.movieId = m.movieId
JOIN movies_by_genre g ON m.movieId = g.movieId
GROUP BY year, genre;
```

### Seasonal Effects
```mysql
CREATE TABLE user_profiles AS
SELECT userId, genre, AVG(rating) AS avg_rating
FROM ratings r
JOIN movies m ON r.movieId = m.movieId
JOIN movies_by_genre g ON m.movieId = g.movieId
GROUP BY userId, genre;
```

###  User Clustering and Profiling
```mysql
CREATE TABLE user_profiles AS
SELECT userId, genre, AVG(rating) AS avg_rating
FROM ratings r
JOIN movies m ON r.movieId = m.movieId
JOIN movies_by_genre g ON m.movieId = g.movieId
GROUP BY userId, genre;
```

### User Engagement
```mysql
CREATE TABLE user_engagement AS
SELECT userId, COUNT(*) AS num_ratings, AVG(rating) AS avg_rating
FROM ratings
GROUP BY userId;
```

### Genre Recommendations
````mysql
CREATE TABLE genre_recommendations AS
SELECT userId, genre, movieId, AVG(rating) AS predicted_rating
FROM user_profiles p
JOIN movies_by_genre g ON p.genre = g.genre
LEFT JOIN ratings r ON g.movieId = r.movieId
GROUP BY userId, genre, movieId
ORDER BY predicted_rating DESC;
```
```
