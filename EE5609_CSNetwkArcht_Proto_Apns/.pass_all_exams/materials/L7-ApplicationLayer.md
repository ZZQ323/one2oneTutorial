# L7 - Application Layer

## DHCP（Dynamic Host Configuration Protocol）
- **功能**：自动为主机配置IP地址、默认网关、DNS等
- **运行在UDP上**：服务器端口67，客户端端口68
- **四步过程**：
  1. **DHCP Discover**：客户端广播请求
     - UDP源端口68，目的端口67
     - 源IP: 0.0.0.0，目的IP: 255.255.255.255
     - 包含客户端MAC地址
  2. **DHCP Offer**：服务器响应
     - 单播（用offer的IP作目的）或广播
     - 包含提供的IP、子网掩码、网关、DNS、租约时间
  3. **DHCP Request**：客户端选择一个offer并广播
     - 目的IP: 255.255.255.255（告知其他服务器）
     - 源IP: 0.0.0.0（尚未确认）
     - 包含选中的服务器标识
  4. **DHCP Acknowledge**：服务器确认
     - 单播或广播
     - 客户端开始使用IP
- **租约时间**：IP地址的使用期限
- **续租**：重复Request/Ack过程
- **DHCP Release**：主动释放IP（单播给服务器）
- **DHCP Relay**：跨子网的DHCP，由中继代理转发广播

## DNS（Domain Name System）
- **功能**：将域名转换为IP地址
- **运行在UDP或TCP上**：端口53
- **分布式数据库**：层次化结构
  - 根DNS服务器（13个逻辑根，全球分布）
  - 顶级域（TLD）服务器：.com, .org, .edu, .cn等
  - 权威DNS服务器：组织的DNS服务器
  - 本地DNS服务器：ISP的DNS，缓存查询结果
- **记录类型**：
  - A记录：域名 -> IPv4地址
  - AAAA记录：域名 -> IPv6地址
  - CNAME：别名 -> 规范名（canonical name）
  - MX：邮件交换服务器
- **查询方式**：
  - **递归查询**：客户端->本地DNS->根->TLD->权威（本地DNS承担全部解析负担）
  - **迭代查询**：每一级返回下一级的引用（客户端逐级查询）
- **缓存**：DNS响应可缓存（TTL指定缓存时间），减少查询延迟
- **DNS消息格式**：
  - Header：identification, flags(query/reply, recursion desired/available)
  - Questions：查询的问题
  - Answers：回答的RR
  - Authority：权威服务器的RR
  - Additional：额外信息

## HTTP（HyperText Transfer Protocol）
- **功能**：Web浏览器和服务器之间的通信
- **运行在TCP上**：端口80（HTTP）或443（HTTPS）
- **客户端/服务器模型**：浏览器请求，服务器响应
- **无状态**：服务器不维护客户端状态
- **HTTP请求方法**：
  - GET：请求资源
  - POST：提交表单数据（数据在body）
  - HEAD：只请求头部（用于检查）
  - PUT：上传/替换文件
  - DELETE：删除资源
- **HTTP响应状态码**：
  - 200 OK：请求成功
  - 301 Moved Permanently：资源已移动，新位置在Location头
  - 400 Bad Request：请求格式错误
  - 404 Not Found：资源不存在
  - 505 HTTP Version Not Supported：不支持的HTTP版本

## HTTP 版本演进
- **HTTP/1.0**：每个请求一个TCP连接（短连接）
- **HTTP/1.1**：持久连接（keep-alive），管线化（pipelining）
  - 管线化：连续发送请求，不等响应（解决请求连续发送）
  - 持久连接：连接复用（解决连接建立开销）
- **HTTP/2**：
  - 多路复用：一个TCP连接上并行传输多个请求/响应
  - 优先级：按客户端指定优先级发送（非FCFS）
  - 服务器推送：主动推送未请求的资源
  - 帧化：对象分成帧，交错传输，缓解队头阻塞
