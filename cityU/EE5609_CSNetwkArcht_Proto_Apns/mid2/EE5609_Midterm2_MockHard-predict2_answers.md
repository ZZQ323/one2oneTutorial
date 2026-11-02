# EE5609 Midterm 2 — Self-Test Answers

## Question 1 (16 marks) — Warm-Up: ARP, DHCP, DNS

### (a) ARP Basics (6 marks)

**(i)** Host A broadcasts an **ARP request** asking "Who has 192.168.1.20?" The destination MAC address is **FF-FF-FF-FF-FF-FF** (broadcast). *(2 marks)*

**(ii)** Host B replies with an **ARP reply** containing its MAC address (BB-BB-BB-BB-BB-BB). The reply is **unicast** (destination MAC = AA-AA-AA-AA-AA-AA) because Host A's MAC address was included in the broadcast request, so Host B knows where to send the reply directly. *(2 marks)*

**(iii)** After ARP completes, Host A sends the 500-byte IP datagram in an Ethernet frame with:
- Source MAC: **AA-AA-AA-AA-AA-AA** (Host A)
- Destination MAC: **BB-BB-BB-BB-BB-BB** (Host B)

*(2 marks)*

### (b) DHCP Overview (4 marks)

**(i)** The four DHCP messages in order are:
1. **DHCP Discover**
2. **DHCP Offer**
3. **DHCP Request**
4. **DHCP ACK**

*(2 marks)*

**(ii)** For DHCP Discover:
- Ethernet destination MAC: **FF-FF-FF-FF-FF-FF** (broadcast)
- Source IP: **0.0.0.0** (host has no IP yet)
- Destination IP: **255.255.255.255** (broadcast)

*(2 marks)*

### (c) DNS Query Types (6 marks)

**(i)** This is an **iterative query**. The root server does not perform the full resolution on behalf of the client; instead, it returns a **referral** (the address of the .hk TLD server) and tells the client to query that server next. In iterative queries, each server provides the best information it has without taking responsibility for the full lookup. *(3 marks)*

**(ii)** 
- Domain name to IPv6 address: **AAAA record**
- Domain name to another domain name (alias): **CNAME record**

*(3 marks)*

---

## Question 2 (22 marks) — Routing: Dijkstra, DV, OSPF vs BGP

### (a) Dijkstra's Algorithm (14 marks)

**(i)** Dijkstra iteration table (source = S):

| Step | N' | D(A), p(A) | D(B), p(B) | D(C), p(C) | D(D), p(D) | D(E), p(E) |
|------|-----|-----------|-----------|-----------|-----------|-----------|
| 0 | {S} | 3, S | ∞ | 1, S | ∞ | ∞ |
| 1 | {S,C} | 3, S | ∞ | — | 3, C | ∞ |
| 2 | {S,C,A} | — | 5, A | — | 3, C | ∞ |
| 3 | {S,C,A,D} | — | 5, A | — | — | 6, D |
| 4 | {S,C,A,D,B} | — | — | — | — | 6, D |
| 5 | {S,C,A,D,B,E} | — | — | — | — | — |

*(8 marks)*

**(ii)** Least-cost paths from S:

| Destination | Cost | Path |
|-------------|------|------|
| A | 3 | S → A |
| B | 5 | S → A → B |
| C | 1 | S → C |
| D | 3 | S → C → D |
| E | 6 | S → C → D → E |

*(4 marks)*

**(iii)** S's forwarding table (next hop from S):

| Destination | Next Hop |
|-------------|----------|
| A | A |
| B | A |
| C | C |
| D | C |
| E | C |

*(2 marks)*

### (b) Count-to-Infinity (4 marks)

When c(x,y) changes from 5 to 50:
- y learns the new cost and updates Dy(x) = 2 + 100 = 102 (via z, since direct cost is now 50).
- z receives y's update and computes Dz(x) = 2 + 102 = 104 (via y).
- y then receives z's update and recomputes Dy(x) = 2 + 104 = 106 (via z).
- This mutual dependency causes costs to increment indefinitely → **count-to-infinity**.

**Bad news travels slow** in distance-vector routing. *(4 marks)*

### (c) OSPF vs BGP (4 marks)

| Feature | OSPF | BGP |
|---------|------|-----|
| Scope | **Intra-AS** (within one autonomous system) | **Inter-AS** (between autonomous systems) |
| Algorithm | **Link-state** (Dijkstra) | **Path-vector** |
| AS-PATH purpose | N/A | (1) **Prevent routing loops** (reject if own AS appears in path); (2) **Policy-based routing** (select path based on AS sequence, not just shortest) |

*(4 marks)*

---

## Question 3 (18 marks) — IP Fragmentation + Pipeline Delay

### (a) IP Fragmentation (10 marks)

**(i)** Original datagram: 5200 bytes total = 20 bytes header + **5180 bytes data**

MTU = 1500 bytes → max data per fragment = 1500 − 20 = **1480 bytes**

