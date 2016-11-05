import pymongo


def process_top_balance_transaction(db):
    result = []
    for c in db.customer.find().sort('c_balance', pymongo.DESCENDING)[:10]:
        result.append({'customer_identifier': {
                            'customer_first': c.c_first,
                            'customer_middle': c.c_middle,
                            'customer_last': c.c_last },
                      'balance': c.c_balance,
                      'warehouse_name': c.c_w_name,
                      'district_name': c.c_d_name})
    return result
