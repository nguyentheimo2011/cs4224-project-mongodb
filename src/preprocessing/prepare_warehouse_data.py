import os
import argparse


def prepare_data():
    original_warehouse_file_path = os.path.join(original_data_directory, 'warehouse.csv')
    original_district_file_path = os.path.join(original_data_directory, 'district.csv')
    prepared_warehouse_file_path = os.path.join(destination_directory, 'warehouse.json')
    with open(prepared_warehouse_file_path, 'w') as r_f:
        with open(original_warehouse_file_path) as w_f:
            for w_line in w_f:
                warehouse_obj = {}
                warehouse_attributes = w_line.replace('\n', '').split(',')
                warehouse_obj['w_num'] = int(warehouse_attributes[0])
                warehouse_obj['w_name'] = warehouse_attributes[1]
                warehouse_obj['w_street_1'] = warehouse_attributes[2]
                warehouse_obj['w_street_2'] = warehouse_attributes[3]
                warehouse_obj['w_city'] = warehouse_attributes[4]
                warehouse_obj['w_state'] = warehouse_attributes[5]
                warehouse_obj['w_zip'] = warehouse_attributes[6]
                warehouse_obj['w_tax'] = float(warehouse_attributes[7])
                warehouse_obj['w_ytd'] = float(warehouse_attributes[8])
                warehouse_obj['w_districts'] = []

                with open(original_district_file_path) as d_f:
                    for d_line in d_f:
                        district_attributes = d_line.replace('\n', '').split(',')
                        if district_attributes[0] != warehouse_attributes[0]:
                            continue
                        district_obj = {}
                        district_obj['d_w_num'] = int(district_attributes[0])
                        district_obj['d_num'] = int(district_attributes[1])
                        district_obj['d_name'] = district_attributes[2]
                        district_obj['d_street_1'] = district_attributes[3]
                        district_obj['d_street_2'] = district_attributes[4]
                        district_obj['d_city'] = district_attributes[5]
                        district_obj['d_state'] = district_attributes[6]
                        district_obj['d_zip'] = district_attributes[7]
                        district_obj['d_tax'] = float(district_attributes[8])
                        district_obj['d_ytd'] = float(district_attributes[9])
                        district_obj['d_next_o_id'] = int(district_attributes[10])
                        warehouse_obj['w_districts'].append(district_obj)

                r_f.write(str(warehouse_obj) + '\n')



if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-o', '--original', required=True, help="Path to the directory containing original data")
    arg_parser.add_argument('-d', '--destination', required=True, help="Path to the directory containing result data")
    args = vars(arg_parser.parse_args())
    original_data_directory = args['original']
    destination_directory = args['destination']

    prepare_data()

