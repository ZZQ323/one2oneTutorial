# L7 - Application Layer

## DHCP（Dynamic Host Configuration Protocol）
- **功能**：自动为主机配置IP地址、默认网关、DNS等
- **运行在UDP上**：服务器端口67，客户端端口68
- **四步过程**：
  1. **DHCP Discover**：客户端广播请求（源IP 0.0.0.0，目的IP 255.255.255.255）
  2. **DHCP Offer**：服务器响应（单播或广播）
  3. **DHCP Request**：客户端选择一个offer并广播（告知其他服务器）
  4. **DHCP Acknowledge**：服务器确认（客户端开始使用IP）
- **租约时间**：IP地址的使用期限
- **DHCP Release**：主动释放IP

## DNS（Domain Name System）
- **功能**：将域名转换为IP地址
- **分布式数据库**：层次化结构
  - 根DNS服务器
  - 顶级域（TLD）服务器
  - 权威DNS服务器
- **记录类型**：
  - A记录：域名->IPv4地址
  - AAAA记录：域名->IPv6地址
  - CNAME：别名->规范名
  - MX：邮件服务器
- **查询方式**：
  - 递归查询：客户端->本地DNS->根->TLD->权威
  - 迭代查询：每一级返回下一级的引用
- **缓存**：DNS响应可缓存，减少查询延迟

## HTTP（HyperText Transfer Protocol）
- **功能**：Web浏览器和服务器之间的通信
- **运行在TCP上**：端口80（HTTP）或443（HTTPS）
- **无状态**：服务器不维护客户端状态
- **请求方法**：GET、POST、PUT、DELETE
- **响应状态码**：200 OK、301 Moved、404 Not Found、500 Server Error

## HTTP 版本演进
- **HTTP/1.0**：每个请求一个TCP连接（短连接）
- **HTTP/1.1**：持久连接（keep-alive），管线化
- **HTTP/2**：多路复用、头部压缩、服务器推送
- **HTTP/3**：基于QUIC（UDP），解决队头阻塞

## CDN（Content Delivery Network）
- **目标**：减少用户获取内容的延迟
- **策略**：
  - 进入深网：在ISP内部部署缓存服务器
  - 进入浅网：在ISP边缘部署
- **路由决策**：地理就近、实时负载、网络拥塞

## Web缓存（代理服务器）
- **功能**：缓存频繁请求的对象
- **优势**：减少响应时间、减少网络流量
- **条件GET**：客户端发送If-Modified-Since，服务器返回304 Not Modified或新内容
