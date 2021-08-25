#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
import fnmatch
import re
import sys

pd.options.display.float_format = '{:.4f}'.format

if len(sys.argv) < 3:
    print(
        "Usage: %s <base_dir> <metric> [interface] [ylabel] [xlabel]" % sys.argv[0])
    print(" metrics: bytes_out/s;bytes_in/s;bytes_total/s;bytes_in;bytes_out;packets_out/s;packets_in/s;packets_total/s;packets_in;packets_out;errors_out/s;errors_in/s;errors_in;errors_out")
    exit(1)

base_dir = sys.argv[1]
metric = sys.argv[2]
target = "total"
if len(sys.argv) > 3:
    target = sys.argv[3]
ylabel = metric
if len(sys.argv) > 4:
    ylabel = sys.argv[4]
xlabel = "time in s"
if len(sys.argv) > 5:
    xlabel = sys.argv[5]


start_time = -1
with open(base_dir + "/start.txt", "r") as file:
    start_time = int(file.readline().strip())

if start_time < 0:
    print("Fatal error, cannot determine start time")
    exit(2)


stop_time = -1
with open(base_dir + "/stop.txt", "r") as file:
    stop_time = int(file.readline().strip())

if stop_time < 0:
    print("Fatal error, cannot determine stop time")
    exit(2)

logfiles = []

for root, dir, files in os.walk(base_dir):
    for items in fnmatch.filter(files, "net-*.log"):
        logfiles.append(root + "/" + items)

dfs = []

p = re.compile('.*/net-(.+).log')


for f in logfiles:
    m = p.match(f)
    node_name = m.group(1)
    df = pd.read_csv(f, sep=";", names="timestamp;iface_name;bytes_out/s;bytes_in/s;bytes_total/s;bytes_in;bytes_out;packets_out/s;packets_in/s;packets_total/s;packets_in;packets_out;errors_out/s;errors_in/s;errors_in;errors_out".split(";"))
    df = df[df['iface_name'] == target]
    df['node'] = node_name
    df = df[df['timestamp'] > start_time]
    df["timestamp"] -= start_time
    df['timestamp'] = df['timestamp'].apply(np.int64)
    dfs.append(df)

df = pd.concat(dfs)
df = df.sort_values(by=['timestamp', 'node'])
#print(df[['timestamp', 'node', 'bytes_total/s']])
# print(df.node.unique())
ax = None
for i in df.node.unique():
    df_sub = df[df.node == i]
    if ax:
        ax = df_sub.plot.line(ax=ax, x="timestamp", y=metric)
    else:
        ax = df_sub.plot.line(x="timestamp", y=metric)

ax.ticklabel_format(style='plain', useLocale=True)
ax.legend(df.node.unique())
plt.axhline(df[metric].describe().T['mean'], color='r', linestyle='--')
plt.xlabel(xlabel)
plt.ylabel(ylabel)
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

# print(df[metric].describe().T['mean'])

plt.tight_layout()
# plt.show()

output_dir = base_dir + "/figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

metric = metric.replace("/", "_per_")
output_filename = "net-" + target + '-' + metric + ".pdf"
# output_filename = "net-" + target + '-' + \
#    ''.join(filter(str.isalnum, metric)) + ".pdf"
plt.savefig(output_dir+"/" + output_filename)
