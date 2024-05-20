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

Create tables: 
```mysql
# Movies table
CREATE EXTERNAL TABLE movies (
  movieId INT,
  title STRING,
  genres STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/movielens/movies'
TBLPROPERTIES ("skip.header.line.count"="1");

# Ratings table
CREATE EXTERNAL TABLE ratings (
  userId INT,
  movieId INT,
  rating DOUBLE,
  rating_timestamp BIGINT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/movielens/ratings'
TBLPROPERTIES ("skip.header.line.count"="1");
```
![img/tables1.png](img/tables1.png)
