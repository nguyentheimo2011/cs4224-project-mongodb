import os
import argparse


def prepare_data():
    next_delivery_order_ids = prepare_next_delivery_order_id_for_districts()

    original_warehouse_file_path = os.path.join(original_data_directory, 'warehouse.csv')
    original_district_file_path = os.path.join(original_data_directory, 'district.csv')
    prepared_warehouse_file_path = os.path.join(destination_directory, 'warehouse.json')
    with open(prepared_warehouse_file_path, 'w') as p_f:
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
                warehouse_obj['w_districts'] = {}

                with open(original_district_file_path) as d_f:
                    for d_line in d_f:
                        district_attributes = d_line.replace('\n', '').split(',')
                        if district_attributes[0] != warehouse_attributes[0]:
                            continue
                        district_obj = {}
                        district_number = int(district_attributes[1])
                        district_obj['d_name'] = district_attributes[2]
                        district_obj['d_street_1'] = district_attributes[3]
                        district_obj['d_street_2'] = district_attributes[4]
                        district_obj['d_city'] = district_attributes[5]
                        district_obj['d_state'] = district_attributes[6]
                        district_obj['d_zip'] = district_attributes[7]
                        district_obj['d_tax'] = float(district_attributes[8])
                        district_obj['d_ytd'] = float(district_attributes[9])
                        district_obj['d_next_o_id'] = int(district_attributes[10])
                        district_obj['d_next_delivery_o_id'] = next_delivery_order_ids[warehouse_obj['w_num']][
                            district_number
                        ]
                        warehouse_obj['w_districts'][str(district_number)] = district_obj

                p_f.write(str(warehouse_obj) + '\n')


def prepare_next_delivery_order_id_for_districts():
    num_warehouses = 0
    original_warehouse_file_path = os.path.join(original_data_directory, 'warehouse.csv')
    with open(original_warehouse_file_path) as f:
        for line in f:
            num_warehouses += 1

    original_order_file_path = os.path.join(original_data_directory, 'order.csv')
    next_delivery_order_ids = {}

    for i in range(1, num_warehouses + 1):
        next_delivery_order_ids[i] = {}

    with open(original_order_file_path) as f:
        for line in f:
            order_attributes = line.replace('\n', '').split(',')
            warehouse_id = int(order_attributes[0])
            district_id = int(order_attributes[1])
            order_id = int(order_attributes[2])
            carrier_id = order_attributes[4]
            if carrier_id == 'null':
                last_order_id_in_district = next_delivery_order_ids.get(warehouse_id).get(district_id, None)
                if last_order_id_in_district is None or last_order_id_in_district > order_id:
                    next_delivery_order_ids[warehouse_id][district_id] = order_id

    return next_delivery_order_ids


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-o', '--original', required=True, help="Path to the directory containing original data")
    arg_parser.add_argument('-d', '--destination', required=True, help="Path to the directory containing result data")
    args = vars(arg_parser.parse_args())
    original_data_directory = args['original']
    destination_directory = args['destination']

    prepare_data()
