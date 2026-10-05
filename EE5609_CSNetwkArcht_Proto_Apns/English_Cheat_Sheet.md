# EE5609 English Key Terms — A4 Double-Side Cheat Sheet

> Side A = terms & phrases (read English questions without panic)
> Side B = formulas + essay skeletons in English (write English answers)

---

## SIDE A: Terminology by Topic

### 1. Layering & Encapsulation
| English | 中文 | Note |
|---|---|---|
| OSI 7-layer: Physical / Data Link / Network / Transport / Session / Presentation / Application | 物理/链路/网络/传输/会话/表示/应用 | memorize order |
| encapsulation / decapsulation | 封装/解封装 | |
| PDU: message → segment → datagram(packet) → frame → bits | 报文→段→数据报→帧→比特 | app/transport/network/link/physical |
| header / trailer / payload | 头/尾/载荷 | |
| hub, repeater (L1); switch, bridge (L2); router (L3) | 集线器/中继器；交换机/网桥；路由器 | |
| demultiplexing | 解复用 | Type field / Protocol field |

### 2. Switching & Delay
| English | 中文 |
|---|---|
| circuit switching / packet switching | 电路交换/分组交换 |
| datagram vs virtual circuit (VC) | 数据报 vs 虚电路 |
| connection-oriented / connectionless | 面向连接/无连接 |
| store-and-forward | 存储转发 |
| statistical multiplexing | 统计复用 |
| resource reservation / dedicated | 资源预留/独占 |
| transmission delay = L/R | 传输延迟 |
| propagation delay = d/s | 传播延迟 |
| processing delay, queueing delay | 处理延迟、排队延迟 |
| pipelining | 流水线 |
| best-effort delivery | 尽力而为交付 |

### 3. Resilience
| English | 中文 |
|---|---|
| availability / reliability / failure probability | 可用性/可靠性/失效概率 |
| links in series / in parallel | 串联/并联链路 |
| downtime / uptime | 停机/正常运行时间 |
| MTBF / MTTF / MTTR | 平均故障间隔/平均失效时间/平均修复时间 |
| single point of failure | 单点故障 |
| redundancy / alternative path | 冗余/备用路径 |

### 4. Data Link: Flow & Error Control
| English | 中文 |
|---|---|
| Stop-and-Wait ARQ | 停等 ARQ |
| Sliding Window protocol | 滑动窗口协议 |
| Go-Back-N (GBN) / Selective Repeat (Selective Reject) | 回退N/选择重传 |
| cumulative ACK / duplicate ACK / NAK | 累积确认/重复确认/否定确认 |
| retransmission / timeout | 重传/超时 |
| link utilization / efficiency | 链路利用率/效率 |
| sequence number, window size | 序号、窗口大小 |
| out-of-order frames, buffer | 乱序帧、缓存 |
| error detection vs error correction | 检错 vs 纠错 |
| parity check / two-dimensional parity | 奇偶校验/二维奇偶校验 |
| CRC: generator (polynomial) G, remainder R, dividend D·2^r | CRC:生成多项式/余数 |
| burst error | 突发错误 |
| FEC (Forward Error Correction), Hamming code | 前向纠错、汉明码 |

### 5. MAC Protocols
| English | 中文 |
|---|---|
| channel partitioning: TDMA / FDMA / CDMA (Code Division Multiple Access) | 信道划分 |
| random access | 随机接入 |
| controlled access: polling, token passing | 受控接入：轮询、令牌传递 |
| ALOHA / slotted ALOHA | |
| collision / collision detection / collision avoidance | 碰撞/检测/避免 |
| CSMA (Carrier Sense Multiple Access) | 载波监听多路访问 |
| CSMA/CD / CSMA/CA | |
| carrier sensing, listen before transmit | 载波监听、先听后发 |
| binary exponential backoff | 二进制指数退避 |
| jam signal | 阻塞信号 |
| slot / contention | 时隙/争用 |
| broadcast channel / shared medium | 广播信道/共享介质 |

