import os
import argparse


def prepare_data():
    original_warehouse_file_path = os.path.join(original_data_directory, 'warehouse.csv')
    prepared_warehouse_file_path = os.path.join(destination_directory, 'warehouse.json')
    with open(prepared_warehouse_file_path, 'w'):
        with open(original_warehouse_file_path) as f:
            for line in f:
                warehouse_attributes = line.replace('\n', '').split(',')
                print warehouse_attributes


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-o', '--original', required=True, help="Path to the directory containing original data")
    arg_parser.add_argument('-d', '--destination', required=True, help="Path to the directory containing result data")
    args = vars(arg_parser.parse_args())
    original_data_directory = args['original']
    destination_directory = args['destination']

    prepare_data()