Number of fragments = ⌈5180 / 1480⌉ = ⌈3.5⌉ = **4 fragments** *(2 marks)*

**(ii)** Fragment table:

| Fragment | Total Length | Data Length | MF | Offset |
|----------|--------------|-------------|-----|--------|
| 1 | 1500 | 1480 | 1 | 0 |
| 2 | 1500 | 1480 | 1 | 185 (1480/8) |
| 3 | 1500 | 1480 | 1 | 370 (2960/8) |
| 4 | 740 | 720 | 0 | 555 (4440/8) |

**Calculation:**
- Fragments 1–3: 1480 bytes data each, offset increases by 1480/8 = 185
- Fragment 4: 5180 − 3×1480 = 5180 − 4440 = **740 bytes total** (720 data + 20 header)
- Offset of fragment 4: 4440 / 8 = **555**

*(6 marks)*

**(iii)** If MTU = 2000 bytes:
- Max data per fragment = 2000 − 20 = **1980 bytes**
- Number of fragments = ⌈5180 / 1980⌉ = ⌈2.62⌉ = **3 fragments**
- Offsets: 0, 247 (1980/8), 495 (3960/8)

*(2 marks)*

### (b) Pipeline Delay (8 marks)

**(i)** Packet size:
- Payload per packet: 6000 / 5 = **1200 bytes**
- Header per packet: **40 bytes**
- Total packet size: 1200 + 40 = **1240 bytes**

Transmission time:
```
T_trans = 1240 × 8 / (3 × 10⁶) = 9920 / 3,000,000 = 3.307 ms ≈ 3.31 ms
```

*(2 marks)*

**(ii)** First packet at D:
- 3 hops, each with T_trans + T_prop
- T_first = 3 × (T_trans + T_prop) = 3 × (3.307 + 0.5) = 3 × 3.807 = **11.42 ms**

*(3 marks)*

**(iii)** Last bit of last packet at D (pipeline effect):
```
T_all = T_first + (N − 1) × T_trans
      = 11.42 + (5 − 1) × 3.307
      = 11.42 + 4 × 3.307
      = 11.42 + 13.228
      = 24.648 ms ≈ 24.65 ms
```

*(3 marks)*

---

## Question 4 (22 marks) — TCP Comprehensive

### (a) Three-Way Handshake (6 marks)

| Direction | Flags | SN | AN |
|-----------|-------|----|----|
| Client → Server | SYN | 800 | — |
| Server → Client | SYN + ACK | 2000 | 801 |
| Client → Server | ACK | 801 | 2001 |

