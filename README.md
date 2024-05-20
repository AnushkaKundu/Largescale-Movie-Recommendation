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
