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

if len(sys.argv) < 2:
    print(
        "Usage: %s <base_dir> [ylabel] [xlabel]" % sys.argv[0])
    exit(1)

base_dir = sys.argv[1]

ylabel = ""
if len(sys.argv) > 2:
    ylabel = sys.argv[2]

xlabel = ""
if len(sys.argv) > 3:
    xlabel = sys.argv[3]

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

nodes_xy = {}

xy_log = open(base_dir + "/xy.log", "r")
for line in xy_log.readlines():
    if line.startswith("STEP") or len(line) < 7:
        continue
    line = line.strip().replace("=", ",")
    [node, x, y, z] = line.strip().split(",")

    x = float(x)
    y = float(y)
    z = float(z)
    node = node.replace("\"", "")
    if not node in nodes_xy:
        nodes_xy[node] = []
    nodes_xy[node].append([node, x, y])

fig, ax = plt.subplots()
for n in sorted(nodes_xy):
    df = pd.DataFrame(nodes_xy[n], columns=['node', 'x', 'y'])
    ax.scatter(df["x"], df["y"])
    # print(df)

#ax.set_ylim([0, max_contacts + 2])


plt.xlabel(xlabel)
plt.ylabel(ylabel)
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

# # print(df[metric].describe().T['mean'])

plt.tight_layout()
# plt.show()

output_dir = base_dir + "/figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


output_filename = "xy-positions.pdf"
plt.savefig(output_dir + "/" + output_filename)
