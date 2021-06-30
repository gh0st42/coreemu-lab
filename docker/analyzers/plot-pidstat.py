#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import fnmatch
import re
import sys

#print("analyzing pidstat results from all nodes")

if len(sys.argv) < 4:
    print(
        "Usage: %s <base_dir> <property> <process_name> [ylabel] [xlabel]" % sys.argv[0])

    print("property list: Time        UID       PID    %usr %system  %guest   %wait    %CPU   CPU  minflt/s  majflt/s     VSZ     RSS   %MEM   kB_rd/s   kB_wr/s kB_ccwr/s iodelay  Command")
    exit(1)

base_dir = sys.argv[1]
prop = sys.argv[2]
target = sys.argv[3]
ylabel = ""
if len(sys.argv) > 4:
    ylabel = sys.argv[4]
xlabel = ""
if len(sys.argv) > 5:
    xlabel = sys.argv[5]

logfiles = []

for root, dir, files in os.walk(base_dir):
    for items in fnmatch.filter(files, "pidstat-*.csv.log"):
        logfiles.append(root + "/" + items)

dfs = []

p = re.compile('.*/pidstat-(.+).csv.log')

for f in logfiles:
    m = p.match(f)
    node_name = m.group(1)
    df = pd.read_csv(f, sep="\s+")
    stats = df.describe().T
    the_row = stats[(stats.index == prop)]
    the_row.rename(index={prop: node_name}, inplace=True)
    dfs.append(the_row)

df = pd.concat(dfs)

ax = df.plot.bar(y="mean", legend=False, yerr="std", title=prop)
plt.axhline(df["mean"].mean(), color='r', linestyle='--')
plt.xlabel(xlabel)
plt.ylabel(ylabel)
# plt.show()

output_dir = base_dir + "/figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_filename = "pidstat-" + ''.join(filter(str.isalnum, prop)) + ".pdf"
plt.savefig(output_dir+"/" + output_filename)
