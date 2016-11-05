

def process_stock_level_transaction(db, w_id, d_id, thshold, num_last_orders):
    # Make sure types of data
    w_id = int(w_id)
    d_id = int(d_id)
    thshold = int(thshold)
    num_last_orders = int(num_last_orders)

    # Last L orders
    last_orders = db.order.find({"o_w_id": w_id, "o_d_id": d_id)
                          .sort('o_num', pymongo.DESCENDING)[:num_last_orders]

    checked = {}
    count = 0
    for order in last_orders:
        for ol in order.o_order_line:
            item = db.item.find_one({"i_num": ol.ol_i_num})
            if item.i_num not in checked and item.i_warehouse_stocks[str(w_id)].s_quantity < thshold:
                checked[item.i_num] = True
                count += 1

    return {'Stock_lvl_transaction_result': count}
