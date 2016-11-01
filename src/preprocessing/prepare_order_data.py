import os
import argparse


def prepare_data():
    customer_map = prepare_customer_info()

    original_order_file_path = os.path.join(original_data_directory, 'order.csv')
    prepared_order_file_path = os.path.join(destination_directory, 'order.json')
    with open(prepared_order_file_path, 'w') as p_f:
        with open(original_order_file_path) as o_f:
            for o_line in o_f:
                order_obj = {}
                order_attributes = o_line.replace('\n', '').split(',')
                order_obj['o_w_num'] = int(order_attributes[0])
                order_obj['o_d_num'] = int(order_attributes[1])
                order_obj['o_num'] = int(order_attributes[2])

                customer_id = int(order_attributes[3])
                order_obj['o_customer'] = customer_map[order_obj['o_w_num']][order_obj['o_d_num']][customer_id]

                carrier_id = order_attributes[4]
                if carrier_id == 'null':
                    order_obj['o_carrier_id'] = None
                else:
                    order_obj['o_carrier_id'] = int(order_attributes[4])

                order_obj['o_all_local'] = int(order_attributes[6])
                order_obj['o_entry_d'] = order_attributes[7]

                stringified_order = str(order_obj).replace('None', 'null')
                p_f.write(stringified_order)


def prepare_customer_info():
    """
    Retrieve first name, middle name and last name for all customers
    """
    customer_map = {}
    original_customer_file_path = os.path.join(original_data_directory, 'customer.csv')
    with open(original_customer_file_path) as f:
        for line in f:
            customer_attributes = line.replace('\n', '').split(',')

            warehouse_id = int(customer_attributes[0])
            if warehouse_id not in customer_map:
                customer_map[warehouse_id] = {}

            district_id = int(customer_attributes[1])
            if district_id not in customer_map[warehouse_id]:
                customer_map[warehouse_id][district_id] = {}

            customer_id = int(customer_attributes[2])
            customer = {'c_d_num': customer_id, 'c_first': customer_attributes[3], 'c_middle': customer_attributes[4],
                        'c_last': customer_attributes[5]}
            customer_map[warehouse_id][district_id][customer_id] = customer
    return customer_map


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-o', '--original', required=True, help="Path to the directory containing original data")
    arg_parser.add_argument('-d', '--destination', required=True, help="Path to the directory containing result data")
    args = vars(arg_parser.parse_args())
    original_data_directory = args['original']
    destination_directory = args['destination']

    prepare_data()
