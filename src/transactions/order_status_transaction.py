from pymongo import ReturnDocument, DESCENDING

def order_status_transaction(db, w_id, d_id, c_id):
    # Make sure types of data
    w_id = int(w_id)
    d_id = int(d_id)
    c_id = int(c_id)

    # Last order
    last_order = db.order.find({"o_w_num": w_id, "o_d_num": d_id, "o_customer.c_num": c_id}) \
                         .sort('o_num', DESCENDING)[0]

    result = {
        'customer': last_order['o_customer'],
        'last_order': { key: last_order[key] for key in ['o_num','o_entry_d','o_carrier_id'] },
        'order_lines': [
            { key: ol[key] for key in ['ol_i_num','ol_supply_w_num','ol_quantity','ol_amount','ol_delivery_d'] }
            for ol in last_order['o_order_line'] ]
    }

    return result
