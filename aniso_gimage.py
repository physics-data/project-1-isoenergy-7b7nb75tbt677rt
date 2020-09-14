#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import h5py
import numpy as np

# 这个脚本只是是用来画图的。

inputfile = sys.argv[1]
outputfile = sys.argv[2]

with h5py.File(inputfile, "r") as ipt:
	dos = np.array(ipt["QPI"][()])

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(dos)
fig.colorbar(im)
plt.savefig(outputfile)
