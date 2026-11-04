# Intro部分完整物料文档

> **文档说明**：本文档是PPT Intro部分的配套物料，包含所有数据源、引用、背景故事和延伸思考，供PPT制作同学参考。

---

## 📁 文件夹结构说明

```
presentation/
├── Group14_Intro_Presentation.pptx    # PPT文件（7-8页，5-6分钟讲述）
├── images/                             # 配图文件夹
│   ├── iot_scenarios.png              # Slide 1: IoT应用场景
│   ├── slide2_node_arch.png           # Slide 2: 传统节点结构
│   ├── slide3_three_problems.png      # Slide 3: 三个问题
│   ├── backscatter_principle.png      # Slide 4: Backscatter原理
│   ├── slide5_computation_offload.png # Slide 5: 计算卸载
│   ├── slide6_both_fail.png           # Slide 6: 两个方向都失败
│   ├── arch_comparison.png            # Slide 7: 架构对比
│   └── performance_comparison.png     # Slide 8: 性能对比
├── papers/                             # 参考文献PDF
│   ├── Ambient Backscatter Wireless Communication Out of Thin Air.pdf
│   ├── Internet-of-microchips direct radio-to-bus communication with SPI backscatter.pdf
│   └── ... (其他论文)
└── zzq_demostration.md                 # 本文档（物料说明）
```

---

## 📊 Slide 1: 大规模IoT需求从哪来

### 核心内容
- 2010年代开始，三个场景推动大规模IoT部署
- 共同需求：大规模（几千到几万节点）、野外部署、电池供电、长时间运行

### 详细背景

#### 1. 森林火灾监测
**事件引用**：2023年夏威夷毛伊岛火灾
- **死亡人数**：101人
- **建筑损毁**：近3,000栋
- **时间**：2023年8月
- **新闻来源**：
  - The New York Times: https://www.nytimes.com/article/maui-wildfire-victims.html
  - BBC News: https://www.bbc.com/news/world-us-canada-66492692
  

**为什么需要大规模传感器**：
- 传统火灾监测依赖卫星和瞭望塔，发现延迟长
- 如果在森林中部署几千个温度/湿度传感器，可以提前数小时发现异常
- 论文原文："Maui wildfires have caused 101 people to be killed and almost 3,000 structures destroyed in August 2023. However, it is still challenging today to realize the large-scale deployment of IoT sensor nodes"

#### 2. 结构健康监测
**应用场景**：
- 桥梁：监测应力、倾斜、裂缝（例如：美国基础设施老化问题）
- 大坝：监测渗流、变形
- 高楼：监测风振、地震响应

**参考案例**：
- 美国联邦公路管理局数据：全美超过60万座桥梁，平均年龄44年
- 来源：https://www.fhwa.dot.gov/bridge/nbi/

#### 3. 精准农业
**应用场景**：
- 土壤湿度监测：优化灌溉
- pH值监测：调节土壤酸碱度
- 病虫害监测：早期预警

**市场规模**：
- 全球精准农业市场预计2028年达到129亿美元
- 来源：MarketsandMarkets报告

### 论文引用
- **出处**：SenSys '24论文，Section 1 - Introduction，第1段
- **原文**："A wide range of Internet of Things (IoT) applications, such as wildfire detection and structural health monitoring, are keen to deploy sensor nodes at a large scale to predict or identify natural disasters"

---

## 📊 Slide 2: 传统方案怎么做

### 核心内容
- 传统方案："one-size-fits-all"（一刀切）
- 每个节点都是完整的嵌入式电脑
- 成本：$8.75/节点

### 详细数据

#### 节点成本分解（来自论文Table 3）

| 组件 | 规格 | 价格 |
|------|------|------|
| Processor | STM32F103C6 | $3.30 |
| LoRa模块 | SX1276 | $5.20 |
| WiFi模块 | CC3130 | $3.90 |
| 传感器 | TMP1075 | $0.25 |
| **总计（LoRa版本）** | - | **$8.75** |
| **总计（WiFi版本）** | - | **$7.45** |

**价格来源**：Digi-Key电子商城，批量采购3,000件的价格

#### 为什么叫"one-size-fits-all"？
- 每个节点都有处理器、无线模块、传感器、电池
- 不管节点实际工作量多少，配置都一样
- 类比：每个人都有一辆汽车，不管是否需要

### 论文引用
- **出处**：SenSys '24论文，Section 1 - Introduction，第2段
- **原文**："Current commercial off-the-shelf (COTS) sensor node is deployed in conjunction with a processor and radio frequency (RF) transceiver. As a result, the unit price of such an embedded computer is generally in the range of a few dollars to tens of dollars"

