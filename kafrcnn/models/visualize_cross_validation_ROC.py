import os
import csv
import pandas as pd
import matplotlib.pyplot as plt


def visualize_results():
    with open(os.path.join('/kaf-frcnn/result/',
                           'List_of_roc_10.csv'), 'w') as f:
        writer = csv.writer(f)
        roc_final = []
        for z in range(1, 9):
            f = open(os.path.join('/kaf-frcnn/log', "log_10_%s.txt" % z), "r")
            ff = f.read().splitlines()
            roc = []
            roc.append("%s" % z)
            roc.append(ff[len(ff) - 5][-4:])
            roc.append(ff[len(ff) - 4][-4:])
            roc.append(ff[len(ff) - 3][-4:])
            roc.append(ff[len(ff) - 2][-4:])
            roc.append(ff[len(ff) - 1][-4:])
            roc_final.append(roc)
        writer.writerows(roc_final)

    # Read from csv file and output graph called roc.png
    headers = ['EvaluateID', 'Precision',
               'Recall', 'FPR', 'F1 score',
               'Avg matching-pair IOU']
    df = pd.read_csv(os.path.join('/kaf-frcnn/result/',
                                  'List_of_roc_10.csv'),
                     names=headers)
    x = df['Recall']
    x = x.tolist()
    y = df['Precision']
    y = y.tolist()
    plt.plot(x, y, 'ro')
    plt.gcf().autofmt_xdate()
    plt.title("ROC for 8 cross-validation splits")
    plt.ylabel("Precision")
    plt.xlabel("Recall")
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.savefig(os.path.join('/kaf-frcnn/result/', 'roc.png'))
    plt.close()
