import os
import argparse
from datetime import datetime


def prepare_data():
    original_warehouse_file_path = os.path.join(original_data_directory, 'warehouse.csv')
    original_district_file_path = os.path.join(original_data_directory, 'district.csv')
    original_customer_file_path = os.path.join(original_data_directory, 'customer.csv')
    prepared_customer_file_path = os.path.join(destination_directory, 'customer.json')
    with open(prepared_customer_file_path, 'w') as p_f:
        warehouses = {}
        with open(original_warehouse_file_path) as w_f:
            for w_line in w_f:
                warehouse_attributes = w_line.replace('\n', '').split(',')
                w_num = int(warehouse_attributes[0])
                w_name = warehouse_attributes[1]
                warehouses[w_num] = w_name

        districts = {}
        with open(original_district_file_path) as d_f:
            for d_line in d_f:
                district_attributes = d_line.replace('\n', '').split(',')
                w_num = int(district_attributes[0])
                d_num = int(district_attributes[1])
                d_name = district_attributes[2]
                if w_num not in districts:
                    districts[w_num] = {}
                districts[w_num][d_num] = w_name

        with open(original_customer_file_path) as c_f:
            for c_line in c_f:
                customer_attributes = c_line.replace('\n', '').split(',')
                customer_obj = {}
                customer_obj['c_w_num'] = int(customer_attributes[0])
                customer_obj['c_w_name'] = warehouses[customer_obj['c_w_num']]

                customer_obj['c_d_num'] = int(customer_attributes[1])
                customer_obj['c_d_name'] = districts[customer_obj['c_w_num']][customer_obj['c_d_num']]

                customer_obj['c_num'] = int(customer_attributes[2])
                customer_obj['c_first'] = customer_attributes[3]
                customer_obj['c_middle'] = customer_attributes[4]
                customer_obj['c_last'] = customer_attributes[5]
                customer_obj['c_street_1'] = customer_attributes[6]
                customer_obj['c_street_2'] = customer_attributes[7]
                customer_obj['c_city'] = customer_attributes[8]
                customer_obj['c_state'] = customer_attributes[9]
                customer_obj['c_zip'] = customer_attributes[10]
                customer_obj['c_phone'] = customer_attributes[11]
                customer_obj['c_since'] = {'$date': convert_datetime_to_unix_time(customer_attributes[12])}
                customer_obj['c_credit'] = customer_attributes[13]
                customer_obj['c_credit_lim'] = float(customer_attributes[14])
                customer_obj['c_discount'] = float(customer_attributes[15])
                customer_obj['c_balance'] = float(customer_attributes[16])
                customer_obj['c_ytd_payment'] = float(customer_attributes[17])
                customer_obj['c_payment_cnt'] = int(customer_attributes[18])
                customer_obj['c_delivery_cnt'] = int(customer_attributes[19])
                customer_obj['c_data'] = customer_attributes[20]

                p_f.write(str(customer_obj) + '\n')


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
