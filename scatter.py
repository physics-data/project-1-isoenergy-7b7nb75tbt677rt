#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import h5py
import numpy as np

mode = int(sys.argv[1])
inputfile = sys.argv[2]
outputfile = sys.argv[3]

with h5py.File(inputfile, "r") as ipt:
	dos = np.array(ipt["isoE"][()])

# 经过理论计算，结果为两部分之和： A1^3 + 3*A1*A5^2 ，其中 A1 为动量空间态密度积
# 分（求和），A5 为动量空间态密度的傅里叶变换，即乘上 exp^(i(kx*x + ky*y)) 然后
# 求和，由于变换前的对称性 f(k) = f(-k) ，A5 的虚部可略去，若为磁性散射，则第二
# 项的系数 3 改为 -1。

A1 = np.sum(dos)
A2 = np.power(A1, 3)
# 计算第一部分。

length = 1000 # 为了让结果更精细，实空间的格点选取得更密集，态密度数组尺寸为
	# 2001 * 2001。
xy = np.arange(-length, 1+length)
kxy = np.arange(-100, 101)
A3 = np.exp(np.tensordot(kxy, xy, axes=0) * (1j*np.pi/length)) # 由于动量空间格
	# 点有限，得到的是空间态密度是周期函数，为了使生成的实空间范围正好为一个
	# 周期，在指数上乘以 pi/length 。
A4 = np.tensordot(dos, A3, (0, 0)) # 为了使数组不致过大，将 exp^(i(kx*x + ky*xy)
	# ) 分解为两项之积，解开变量 x 与 y 的关联，分两次参与 tensordot 运算。
A5 = np.tensordot(A4, A3, (0, 0))
A6 = np.power(A5.real, 2) * A1
# 计算第二部分。

A7 = (3 - 4 * mode) * A6 + A2

with h5py.File(outputfile, "w") as opt:
	opt["QPI"] = A7

#import matplotlib.pyplot as plt
#fig, ax = plt.subplots(figsize=(10,10))
#im = ax.imshow(A7)
#fig.colorbar(im)
#plt.show()
# 用于测试的代码
