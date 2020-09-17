## 大作业“扫描隧道显微镜散射解金属等能面”第一阶段实验报告

姓名：何泰文
学号：2018012045
github用户名：htw18
小组名称：7b7nb75tbt677rt

### 小组分工

小组只有一个组员，所以没有分工。

### 整体思路

本次作业完成的工作包括基本要求部分与提高要求部分，提高要求部分完全按照 README 中的第一个提高要求实例的要求实现。

本次作业中的各项任务描述十分清晰细致，物理公式明确且够用，因此只需按照步骤来实现各项功能即可，在基本思路上没有困难，换句话说，基本思路大体上就是 README 中描述的那样。

另外，在具体计算中，由于动量空间的数据是数组的形式，动量与位矢也应该以数组的形式参与运算，因此积分计算应该以求和的形式来实现，所以将会涉及到数组的直积、数组中元素分别进行同样的解析计算、数组的缩并等操作，为加速计算，应使用 numpy 进行计算。这些计算是本次作业的核心任务。

### 程序实现方式

数据的读取、数据的写入、作图等常规步骤只需按部就班地执行即可，需要说明的是涉及数组的计算。

#### `scatter.py`

这一部分需要说明的是以下计算：

$$
D(\mathbf{r}) = \int \mathrm{d}\mathbf{k}_1 f(\mathbf{k}_1) \left|\int \mathrm{d}\mathbf{k}_2 f(\mathbf{k}_2) (e^{-i\mathbf{k}_1\mathbf{r}} + e^{-i\mathbf{k}_2\mathbf{r}})\right|^2 \\
= \int \mathrm{d}\mathbf{k}_1 f(\mathbf{k}_1) (\int \mathrm{d}\mathbf{k}_2 f(\mathbf{k}_2) (e^{-i\mathbf{k}_1\mathbf{r}} + e^{-i\mathbf{k}_2\mathbf{r}}) \int \mathrm{d}\mathbf{k}_3 f(\mathbf{k}_3) (e^{i\mathbf{k}_1\mathbf{r}} + e^{i\mathbf{k}_3\mathbf{r}})) \\
= (\int \mathrm{d}\mathbf{k} f(\mathbf{k}))^{3} + 3 (\int \mathrm{d}\mathbf{k} f(\mathbf{k}))(\int \mathrm{d}\mathbf{k} f(\mathbf{k}) e^{i\mathbf{k}\cdot\mathbf{r}})^{2}
$$

其中使用了$f(\mathbf{k})$的对称性：$f(\mathbf{k}) = f(\mathbf{-k})$ 。

### 遇到的问题以及解决方法

### 提高要求部分