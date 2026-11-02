# EE5609 Midterm 2 — Mock Paper Answers

## Question 1 (20 marks) — VLSM + Longest Prefix Match

### (a) Subnet Allocation (12 marks)

**Given:** 198.51.100.0/22 → 1024 addresses (198.51.100.0 – 198.51.103.255)

**Allocate largest first:**

| LAN | Need | Prefix | Network | Mask | Usable Range | Broadcast |
|-----|------|--------|---------|------|--------------|-----------|
| Engineering | 500 | /23 (510 hosts) | 198.51.100.0/23 | 255.255.254.0 | .100.1 – .101.254 | .101.255 |
| Science | 200 | /24 (254 hosts) | 198.51.102.0/24 | 255.255.255.0 | .102.1 – .102.254 | .102.255 |
| Arts | 80 | /25 (126 hosts) | 198.51.103.0/25 | 255.255.255.128 | .103.1 – .103.126 | .103.127 |

**Calculation:**
- Engineering: need 500 → 2^9 − 2 = 510 → /23 (9 host bits)
- Science: need 200 → 2^8 − 2 = 254 → /24 (8 host bits)
- Arts: need 80 → 2^7 − 2 = 126 → /25 (7 host bits)

### (b) Remaining Block (3 marks)

**Remaining:** 198.51.103.128/25 (addresses .103.128 – .103.255)

**Maximum usable:** 2^7 − 2 = **126 hosts**

### (c) Longest Prefix Match (5 marks)

**Rule:** Select the routing entry with the **longest matching prefix**.

| Destination | Matching Prefix | Prefix Length | Interface |
|-------------|----------------|---------------|-----------|
| 198.51.103.200 | 198.51.103.128/26 | /26 (longest) | **3** |
| 198.51.103.50 | 198.51.103.0/25 | /25 | **2** |
| 198.51.102.10 | 198.51.102.0/24 | /24 | **1** |
| 198.51.100.10 | 198.51.100.0/22 | /22 | **0** |
| 198.51.104.1 | 0.0.0.0/0 | /0 (default) | **4** |

---

## Question 2 (18 marks) — Pipeline Delay

### (a) Packet Switching (9 marks)

**Given:** 4800-byte message → 4 packets, 40-byte header each, 4 Mbps links, 1.0 ms propagation per hop, 3 hops (S→R1→R2→D)

**Packet size:** 4800/4 + 40 = **1240 bytes**

**Transmission time per packet:**
```
T_trans = 1240 × 8 / (4 × 10⁶) = 2.48 ms
```

**First packet at D:**
```
T_first = 3 × (T_trans + T_prop) = 3 × (2.48 + 1.0) = 10.44 ms
```

**All packets at D (pipeline effect):**
```
T_all = T_first + (N − 1) × T_trans = 10.44 + 3 × 2.48 = 17.88 ms
```

> **Pipeline formula:** Total delay = (hops + packets − 1) × T_trans + hops × T_prop

### (b) Circuit Switching (9 marks)

**Given:** Setup time = 12 ms, no packet headers, no store-and-forward

**Propagation delay (total):**
```
T_prop_total = 3 × 1.0 = 3.0 ms
```

**Transmission delay:**
```
T_trans = 4800 × 8 / (4 × 10⁶) = 9.6 ms
```

**Total completion time:**
```
T_circuit = 12 + 9.6 + 3.0 = 24.6 ms
```

**Comparison:** Circuit (24.6 ms) is **slower** than packet switching (17.88 ms) by 6.72 ms.

**Setup-time threshold:**
```
Packet faster when: s + 9.6 + 3.0 > 17.88
→ s > 5.28 ms
```

---

## Question 3 (22 marks) — Routing Algorithms

### (a) Dijkstra's Algorithm (14 marks)

**Iteration table (source = A):**

| Step | N' | D(B), p(B) | D(C), p(C) | D(D), p(D) | D(E), p(E) |
|------|-----|-----------|-----------|-----------|-----------|
| 0 | {A} | 2, A | 5, A | 1, A | ∞ |
| 1 | {A,D} | 2, A | 3, D | — | 7, D |
| 2 | {A,D,B} | — | 3, D | — | 6, B |
| 3 | {A,D,B,C} | — | — | — | 4, C |
| 4 | {A,D,B,C,E} | — | — | — | — |

**Least-cost paths:**

| Destination | Cost | Path |
|-------------|------|------|
| B | 2 | A → B |
| C | 3 | A → D → C |
| D | 1 | A → D |
| E | 4 | A → D → C → E |

**Forwarding table (next hop from A):**

| Destination | Next Hop |
|-------------|----------|
| B | B |
| C | D |
| D | D |
| E | D |

### (b) Count-to-Infinity (4 marks)

When c(x,y) changes from 4 to 60:
- y learns the new cost and updates Dy(x) = 1 + 50 = 51 (via z).
- z receives y's update and computes Dz(x) = 1 + 51 = 52 (via y).
- y then receives z's update and recomputes Dy(x) = 1 + 52 = 53 (via z).
- This mutual dependency causes costs to increment indefinitely → **count-to-infinity**.

> **Bad news travels slow** in distance-vector routing.

### (c) OSPF vs BGP (4 marks)

| Feature | OSPF | BGP |
|---------|------|-----|
| Scope | Intra-AS (within one AS) | Inter-AS (between ASes) |
| Algorithm | Link-state (Dijkstra) | Path-vector |
| AS-PATH purpose | N/A | (1) Prevent routing loops (reject if own AS in path); (2) Policy-based routing (select path by AS sequence) |

