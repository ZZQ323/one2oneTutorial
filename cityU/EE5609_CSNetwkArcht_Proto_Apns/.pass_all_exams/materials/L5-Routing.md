# L5 - Network Layer Part II: Routing

## 核心主题
- 路由算法：Dijkstra（链路状态）、Distance Vector（距离向量）
- 路由协议：OSPF、BGP（eBGP/iBGP）
- 转发 vs 路由的区别
- 毒性反转（poisoned reverse）

## Forwarding vs Routing
- **Forwarding（转发）**：数据平面功能，将包从路由器输入移到适当输出
- **Routing（路由）**：控制平面功能，确定包从源到目的经过的路径
- 路由算法在控制平面运行，决定转发表

## 路由算法分类
- **全局/集中式**：所有路由器有完整拓扑和链路成本 → 链路状态算法（Dijkstra）
- **分布式**：迭代计算，只与邻居交换信息 → 距离向量算法
- **静态 vs 动态**：路由变化速度

## Dijkstra 算法（链路状态）
- 所有节点有完整拓扑信息（通过链路状态广播）
- 从源节点计算到所有其他节点的最短路径
- 符号：
  - c(x,y): 节点x到y的直接链路成本
  - D(v): 从源到v的当前最小成本估计
  - p(v): 从源到v路径上的前驱节点
  - N': 已确定最小成本路径的节点集合
- 步骤：初始化D(源)=0，其他=∞；每次选D最小的未加入节点u加入N'，更新邻居D值
- **复杂度**：O(n²)消息，O(n²)算法
- **结果**：生成最短路径树和转发表

## Distance Vector 算法
- 每个节点维护自己的距离向量（到所有其他节点的成本估计）
- 周期性或链路成本变化时发送自己的DV给邻居
- Bellman-Ford方程：Dx(y) = min_v{c(x,v) + Dv(y)}
- **迭代异步**：每个节点等待（链路成本变化或邻居消息），重新计算DV，如果改变则通知邻居
- **信息扩散**：t时刻的状态在t+hops时刻可影响hops距离的节点
- **Count-to-infinity问题**：链路成本增加时可能出现路由环路，收敛慢
  - "Good news travels fast"：成本减少快速收敛
  - "Bad news travels slow"：成本增加慢速收敛（count-to-infinity）
- **毒性反转（Poisoned Reverse）**：
  - 节点z通过y到达x时，z告诉y：Dz(x) = ∞（即使实际不是）
  - 打破循环依赖，2轮收敛
  - 代价：路径表项变大（∞标记）

## LS vs DV算法对比
| 特性 | Link State | Distance Vector |
|------|-----------|-----------------|
| 消息复杂度 | O(n²)消息 | 邻居间交换 |
| 收敛时间 | O(n²)算法，可能振荡 | 变化，可能路由环路，count-to-infinity |
| 鲁棒性 | 路由器可广播错误链路成本，但只计算自己的表 | DV可广播错误路径成本，错误传播到整个网络 |

## OSPF（Open Shortest Path First）
- 链路状态路由协议
- 每个路由器洪泛OSPF链路状态通告（直接在IP上运行，Protocol=89）
- 每个路由器有完整拓扑，用Dijkstra算法计算路由
- 安全性：所有OSPF消息都经过认证
- **层次化OSPF**：
  - 区域（Area）划分，减少路由表大小
  - Backbone area (area 0) 连接所有其他area
  - Area border router：运行多个area的路由器，汇总距离到backbone
  - Internal router：只在area内洪泛LS，计算area内路由
  - Boundary router：连接到其他AS

## BGP（Border Gateway Protocol）
- Internet的域间路由标准
- "glue that holds the Internet together"
- **eBGP**：不同AS之间的BGP会话
- **iBGP**：同一AS内部的BGP会话
- BGP通过TCP连接交换消息（端口179）
- **BGP消息类型**：
  - OPEN：打开TCP连接，认证
  - UPDATE：通告新路径或撤回旧路径
  - KEEPALIVE：保持连接，确认OPEN
  - NOTIFICATION：报告错误，关闭连接
- **路径向量协议**：通告的是AS_PATH（经过的AS序列）而非成本
- **路径属性**：
  - AS_PATH：路径经过的AS列表
  - NEXT_HOP：到达目的的下一跳IP
- **策略驱动路由**：基于AS策略选择路径，不仅仅是最短
  - import policy：决定接受/拒绝路径
  - 决定通告给哪些邻居AS
- **iBGP/eBGP split-horizon规则**：
  - eBGP学到的路由可以通告给iBGP对等体
  - iBGP学到的路由**不能**通告给其他iBGP对等体（防止环路）
  - 解决方案：route reflector 或 full mesh iBGP
- **BGP填充转发表**：
  - 通过iBGP学习到"到X的路径经过gateway 1c"
  - 通过OSPF确定到gateway的内部路径
  - 最终转发表：目的X → 接口（到gateway的接口）

## 为什么需要不同的路由协议？
- **层次化路由**：节省路由表大小，减少更新流量
- **域内 vs 域间**：
  - 域内（Intra-AS）：同一AS内，追求效率（OSPF, RIP, EIGRP）
  - 域间（Inter-AS）：不同AS间，需要策略控制（BGP）
- **策略 vs 性能**：
  - Inter-AS：admin想控制流量路由，谁通过其网络
  - Intra-AS：单一admin，策略问题少，可专注性能

## RIP（Routing Information Protocol）
- 距离向量协议
- 最大跳数15（超过=不可达）
- 每30秒交换路由表
- 适合小型网络

## 路由聚合（Route Aggregation）
- 多个连续地址块合并通告（如200.23.16.0/20）
- 减少路由表大小
- 与最长前缀匹配配合：更具体的路由优先
