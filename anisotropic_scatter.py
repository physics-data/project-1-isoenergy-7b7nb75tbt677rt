#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import h5py
import numpy as np

# 提高要求的第一部分，按照 README.pdf 中给出的的概率公式来计算。

mode = int(sys.argv[1]) # 若为 0 则为普通散射，1 则为磁性散射。
damp = float(sys.argv[2]) # 衰减系数，若无衰减应输入 -1。
inputfile = sys.argv[3]
outputfile = sys.argv[4]
#save_image = sys.argv[5]

with h5py.File(inputfile, "r") as ipt:
	dos = np.array(ipt["isoE"][()])

length = 1000
xy = np.arange(-length, 1+length)
kxy = np.arange(-100, 101)
x, y = np.mgrid[-length:1+length, -length:1+length]
r = np.power(np.power(x, 2) + np.power(y, 2), 0.5)
L = damp * length / 100
# 计算衰减所用的距离矩阵与常数，与基本要求部分中的同理。
# 由于 README 中 scatter 部分与 multiscatter 部分的公式不自洽（确实是这样），本
# 部分中使用看起来更靠谱的后者。

# 由于概率因子 P 的存在，所以将其分为d三部分计算，在原来的表达式的基础上分别乘上
# 1/2 , -(1/2)*(kx/k) , -(1/2)*(ky/k) 三个因子，分别计算，相关变量分别以 C, A, B
# 标记。

kx, ky = np.mgrid[-100:101, -100:101]
k = np.power(np.power(kx, 2) + np.power(ky, 2), 0.5)
k[100][100] = 1 # 防止出现无穷大。
kx_on_k = kx * np.power(k, -1)
ky_on_k = ky * np.power(k, -1) # 这两个变量的物理意义就是它们的名称。
kx_on_k[100][100] = 0
ky_on_k[100][100] = 0 # 经过理论计算，将此项记为零影响不大。
A1 = dos * kx_on_k
B1 = dos * ky_on_k
C1 = np.exp(np.tensordot(kxy, xy, axes=0) * (1j*np.pi/length))

A2 = np.tensordot(A1, C1, (0, 0))
A3 = np.tensordot(A2, C1, (0, 0)).imag
if damp >= 0: # 若该参数小于零则无衰减。
	A3 = A3 * np.exp(-r / L)
A3 = np.power(A3, 2)
# 这里计算的是乘上了 (kx/k) 因子的项。
# 这里的计算与 scatter.py 中的同理，下同。
# 稍有不同的是：因为 kx_on_k 因子的存在，函数奇偶性发生反转，求和后不再是虚部为
# 零而是实部为零，故取其虚部。

B2 = np.tensordot(B1, C1, (0, 0))
B3 = np.tensordot(B2, C1, (0, 0)).imag
if damp >= 0:
	B3 = B3 * np.exp(-r / L)
B3 = np.power(B3, 2)
# 这里计算的是乘上了 (ky/k) 因子的项。

C2 = np.tensordot(dos, C1, (0, 0))
C3 = np.tensordot(C2, C1, (0, 0)).real
if damp >= 0:
	C3 = C3 * np.exp(-r / L)
C3 = np.power(C3, 2)
# 这里计算的是乘上了常数因子的项。

C4 = 0.5 * (C3 - A3 - B3) + np.power(np.sum(dos), 2) * np.power(-1, mode)
C4 = np.power(C4, 2)
# 求和并平方。

with h5py.File(outputfile, "w") as opt:
	opt["QPI"] = C4

#import matplotlib.pyplot as plt
#fig, ax = plt.subplots(figsize=(10, 10))
#im = ax.imshow(C4)
#fig.colorbar(im)
#plt.savefig(save_image)
# 测试用的代码（前面被注释掉的第五个输入参数也是）。
