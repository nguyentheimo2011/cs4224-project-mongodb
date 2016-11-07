import os
import argparse
from datetime import datetime


def prepare_data():
    customer_map = prepare_customer_info()
    order_line_map = prepare_order_line_info()

    original_order_file_path = os.path.join(original_data_directory, 'order.csv')
    prepared_order_file_path = os.path.join(destination_directory, 'order.json')
    with open(prepared_order_file_path, 'w') as p_f:
        with open(original_order_file_path) as o_f:
            count = 0
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
                order_obj['o_entry_d'] = {'$date': convert_datetime_to_unix_time(order_attributes[7])}
                order_obj['o_order_line'] = order_line_map[order_obj['o_w_num']][order_obj['o_d_num']][
                    order_obj['o_num']]

                stringified_order = str(order_obj).replace('None', 'null')
                p_f.write(stringified_order + '\n')

                count += 1
                if count % 50000 == 0:
                    print 'Complete processing {} lines in Order file'.format(count)


def prepare_customer_info():
    """
    Retrieve first name, middle name and last name for all customers
    """
    print 'Start preparing Customer info'
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
    print 'Finish preparing Customer info'
    return customer_map


def prepare_order_line_info():
    """
    Organize order lines in order to efficiently retrieving data
    """
    print 'Start preparing Order Line info'
    item_map = prepare_item_info()
    order_line_map = {}
    original_order_line_file_path = os.path.join(original_data_directory, 'order-line.csv')
    with open(original_order_line_file_path) as f:
        for ol_line in f:
            ol_attributes = ol_line.replace('\n', '').split(',')

            warehouse_id = int(ol_attributes[0])
            if warehouse_id not in order_line_map:
                order_line_map[warehouse_id] = {}

            district_id = int(ol_attributes[1])
            if district_id not in order_line_map[warehouse_id]:
                order_line_map[warehouse_id][district_id] = {}

            order_id = int(ol_attributes[2])
            if order_id not in order_line_map[warehouse_id][district_id]:
                order_line_map[warehouse_id][district_id][order_id] = []

            ol_obj = {}
            ol_obj['ol_number'] = int(ol_attributes[3])
            ol_obj['ol_i_num'] = int(ol_attributes[4])
            ol_obj['ol_i_name'] = item_map[ol_obj['ol_i_num']]

            delivery_date = ol_attributes[5]
            if delivery_date == 'null':
                ol_obj['ol_delivery_d'] = None
            else:
                ol_obj['ol_delivery_d'] = convert_datetime_to_unix_time(delivery_date)

            ol_obj['ol_amount'] = float(ol_attributes[6])
            ol_obj['ol_supply_w_num'] = int(ol_attributes[7])
            ol_obj['ol_quantity'] = float(ol_attributes[8])
            ol_obj['ol_dist_info'] = ol_attributes[9]
            order_line_map[warehouse_id][district_id][order_id].append(ol_obj)

    print 'Finish preparing Order Line info'
    return order_line_map


def prepare_item_info():
    """
    Retrieve name for all items
    """
    print 'Start preparing Item info'
    item_map = {}
    original_item_file_path = os.path.join(original_data_directory, 'item.csv')
    with open(original_item_file_path) as f:
        for line in f:
            item_attributes = line.replace('\n', '').split(',')
            item_id = int(item_attributes[0])
            item_name = item_attributes[1]
            item_map[item_id] = item_name

    print 'Finish preparing Item info'
    return item_map


def convert_datetime_to_unix_time(date_time_str):
    date_time_components = date_time_str.split('.')
    date_time_str = date_time_components[0]
    milliseconds = 0
    if len(date_time_components) == 2:
        milliseconds = int(date_time_components[1])
    unix_time = int(datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S').strftime('%s'))
    unix_time_in_milliseconds = 1000 * unix_time + milliseconds
    return unix_time_in_milliseconds


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-o', '--original', required=True, help="Path to the directory containing original data")
    arg_parser.add_argument('-d', '--destination', required=True, help="Path to the directory containing result data")
    args = vars(arg_parser.parse_args())
    original_data_directory = args['original']
    destination_directory = args['destination']

    prepare_data()
