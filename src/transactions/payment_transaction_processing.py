

def process_payment_transaction(database, warehouse_id, district_id, customer_id, payment):
    """
    :param database: pymongo.database.Database
    :param warehouse_id: int
    :param district_id: int
    :param customer_id: int
    :param payment: float
    :return:
    """
    print 'process_payment_transaction'
