#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import h5py
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

mode = sys.argv[1]
inputfile = sys.argv[2]
outputfile = sys.argv[3]

name = ["isoE", "QPI"][int(mode)]
# 按输入参数选取名称。

with h5py.File(inputfile, "r") as ipt:
	dos = np.array(ipt[name][()])

fig, ax = plt.subplots(figsize=(10,10))
im = ax.imshow(dos)
fig.colorbar(im)
plt.savefig(outputfile)
# 作图并储存。
