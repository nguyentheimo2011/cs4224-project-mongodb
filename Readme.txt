1. Pre-process data
   Example:
   python prepare_warehouse_data.py -o /Users/Thomas/Documents/Study/Year-5/CS4224-Distributed_Database/Project/initial-data/D8-data -d /Users/Thomas/Documents/Study/Year-5/CS4224-Distributed_Database/Project/preprocessed-data

2. Import data to the database
   Example:
   ./mongoimport -h 192.168.51.8:27017 --db wholesale_supplier --collection warehouse --drop --file ../data/primer-dataset.json