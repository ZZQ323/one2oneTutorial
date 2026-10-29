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

### 8. Routing (L5)
| English | 中文 | Note |
|---|---|---|
| routing algorithm: link-state vs distance-vector | 链路状态 vs 距离向量 | |
| Dijkstra's algorithm, shortest path | Dijkstra算法，最短路径 | global info |
| Bellman-Ford equation | Bellman-Ford方程 | distributed |
| Distance Vector (DV), routing table | 距离向量，路由表 | |
| count-to-infinity problem | 无穷计数问题 | DV flaw |
| poisoned reverse | 毒性反转 | break loop, 2 rounds |
| OSPF (Open Shortest Path First) | | link-state, area-based |
| BGP (Border Gateway Protocol) | | path-vector, inter-AS |
| eBGP / iBGP | 外部/内部BGP | |
| AS_PATH, NEXT_HOP, LOCAL_PREF | BGP属性 | |
| split-horizon rule (iBGP) | iBGP水平分割 | iBGP learned route NOT advertised to other iBGP peers |
| route aggregation, prefix summarization | 路由聚合 | reduce table size |
| intra-AS routing (IGP) vs inter-AS routing (EGP) | 域内 vs 域间 | OSPF/RIP vs BGP |

### 9. Transport Layer (L6)
| English | 中文 | Note |
|---|---|---|
| multiplexing / demultiplexing | 复用/解复用 | port-based |
| TCP: reliable, in-order, byte-stream | 可靠、有序、字节流 | |
| UDP: unreliable, connectionless, no congestion control | 不可靠、无连接、无拥塞控制 | |
| three-way handshake | 三次握手 | SYN -> SYN+ACK -> ACK |
| ISN (Initial Sequence Number) | 初始序号 | random, anti-spoof |
| sequence number (SN), acknowledgement number (AN) | 序号、确认号 | SN=first byte, AN=next expected |
| cumulative ACK | 累积确认 | ACK N = all bytes < N received |
| receive window (rwnd) | 接收窗口 | flow control |
| congestion window (cwnd) | 拥塞窗口 | congestion control |
| slow start, congestion avoidance, fast retransmit | 慢启动、拥塞避免、快速重传 | |
| ssthresh (slow start threshold) | 慢启动阈值 | cwnd/2 after loss |
| MSS (Maximum Segment Size) | 最大段大小 | |
| RTT, SRTT, RTO | 往返时延、平滑RTT、重传超时 | |
| fast recovery | 快速恢复 | 3 dup ACKs, cwnd=ssthresh |
| TIME_WAIT, 2×MSL | | ensure ACK received |
| FIN, SYN, RST, ACK flags | 标志位 | |
| SYN consumes 1 seq#, FIN consumes 1 seq#, pure ACK consumes 0 | SYN/FIN消耗序号，纯ACK不消耗 | |

### 10. Application Layer (L7)
| English | 中文 | Note |
|---|---|---|
| DHCP: Discover, Offer, Request, Ack | 四步 | UDP 67/68, broadcast |
| DNS: recursive vs iterative query | 递归 vs 迭代 | |
| DNS records: A, AAAA, CNAME, MX | | |
| root DNS server, TLD server, authoritative server, local DNS | 根/TLD/权威/本地 | hierarchy |
| HTTP methods: GET, POST, PUT, HEAD, DELETE | | |
| HTTP status codes: 200 OK, 301 Moved, 404 Not Found, 304 Not Modified | | |
| persistent connection, pipelining | 持久连接、管线化 | HTTP/1.1 |
| multiplexing (HTTP/2), frame interleaving | 多路复用、帧交错 | HTTP/2 |
| head-of-line (HOL) blocking | 队头阻塞 | TCP problem |
| QUIC, 0-RTT, 1-RTT handshake | | HTTP/3, over UDP |
| CDN: enter deep vs bring home | 进入深网 vs 进入浅网 | Akamai vs Limelight |
| DASH (Dynamic Adaptive Streaming over HTTP) | | manifest, adaptive bitrate |
| Web cache, conditional GET, If-Modified-Since | Web缓存、条件GET | 304 Not Modified |
| TLS (Transport Layer Security), HTTPS | | encryption + authentication |

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
