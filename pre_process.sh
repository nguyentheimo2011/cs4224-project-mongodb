source_dir=$1
target_dir=$2

if [ -n "$source_dir" ] && [ -n "$target_dir" ]; then
    start=`date +%s`

    for collection in 'warehouse' 'order' 'item' 'customer'
    do
        echo "Start processing $collection !"
        source_file="src/preprocessing/prepare_"$collection"_data.py"
        python $source_file -o $source_dir -d $target_dir
        echo "Done processing" $collection "!"
        echo "------------------------------------------------------------------"
    done

    end=`date +%s`
    runtime=$((end-start))
    echo "Time used:" $runtime "seconds"
else
    echo "Argument Error: Need both source path & target path!"
fi
