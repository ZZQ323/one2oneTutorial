# L6 - Transport Layer: TCP and UDP

## 传输层服务
- 提供应用进程之间的逻辑通信
- 发送方：将应用消息分成段，传给网络层
- 接收方：重组段成消息，传给应用层
- **复用/解复用**：根据端口号将段交付到正确的socket

## UDP（User Datagram Protocol）
- **无连接**：无需握手
- **不可靠**：段可能丢失或乱序
- **无拥塞控制**：可以尽可能快地发送
- **优点**：
  - 无连接建立延迟
  - 无连接状态
  - 头部小
  - 可在拥塞下工作
- **应用**：DNS、流媒体、在线游戏

## TCP（Transmission Control Protocol）
- **面向连接**：需要三次握手建立连接
- **可靠传输**：有序、无差错、无丢失
- **流控**：保持发送速率在接收方容量内
- **拥塞控制**：调整网络负载
- **累积ACK**：确认已收到的字节

## TCP 段结构
- **Sequence Number (SN)**：段的第一个字节的序号
- **Acknowledgement Number (AN)**：期望收到的下一个字节序号（累积确认）
- **rwnd**：接收窗口大小（流控）
- **cwnd**：拥塞窗口（拥塞控制）
- 标志位：SYN、FIN、RST、ACK

## TCP 连接管理
### 三次握手（建立连接）
1. Client -> Server: SYN (SN=x)
2. Server -> Client: SYN+ACK (SN=y, AN=x+1)
3. Client -> Server: ACK (AN=y+1)

### 四次挥手（关闭连接）
1. 一方发送 FIN
2. 另一方 ACK
3. 另一方发送 FIN
4. 发起方 ACK

## TCP 流控
- 接收方在TCP头部的rwnd字段通告空闲缓冲区大小
- 发送方限制未确认的数据量 <= rwnd
- 防止发送方淹没接收方

## TCP 拥塞控制
- 发送方限制：LastByteSent - LastByteAcked <= min(cwnd, rwnd)
- **慢启动**：连接开始时，cwnd从1 MSS开始，每收到一个ACK翻倍
- **拥塞避免**：cwnd达到阈值后，每个RTT增加1 MSS
- **快速重传**：收到3个重复ACK时立即重传

## TCP 序号空间
- SYN消耗一个序号
- FIN消耗一个序号
- 纯ACK不消耗序号