### 6. Ethernet & WLAN
| English | 中文 |
|---|---|
| Ethernet frame: preamble, SFD (start frame delimiter), dest./src. MAC address, type field, payload, CRC (FCS) | 以太网帧各字段 |
| minimum frame size 64 bytes / padding | 最小帧长/填充 |
| unreliable, connectionless | 不可靠、无连接 |
| WLAN, STA (station), AP (access point) | 无线局域网/站点/接入点 |
| BSS / ESS / IBSS, infrastructure mode / ad hoc mode | 基本服务集/扩展服务集；基础架构/自组织模式 |
| distribution system (DS) | 分配系统 |
| hidden terminal / exposed terminal problem | 隐藏/暴露终端问题 |
| path loss, multipath propagation, interference | 路径损耗、多径传播、干扰 |
| RTS / CTS / ACK; DIFS / SIFS; backoff counter | 请求发送/允许发送；帧间间隔；退避计数器 |
| DCF (distributed coordination) / PCF (point coordination) | 分布式协调/点协调 |
| virtual carrier sensing (duration field) | 虚拟载波监听（时长字段） |
| 802.11 frame: Address 1 (receiver), 2 (transmitter), 3 (router interface), 4 (ad hoc only) | 四地址字段 |

### 7. Network Layer
| English | 中文 |
|---|---|
| IP datagram header: version, header length, total length, identification, flags (DF/MF), fragment offset, TTL, protocol, header checksum, source/destination address, options | IP 头字段 |
| DF = Don't Fragment, MF = More Fragments | 禁止分片/更多分片 |
| MTU (Maximum Transmission Unit) | 最大传输单元 |
| fragmentation / reassembly (only at destination) | 分片/重组（只在目的端） |
| CIDR, prefix length, subnet mask | 无类域间路由、前缀、子网掩码 |
| network address / broadcast address / usable host range | 网络地址/广播地址/可用主机范围 |
| VLSM (Variable Length Subnet Mask), address block allocation | 可变长子网划分 |
| private address space / public address | 私网/公网地址 |
| NAT (Network Address Translation), translation table, port mapping | 地址转换、转换表、端口映射 |
| DHCP: Discover → Offer → Request → ACK; lease; broadcast | 四步、租期 |
| default gateway / first-hop router | 默认网关/第一跳路由器 |
| ARP: request (broadcast) / reply (unicast), ARP cache | 广播请求/单播回复、缓存 |
| longest-prefix matching, forwarding table, route aggregation, default route | 最长前缀匹配、转发表、路由聚合 |
| next hop | 下一跳 |
| IPv6: 128-bit address, fixed 40-byte header, no checksum, no router fragmentation, flow label, hop limit, next header | |
| PMTUD (Path MTU Discovery), "Packet Too Big" | 路径MTU发现 |
| tunneling (IPv6-in-IPv4), transition | 隧道、过渡 |
| Neighbor Discovery (NS/NA/RA), ICMPv6 | 邻居发现（替代 ARP） |
| ICMP: echo request/reply (ping), destination unreachable, TTL expired / time exceeded, fragmentation needed | |
| traceroute | 路由追踪 |
| end-to-end principle | 端到端原则 |

---

## SIDE B: Formulas + Essay Skeletons (write IN ENGLISH)

