#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import csv
import h5py
import numpy as np

MSP = sys.argv[2]
inputfile = sys.argv[3]
outputfile = sys.argv[4]

data = []
# 用来储存散射点的坐标（是数组中的坐标，不是以中心为零点的坐标）。
with open(MSP, "r") as csvfile:
	reader = csv.reader(csvfile, skipinitialspace=True)
	next(reader) # 把第一行跳过。
	for x, y in reader:
		data.append((int(x), int(y)))

with h5py.File(inputfile, "r") as ipt:
	dos = np.array(ipt["isoE"][()])

length = 1000
xy = np.arange(-length, 1+length)
kxy = np.arange(-100, 101)
A1 = np.exp(np.tensordot(kxy, xy, axes=0) * (1j*np.pi/length))
A2 = np.tensordot(dos, A1, (0, 0))
A3 = np.tensordot(A2, A1, (0, 0)).real
# 对动量空间态密度做傅里叶变换，与 scatter.py 中一样的步骤，故不细讲。

A3 = A3[np.mod(np.arange(-length-1, length), 1+2*length),:]
A3 = A3[:,np.mod(np.arange(-length-1, length), 1+2*length)]
# 把图片中心挪到数组的 [0, 0] 的位置

A3 = np.concatenate((A3, A3), axis=0)
A3 = np.concatenate((A3, A3), axis=1)
# 将四张图片组合成一张大图片。
x, y = np.mgrid[-1-2*length:1+2*length, -1-2*length:1+2*length]
r = np.power(np.power(x, 2) + np.power(y, 2), 0.5)
L = 20 * length / 100
A3 = A3 * np.exp(- r * (1 / L))
# 然后乘上衰减的因子。

# 之所以要先合成一张大图再做衰减，是因为实空间态函数存在周期性（这是由动量空间态
# 密度的离散形式所决定的），如果一个散射中心出现在图片边缘附近，它的一小部分散射
# 图样可能出现在图的另一侧，这是不希望看到的。而通过此做法可以使得脱离于散射中心
# 的图样由于衰减因子而消失。

gain = int(length / 100)
# 为方便阅读而写的辅助因子。
A4 = np.zeros([1+2*length, 1+2*length]) + np.power(np.sum(dos), 2)
# 后面加上的数对应于公式中的“1”，由于之前的步骤中略去了归一化的操作，所以这里要
# 额外乘上一个因子。
for x, y in data:
	A5 = A3[1+2*length-x*gain:2+4*length-x*gain,:]
	A5 = A5[:,1+2*length-y*gain:2+4*length-y*gain]
	# 从四倍的大图中按照散射点位置裁剪出所需的小图。
	A4 = A4 + np.power(A5, 2)
A4 = np.power(A4, 2)

with h5py.File(outputfile, "w") as opt:
	opt["QPI"] = A4

#import matplotlib.pyplot as plt
#fig, ax = plt.subplots(figsize=(10,10))
#im = ax.imshow(A4)
#fig.colorbar(im)
#plt.savefig("wula1.png")
#plt.show()
# 测试用的代码
