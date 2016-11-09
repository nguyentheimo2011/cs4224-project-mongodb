mkdir results
rm results/*.txt

# mkdir ../processed-data
# ./pre_process.sh -p ../data/D8-data -d ../processed-data

for i in 10 20 40
do
    echo "start loading data"
    ./load_data.sh ../processed-data > results/$i-loadD8.txt
    echo "done loading data"
    echo "start running with $i clients"
    python src/driver/main_driver.py -p ../data/D8-xact-revised-b -c $i -o results/$i-runD8.txt &> test.out
    echo "done running with $i clients"
done


# ../apache-cassandra-3.9/bin/cqlsh 192.168.51.8 9042 -f model.sql
# python src/data_loader.py -p ../data/D40-data > results/D40_loader.txt
#
# for i in 10 20 40
# do
#   python src/main_driver.py -p ../data/D40-xact-revised-b -c $i &> results/D40_driver_$i.txt
# done