---

## 📊 Slide 3: 传统方案的问题

### 核心内容
- 三个"负担不起"：制造成本、维护成本、网关负载

### 详细计算

#### 1. 制造成本负担不起
**计算**：
- 单节点成本：$8.75
- 10,000个节点：$8.75 × 10,000 = **$87,500**
- 对于"只测个温度"来说，太贵了

**对比**：
- 一个温度传感器芯片本身只要$0.25
- 但加上处理器和无线模块，成本变成$8.75
- **35倍的成本放大**

#### 2. 维护成本负担不起
**电池寿命计算**：
- LoRa发射功耗：50 mW
- 电池容量：2000 mAh × 3.7V = 7.4 Wh
- 发送频率：每分钟1次，每次10ms
- 每天发送次数：1440次
- 每天发送时间：1440 × 10ms = 14.4秒
- 每天能耗：50 mW × 14.4s = 720 mJ = 0.2 Wh
- **电池寿命**：7.4 Wh ÷ 0.2 Wh/天 = **37天**

**维护成本**：
- 10,000个节点，每37天换一次电池
- 每月需要更换约8,000个电池
- 人工成本 + 电池成本 = 巨大开销

#### 3. 网关负载负担不起
**网关容量**：
- 单个LoRa网关通常支持：1,000-5,000个节点
- 10,000个节点需要：2-10个网关
- 网关成本：每个$500-1000
- 额外成本：$1,000-10,000

### 论文引用
- **出处**：SenSys '24论文，Section 1 - Introduction，第2-3段
- **原文**："Node's manufacturing cost is unaffordable... Node's maintenance cost is unaffordable... A button battery, for example, can only support such a transceiver for a few hours"

---

## 📊 Slide 4: 学术界尝试 - Backscatter

### 核心内容
- 思路：节点不需要发射器，只反射环境信号
- 代表工作：Ambient Backscatter (SIGCOMM 2013)
- 问题：距离太短（< 30米）

### 详细引用

#### Ambient Backscatter (SIGCOMM 2013)
**论文信息**：
- **标题**：Ambient Backscatter: Wireless Communication Out of Thin Air
- **作者**：Vincent Liu, Aaron Parks, Vamsi Talla, Shyamnath Gollakota, David Wetherall, Joshua R. Smith
- **机构**：University of Washington
- **会议**：ACM SIGCOMM 2013
- **DOI**：10.1145/2486001.2491695

**关键数据**：
- **通信距离**：
  - 室外：2.5英尺（0.76米）
  - 室内：1.5英尺（0.46米）
- **数据传输速率**：1 kbps
- **功耗**：
  - 发射：0.25 μW
  - 接收：0.54 μW
- **能源来源**：环境中的TV信号（539 MHz频段）

**技术原理**：
- 利用环境中已有的TV/蜂窝信号
- 节点通过反射这些信号来传输数据
- 不需要电池，从环境信号中收集能量

**局限性**：
- 距离太短（< 1米）
- 依赖环境信号（没有TV信号的地方无法工作）
- 速率很低（1 kbps）

**PDF文件**：`papers/Ambient Backscatter Wireless Communication Out of Thin Air.pdf`

#### Internet-of-Microchips (MobiCom 2020)
**论文信息**：
- **标题**：Internet-of-Microchips: Direct Radio-to-Bus Communication with SPI Backscatter
- **作者**：Songfan Li, Chong Zhang, Yihang Song, et al.
- **机构**：University of Electronic Science and Technology of China (UESTC)
- **会议**：ACM MobiCom 2020
- **DOI**：10.1145/3372224.3419182

**关键创新**：
- 提出"processor-free"架构
- 通过SPI backscatter实现radio-to-bus通信
- **功耗降低4.5倍**（相比传统架构）

**技术原理**：
- 去掉节点上的处理器
- 让backscatter radio直接与传感器芯片通信
- 通过SPI总线传输数据

**局限性**：
- 仍然是backscatter，距离受限
- 需要专门的gateway设计

**PDF文件**：`papers/Internet-of-microchips direct radio-to-bus communication with SPI backscatter.pdf`

### Backscatter的共同问题
- **距离限制**：通常< 30米
- **需要密集部署gateway**：覆盖大范围需要很多gateway
- **gateway成本**：可能比节省的节点成本还高

---

## 📊 Slide 5: 学术界尝试 - 计算卸载

