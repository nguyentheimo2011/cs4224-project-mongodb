from datetime import datetime

def delivery_transaction(db, w_id, carrier_id):
    # Make sure types of data
    w_id = int(w_id)
    carrier_id = int(carrier_id)

    # Warehouse
    warehouse = db.warehouse.find_one({'w_num': w_id})
    update_warehouse = {'w_districts': {}}

    for d_id in range(1, 11, 1):
        district = warehouse['w_districts'][str(d_id)]
        next_o_id = district['d_next_delivery_o_id']

        # UPDATE warehouse next_delivery_o_id
        update_warehouse['w_districts'][str(d_id)] = {'d_next_delivery_o_id': next_o_id+1}

        # UPDATE order + orderlines
        update_order = {}
        order = db.order.find_one({'o_w_num': w_id, 'o_d_num': d_id, 'o_num': next_o_id})
        update_order['o_carrier_id'] = carrier_id
        update_order['o_order_line'] = []
        total_amount = 0.0
        for ol in order['o_order_line']:
            total_amount += ol['ol_amount']
            ol['ol_delivery_d'] = datetime.now()
            update_order['o_order_line'].append(ol)
        db.order.update_one(
            {'o_w_num': w_id, 'o_d_num': d_id, 'o_num': next_o_id},
            {'$set': update_order}, True)

        # UPDATE Customer
        c_id = order['o_customer']['c_num']
        db.customer.find_one_and_update(
            {'c_w_num': w_id, 'c_d_num': d_id, 'c_num': c_id},
            {'$inc': {'c_balance': total_amount, 'c_delivery_cnt': 1}},
        )

    db.warehouse.update_one({'w_num': w_id}, {'$set': update_warehouse}, True)

    return {'delivery_transaction': 'done'}
