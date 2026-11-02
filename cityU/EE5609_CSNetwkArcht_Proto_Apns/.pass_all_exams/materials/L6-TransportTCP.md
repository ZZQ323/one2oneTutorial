# L6 - Transport Layer: TCP and UDP

## 传输层服务
- 提供应用进程之间的逻辑通信
- 发送方：将应用消息分成段（segment），传给网络层
- 接收方：重组段成消息，传给应用层
- **复用/解复用**：根据端口号将段交付到正确的socket
  - 复用：发送方给段加上源/目的端口
  - 解复用：接收方根据端口交付到对应进程
- **端口**：单个传输层支持多个应用进程

## UDP（User Datagram Protocol）
- **无连接**：无需握手
- **不可靠**：段可能丢失或乱序
- **无拥塞控制**：可以尽可能快地发送
- **优点**：
  - 无连接建立延迟（适合实时应用）
  - 无连接状态
  - 头部小（8字节）
  - 可在拥塞下工作（不会被限速）
- **UDP头部**：源端口(16) | 目的端口(16) | 长度(16) | 校验和(16)
- **应用**：DNS、流媒体、SNMP、HTTP/3、在线游戏
- **可靠传输 over UDP**：应用层实现（如QUIC）

## TCP（Transmission Control Protocol）
- **面向连接**：需要三次握手建立连接
- **可靠传输**：有序、无差错、无丢失
- **点对点**：一个发送方，一个接收方
- **全双工**：双向数据流
- **字节流**：无消息边界（MSS限制段大小）
- **累积ACK**：确认已收到的字节
- **流水线**：允许同时有多个未确认段
- **四大功能**：
  - Connection management：建立、使用、关闭连接
  - Flow control：保持在接收方容量内
  - Error control：检测丢失数据并恢复
  - Congestion control：调整发送到网络的负载

## TCP 段结构
- **Sequence Number (SN)**：段的第一个字节的序号
  - 每个连接从ISN开始
  - 字节流位置从ISN+1开始标记
  - SN指示段中第一个字节的位置
- **Acknowledgement Number (AN)**：期望收到的下一个字节序号（累积确认）
  - 暗示AN-1之前的所有字节都已正确接收
- **rwnd**：接收窗口大小（流控）
  - 从AN开始，接收方准备接受的字节数
- **cwnd**：拥塞窗口（拥塞控制）
- **标志位**：
  - SYN：连接建立
  - FIN：连接关闭
  - RST：重置连接
  - ACK：确认有效
  - PSH：推送数据
  - URG：紧急数据
  - C/E：拥塞通知
- **Header Length**：TCP头长度（单位4字节，无options=5）
- **Checksum**：覆盖头+数据+伪首部
- **Options**：可变长，如MSS协商、时间戳、窗口缩放

## TCP 连接管理
### 三次握手（建立连接）
1. Client -> Server: SYN (SN=x)
2. Server -> Client: SYN+ACK (SN=y, AN=x+1)
3. Client -> Server: ACK (AN=y+1)
- **为什么三次**：防止half-open连接（旧的SYN延迟到达导致服务器误以为新连接）
- **ISN选择**：随机生成，防止旧连接的段被新连接接收
- **状态机**：
  - Client: CLOSED → SYN_SENT → ESTABLISHED
  - Server: LISTEN → SYN_RCVD → ESTABLISHED

### 四次挥手（关闭连接）
1. 一方发送 FIN（SN=x）
2. 另一方 ACK（AN=x+1）
3. 另一方发送 FIN（SN=y）
4. 发起方 ACK（AN=y+1）
- **状态机**：
  - 主动关闭方：ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED
  - 被动关闭方：ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED
- **TIME_WAIT**：等待2×MSL（Maximum Segment Lifetime），确保对方收到ACK，让旧段消失
- **可合并**：FIN+ACK可合并为一个消息

## TCP 流控
- 接收方在TCP头部的rwnd字段通告空闲缓冲区大小
- rwnd = 缓冲区总大小 - 已占用
- 发送方限制：LastByteSent - LastByteAcked <= rwnd
- 防止发送方淹没接收方
- **rwnd上限**：≤ 接收缓冲区总大小，不是累加值
- RcvBuffer默认4096字节，可通过socket选项设置

## TCP 错误控制
- **为什么**：即使IP不可靠，也保证可靠服务
- **错误类型**：
  - 乱序：基于SN检测，重排并ACK
  - 重复：基于SN检测，丢弃并ACK
  - 损坏：基于checksum检测，丢弃等待超时重传
  - 丢失：等待超时重传
- **超时重传**：
  - RTT：发送数据到收到ACK的时间
  - SRTT：平滑RTT（指数加权移动平均）
  - RTO（Retransmission Timeout）：基于SRTT计算，通常 RTO = SRTT + 4×RTTVAR
  - RTO太短：不必要重传
  - RTO太长：丢失恢复慢
- **快速重传**：收到3个重复ACK时立即重传，不等超时

## TCP 拥塞控制
- 发送方限制：LastByteSent - LastByteAcked <= min(cwnd, rwnd)
- **慢启动**：
  - 连接开始时，cwnd = 1 MSS
  - 每收到一个ACK，cwnd += 1（指数增长：每RTT翻倍）
  - 直到cwnd >= ssthresh 或丢包
- **拥塞避免**：
  - cwnd >= ssthresh后进入
  - 每个RTT增加1 MSS（线性增长）
  - 直到丢包
- **快速重传**：收到3个重复ACK时立即重传
- **丢包后**：
  - ssthresh = cwnd / 2
  - cwnd = 1 MSS（重新慢启动）或 cwnd = ssthresh（快速恢复，仅3个重复ACK时）

## TCP 序号空间
- SYN消耗一个序号
- FIN消耗一个序号
- 纯ACK不消耗序号
- SYN+ACK消耗一个序号

## MSS（Maximum Segment Size）
- TCP段数据部分的最大长度
- 通常在三次握手时协商
- 典型值：536字节（IPv4）或1460字节（以太网）

## 综合练习题
- 给定ISN、MSS、rwnd，计算TCP交互的段数、SN/AN
- 分析拥塞控制图中cwnd变化
- **示例**：ISN_client=100, ISN_server=600, rwnd=2048, MSS=536, 初始cwnd=1 MSS
  - 三次握手：SYN(SN=100) → SYN+ACK(SN=600,AN=101) → ACK(AN=601)
  - 数据传输：考虑cwnd限制和MSS分片
  - 连接关闭：FIN序列
