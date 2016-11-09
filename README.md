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
For importing to Mongo directly, to preprocess collections:
```
python src/preprocessing/prepare_warehouse_data.py -o /path/D8-data -d /path/pre-processed-data
python src/preprocessing/prepare_order_data.py -o /path/D8-data -d /path/pre-processed-data
python src/preprocessing/prepare_item_data.py -o /path/D8-data -d /path/pre-processed-data
python src/preprocessing/prepare_customer_data.py -o /path/D8-data -d /path/pre-processed-data
```
Or run the **pre_process.sh** script for pre-processing all collections:
```
./pre_process.sh /path/D8-data /path/processed-data
```

## Import data to the database
```
./mongoimport -h 192.168.51.8:27017 --db wholesale_supplier --collection warehouse --drop --file path/warehouse.json
./mongoimport -h 192.168.51.8:27017 --db wholesale_supplier --collection order --drop --file path/order.json
./mongoimport -h 192.168.51.8:27017 --db wholesale_supplier --collection item --drop --file path/item.json
./mongoimport -h 192.168.51.8:27017 --db wholesale_supplier --collection customer --drop --file path/customer.json
```
Or run the **load_data.sh** script for pre-processing all data and saving to /pre-processed-data
```
./load_data.sh /path/processed-data {database-address, default 192.168.51.8:27017}
```

## Run transactions
```
python src/driver/main_driver.py -c ${num_client} -p ${transaction folder}
```
