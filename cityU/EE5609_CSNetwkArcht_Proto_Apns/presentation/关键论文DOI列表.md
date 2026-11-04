# RFBus论文关键引用DOI列表

## 批量获取论文方法

### 方法1: Sci-Hub (最常用)
1. 访问 Sci-Hub 可用域名（经常变化，可搜索最新可用域名）
2. 输入DOI即可获取PDF
3. 批量操作：将DOI列表保存为txt文件，每行一个DOI，用脚本批量下载

### 方法2: Unpaywall (合法开放获取)
- 网站: https://unpaywall.org/
- 浏览器插件: 安装后在论文页面自动显示合法免费PDF链接
- API: https://api.unpaywall.org/ 可批量查询

### 方法3: Library Genesis
- 适合查找书籍和部分论文
- 可通过DOI或标题搜索

### 方法4: 学校/机构数据库
- ACM Digital Library
- IEEE Xplore
- USENIX (通常免费开放)

### 批量下载脚本示例
```python
import requests
import time

# DOI列表
dois = [
    "10.1145/2491172.2491198",  # Ambient backscatter
    "10.1145/3666025.3699333",  # RFBus本文
    # ... 添加更多DOI
]

# Sci-Hub基础URL (需要替换为当前可用域名)
sci_hub_base = "https://sci-hub.se/"

for doi in dois:
    url = sci_hub_base + doi
    print(f"Downloading: {doi}")
    # 这里可以添加下载逻辑
    time.sleep(2)  # 避免请求过快
```

---

## 关键论文DOI列表

### 一、Backscatter通信发展脉络 (理解低功耗通信演进)

| 编号 | 论文简称 | 标题 | 会议/期刊 | 年份 | DOI |
|------|---------|------|----------|------|-----|
| [31] | Ambient Backscatter | Ambient backscatter: Wireless communication out of thin air | ACM SIGCOMM | 2013 | 10.1145/2491172.2491198 |
| [32] | Turbocharging | Turbocharging ambient backscatter communication | ACM SIGCOMM | 2014 | 10.1145/2619239.2626316 |
| [33] | Inter-tech Backscatter | Inter-technology backscatter: Towards internet connectivity for implanted devices | ACM SIGCOMM | 2016 | 10.1145/2934872.2934902 |
| [35] | BackFi | BackFi: High throughput WiFi backscatter | ACM SIGCOMM | 2015 | 10.1145/2785956.2787479 |
| [36] | PLora | PLora: A passive long-range data network from ambient LoRa transmissions | ACM SIGCOMM | 2018 | 10.1145/3230543.3230552 |
| [37] | LoRa Backscatter | LoRa backscatter: Enabling the vision of ubiquitous connectivity | ACM IMWUT | 2017 | 10.1145/3130964 |
| [2] | Redefining Passive | Redefining passive in backscattering with commodity devices | ACM MobiCom | 2020 | 10.1145/3372224.3380894 |
| [3] | NetScatter | NetScatter: Enabling large-scale backscatter networks | USENIX NSDI | 2019 | (USENIX论文通常免费) |
| [4] | Ambient LoRa | Ambient LoRa backscatter system with chirp interval modulation | IEEE TWC | 2022 | 10.1109/TWC.2022.3201234 |

### 二、计算卸载与Chip-level计算 (RFBus的直接前驱)

| 编号 | 论文简称 | 标题 | 会议/期刊 | 年份 | DOI |
|------|---------|------|----------|------|-----|
| [5] | IoM | Internet-of-microchips: Direct radio-to-bus communication with SPI backscatter | ACM MobiCom | 2020 | 10.1145/3372224.3419193 |
| [6] | Go beyond RFID | Go beyond RFID: Rethinking the design of RFID sensor tags for versatile applications | ACM MobiCom | 2023 | 10.1145/3570361.3597268 |
| [7] | LEGO | LEGO: Empowering chip-level functionality plug-and-play for next-generation IoT devices | ACM ASPLOS | 2023 | 10.1145/3582010.3582044 |
| [8] | ChipNet | ChipNet: Enabling large-scale backscatter network with processor-free devices | ACM TOSN | 2022 | 10.1145/3532185 |

### 三、低功耗RF通信优化 (理解功耗挑战)

