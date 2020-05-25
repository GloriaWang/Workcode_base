import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict


def get_training_loss(path_to_log):
    regex_iteration = re.compile('Iteration (\d+)')
    regex_train_output = re.compile('Train net output #(\d+): (\S+) = ([\.\deE+-]+)')
    iteration = -1
    train_dict_list = []
    train_row = None
    with open(path_to_log) as f:
        for line in f:
            iteration_match = regex_iteration.search(line)
            if iteration_match:
                iteration = float(iteration_match.group(1))
            if iteration == -1:
                continue
            train_dict_list, train_row = parse_line_for_net_output(regex_train_output,
                                                                   train_row,
                                                                   train_dict_list,
                                                                   line,
                                                                   iteration)
    df = pd.DataFrame.from_dict(train_dict_list)
    df.plot(x='NumIters', y=['accuracy', 'loss_bbox'])
    print(df)
    plt.gcf().autofmt_xdate()
    plt.title("Evaluating training iterations")
    plt.ylabel("Metric")
    plt.xlabel("Iteration")
    plt.margins(x=0.1, y=0.1)
    plt.savefig(os.path.join('/kaf-frcnn/result/',
                             'Training_loss_over_iterations.png'))
    plt.close()
    return train_dict_list


def parse_line_for_net_output(regex_obj, row, row_dict_list, line, iteration):
    output_match = regex_obj.search(line)
    if output_match:
        if not row or row['NumIters'] != iteration:
            if row:
                row_dict_list.append(row)
            row = OrderedDict([('NumIters', iteration)])
        output_name = output_match.group(2)
        output_val = output_match.group(3)
        row[output_name] = float(output_val)
    if row and len(row_dict_list) >= 1 and len(row) == len(row_dict_list[0]):
        # The row is full, based on the fact that it has the same number of
        # columns as the first row; append it to the list
        row_dict_list.append(row)
        row = None
    return row_dict_list, row
