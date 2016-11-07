import os
import argparse


def prepare_data():
    stock_map = prepare_stock_data()

    original_item_file_path = os.path.join(original_data_directory, 'item.csv')
    prepared_item_file_path = os.path.join(destination_directory, 'item.json')

    with open(prepared_item_file_path, 'w') as p_f:
        with open(original_item_file_path) as i_f:
            count = 0
            for i_line in i_f:
                item_obj = {}
                item_attributes = i_line.replace('\n', '').split(',')
                item_obj['i_num'] = int(item_attributes[0])
                item_obj['i_name'] = item_attributes[1]
                item_obj['i_price'] = float(item_attributes[2])
                item_obj['i_im_id'] = int(item_attributes[3])
                item_obj['i_data'] = item_attributes[4]
                item_obj['i_warehouse_stocks'] = stock_map[item_obj['i_num']]

                p_f.write(str(item_obj) + '\n')

                count += 1
                if count % 50000 == 0:
                    print 'Complete processing {} lines in Item file'.format(count)


def prepare_stock_data():
    print 'Start preparing Stock data'
    stock_map = {}
    original_stock_file_path = os.path.join(original_data_directory, 'stock.csv')
    with open(original_stock_file_path) as f:
        for line in f:
            stock_attributes = line.replace('\n', '').split(',')

            warehouse_id = int(stock_attributes[0])
            item_id = int(stock_attributes[1])

            if item_id not in stock_map:
                stock_map[item_id] = {}

            stock_obj = {}
            stock_obj['s_quantity'] = float(stock_attributes[2])
            stock_obj['s_ytd'] = float(stock_attributes[3])
            stock_obj['s_order_cnt'] = int(stock_attributes[4])
            stock_obj['s_remote_cnt'] = int(stock_attributes[5])
            stock_obj['s_dist_01'] = stock_attributes[6]
            stock_obj['s_dist_02'] = stock_attributes[7]
            stock_obj['s_dist_03'] = stock_attributes[8]
            stock_obj['s_dist_04'] = stock_attributes[9]
            stock_obj['s_dist_05'] = stock_attributes[10]
            stock_obj['s_dist_06'] = stock_attributes[11]
            stock_obj['s_dist_07'] = stock_attributes[12]
            stock_obj['s_dist_08'] = stock_attributes[13]
            stock_obj['s_dist_09'] = stock_attributes[14]
            stock_obj['s_dist_10'] = stock_attributes[15]
            stock_obj['s_data'] = stock_attributes[16]
            stock_map[item_id][str(warehouse_id)] = stock_obj
    print 'Finish preparing Stock data'
    return stock_map


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-o', '--original', required=True, help="Path to the directory containing original data")
    arg_parser.add_argument('-d', '--destination', required=True, help="Path to the directory containing result data")
    args = vars(arg_parser.parse_args())
    original_data_directory = args['original']
    destination_directory = args['destination']

    prepare_data()
