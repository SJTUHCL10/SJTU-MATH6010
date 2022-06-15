# Steiner Triple System, STS(v)

## 问题描述

给定全集 $S=\{1,2,...,v\}$，
需要找到全集中元素的三元组构成的集合
$B=\{B_1,B_2,...,B_n\}$，
使得
$\forall i,j\in S, \exist ! B_m \in B, i,j\in B_m$。

根据理论分析可知，
$\forall x\in S$，
$x$
会出现在
$\frac{v-1}{2}$
个三元组中，三元组的数量为
$|B|=n=\frac{v(v-1)}{6}$，全集大小必须满足 $v=1,3(mod 6)$。
