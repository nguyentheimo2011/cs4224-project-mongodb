

def process_order_status_transaction(db, w_id, d_id, c_id):
    # Make sure types of data
    w_id = int(w_id)
    d_id = int(d_id)
    c_id = int(c_id)

    # Last order
    last_order = db.order.find({"o_w_id": w_id, "o_d_id": d_id, "o_c_id": c_id)
                         .sort('o_num', pymongo.DESCENDING)[0]

    result = {
        'customer': last_order.o_customer,
        'last_order': {
            'order_num': last_order.o_num,
            'order_entry_date': last_order.o_entry_d,
            'carrier_id': last_order.o_carrier_id},
        'order_lines': [{
            'item_num': ol.ol_i_num,
            'supply_warehouse': ol.ol_supply_w_num,
            'quantity': ol.ol_quantity,
            'total_price': ol.ol_amount,
            'delivery_time': ol.ol_delivery_d
        } for ol in last_order.o_order_line]
    }
    
    return result