---

## Question 4 (22 marks) — TCP Comprehensive

### (a) Three-Way Handshake (6 marks)

| Direction | Flags | SN | AN |
|-----------|-------|----|----|
| Client → Server | SYN | 250 | — |
| Server → Client | SYN + ACK | 900 | 251 |
| Client → Server | ACK | 251 | 901 |

> **Rule:** SYN consumes 1 sequence number; ACK in handshake does not consume SN but sets AN = received SN + 1.

### (b) Client's 50-Byte Write (4 marks)

**Client sends 50 bytes:**
- SN = **251** (ISN + 1 for SYN)
- Payload = **50 bytes**
- AN = **901** (acknowledging Server's SYN)

**Server's ACK:**
- AN = **301** (251 + 50 = cumulative acknowledgment)

### (c) Slow Start (8 marks)

**(i)** cwnd = 1 MSS = 512 → Server may send **512 bytes** before waiting for ACK.

**(ii)** First data segment:
- SN = **901** (Server's ISN + 1)
- Payload = **512 bytes**

**(iii)** After ACK received:
- cwnd = 2 MSS = **1024 bytes** (doubles each RTT in slow start)
- max unACKed = min(cwnd, rwnd) = min(1024, 2048) = **1024 bytes**

**(iv)** Total segments for 2500 bytes:
```
2500 / 512 = 4.88 → 5 segments
(4 × 512 + 1 × 452)
```

### (d) FIN (4 marks)

**Does FIN consume a sequence number?** Yes.

**Client's FIN:**
- SN = **301** (251 + 50 = data sent)

**Server's ACK of FIN:**
- AN = **302** (301 + 1 = FIN consumes 1 SN)

---

## Question 5 (18 marks) — ARP/DNS/HTTP Frame Sequence

### (a) Frame Exchange (10 marks)

**Given:** H (192.168.1.68, MAC: 00-23-26-AA-AA-AA), Gateway R (192.168.1.254, MAC: 00-24-17-BB-BB-BB), DNS server = 192.168.1.254, target = 93.184.216.34

| Frame | Src MAC | Dst MAC | Src IP | Dst IP | Purpose |
|-------|---------|---------|--------|--------|---------|
| 1 | 00-23-26-AA-AA-AA | FF-FF-FF-FF-FF-FF | 192.168.1.68 | 192.168.1.254 | ARP Request (who has gateway?) |
| 2 | 00-24-17-BB-BB-BB | 00-23-26-AA-AA-AA | 192.168.1.254 | 192.168.1.68 | ARP Reply (gateway's MAC) |
| 3 | 00-23-26-AA-AA-AA | 00-24-17-BB-BB-BB | 192.168.1.68 | 192.168.1.254 | DNS Query (www.example.edu → ?) |
| 4 | 00-24-17-BB-BB-BB | 00-23-26-AA-AA-AA | 192.168.1.254 | 192.168.1.68 | DNS Reply (93.184.216.34) |
| 5 | 00-23-26-AA-AA-AA | 00-24-17-BB-BB-BB | 192.168.1.68 | 93.184.216.34 | TCP SYN (connection setup) |
| 6 | 00-24-17-BB-BB-BB | 00-23-26-AA-AA-AA | 93.184.216.34 | 192.168.1.68 | TCP SYN+ACK |
| 7 | 00-23-26-AA-AA-AA | 00-24-17-BB-BB-BB | 192.168.1.68 | 93.184.216.34 | TCP ACK |
| 8 | 00-23-26-AA-AA-AA | 00-24-17-BB-BB-BB | 192.168.1.68 | 93.184.216.34 | HTTP GET request |
| 9 | 00-24-17-BB-BB-BB | 00-23-26-AA-AA-AA | 93.184.216.34 | 192.168.1.68 | **HTTP Response** ← first response |

> **Key observation:** IP addresses remain unchanged end-to-end; MAC addresses change at each hop. H always sends frames to gateway's MAC (00-24-17-BB-BB-BB) because the destination is on a remote network.

### (b) Why ARP for Gateway, Not Server? (4 marks)

ARP operates at the **link layer** and can only resolve MAC addresses for devices on the **same subnet**. Since 93.184.216.34 is on a remote network, H must forward packets to its default gateway (192.168.1.254). Therefore, H needs the gateway's MAC address, not the remote server's MAC address. The gateway will handle further routing.

### (c) HTTP/1.0 vs HTTP/1.1 (4 marks)

**Non-persistent HTTP/1.0:** Each object requires a separate TCP connection. For 1 HTML + 2 images = **3 TCP handshakes**.

**Persistent HTTP/1.1:** All objects share a single TCP connection. Only **1 TCP handshake** is needed.

**Which requires fewer handshakes?** Persistent HTTP/1.1 (1 vs 3).

---

## Key Formulas & Rules

### VLSM
- Usable hosts = 2^h − 2 (where h = host bits)
- Allocate largest subnet first to minimize fragmentation

### Pipeline Delay
```
Total delay = (hops + packets − 1) × T_trans + hops × T_prop
```

### TCP Sequence Numbers
- SYN consumes 1 SN
- FIN consumes 1 SN
- Pure ACK consumes 0 SN
- AN = cumulative acknowledgment (next expected byte)

### Longest Prefix Match
- When multiple routes match, select the one with the **longest prefix length**
- Default route (0.0.0.0/0) matches everything but has lowest priority

### ARP
- Resolves IP → MAC for devices on the **same subnet**
- For remote destinations, ARP resolves the **gateway's MAC**, not the final destination's MAC