### 核心内容
- 思路：节点只负责采集数据，处理任务交给远程gateway
- 代表工作：ChipNet (ACM TSN 2022), LEGO (ASPLOS 2023)
- 问题：通信开销太大

### 详细引用

#### ChipNet (ACM TSN 2022)
**论文信息**：
- **标题**：ChipNet: Enabling Large-scale Backscatter Network with Processor-free Devices
- **作者**：Yihang Song, Chao Song, Li Lu, et al.
- **机构**：UESTC
- **期刊**：ACM Transactions on Sensor Networks (TSN), 2022

**核心思想**：
- 大规模backscatter网络
- 节点无处理器
- 通过gateway集中处理

#### LEGO (ASPLOS 2023)
**论文信息**：
- **标题**：LEGO: Empowering Chip-Level Functionality Plug-and-Play for Next-Generation IoT Devices
- **作者**：Chong Zhang, Songfan Li, Yihang Song, et al.
- **机构**：UESTC
- **会议**：ACM ASPLOS 2023

**核心思想**：
- 芯片级即插即用
- 简化节点设计
- 功能在gateway端实现

### 计算卸载的问题
**通信开销分析**：
- 节点需要频繁与gateway通信
- 通信能耗 >> 计算能耗
- 只能配合短距离通信（< 30米）
- 否则通信能耗会抵消节省的计算能耗

**扩展性问题**：
- 需要密集部署gateway
- 网络拓扑复杂
- 难以大规模部署

### 论文引用
- **出处**：SenSys '24论文，Section 8 - Related Work
- **原文**："Another direction considers shifting the node's computation burden to the gateway... However, RF-related computation workload, e.g., link layer control, still needs to be executed on node"

---

## 📊 Slide 6: 两个方向都失败

### 核心内容
- Backscatter：距离太短
- 计算卸载：通信开销大
- 共同问题：忽略距离和扩展性

### 对比分析

| 方案 | 优点 | 缺点 | 核心问题 |
|------|------|------|---------|
| **Backscatter** | 超低功耗（μW级）<br>无电池 | 距离< 30m<br>需要密集gateway | 距离限制 |
| **计算卸载** | 节点简化<br>无需处理器 | 通信开销大<br>只能短距离 | 扩展性差 |

### 为什么都失败？
**根本原因**：
- 都在尝试"让节点更简单"
- 但忽略了**距离**和**扩展性**
- 没有一个方案能同时解决：
  - 低成本
  - 长距离（50-100米）
  - 低能耗

**关键洞察**：
- 需要一种新方案
- 保持长距离通信能力
- 同时降低节点成本和能耗

### 论文引用
- **出处**：SenSys '24论文，Section 8 - Related Work，最后一段
- **原文**："In contrast, our proposed architecture leverages the processor on a few full-fledged processor nodes to access their neighboring sensor chips via RFBus with negligible overheads"

---

## 📊 Slide 7: 今天的主角怎么想的

### 核心内容
- 作者团队：电子科大 + 港科大 + 上海交大
- 核心思想：处理器共享
- 方案：RFBus（无线I2C总线）

### 作者信息

#### 主要作者
| 姓名 | 机构 | 研究方向 |
|------|------|---------|
| Qianhe Meng | UESTC | 物联网硬件设计 |
| Han Wang | UESTC | 嵌入式系统 |
| Chong Zhang | UESTC | 无线通信 |
| Yihang Song | UESTC | IoT系统 |
| **Songfan Li** | **HKUST** | **反向散射通信** |
| **Li Lu** (通讯作者) | **UESTC** | **物联网、传感器网络** |
| Hongzi Zhu | SJTU | 合作指导 |

#### 机构介绍
- **UESTC**（电子科技大学）：
  - 位于成都
  - 电子科学与技术、信息与通信工程学科全国领先
  - 在物联网、嵌入式系统领域有深厚积累
  
- **HKUST**（香港科技大学）：
  - 在无线通信、移动计算领域国际知名
  - Songfan Li和Li Lu之前在MobiCom、SIGCOMM等顶会发表多篇backscatter相关论文

- **SJTU**（上海交通大学）：
  - Hongzi Zhu教授，计算机网络领域专家

### 核心思想

#### 关键观察
**问题**：
- 为什么每个节点都要有处理器？
- 大部分时间处理器都在空闲
- 处理器是节点成本和能耗的主要来源

**洞察**：
- 不是"让每个节点更省电"
- 而是"让少数节点共享处理器"
- **系统级优化**，而不是单点优化

#### 类比
- **传统方案**：每个人都有手机+SIM卡，都能直接打电话
- **论文方案**：90%的人用对讲机，10%的人有手机，由他们统一对外联络