### Formulas (English variable names as they appear in exam questions)
```
Utilization:  U = 1/(1+2a)          a = T_prop / T_frame (propagation ratio)
Sliding win:  U = N/(1+2a) if N < 2a+1;  U = 1 if N ≥ 2a+1
Min window:   N = ceil( U_min × (1+2a) )
CRC:          R = (D × 2^r) mod G   (mod-2 division)
Min frame:    L_min ≥ 2 × T_prop(end-to-end) × R_bandwidth
Availability: series: r = r1×r2 ; parallel: b = b1×b2 ; b = 1 − r
Delays:       T_trans = L/R ; T_prop = d/s
Pipeline:     Total = k×(T_x + d) + (n−1)×T_x
Circuit:      Total = s + x/b + k·d
Fragment:     Offset = (byte position in original payload) / 8
Subnet:       block size = 2^(32−prefix);  usable hosts = block − 2
ALOHA:        Slotted: E = N·p(1−p)^(N−1), p*=1/N, E_max = 1/e ≈ 37%
              Pure:    S = G·e^(−2G), G*=1/2, S_max = 1/(2e) ≈ 18%
```

### Essay skeleton phrases (copy these sentence openers)
```
GBN vs SR:
 "In GBN the receiver window is 1: it discards out-of-order frames and
  re-sends the last cumulative ACK. The sender retransmits the lost frame
  AND ALL subsequent frames. In Selective Repeat the receiver buffers
  out-of-order frames and the sender retransmits ONLY the missing frame,
  at the cost of more complex receiver buffer management."

Circuit vs packet switching:
 "Circuit switching reserves dedicated end-to-end resources (guaranteed
  performance, wasteful when idle, both ends at the same rate); packet
  switching shares links via statistical multiplexing (no setup, efficient
  for bursty data, but queueing delay and possible loss)."

Datagram vs VC:
 "Datagram: each packet routed independently, carries full destination
  address, stateless routers, may arrive out of order (Internet).
  VC: pre-established path, packets carry a VCI, routers keep per-connection
  state, in-order delivery — but NO resource reservation (X.25, ATM)."

Hidden terminal:
 "A and C are out of each other's range but both within B's range. Each
  senses the channel IDLE and transmits simultaneously; the collision
  occurs AT B. RTS/CTS fixes it: B's CTS (heard by C) carries a duration
  field that silences neighbors — virtual carrier sensing."

DHCP:
 "Discover (broadcast, src 0.0.0.0:68 → 255.255.255.255:67), Offer,
  Request, ACK. Also provides subnet mask, default gateway, DNS server.
  Addresses are leased and can be renewed/reused."

NAT:
 "Outgoing: replace (src IP, src port) with (NAT IP, new port) and record
  in the translation table. Incoming: look up (dst IP, dst port) and
  restore. Advantages: one public IP for all; renumbering/ISP change is
  transparent; inbound connections are blocked (security).
  Drawback: violates the end-to-end principle — a middlebox keeps
  per-flow state; P2P needs NAT traversal."

IP fragmentation (4000B datagram, MTU 1500):
 "Frag1: 1480 data, offset 0, MF=1; Frag2: 1480 data, offset 185, MF=1;
  Frag3: 1020 data, offset 370, MF=0. Data per fragment must be a
  multiple of 8 because offset counts 8-byte units. Reassembly happens
  ONLY at the destination."

IPv4 vs IPv6:
 "IPv6: 128-bit addresses, fixed 40-byte header, no header checksum, no
  fragmentation at routers (PMTUD instead), flow label, hop limit.
  Transition by tunneling: the whole IPv6 datagram is carried as payload
  inside an IPv4 datagram."

Router per-hop steps:
 "Decrement TTL and recompute header checksum → longest-prefix match to
  select next hop → MTU check (fragment or drop + ICMP) → ARP resolve
  next-hop MAC → rebuild frame with new src/dst MAC. IP addresses stay
  unchanged end-to-end; MAC addresses change at every hop."
```

### Trap pairs (English exam wording)
```
block size ≠ usable hosts   (/30: block = 4, usable = 2)
offset units = 8 bytes, NOT bytes
collision happens AT THE RECEIVER (hidden terminal), not "in the middle"
ESS ≠ Internet (Extended Service Set is still one WLAN)
CDMA (code division) ≠ CSMA/CD (carrier sense / collision detection)
SFD = START of frame, not end
tunneling direction: IPv6 wrapped INSIDE IPv4
```
