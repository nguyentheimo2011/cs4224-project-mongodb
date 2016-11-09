from pymongo import ReturnDocument


def payment_transaction(db, w_id, d_id, c_id, payment):
    # Make sure types of data
    w_id = int(w_id)
    d_id = int(d_id)
    c_id = int(c_id)
    payment = float(payment)

    warehouse = db.warehouse.find_one_and_update(
        {'w_num': w_id},
        {'$inc': {'w_ytd': payment, (str(d_id)+'.d_ytd'): payment}},
        return_document=ReturnDocument.AFTER
    )
    customer = db.customer.find_one_and_update(
        {'c_w_num': w_id, 'c_d_num': d_id, 'c_num': c_id},
        {'$inc': {'c_balance': -payment, 'c_ytd_payment': payment, 'c_payment_cnt': 1}},
        return_document=ReturnDocument.AFTER
    )

    result = {
        'customer': customer,
        'warehouse': { key: warehouse[key] for key in ['w_street_1','w_street_2','w_city','w_state','w_zip'] },
        'district': { key: warehouse['w_districts'][str(d_id)][key] for key in ['d_street_1','d_street_2','d_city','d_state','d_zip'] },
        'payment': payment
    }

    return result
