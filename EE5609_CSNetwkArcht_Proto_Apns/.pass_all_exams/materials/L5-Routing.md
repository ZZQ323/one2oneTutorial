# L5 - Network Layer Part II: Routing

## 核心主题
- 路由算法：Dijkstra（链路状态）、Distance Vector（距离向量）
- 路由协议：OSPF、BGP（eBGP/iBGP）
- 转发 vs 路由的区别
- 毒性反转（poisoned reverse）

## 路由算法分类
- **全局/集中式**：所有路由器有完整拓扑和链路成本 → 链路状态算法（Dijkstra）
- **分布式**：迭代计算，只与邻居交换信息 → 距离向量算法

## Dijkstra 算法（链路状态）
- 所有节点有完整拓扑信息（通过链路状态广播）
- 从源节点计算到所有其他节点的最短路径
- 符号：
  - c(x,y): 节点x到y的直接链路成本
  - D(v): 从源到v的当前最小成本估计
  - p(v): 从源到v路径上的前驱节点
  - N': 已确定最小成本路径的节点集合
- 步骤：初始化D(源)=0，其他=∞；每次选D最小的未加入节点u加入N'，更新邻居D值

## Distance Vector 算法
- 每个节点维护自己的距离向量（到所有其他节点的成本估计）
- 周期性或链路成本变化时发送自己的DV给邻居
- Bellman-Ford方程：Dx(y) = min_v{c(x,v) + Dv(y)}
- **Count-to-infinity问题**：链路成本增加时可能出现路由环路，收敛慢
- **毒性反转（Poisoned Reverse）**：
  - 节点z通过y到达x时，z告诉y：Dz(x) = ∞（即使实际不是）
  - 打破循环依赖，2轮收敛
  - 代价：路径表项变大（∞标记）

## OSPF（Open Shortest Path First）
- 链路状态路由协议
- 每个路由器洪泛OSPF链路状态通告（直接在IP上运行，Protocol=89）
- 每个路由器有完整拓扑，用Dijkstra算法计算路由
- 安全性：所有OSPF消息都经过认证
- **层次化OSPF**：
  - 区域（Area）划分，减少路由表大小
  - Backbone area (area 0) 连接所有其他area
  - Area border router：运行多个area的路由器

## BGP（Border Gateway Protocol）
- Internet的域间路由标准
- **eBGP**：不同AS之间的BGP会话
- **iBGP**：同一AS内部的BGP会话
- BGP通过TCP连接交换消息（端口179）
- **路径向量协议**：通告的是AS_PATH（经过的AS序列）而非成本
- **策略驱动路由**：基于AS策略选择路径，不仅仅是最短
- BGP属性：
  - AS_PATH：路径经过的AS列表
  - NEXT_HOP：到达目的的下一跳IP
  - LOCAL_PREF：本地优先级（iBGP内部）
- **iBGP/eBGP split-horizon规则**：
  - eBGP学到的路由可以通告给iBGP对等体
  - iBGP学到的路由**不能**通告给其他iBGP对等体（防止环路）
  - 解决方案：route reflector 或 full mesh iBGP

## 为什么需要不同的路由协议？
- **层次化路由**：节省路由表大小，减少更新流量
- **域内 vs 域间**：
  - 域内（Intra-AS）：同一AS内，追求效率（OSPF, RIP）
  - 域间（Inter-AS）：不同AS间，需要策略控制（BGP）

## RIP（Routing Information Protocol）
- 距离向量协议
- 最大跳数15（超过=不可达）
- 每30秒交换路由表
- 适合小型网络

## 路由聚合（Route Aggregation）
- 多个连续地址块合并通告（如200.23.16.0/20）
- 减少路由表大小
- 与最长前缀匹配配合：更具体的路由优先
