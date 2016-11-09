from pymongo import DESCENDING


def stock_level_transaction(db, w_id, d_id, thshold, num_last_orders):
    # Make sure types of data
    w_id = int(w_id)
    d_id = int(d_id)
    thshold = int(thshold)
    num_last_orders = int(num_last_orders)

    # Last L orders
    last_orders = db.order.find({"o_w_num": w_id, "o_d_num": d_id}) \
                          .sort('o_num', DESCENDING)[:num_last_orders]

    i_nums = set()
    for order in last_orders:
        for ol in order['o_order_line']:
            i_nums.add(ol['ol_i_num'])

    items = db.item.find({"i_num": {'$in': list(i_nums)}})
    count = 0
    for item in items:
        if item['i_warehouse_stocks'][str(w_id)]['s_quantity'] < thshold:
            count += 1

    return {'Stock_lvl_transaction_result': count}
