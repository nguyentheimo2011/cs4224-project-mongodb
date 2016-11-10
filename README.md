# CS4224-project-mongodb
---Team 16---


## Environments
* python2.7
* mongodb 3


## Requirements
* pymongo


## Connect to the database from client
```
./mongo 192.168.51.8:27017/test
```


## Data Preprocessing
You need to pre-process the data before importing.
There are two ways to pre-process the data and you can choose either way.
You can run four commands as below, each command prepares data for one collection
```
python src/preprocessing/prepare_warehouse_data.py -o /path/D8-data -d /path/pre-processed-data
python src/preprocessing/prepare_order_data.py -o /path/D8-data -d /path/pre-processed-data
python src/preprocessing/prepare_item_data.py -o /path/D8-data -d /path/pre-processed-data
python src/preprocessing/prepare_customer_data.py -o /path/D8-data -d /path/pre-processed-data
```
Or you run the **pre_process.sh** script to pre-process all data and save to JSON files:
```
./pre_process.sh /path/D8(or40)-data /path/processed-data
```


## Import data to the database
After the data has been pre-processed, you can start importing data to the MongoDB database.
Similar to the step above, there are two ways to import data and you can choose either way.
You run four commands as below, each command loads data for one collection:
```
./mongoimport -h 192.168.51.8:27017 --db wholesale_supplier --collection warehouse --drop --file path/warehouse.json
./mongoimport -h 192.168.51.8:27017 --db wholesale_supplier --collection order --drop --file path/order.json
./mongoimport -h 192.168.51.8:27017 --db wholesale_supplier --collection item --drop --file path/item.json
./mongoimport -h 192.168.51.8:27017 --db wholesale_supplier --collection customer --drop --file path/customer.json
```
Or you can run the **load_data.sh** script to load data for all collection. The prerequisite for this to work is that
you need copy the 'mongodb' folder (the folder that contains 'bin/mongoimport') to put in the folder that contains
'cs4224-project-mongodb' folder. For example, if 'cs4224-project-mongodb' is inside 'Documents/cs4224/', then you need
to copy 'mongodb' folder to put inside 'Documents/cs4224/'. The reason for this is because we call
'../mongodb/bin/mongoimport -h $database --db wholesale_supplier ...' inside 'load_data.sh'
```
./load_data.sh /path/processed-data {database-address, default 192.168.51.8:27017}
```

## Benchmark
To benchmark the database, run the following command
```
python src/driver/main_driver.py -c ${num_client} -p ${transaction_folder}
```
In case you want to run the file on your own node, please change the IP address in function
'run_multiple_transaction_sets_with_multiple_clients' in 'main_driver.py'.
The benchmarking results are written in the file 'benchmarking_results.txt' inside 'cs4224-project-mongodb' folder.
To simulate the n number of clients, we use n threads to execute transactions from n files which puts the burden to
one computer. Therefore, the benchmarking results are significantly lower than benchmarking with n actual clients.
Note: To shorten the benchmarking process, we only run the first 500 transactions from each transaction file
