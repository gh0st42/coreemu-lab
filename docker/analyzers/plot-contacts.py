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
        "Usage: %s <base_dir> <time|node> [ylabel] [xlabel]" % sys.argv[0])
    exit(1)

base_dir = sys.argv[1]
mode = sys.argv[2]

ylabel = "total number of contacts"
if len(sys.argv) > 3:
    ylabel = sys.argv[3]

if mode == "node":
    xlabel = "node number"
else:
    xlabel = "time in s"
if len(sys.argv) > 4:
    xlabel = sys.argv[4]

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

max_contacts = 0

total_contacts_per_ts = []
total_contacts_per_node = {}

contacts_log = open(base_dir + "/contacts.log", "r")
for line in contacts_log.readlines():
    line = line.strip()
    num_contacts = 0
    ts = 0
    if not " " in line:
        ts = int(line) - start_time
    else:
        [ts_str, contacts] = line.split(" ")
        ts = int(ts_str) - start_time
        contacts = contacts.split(",")
        for c in contacts:
            if "-" in c:
                [n1, n2] = c.split("-")
                if n1 not in total_contacts_per_node:
                    total_contacts_per_node[n1] = 1
                else:
                    total_contacts_per_node[n1] += 1

                if n2 not in total_contacts_per_node:
                    total_contacts_per_node[n2] = 1
                else:
                    total_contacts_per_node[n2] += 1
        num_contacts = len(contacts)

    total_contacts_per_ts.append([ts, num_contacts])
    max_contacts = max(max_contacts, num_contacts)

if mode == "time":
    df = pd.DataFrame(total_contacts_per_ts, columns=['ts', 'contacts'])
    ax = df.plot(x="ts", y="contacts")
    ax.set_ylim([0, max_contacts + 2])
elif mode == "node":
    c_p_n = []
    nodes = []
    count = 1
    for k in sorted(total_contacts_per_node):
        c_p_n.append(total_contacts_per_node[k])
        nodes.append(count)
        count += 1
    df = pd.DataFrame(c_p_n, columns=["contacts"])
    df['node number'] = nodes
    ax = df.plot.bar(x="node number", y="contacts", legend=False)
else:
    print("unknown mode selected")
    exit(1)


plt.xlabel(xlabel)
plt.ylabel(ylabel)
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

# # print(df[metric].describe().T['mean'])

plt.tight_layout()
# plt.show()

output_dir = base_dir + "/figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


output_filename = "contacts-" + mode + ".pdf"
plt.savefig(output_dir + "/" + output_filename)