- **HTTP/3**：基于QUIC（UDP）
  - 解决TCP队头阻塞
  - 每对象独立的错误和拥塞控制
  - 内置安全（TLS）

## HTTPS and TLS
- **HTTPS**：HTTP over TLS
- **TLS**（Transport Layer Security）：
  - 加密连接
  - 数据完整性
  - 端点认证
- TLS在应用层实现，使用TCP

## QUIC（Quick UDP Internet Connections）
- 应用层协议，基于UDP
- 合并TCP+TLS功能到一个握手
- **连接建立**：
  - TCP+TLS：2次握手（TCP）+ 多次握手（TLS）= 高延迟
  - QUIC 1-RTT：一次握手完成连接建立+安全
  - QUIC 0-RTT：使用缓存的session ticket，首次即可发数据
- 部署：Google服务器、Chrome、YouTube

## CDN（Content Delivery Network）
- **目标**：减少用户获取内容的延迟
- **挑战**：单一大服务器无法扩展（单点故障、拥塞、长路径）
- **策略**：
  - **Enter Deep**（进入深网）：在ISP内部部署大量小集群
    - 优点：靠近用户，低延迟
    - 缺点：维护成本高
    - 代表：Akamai（240,000+服务器，120+国家）
  - **Bring Home**（进入浅网）：在ISP边缘部署少量大集群
    - 优点：维护成本低
    - 缺点：离用户较远
    - 代表：Limelight
- **路由决策**：地理就近、实时负载、网络拥塞

## Netflix CDN案例
- OpenConnect CDN节点存储内容副本
- 订阅者请求内容，ISP返回manifest文件
- 客户端根据manifest选择最高支持码率的块
- 网络拥塞时可切换码率或服务器

## DASH（Dynamic Adaptive Streaming over HTTP）
- **流媒体 over HTTP**
- **服务器**：
  - 将视频分成多个chunk
  - 每个chunk用多种码率编码
  - 不同码率存储在不同文件
  - 文件复制到CDN节点
- **Manifest文件**：提供不同chunk的URL
- **客户端**：
  - 周期性估计带宽
  - 根据manifest一次请求一个chunk
  - 选择当前带宽支持的最高码率
  - 可动态切换码率和服务器
- **智能在客户端**：决定何时请求、请求什么码率、从哪里请求

## Web缓存（代理服务器）
- **功能**：缓存频繁请求的对象
- **工作原理**：
  - 浏览器配置指向本地缓存
  - 所有HTTP请求先发给缓存
  - 缓存命中：直接返回对象
  - 缓存未命中：向源服务器请求，缓存后返回
- **优势**：
  - 减少响应时间（缓存离用户更近）
  - 减少机构接入链路的流量
  - 让"穷"内容提供商也能有效分发内容
- **条件GET**：
  - 客户端发送 If-Modified-Since: <date>
  - 服务器检查对象是否在该日期后修改
  - 未修改：返回 304 Not Modified（无对象）
  - 已修改：返回 200 OK + 新对象

## ADSL综合题（ISP宽带场景）
- **ADSL Modem角色**：
  - DHCP服务器：配置主机IP、子网掩码等
  - DNS服务器：域名解析
  - 默认网关：转发到外部网络
  - NAT：私有IP <-> 公网IP转换
- **访问网页的帧序列**：
  1. ARP请求网关MAC（广播）
  2. ARP回复（单播）
  3. DNS请求（目的IP=网关，UDP）
  4. DNS回复（目的IP=主机，UDP）
  5-7. TCP三次握手（目的IP=服务器，经过NAT转换）
  8. HTTP请求
  9. HTTP回复

## 五层模型总结
| 层 | 功能 | 例子 |
|---|---|---|
| Application | 定义应用消息 | DHCP, DNS, HTTP |
| Transport | 进程间交付 | TCP, UDP |
| Network | 跨网络移动包 | IP, 路由 |
| Data Link | 一跳内移动帧 | Ethernet, WiFi, MAC |
| Physical | 发送比特信号 | 电、光、无线电 |
