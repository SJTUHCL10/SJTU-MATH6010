# 均匀图分割问题

## 问题描述

给定 $2n$ 个结点的完全图 $G$，每条边的权重都为整数。目标是把图均匀分割为两部分 $P_0, P_1$，每部分结点数都为 $n$。目标是最小化跨越两部分结点的边的权重之和，即：
$$\min_{P_0,P_1} \sum_{u\in P_0, v\in P_1} w(u,v).$$