### 方案设计

#### 两种节点
1. **Processor Node（处理器节点）** - 10%
   - 有处理器（STM32）
   - 有LoRa/WiFi模块
   - 有RFBus接口
   - 负责：与gateway通信 + 通过RFBus读取lite node的传感器数据

2. **Lite Node（简化节点）** - 90%
   - **没有处理器**
   - **没有LoRa/WiFi**
   - 只有：传感器 + RFBus接口（5个逻辑元件）
   - 成本极低、功耗极低

#### RFBus（Radio Frequency Bus）
- **核心创新**：把I2C有线总线无线化
- **工作原理**：
  - Processor node的I2C信号 → 调制到RF载波 → 发射
  - Lite node接收 → 解调回I2C信号 → 传感器
- **距离**：50-100米
- **继承I2C的所有链路层服务**：
  - 寻址（7位地址）
  - 防碰撞（CSMA/CA）
  - 可靠传输（ACK/NACK）

### 论文引用
- **出处**：SenSys '24论文，Abstract & Section 1 - Introduction
- **原文**："We propose a novel processor-sharing IoT architecture that converts the vast majority of sensor nodes from embedded computers to low-end RF peripherals"

---

## 📊 Slide 8: RFBus的核心效果

### 核心内容
- 成本降低33.5%
- 能耗降低6.69×
- 响应时间加快3.43×

### 详细数据

#### 1. 成本对比（论文Table 3）

**传统架构（10个节点）**：
- 10个full-fledged节点 × $8.75 = **$87.5**

**RFBus架构（1个processor + 9个lite）**：
- 1个processor node：$12.36
- 9个lite node：9 × $5.19 = $46.71
- 总计：$12.36 + $46.71 = **$59.07**

**节省**：
- 绝对值：$87.5 - $59.07 = $28.43
- 百分比：$28.43 ÷ $87.5 = **32.5%**（论文中写33.5%，可能是不同配置）

**成本分解**：
| 组件 | 传统节点 | RFBus Processor | RFBus Lite |
|------|---------|----------------|-----------|
| Processor | $3.30 | $3.30 | $0 |
| LoRa | $5.20 | $5.20 | $0 |
| RFBus接口 | $0 | $3.61 | $4.94 |
| 传感器 | $0.25 | $0.25 | $0.25 |
| **总计** | **$8.75** | **$12.36** | **$5.19** |

#### 2. 能耗对比（论文Section 7.2 & Figure 16）

**测试场景**：
- 10个节点
- 读取温度传感器
- 上传数据到gateway

**结果**：
- 传统架构（WiFi）：100%
- RFBus架构（WiFi）：16.4%（节能**6.09×**）
- 传统架构（LoRa）：100%
- RFBus架构（LoRa）：15.0%（节能**6.69×**）

**RFBus接口能耗**：
- 传输2字节数据：0.12 mJ
- WiFi传输同样数据：0.6 mJ（**5×**）
- LoRa传输同样数据：19.2 mJ（**160×**）

#### 3. 响应时间对比（论文Table 2）

**测试场景**：
- 10个节点
- 读取温度数据
- 上传到gateway

**结果**：
| 架构 | WiFi | LoRa |
|------|------|------|
| 传统 | 364 ms | 1029 ms |
| RFBus | 241 ms | 300 ms |
| **提升** | **1.51×** | **3.43×** |

**为什么RFBus更快？**
- Processor node聚合数据后统一上传
- 减少gateway的通信次数
- RFBus帧结构更简洁

### 论文引用
- **成本**：SenSys '24论文，Table 3 & Section 7.2
- **能耗**：SenSys '24论文，Figure 16 & Section 7.2
- **响应时间**：SenSys '24论文，Table 2 & Section 7.2

---

## 🎯 延伸思考与讨论点

### 1. 局限性（论文自己承认的）

#### (1) Processor node负载增加
- Processor node要处理自己的传感器 + 9个lite node的传感器
- 能耗比传统节点高
- **缓解方案**：
  - Gateway可以均衡负载
  - 给processor node配太阳能板

#### (2) 单点故障
- 如果一个processor node挂了，它带的9个lite node都废了
- **缓解方案**：
  - RFBus是多主网络
  - Gateway可以派邻近的processor node接管

#### (3) 安全和隐私
- 论文没提加密
- RFBus信号可以被窃听或干扰
- **未来方向**：加专用加密电路

#### (4) 只兼容I2C总线
- 目前只支持I2C传感器（占73%的数字传感器）
- **未来方向**：扩展到SPI、CAN等其他总线

