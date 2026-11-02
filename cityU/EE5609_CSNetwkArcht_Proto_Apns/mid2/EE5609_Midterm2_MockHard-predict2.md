# EE5609 Midterm 2 — Self-Test (Comprehensive)

> Covers L4–L7. Progressive difficulty: warm-up → algorithms → calculations → comprehensive scenario.
> Time limit: 90 minutes. Total: 100 marks.

---

## Question 1 (16 marks) — Warm-Up: ARP, DHCP, DNS

### (a) ARP Basics (6 marks)

Host A (192.168.1.10, MAC: AA-AA-AA-AA-AA-AA) wants to send an IP datagram to Host B (192.168.1.20) on the **same subnet**. Host A's ARP cache is empty.

**(i)** What does Host A broadcast, and to what destination MAC address? *(2 marks)*

**(ii)** What does Host B reply with, and is the reply broadcast or unicast? Why? *(2 marks)*

**(iii)** After the exchange, Host A sends a 500-byte IP datagram to Host B. What are the source and destination MAC addresses in the Ethernet frame? *(2 marks)*

### (b) DHCP Overview (4 marks)

A new host H boots up with no IP configuration. It needs an IP address, subnet mask, default gateway, and DNS server address.

**(i)** Name the four DHCP messages in order. *(2 marks)*

**(ii)** For the first message (Discover), specify the values at three layers: Ethernet destination MAC, source IP, and destination IP. *(2 marks)*

### (c) DNS Query Types (6 marks)

**(i)** A client wants to resolve `www.cityu.edu.hk`. It queries the root DNS server, which responds with a reference to the `.hk` TLD server. Is this a recursive or iterative query? Explain briefly. *(3 marks)*

**(ii)** What DNS record type maps a domain name to an IPv6 address? What record type maps a domain name to another domain name (alias)? *(3 marks)*

---

## Question 2 (22 marks) — Routing: Dijkstra, DV, OSPF vs BGP

### (a) Dijkstra's Algorithm (14 marks)

Run Dijkstra's algorithm with source node **S**. The topology and link costs are:

```
        3       2
   S ------ A ------ B
   |        |        |
 1 |      4 |      1 |
   |        |        |
   C ------ D ------ E
        2       3
```

| Link | Cost | Link | Cost |
|------|------|------|------|
| S–A | 3 | A–D | 4 |
| S–C | 1 | B–E | 1 |
| A–B | 2 | C–D | 2 |
| | | D–E | 3 |

**(i)** Complete the Dijkstra iteration table. For each step, show N' and D(v), p(v) for v ∈ {A, B, C, D, E}. *(8 marks)*

**(ii)** Give the least-cost path and cost from S to each node. *(4 marks)*

**(iii)** Construct S's next-hop forwarding table (destination → first hop). *(2 marks)*

### (b) Count-to-Infinity (4 marks)

Three routers x, y, z run distance-vector routing. Initially c(x,y) = 5, c(y,z) = 2, c(x,z) = 100. The least costs to x have converged: Dy(x) = 5, Dz(x) = 7 (via y). Now c(x,y) changes from 5 to 50.

Explain in at most four sentences why y and z can enter a count-to-infinity loop. Does "bad news" travel fast or slow? *(4 marks)*

### (c) OSPF vs BGP (4 marks)

Compare OSPF and BGP in at most five sentences. Address:
- Routing scope (intra-AS vs inter-AS)
- Algorithmic family (link-state vs path-vector)
- One reason BGP carries the AS-PATH attribute *(4 marks)*

---

## Question 3 (18 marks) — IP Fragmentation + Pipeline Delay

### (a) IP Fragmentation (10 marks)

A router receives an IP datagram of **5200 bytes** (including the 20-byte IP header). The outgoing link has MTU = **1500 bytes**. DF flag = 0.

**(i)** How many fragments are produced? *(2 marks)*

**(ii)** For each fragment, fill in the table: *(6 marks)*

| Fragment | Total Length (bytes) | Data Length (bytes) | MF | Offset |
|----------|---------------------|---------------------|-----|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

**(iii)** If the MTU were **2000 bytes** instead, how many fragments and what are the offsets? *(2 marks)*

### (b) Pipeline Delay (8 marks)

