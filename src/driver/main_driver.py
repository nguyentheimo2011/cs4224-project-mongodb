import time
import sys
import argparse
from threading import Thread

from pymongo import MongoClient

sys.path.append('../transactions')
import new_order_transaction_processing


def run_multiple_transaction_sets_with_multiple_clients():
    client = MongoClient('192.168.51.9', 27017)
    database = client['wholesale_supplier']
    # orders = database['order']
    # print orders.find_one()

    threads = [None] * num_clients
    running_results = [None] * num_clients
    for i in range(0, num_clients, 1):
        trans_file_path = trans_dir_path + '/{}.txt'.format(i)
        try:
            threads[i] = Thread(target=run_a_transaction_set_from_file, args=(trans_file_path, database,
                                                                              running_results, i))
            threads[i].start()
        except:
            print "Error: unable to start thread ", i

    # join all threads
    for t in threads:
        t.join()

    write_benchmarking_results_to_file(running_results)


def run_a_transaction_set_from_file(trans_file_path, database, running_results, thread_id):
    with open(trans_file_path) as f:
        lines = f.readlines()
        total_num_of_transactions = 0
        start_time = time.time()
        for (i, line) in enumerate(lines):
            total_num_of_transactions += 1

            trans_input_values = line.replace('\n', '').split(',')

            output = None

            if trans_input_values[0] == 'N':
                order_line_list = []
                num_of_items = int(trans_input_values[4])
                for j in range(i+1, i+num_of_items+1, 1):
                    item_line = lines[j].replace('\n', '')
                    order_line_list.append(item_line.split(','))
                # output = new_order_transaction.new_order_transaction(database_session, trans_input_values[1],
                    # trans_input_values[2], trans_input_values[3],
                #                                                     trans_input_values[4], order_line_list)
            elif trans_input_values[0] == 'P':
                print 'Payment Transaction'
            elif trans_input_values[0] == 'D':
                print 'Delivery Transaction'
            elif trans_input_values[0] == 'O':
                print 'Order Status Transaction'
            elif trans_input_values[0] == 'S':
                print 'Stock Level Transaction'
            elif trans_input_values[0] == 'I':
                print 'Popular Item Transaction'
            elif trans_input_values[0] == 'T':
                print 'Top Balance Transaction'
            else:
                total_num_of_transactions -= 1
                continue

            if total_num_of_transactions == 1000:
                break

            text = "\nClient: {0}   Transaction: {1}\n".format(thread_id, line.replace('\n', ''))
            text += str(output) + '\n'
            sys.stderr.write(text)

    end_time = time.time()
    running_time = end_time - start_time

    running_results[thread_id] = {
        'thread_id': thread_id,
        'transactions': total_num_of_transactions,
        'elapsed_time': running_time,
        'throughput': float(total_num_of_transactions) / running_time,
    }


def write_benchmarking_results_to_file(results):
    file_name = "benchmarking_results.txt"
    with open(file_name, 'a') as result_file:
        result_file.write('-----------------------------------------------------\n')
        result_file.write('Number of clients: {0}\n'.format(num_clients))

        min_throughput = 1000000000000.0
        max_throughput = -1.0
        total_throughput = 0.0
        for client in results:
            result_file.write(str(client) + '\n')
            min_throughput = min(min_throughput, client['throughput'])
            max_throughput = max(max_throughput, client['throughput'])
            total_throughput += client['throughput']

        stats_text = ""
        stats_text += 'Min. Throughput: {0} (trans/sec)\n'.format(min_throughput)
        stats_text += 'Max. Throughput: {0} (trans/sec)\n'.format(max_throughput)
        stats_text += 'Avg. Throughput: {0} (trans/sec)\n'.format(total_throughput / len(results))

        sys.stderr.write(stats_text)
        result_file.write(stats_text)
        result_file.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--clients", required=True, help="Number of clients issuing transactions")
    ap.add_argument("-p", "--path", required=True, help="Path to the directory containing transaction files")
    args = vars(ap.parse_args())
    num_clients = int(args['clients'])
    trans_dir_path = args['path']

    run_multiple_transaction_sets_with_multiple_clients()
