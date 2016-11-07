source_dir=$1
database=$2

if [ -n "$source_dir" ]; then
    if [ ! -n "$database" ]; then
        # Default database
        database="192.168.51.8:27017"
    fi

    start=`date +%s`

    for collection in 'warehouse' 'order' 'item' 'customer'
    do
        echo "Start importing $collection !"
        source_file="$source_dir/$collection.json"
        mongoimport -h $database --db wholesale_supplier --collection $collection --drop --file $source_file
        echo "Done importing $collection !"
        echo "------------------------------------------------------------------"
    done

    end=`date +%s`
    runtime=$((end-start))
    echo "Time used:" $runtime "seconds"
else
    echo "Argument Error: Need source path contains .json files!"
fi