**Explanation:**
- Client SYN: SN = ISN = 800, no AN (first message)
- Server SYN+ACK: SN = ISN = 2000, AN = 801 (acknowledges Client's SYN: 800 + 1)
- Client ACK: SN = 801 (SYN consumed 1 sequence number), AN = 2001 (acknowledges Server's SYN: 2000 + 1)

*(6 marks)*

### (b) Client's 200-Byte Write (4 marks)

**(i)** Segment carrying Client's 200-byte data:
- SN = **801** (after handshake, data starts at ISN + 1)
- Payload length = **200 bytes**
- AN = **2001** (acknowledging Server's SYN)

*(2 marks)*

**(ii)** Server's pure ACK:
- AN = **1001** (801 + 200 = cumulative acknowledgment of all data received)

*(2 marks)*

### (c) Server's 5000-Byte Transfer Under Slow Start (8 marks)

**(i)** While cwnd = 1 MSS = 1024 bytes:
- Server may send **1024 bytes** before waiting for an ACK.

*(1 mark)*

**(ii)** First data segment:
- SN = **2001** (Server's ISN + 1)
- Payload length = **1024 bytes**

*(2 marks)*

**(iii)** After first ACK received:
- cwnd = 2 MSS = **2048 bytes** (doubles each RTT in slow start)
- max unACKed = min(cwnd, rwnd) = min(2048, 4096) = **2048 bytes**

*(3 marks)*

**(iv)** Total segments for 5000 bytes:
```
5000 / 1024 = 4.88 → 5 segments
(4 × 1024 + 1 × 904)
```

*(2 marks)*

### (d) FIN (4 marks)

**(i)** Yes, a FIN **consumes 1 sequence number**. *(1 mark)*

**(ii)** After all data acknowledged:
- Client has sent: 200 bytes of data → next SN = 801 + 200 = **1001**
- Client's FIN: SN = **1001**
- Server's ACK of FIN: AN = **1002** (FIN consumes 1 sequence number: 1001 + 1)

*(3 marks)*

---

## Question 5 (22 marks) — Comprehensive: ADSL Home Network

### (a) Frame Sequence (12 marks)

| Frame | Src MAC | Dst MAC | Src IP | Dst IP | Purpose |
|-------|---------|---------|--------|--------|---------|
| 1 | 00-11-22-AA-AA-AA | FF-FF-FF-FF-FF-FF | 10.0.0.5 | 10.0.0.1 | ARP Request (who has gateway?) |
| 2 | 00-11-22-BB-BB-BB | 00-11-22-AA-AA-AA | 10.0.0.1 | 10.0.0.5 | ARP Reply (gateway's MAC) |
| 3 | 00-11-22-AA-AA-AA | 00-11-22-BB-BB-BB | 10.0.0.5 | 10.0.0.1 | DNS Query (www.university.edu → ?) |
| 4 | 00-11-22-BB-BB-BB | 00-11-22-AA-AA-AA | 10.0.0.1 | 10.0.0.5 | DNS Reply (140.112.33.50) |
| 5 | 00-11-22-AA-AA-AA | 00-11-22-BB-BB-BB | 10.0.0.5 | 140.112.33.50 | TCP SYN (connection setup) |
| 6 | 00-11-22-BB-BB-BB | 00-11-22-AA-AA-AA | 140.112.33.50 | 10.0.0.5 | TCP SYN+ACK |
| 7 | 00-11-22-AA-AA-AA | 00-11-22-BB-BB-BB | 10.0.0.5 | 140.112.33.50 | TCP ACK |
| 8 | 00-11-22-AA-AA-AA | 00-11-22-BB-BB-BB | 10.0.0.5 | 140.112.33.50 | HTTP GET request |
| 9 | 00-11-22-BB-BB-BB | 00-11-22-AA-AA-AA | 140.112.33.50 | 10.0.0.5 | **HTTP Response** ← first response |

**Key observations:**
- IP addresses remain unchanged end-to-end (Src IP = 10.0.0.5, Dst IP = 140.112.33.50)
- MAC addresses change at each hop: H always sends to gateway's MAC (00-11-22-BB-BB-BB)
- NAT is performed by R but not visible in H's frames (R translates 10.0.0.5 → 140.113.1.100 when forwarding to Internet)

*(12 marks)*

### (b) Why ARP for Gateway? (4 marks)

ARP operates at the **link layer** and can only resolve MAC addresses for devices on the **same subnet**. Since 140.112.33.50 is on a remote network (not in 10.0.0.0/24), H must forward packets to its default gateway (10.0.0.1). Therefore, H needs the gateway's MAC address, not the remote server's MAC address. The gateway will handle further routing and NAT translation. *(4 marks)*

### (c) Router's Role (4 marks)

The home router R performs four roles beyond simple IP forwarding:

1. **DHCP server**: Automatically configures hosts on the LAN with IP addresses, subnet masks, default gateway, and DNS server addresses.

2. **DNS proxy/forwarder**: Receives DNS queries from LAN hosts and forwards them to upstream DNS servers (or caches responses).

3. **Default gateway**: Routes packets between the LAN and the Internet; performs routing table lookups to determine next hops.

4. **NAT (Network Address Translation)**: Translates private IP addresses (10.0.0.x) to a public IP address (140.113.1.100) for Internet communication; maintains translation table mapping (private IP, port) ↔ (public IP, port).

*(4 marks)*

### (d) HTTP Versions (2 marks)

**Non-persistent HTTP/1.0**: Each object requires a separate TCP connection. For 1 HTML page + 3 images = **4 TCP connections** (4 handshakes).

**Persistent HTTP/1.1**: All objects share a single TCP connection. Only **1 TCP connection** (1 handshake) is needed.

**Which requires fewer connections?** Persistent HTTP/1.1 (1 vs 4). *(2 marks)*

---

## Key Formulas & Rules Summary

### ARP
- Broadcast request: dst MAC = FF-FF-FF-FF-FF-FF
- Unicast reply: dst MAC = requester's MAC
- Resolves IP → MAC for devices on the **same subnet**
- For remote destinations, ARP resolves the **gateway's MAC**

### DHCP (DORA)
1. **Discover**: broadcast (dst MAC = FF×6, 0.0.0.0 → 255.255.255.255, UDP 68 → 67)
2. **Offer**: server proposes IP
3. **Request**: client accepts offer (broadcast)
4. **ACK**: server confirms

### DNS
- Iterative query: server returns referral, client queries next server
- Recursive query: server performs full lookup on behalf of client
- Record types: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail)

### IP Fragmentation
- Max data per fragment = MTU − 20 (IP header)
- Offset = byte position in original payload / 8
- MF = 1 for all except last fragment
- Reassembly happens **only at destination**

### Pipeline Delay
```
T_first = hops × (T_trans + T_prop)
T_all = T_first + (packets − 1) × T_trans
```

### TCP Sequence Numbers
- SYN consumes 1 SN
- FIN consumes 1 SN
- Pure ACK consumes 0 SN
- AN = cumulative acknowledgment (next expected byte)
- Slow start: cwnd doubles each RTT until loss

### Home Router Roles
1. DHCP server
2. DNS proxy
3. Default gateway
4. NAT
