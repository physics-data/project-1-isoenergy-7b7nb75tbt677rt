#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import h5py
import numpy as np

inputfile = sys.argv[1]
outputfile = sys.argv[2]

with h5py.File(inputfile, "r") as ipt:
	dos = np.array(ipt["QPI"][()])

length = (dos.shape[0] - 1) / 2
x, y = np.mgrid[-length:length+1, -length:length+1]
# 此时得到的 x, y 分别为格点相对中心格点的横纵坐标。
x = np.power(x, 2)
y = np.power(y, 2)
r = np.power(x + y, 0.5)
# r 为格点到中心格点的距离
L = 20 * length / 100
# 由于实空间格点更密集（2001 * 2001），衰减常数需要乘以一个因子。
dos = dos * np.exp(- r * (1 / L))

with h5py.File(outputfile, "w") as opt:
	opt["QPI"] = dos
