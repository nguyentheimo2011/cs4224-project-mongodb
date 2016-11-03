from datetime import datetime


def process_new_order_transaction(database, customer_id, warehouse_id, district_id, num_items, order_line_list):
    """
    :param database: pymongo.database.Database
    :param customer_id: int
    :param warehouse_id: int
    :param district_id: int
    :param num_items: int
    :param order_line_list: list of (ol_i_id, ol_supply_w_id, ol_quantity) in which ol_i_id (int), ol_supply_w_id (int),
    ol_quantity (float)
    :return:
    """
    print 'process_new_order_transaction'
