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