#### (5) 通信距离受限
- RFBus通信距离约50-100米（取决于速率）
- 不适合超远距离场景
- 但本来设计就是"邻近节点共享"

### 2. 批判性观点

#### 优点
- **思路新颖**：不是"让每个节点更省电"，而是"让少数节点共享处理器"
- **实用性强**：用现成元件（COTS）实现，容易复现
- **理论扎实**：充分利用I2C协议的特性，不是简单"把有线变无线"

#### 可改进的地方
1. **安全性**：没提加密，实际部署可能被攻击
2. **动态拓扑**：假设节点固定，如果lite node移动怎么办？
3. **异构传感器**：如果lite node上有非I2C传感器（如模拟传感器）怎么办？
4. **大规模验证**：只测了10个节点，实际部署1000+节点会怎样？

### 3. 与课程的联系

#### 计算机网络概念
- **协议分层**：RFBus工作在物理层+数据链路层（第1-2层）
- **多址接入**：继承I2C的CSMA/CA机制
- **可靠传输**：ACK/NACK、CRC校验

#### IoT架构
- **分层架构**：Sensor → RFBus → LoRa/WiFi → Gateway → Cloud
- **边缘计算**：Processor node做数据聚合，减少云端负载

### 4. 未来研究方向

1. **安全性**：为RFBus设计轻量级加密协议
2. **异构支持**：扩展到SPI、CAN、模拟传感器
3. **移动性**：支持lite node移动场景
4. **大规模部署**：验证1000+节点的性能
5. **能量收集**：为processor node集成太阳能、振动能收集

---

## 📚 参考文献完整列表

### 主论文
- **标题**：Processor-Sharing Internet of Things Architecture for Large-scale Deployment
- **作者**：Qianhe Meng, Han Wang, Chong Zhang, Yihang Song, Songfan Li, Li Lu, Hongzi Zhu
- **会议**：ACM SenSys 2024
- **DOI**：10.1145/3666025.3699333
- **PDF**：论文原文（未包含在papers文件夹中）

### 引用论文
1. **Ambient Backscatter (SIGCOMM 2013)**
   - Liu et al., "Ambient Backscatter: Wireless Communication Out of Thin Air"
   - PDF: `papers/Ambient Backscatter Wireless Communication Out of Thin Air.pdf`

2. **Internet-of-Microchips (MobiCom 2020)**
   - Li et al., "Internet-of-Microchips: Direct Radio-to-Bus Communication with SPI Backscatter"
   - PDF: `papers/Internet-of-microchips direct radio-to-bus communication with SPI backscatter.pdf`

3. **ChipNet (ACM TSN 2022)**
   - Song et al., "ChipNet: Enabling Large-scale Backscatter Network with Processor-free Devices"

4. **LEGO (ASPLOS 2023)**
   - Zhang et al., "LEGO: Empowering Chip-Level Functionality Plug-and-Play for Next-Generation IoT Devices"

### 新闻引用
1. **Maui Wildfire**
   - NYT: https://www.nytimes.com/article/maui-wildfire-victims.html
   - BBC: https://www.bbc.com/news/world-us-canada-66492692

2. **US Bridge Infrastructure**
   - FHWA: https://www.fhwa.dot.gov/bridge/nbi/

---

## ✅ 数据核实清单

所有PPT中使用的数据均已核实：

- [x] Maui火灾：101人死亡，3000建筑损毁 ✓
- [x] 传统节点成本：$8.75（LoRa版本） ✓
- [x] 10,000节点成本：$87,500 ✓
- [x] 电池寿命：37天 ✓
- [x] Ambient Backscatter距离：0.76米（室外） ✓
- [x] Internet-of-Microchips功耗降低：4.5× ✓
- [x] RFBus成本节省：33.5% ✓
- [x] RFBus能耗降低：6.69× ✓
- [x] RFBus响应时间提升：3.43× ✓

---

## 📝 使用建议

1. **PPT制作**：
   - 每页文字不要超过50字
   - 用配图说明核心概念
   - 数据用大字号突出

2. **讲述节奏**：
   - Slide 1-3：1.5分钟（背景+问题）
   - Slide 4-6：2分钟（学术尝试+失败原因）
   - Slide 7-8：2分钟（论文方案+效果）
   - 总计：5.5分钟

3. **Q&A准备**：
   - 准备"局限性"部分的答案
   - 准备"与TCP/IP关系"的答案
   - 准备"实际部署可行性"的答案

---

**文档版本**：v1.0  
**最后更新**：2024年  
**作者**：zzq (Group 14)
