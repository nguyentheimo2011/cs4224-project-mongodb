from datetime import datetime
from pymongo import ReturnDocument


def new_order_transaction(db, c_id, w_id, d_id, num_items, order_line_list):
    # Make sure types of data
    c_id = int(c_id)
    w_id = int(w_id)
    d_id = int(d_id)
    num_items = int(num_items)

    # Update district
    warehouse = db.warehouse.find_one_and_update(
        {'w_num': w_id},
        {'$inc': {'w_districts.'+(str(d_id)+'.d_next_o_id'): 1}},
        return_document=ReturnDocument.BEFORE
    )

    # Create order
    order = {
        'o_num': warehouse['w_districts'][str(d_id)]['d_next_o_id'],
        'o_d_num': d_id,
        'o_w_num': w_id,
        'o_c_num': c_id,
        'o_entry_d': datetime.now(),
        'o_carrier_id': 0,
        'o_ol_cnt': num_items,
        'o_all_local': 0 if any(w != w_id for (_, w, _) in order_line_list) else 1,
        'o_order_line': []
    }

    total_amount = 0
    item_count = 0
    for (item_id, supply_warehouse_id, quantity) in order_line_list:
        item = db.item.find_one({'i_num': int(item_id)})
        adj_quantity = item['i_warehouse_stocks'][str(supply_warehouse_id)]['s_quantity'] - int(quantity)
        if adj_quantity < 10:
            adj_quantity += 100

        # Update Stock
        db.item.update_one(
            {'i_num': int(item_id)},
            {
                '$set': {'i_warehouse_stocks.'+str(supply_warehouse_id)+'.s_quantity': adj_quantity},
                '$inc': {
                    'i_warehouse_stocks.'+str(supply_warehouse_id)+'.s_ytd': int(quantity),
                    'i_warehouse_stocks.'+str(supply_warehouse_id)+'.s_order_cnt': 1,
                    'i_warehouse_stocks.'+str(supply_warehouse_id)+'.s_remote_cnt': 1 if int(supply_warehouse_id) != w_id else 0,
                },
            }
        )

        # Extra data
        item_amount = int(quantity) * item['i_price']
        total_amount += item_amount
        item_count += 1

        # Create order-line
        order['o_order_line'].append({
            'ol_o_num': order['o_num'],
            'ol_d_num': d_id,
            'ol_w_id': w_id,
            'ol_number': item_count,
            'ol_i_num': int(item_id),
            'ol_i_name': item['i_name'],
            'ol_supply_w_id': int(supply_warehouse_id),
            'ol_quantity': int(quantity),
            'ol_amount': item_amount,
            'ol_delivery_d': 0,
            'ol_dist_info': 'S_DIST_'+str(d_id),
        })

    # Customer
    customer = db.customer.find_one({'c_w_num': w_id, 'c_d_num': d_id, 'c_num': c_id})
    order['o_customer'] = { key: customer[key] for key in ['c_num','c_first','c_middle','c_last'] }
    db.order.insert(order)

    total_amount = total_amount \
        * (1+warehouse['w_tax']+warehouse['w_districts'][str(d_id)]['d_tax']) \
        * (1-customer['c_discount'])

    result = {
        'customer': { key: customer[key] for key in ['c_w_num','c_d_num','c_num','c_last','c_credit','c_discount'] },
        'warehouse_tax': warehouse['w_tax'],
        'district_tax': warehouse['w_districts'][str(d_id)]['d_tax'],
        'order_id': order['o_num'],
        'order_entry_d': order['o_entry_d'],
        'num_items': num_items,
        'total_amount': total_amount,
        'items': order['o_order_line']
    }
    return result
