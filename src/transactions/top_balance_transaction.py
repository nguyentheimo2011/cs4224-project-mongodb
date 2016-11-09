import pymongo


def top_balance_transaction(db):
    result = []
    for c in db.customer.find().sort('c_balance', pymongo.DESCENDING)[:10]:
        result.append({c[key] for key in ['c_first','c_middle','c_last','c_balance','c_w_name','c_d_name']})
    return result
