.PHONY: all
fl:=$(shell seq -w 0000 0099)
# pictures
all: $(fl:%=STM/%.png) $(fl:%=STM/m/%.png)
all: $(fl:%=STM/damp/%.png) $(fl:%=STM/damp/m/%.png)
all: $(fl:%=p_momentum/%.png)
# values
all: $(fl:%=dos-position/%.h5) $(fl:%=dos-position/m/%.h5)
all: $(fl:%=dos-position/damp/%.h5) $(fl:%=dos-position/m/damp/%.h5)
all: dos-multi-position/0001.h5
all: $(fl:%=anisotropic_scatter/dos-position/%.h5)
all: $(fl:%=anisotropic_scatter/STM/%.png)
all: $(fl:%=anisotropic_scatter/dos-position/m/%.h5)
all: $(fl:%=anisotropic_scatter/STM/m/%.png)
all: $(fl:%=anisotropic_scatter/dos-position/damp/%.h5)
all: $(fl:%=anisotropic_scatter/STM/damp/%.png)
all: $(fl:%=anisotropic_scatter/dos-position/damp/m/%.h5)
all: $(fl:%=anisotropic_scatter/STM/damp/m/%.png)

SHELL:=/bin/bash

# dos 是 Density of States，态密度
dos-position/%.h5: dos-momentum/%.h5 scatter.py
	mkdir -p $(dir $@)
	python3 scatter.py 0 $< $@

# 磁性散射中心，在散射中心带 pi 相位差
dos-position/m/%.h5: dos-momentum/%.h5 scatter.py
	mkdir -p $(dir $@)
	python3 scatter.py 1 $< $@

# 加入退相干衰减
dos-position/damp/%.h5: dos-position/%.h5 damping.py
	mkdir -p $(dir $@)
	python3 damping.py $< $@

dos-position/m/damp/%.h5: dos-position/m/%.h5 damping.py
	mkdir -p $(dir $@)
	python3 damping.py $< $@


# 画倒空间等能面附近电子态密度图
p_momentum/%.png: dos-momentum/%.h5 gimage.py
	mkdir -p $(dir $@)
	python3 gimage.py 0 $< $@

# 画实空间散射中心周围电子态密度图
STM/%.png: dos-position/%.h5 gimage.py
	mkdir -p $(dir $@)
	python3 gimage.py 1 $< $@

# 多中心散射
dos-multi-position/0001.h5: multi_scatter_position.csv dos-momentum/0001.h5
	mkdir -p $(dir $@)
	python3 multi_scatter.py 0 $^ $@

# 各向异性散射
anisotropic_scatter/dos-position/%.h5: dos-momentum/%.h5 anisotropic_scatter.py
	mkdir -p $(dir $@)
	python3 anisotropic_scatter.py 0 -1 $< $@

# 磁性各向异性散射
anisotropic_scatter/dos-position/m/%.h5: dos-momentum/%.h5 anisotropic_scatter.py
	mkdir -p $(dir $@)
	python3 anisotropic_scatter.py 1 -1 $< $@

# 加入衰减的各向异性散射
anisotropic_scatter/dos-position/damp/%.h5: dos-momentum/%.h5 anisotropic_scatter.py
	mkdir -p $(dir $@)
	python3 anisotropic_scatter.py 0 20 $< $@

# 加入衰减的磁性各向异性散射
anisotropic_scatter/dos-position/damp/m/%.h5: dos-momentum/%.h5 anisotropic_scatter.py
	mkdir -p $(dir $@)
	python3 anisotropic_scatter.py 1 20 $< $@

# 画各向异性散射的实空间电子态密度图像
anisotropic_scatter/STM/%.png: anisotropic_scatter/dos-position/%.h5 aniso_gimage.py
	mkdir -p $(dir $@)
	python3 aniso_gimage.py $< $@

# Delete partial files when the processes are killed.
.DELETE_ON_ERROR:
# Keep intermediate files around
.SECONDARY:
