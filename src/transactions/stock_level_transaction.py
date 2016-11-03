

def process_stock_level_transaction(database, warehouse_id, district_id, tthreshold, num_last_orders):
    """
    :param database: pymongo.database.Database
    :param warehouse_id: int
    :param district_id: int
    :param tthreshold: int
    :param num_last_orders: int
    :return:
    """
    print 'process_stock_level_transaction'