A 6000-byte message is sent from S to D through 2 intermediate routers (S → R1 → R2 → D, total 3 hops). The message is divided into **5 equal payloads**, and a 40-byte header is added to each packet. All links run at **3 Mbps** with propagation delay **0.5 ms** each. Ignore processing delay.

**(i)** What is the size of each packet (in bytes)? What is the transmission time of one packet? *(2 marks)*

**(ii)** At what time does the first complete packet arrive at D? *(3 marks)*

**(iii)** At what time does the last bit of the last packet arrive at D? *(3 marks)*

---

## Question 4 (22 marks) — TCP Comprehensive

A Client (ISN = 800) and a Server (ISN = 2000) establish a TCP connection. Both receive windows are fixed at rwnd = 4096 bytes. MSS = 1024 bytes. Initial cwnd = 1 MSS.

Application exchange (after sockets are created):
1. Client writes 200 bytes; Server reads them.
2. Server writes 5000 bytes; Client reads them.
3. Client closes; then Server closes.

Assume no loss, no retransmission.

### (a) Three-Way Handshake (6 marks)

List the three TCP segments of the connection establishment. For each, state: direction, flags, SN, and AN. *(6 marks)*

### (b) Client's 200-Byte Write (4 marks)

**(i)** What are the SN, payload length, and AN of the segment carrying the Client's 200-byte data? *(2 marks)*

**(ii)** What is the AN in the Server's pure ACK for that data? *(2 marks)*

### (c) Server's 5000-Byte Transfer Under Slow Start (8 marks)

**(i)** While cwnd = 1 MSS, how many bytes may the Server send before waiting for an ACK? *(1 mark)*

**(ii)** Give the SN and payload length of the Server's first data segment. *(2 marks)*

**(iii)** After that segment is cumulatively ACKed, what is cwnd (in bytes)? What is the maximum number of unacknowledged data bytes the Server may have in flight, given min(cwnd, rwnd)? *(3 marks)*

**(iv)** How many data segments in total does the Server need to send 5000 bytes? *(2 marks)*

### (d) FIN (4 marks)

**(i)** Does a FIN consume a sequence number? *(1 mark)*

**(ii)** After all data have been acknowledged, the Client sends FIN. State the SN of the Client's FIN and the AN in the Server's ACK of that FIN. *(3 marks)*

---

## Question 5 (22 marks) — Comprehensive: ADSL Home Network

A host H is connected to a home router R that provides Internet access. H's configuration:

| Parameter | Value |
|-----------|-------|
| IP address | 10.0.0.5 |
| Subnet mask | 255.255.255.0 |
| Default gateway | 10.0.0.1 |
| DNS server | 10.0.0.1 |

| Device | MAC address |
|--------|-------------|
| H | 00-11-22-AA-AA-AA |
| R (LAN side) | 00-11-22-BB-BB-BB |

The user opens a browser and requests `http://www.university.edu` (port 80). All caches on H (ARP, DNS, browser) are initially empty. A DNS lookup returns that www.university.edu has IP address **140.112.33.50**.

H and the origin server communicate through R. H sends frames only on its LAN. R performs NAT: its public IP is **140.113.1.100**.

### (a) Frame Sequence (12 marks)

Using a table with columns Frame #, Src MAC, Dst MAC, Src IP, Dst IP, and Purpose, list the sequence of frames sent and received by H until the first frame containing the HTTP response is received.

Assume:
- DNS uses a single request/reply
- TCP uses a standard three-way handshake
- HTTP uses one request and one response
- ARP is needed only when H does not yet know a MAC

*(12 marks)*

### (b) Why ARP for Gateway? (4 marks)

Explain briefly why H's ARP request asks for the MAC address of 10.0.0.1 rather than of 140.112.33.50. *(4 marks)*

### (c) Router's Role (4 marks)

The home router R performs four roles beyond simple IP forwarding. Name and briefly describe each. *(4 marks)*

### (d) HTTP Versions (2 marks)

Contrast non-persistent HTTP/1.0 with persistent HTTP/1.1 when downloading one HTML page and three images from the same server (empty cache). Which approach requires fewer TCP connections? *(2 marks)*

---

## End of Examination Paper
