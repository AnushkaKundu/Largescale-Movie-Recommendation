![Screenshot from 2024-05-23 20-24-40](https://github.com/AnushkaKundu/Hive-and-Hadoop-setup-and-usage/assets/97175497/d9b47f9f-4fb0-48e2-b834-3d2b7372dc44)## Start Hadoop
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
