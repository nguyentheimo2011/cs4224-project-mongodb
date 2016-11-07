# CS4224-project-mongodb
---Team 16---

## Connect to the database from client
```
./mongo 192.168.51.8:27017/test
```

## Data Preprocessing
For importing to Mongo directly.
```
python prepare_warehouse_data.py -o /path/D8-data -d /path/pre-processed-data
python prepare_order_data.py -o /path/D8-data -d /path/pre-processed-data
python prepare_item_data.py -o /path/D8-data -d /path/pre-processed-data
python prepare_customer_data.py -o /path/D8-data -d /path/pre-processed-data
```
Or run the **pre_process.sh** script for pre-processing all data and saving to /pre-processed-data
```
./pre_process.sh /path/raw-data(D8-data) -d /path/processed-data
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
./load_data.sh
```

## Run transactions