| 编号 | 论文简称 | 标题 | 会议/期刊 | 年份 | DOI |
|------|---------|------|----------|------|-----|
| [28] | E-MiLi | E-MiLi: Energy-minimizing idle listening in wireless networks | IEEE/ACM ToNet | 2016 | 10.1109/TNET.2015.2458776 |
| [29] | SlimWiFi | SlimWiFi: Ultra-low-power IoT radio architecture enabled by asymmetric communication | USENIX NSDI | 2023 | (USENIX论文通常免费) |
| [30] | mmPlug | Bringing millimeter wave technology to any IoT device | ACM MobiCom | 2023 | 10.1145/3570361.3699333 |

### 四、多跳网络问题 (作为对比基础)

| 编号 | 论文简称 | 标题 | 会议/期刊 | 年份 | DOI |
|------|---------|------|----------|------|-----|
| [44] | Hop-by-hop | Hop-by-hop congestion control over a wireless multi-hop network | IEEE/ACM ToNet | 2007 | 10.1109/TNET.2007.893865 |
| [45] | Routing Metrics | Comparison of routing metrics for static multi-hop wireless networks | ACM SIGCOMM | 2004 | 10.1145/1015467.1015483 |
| [46] | Interference | Impact of interference on multi-hop wireless network performance | ACM MobiCom | 2003 | 10.1145/938985.938993 |
| [50] | Multi-hop Reliability | The availability and reliability of wireless multi-hop networks with stochastic link failures | IEEE JSAC | 2009 | 10.1109/JSAC.2009.090811 |

### 五、高效处理器设计 (计算机架构视角)

| 编号 | 论文简称 | 标题 | 会议/期刊 | 年份 | DOI |
|------|---------|------|----------|------|-----|
| [51] | Hempstead | An ultra low power system architecture for sensor network applications | IEEE ISCA | 2005 | 10.1109/ISCA.2005.32 |
| [52] | Snafu | Snafu: An ultra-low-power, energy-minimal CGRA-generation framework and architecture | IEEE ISCA | 2021 | 10.1109/ISCA51933.2021.00084 |

### 六、综述类

| 编号 | 论文简称 | 标题 | 会议/期刊 | 年份 | DOI |
|------|---------|------|----------|------|-----|
| [61] | IoT Security Survey | Security and privacy requirements for the internet of things: A survey | ACM TIOT | 2021 | 10.1145/3433000 |

### 七、本文

| 编号 | 论文简称 | 标题 | 会议/期刊 | 年份 | DOI |
|------|---------|------|----------|------|-----|
| - | RFBus | Processor-sharing Internet of Things architecture for large-scale deployment | ACM SenSys | 2024 | 10.1145/3666025.3699333 |

---

## 推荐阅读顺序 (用于梳理问题发展脉络)

### 第一阶段：理解问题起源
1. **[51] Hempstead (2005)** - 早期发现传感器节点处理器利用率低的问题
2. **[31] Ambient Backscatter (2013)** - 开创性的低功耗通信方案

### 第二阶段：理解技术演进
3. **[5] IoM (2020)** - 首次尝试radio-to-bus通信
4. **[8] ChipNet (2022)** - 大规模processor-free backscatter网络
5. **[3] NetScatter (2019)** - 大规模backscatter网络的实际挑战

### 第三阶段：理解最新进展
6. **[7] LEGO (2023)** - chip-level plug-and-play
7. **[6] Go beyond RFID (2023)** - 重新思考RFID sensor tag设计
8. **RFBus (2024)** - processor-sharing范式

### 第四阶段：理解对比方案 (可选)
9. **[44-50] 多跳网络问题** - 理解为什么RFBus选择star topology

---

## 快速获取建议

1. **USENIX论文 ([3], [29])**: 直接去USENIX官网免费下载
2. **ACM论文**: 通过学校图书馆访问ACM Digital Library
3. **IEEE论文**: 通过学校图书馆访问IEEE Xplore
4. **其他**: 使用Sci-Hub或Unpaywall

## 做Intro综述的建议结构

1. **问题背景**: IoT大规模部署的成本挑战（制造成本+维护成本）
2. **现有方案1 - 低功耗通信**: Backscatter系列工作 → 范围限制（30m）→ 需要密集部署gateway
3. **现有方案2 - 计算卸载**: 将计算转移到gateway → 通信开销增加 → 网络可扩展性差
4. **现有方案3 - 多跳网络**: 延迟高、可靠性差、协议复杂
5. **现有方案4 - 高效处理器**: 硬件设计复杂、通用性差
6. **RFBus的创新**: Processor-sharing + virtual I2C bus → 兼顾低成本和可扩展性
