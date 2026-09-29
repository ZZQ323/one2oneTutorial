# EE5609 Computer Networks - Lecture 4

## The Network Layer – Part I

### Learning Objectives

- Compare circuit switching, virtual-circuit packet switching, and datagram packet switching
- Calculate transmission and propagation delays, including the effect of packet pipelining
- Use CIDR prefixes to calculate subnet masks, network and broadcast addresses, and allocate subnet address blocks
- Explain how DHCP configures hosts and how NAT translates IP addresses and port numbers

---

## 1. Internet Structure: A "Network of Networks"

### Internet Structure Overview

- Hosts connect to Internet via access ISPs (national or global)
- Access ISPs must be interconnected so that any two hosts can communicate
- Resulting network of networks is very complex
- Evolution driven by economics and national policies

### ISP Hierarchy

- **Tier-1 ISPs**: Commercial backbone ISPs (e.g., Level 3, Sprint, AT&T, NTT)
  - National & international coverage
  - Well-connected large networks
  
- **Content Provider Networks**: Private networks (e.g., Google, Facebook)
  - Connect data centers to Internet
  - Often bypass tier-1 and regional ISPs

- **IXP (Internet eXchange Points)**: Public locations where ISPs interconnect

### Connecting End Systems to Edge Router

- Residential access networks
- Institutional access networks (school, company)
- Mobile access networks (WiFi, 4G/5G)

### Access Networks

| Technology | Speed | Notes |
|------------|-------|-------|
| WiFi wireless access point | 54, 450 Mbps | Wireless |
| Wired Ethernet | 1 Gbps | To/from headend or central office |
| Cable/DSL modem | Varies | Combined in single box with router, firewall, NAT |

---

## 2. Communication at Each Layer

### Layers and Addresses

- **Port number**: Identifies a transport endpoint used by an application
- **IP address**: Identifies a network interface and supports delivery across networks
- **Link address (MAC)**: Identifies a local-link endpoint (Ethernet or Wi-Fi)

### Messages, Segments, Packets and Frames

| Layer | Unit | Description |
|-------|------|-------------|
| Application | **Message** | Information an application sends (e.g., HTTP request) |
| Transport | **Segment/Datagram** | TCP segment or UDP datagram with header (src/dst ports) and payload |
| Network | **IP Packet (Datagram)** | IP header + payload, forwarded across networks |
| Link | **Frame** | Link-layer header + payload + trailer for delivery on one link |

### Encapsulation and Decapsulation

- Each layer adds information for its own task
- The receiver removes it in reverse order

### A Packet's Journey

1. Host obtains server's IP address from DNS
2. Routing table identifies next hop
3. Each router forwards packet using destination IP address
4. Packet crosses several links before reaching server

---

## 3. The Network-Layer Service

### Internet Protocol (IP) Characteristics

- **Connectionless**: Each packet handled independently, no flow control
- **Unreliable**: No error control
- **Best-effort**: No throughput guarantee, no delay guarantee, no QoS guarantee

### Key Functions

- **Forwarding**: Moves packets from router's input link to appropriate output link
- **Routing**: Determines route taken by packets from source to destination

### Quality of Service (QoS)

| Service Model | Bandwidth | Loss | Order | Timing |
|---------------|-----------|------|-------|--------|
| Internet best effort | none | no | no | no |
| ATM CBR | guaranteed | yes | yes | yes |
| ATM ABR | guaranteed min | no | yes | no |
| Internet Intserv | possible | possibly | possibly | no |
| Internet Diffserv | possible | possibly | possibly | no |

---

## 4. Connection-Oriented vs Connectionless

| Connection-Oriented | Connectionless |
|---------------------|----------------|
| Establish a logical connection | No per-connection setup |
| Maintain per-connection state | No per-connection state required |
| Close the connection | No connection-release phase |

### Question 1: Connection-Oriented vs Connectionless

**What is the principal difference between connectionless communication and connection-oriented communication?**

**Answer:**
- **Connection-oriented**: Three phases (establishment → data transfer → release)
- **Connectionless**: No phases, just sends data directly

---

## 5. Network Switching Classification

### Circuit Switching

**Characteristics:**
- End-end resources allocated and reserved for "call"
- Dedicated resources: no sharing
- Circuit-like (guaranteed) performance
- Circuit segment idle if not used (wasteful)

**Problems with Circuit Switching:**
- Designed for voice service
- Resources dedicated to particular call
- For data transmission, connection often idle (e.g., web browsing)
- Data rate fixed - both ends must operate at same rate

### Packet Switching

**Characteristics:**
- Hosts create packets
- Network nodes forward them over shared links
- Buffers hold packets while waiting for output link
- Each packet carries header and portion of data

**Store-and-Forward:**
- Entire packet must arrive at router before transmission on next link
- Packet transmission delay = L/R seconds (L bits at R bps)

**Example:**
- L = 10 Kbits, R = 100 Mbps
- One-hop transmission delay = 0.1 msec

### Datagram vs Virtual Circuit

#### Datagram Approach
- Each packet treated independently
- Each node chooses next hop dynamically
- Packets can take any route
- May arrive out of order or go missing
- Receiver must re-order and recover missing packets
- **Example: Internet**

#### Virtual Circuit Approach
- Pre-planned route established before data transfer
- All packets follow same route
- Packet contains virtual circuit identifier (not full destination)
- No dedicated resources reserved (still store-and-forward)
- **Examples: X.25, Frame Relay, ATM**

---

## 6. Delay in Packet Switched Networks

### Four Components of Delay

1. **Processing**: Examine header and choose output
2. **Queueing**: Wait behind other packets (varies with traffic)
3. **Transmission**: Push L bits onto link of rate R → Delay = L/R
4. **Propagation**: Travel distance d at signal speed s → Delay = d/s

### Pipeline Effect

When multiple packets traverse multiple hops, they can be pipelined:
- First packet arrives after k hops
- Subsequent packets arrive one transmission time apart

### Exercise: Pipeline Effect

**Problem:** Consider a packet switched network with nodes S and D connected through intermediate node I. A message of 1000 bytes is fragmented into four packets, each with 50-byte header. All links run at same data rate. Propagation delay is negligible. Determine minimum data rate for 100ms total transmission delay.

**Solution:**
- Frame size = 250 + 50 = 300 bytes
- Let T_f = transmission time of one packet
- From diagram: Total delay T_d = 5 × T_f
- Since T_d < 100ms: T_f < 20ms
- T_f = (300 bytes × 8) / R
- Therefore: R > 120 kbps

### Exercise: Circuit vs Packet Switching Delay

**Problem:** Compare delay in sending x-bit message over k-hop path in circuit switched vs packet switched network.
- Circuit switching: setup time s seconds per hop, propagation delay d seconds
- Packet switching: packet size p bits, data rate b bps

**Circuit Switching Delay:**
- At t = s: circuit set up
- At t = s + x/b: last bit sent
- At t = s + x/b + kd: message arrives
- **Total = s + x/b + kd**

**Packet Switching Delay (with pipeline):**
- Total delay = k × (T_x + d) + (number of packets - 1) × T_x
- Where T_x = p/b and number of packets = x/p
- **Total = k × (p/b + d) + (x/p - 1) × p/b**

**When does packet switching have lower delay?**
- When: x/p + (k-1)×p/b + kd < s + x/b + kd
- Simplified: x/p + (k-1)×p/b < s + x/b

---

## 7. IP Datagram Format

### IPv4 Header Structure (20 bytes typical)

| Field | Size | Description |
|-------|------|-------------|
| Version | 4 bits | IP protocol version (4 for IPv4) |
| Header Length | 4 bits | Header length in 32-bit words |
| Type of Service | 8 bits | Diffserv (bits 0-5) + ECN (bits 6-7) |
| Total Length | 16 bits | Total datagram length in bytes (max 64KB) |
| Identification | 16 bits | For fragmentation/reassembly |
| Flags | 3 bits | DF (Don't Fragment), MF (More Fragments) |
| Fragment Offset | 13 bits | Position in original datagram (÷8) |
| Time to Live (TTL) | 8 bits | Max hops (decremented at each router) |
| Protocol | 8 bits | Upper layer (TCP=6, UDP=17) |
| Header Checksum | 16 bits | For header error checking |
| Source IP Address | 32 bits | Source address |
| Destination IP Address | 32 bits | Destination address |
| Options | Variable | Optional fields (timestamp, route recording) |

**Overhead:** 20 bytes TCP + 20 bytes IP = 40 bytes + app layer overhead

---

## 8. IP Addressing

### Basic Concepts

- **IP address**: 32-bit identifier associated with each host or router interface
- **Interface**: Connection between host/router and physical link
- Router typically has multiple interfaces
- Host typically has one or two interfaces (wired Ethernet, wireless WiFi)

### Dotted-Decimal Notation

Example: 223.1.1.1 = 11011111 00000001 00000001 00000001

### Subnets

**Definition:**
- Device interfaces that can physically reach each other without passing through a router
- IP addresses have structure:
  - **Subnet part**: High-order bits (common within subnet)
  - **Host part**: Low-order bits (unique within subnet)

**Recipe for defining subnets:**
1. Detach each interface from its host/router
2. Each isolated network is called a subnet

**Example:**
- Subnet 223.1.1.0/24 (subnet mask /24 = high-order 24 bits)

### CIDR: Classless InterDomain Routing

**Format:** a.b.c.d/x
- x = number of bits in subnet portion
- Subnet portion of arbitrary length

**Example:** 200.23.16.0/23

### Network, Host and Broadcast Addresses

**Special addresses in IPv4 LAN:**
- **Network address**: Host bits all 0 (identifies subnet)
- **Broadcast address**: Host bits all 1 (targets all interfaces in subnet)

**Example: 192.0.2.0/24**
- Network: 192.0.2.0
- Broadcast: 192.0.2.255
- Usable interface addresses: 192.0.2.1 – 192.0.2.254

**Formula:** With h host bits: 2^h total addresses, normally 2^h - 2 usable

### Subnet Calculation Example: 192.0.2.130/26

- 26 prefix bits → 6 host bits
- Each block contains 2^6 = 64 addresses
- Final-octet boundaries: 0, 64, 128, 192

| Result | Value |
|--------|-------|
| Subnet mask | 255.255.255.192 |
| Network address | 192.0.2.128 |
| Broadcast address | 192.0.2.191 |
| Usable host range | 192.0.2.129 – 192.0.2.190 |

### Exercise: Broadcast Address

**Given:** 145.32.128.0 / 255.255.224.0

**In binary:**
- 145.32.10000000.0 / 255.255.11100000.0

**Broadcast address** (all 1s in host-id):
- Binary: 145.32.10011111.11111111
- Dotted decimal: **145.32.159.255**

### Exercise: Subnet Allocation

**Problem:** IP block 155.69.0.0/16, need to allocate for:
- 3 schools with 4000 hosts each
- 12 schools with 2000 hosts each

**Solution:**
- /20 mask: 2^12 - 2 = 4094 hosts per subnet
- /21 mask: 2^11 - 2 = 2046 hosts per subnet

**Allocation:**
- **3 blocks with /20:**
  - 155.69.0.0/20: 155.69.0.0 – 155.69.15.255
  - 155.69.16.0/20: 155.69.16.0 – 155.69.31.255
  - 155.69.32.0/20: 155.69.32.0 – 155.69.47.255

- **12 blocks with /21:**
  - 155.69.64.0/21: 155.69.64.0 – 155.69.71.255
  - 155.69.72.0/21: 155.69.72.0 – 155.69.79.255
  - ... (continue for 12 blocks)
  - Remember: no overlapping address blocks

### Exercise: Variable Length Subnet Masking

**Problem:** Divide 193.169.1.0/24 into subnets:
- Subnet A: 30 hosts
- Subnet B: 100 hosts
- Subnet C: 60 hosts
- Subnet D: 10 hosts
- 4 point-to-point links

**Solution:**
| Subnet | Size | Mask | Address Range |
|--------|------|------|---------------|
| Subnet B | 100 hosts | /25 | 193.169.1.0 – 193.169.1.127 |
| Subnet C | 60 hosts | /26 | 193.169.1.128 – 193.169.1.191 |
| Subnet A | 30 hosts | /27 | 193.169.1.192 – 193.169.1.223 |
| Subnet D | 10 hosts | /28 | 193.169.1.224 – 193.169.1.239 |
| P2P links | 2 hosts each | /30 | 4 blocks of /30 |

---

## 9. DHCP: Dynamic Host Configuration Protocol

### Purpose

- Host dynamically obtains IP address from network server
- Can renew lease on address
- Allows reuse of addresses (only hold while connected)
- Supports mobile users

### DHCP Message Exchange

1. **DHCP Discover** (broadcast)
   - Client: "Is there a DHCP server?"
   - src: 0.0.0.0:68, dest: 255.255.255.255:67

2. **DHCP Offer** (broadcast)
   - Server: "Here's an IP address you can use"
   - Includes: offered IP, lifetime, transaction ID

3. **DHCP Request** (broadcast)
   - Client: "I would like to use this IP address"

4. **DHCP ACK** (broadcast)
   - Server: "OK, you've got that IP address"

**Note:** Steps 1-2 can be skipped if client remembers and reuses previous address

### Additional DHCP Information

DHCP server can also provide:
- Address of first-hop router
- Name and IP address of DNS server
- Network mask

### DHCP Encapsulation Example

```
DHCP message
  ↓ UDP segment
    ↓ IP datagram
      ↓ Ethernet frame (broadcast: FFFFFFFFFFFF)
```

- Router with DHCP server receives broadcast
- De-muxes: Ethernet → IP → UDP → DHCP
- Server formulates ACK with client's IP, router address, DNS server
- Reply forwarded back to client

---

## 10. IP Address Allocation

### How Networks Get Addresses

- Network gets allocated portion of provider ISP's address space
- ISP allocates from its block (e.g., 200.23.16.0/20)
- Can divide into smaller blocks (e.g., /23 for organizations)

### Who Allocates IP Addresses?

- **ICANN**: Internet Corporation for Assigned Names and Numbers
  - Allocates IP addresses through 5 regional registries
  - Manages DNS root zone
  - Allocated last chunk of IPv4 addresses in 2011

### IPv4 Address Exhaustion

- ICANN allocated last chunk in 2011
- NAT helps with address space exhaustion
- IPv6 has 128-bit address space

---

## 11. NAT: Network Address Translation

### Concept

- All devices in local network share one IPv4 address (as far as outside world is concerned)
- Local network uses private IP address space:
  - 10.0.0.0/8
  - 172.16.0.0/12
  - 192.168.0.0/16

### Advantages

1. Only one IP address needed from ISP for all devices
2. Can change internal addresses without notifying outside world
3. Can change ISP without changing internal addresses
4. Security: internal devices not directly addressable from outside

### NAT Operation

**Outgoing datagrams:**
- Replace (source IP, port) with (NAT IP, new port)
- Remember translation in NAT table

**Incoming datagrams:**
- Replace (NAT IP, new port) with original (source IP, port) from NAT table

### NAT Translation Example

**Host 10.0.0.1 sends:**
- Original: S: 10.0.0.1:3345, D: 128.119.40.186:80

**NAT router changes:**
- Translated: S: 138.76.29.7:5001, D: 128.119.40.186:80
- Updates table: (10.0.0.1:3345) ↔ (138.76.29.7:5001)

**Reply arrives:**
- Destination: 138.76.29.7:5001
- NAT router translates back to: 10.0.0.1:3345

---

## 12. IPv6

### Motivation

- IPv4 32-bit address space would be completely allocated
- Faster processing: 40-byte fixed length header
- Enable different treatment of "flows"

### IPv6 Datagram Format

| Field | Size | Description |
|-------|------|-------------|
| Version | 4 bits | 6 for IPv6 |
| Priority | 8 bits | Priority among datagrams in flow |
| Flow Label | 20 bits | Identify datagrams in same flow |
| Payload Length | 16 bits | Length of payload |
| Next Header | 8 bits | Identifies upper-layer protocol |
| Hop Limit | 8 bits | Decremented at each hop |
| Source Address | 128 bits | Source IPv6 address |
| Destination Address | 128 bits | Destination IPv6 address |

**What's missing compared to IPv4:**
- No checksum (speeds processing)
- No fragmentation/reassembly
- No options (available as upper-layer protocols)

### Transition from IPv4 to IPv6

- No "flag days" - gradual transition
- **Tunneling**: IPv6 datagram carried inside IPv4 datagram
  - IPv6 header + payload encapsulated in IPv4 header
  - Allows mixed IPv4/IPv4 networks to coexist

### IPv6 Adoption

- Google: ~40% of clients access via IPv6 (2023)
- NIST: 1/3 of US government domains are IPv6 capable

---

## 13. IP Fragmentation

### MTU (Maximum Transfer Unit)

- Network links have MTU - largest possible link-level frame
- Different link types have different MTUs
- Large IP datagram must be fragmented if exceeds MTU

### Fragmentation Process

- One large datagram → several smaller datagrams
- Reassembled only at destination (not at intermediate routers)
- IP header fields used to identify and order fragments

### Fragmentation Fields

| Field | Description |
|-------|-------------|
| DF (Don't Fragment) | 1 = forbids fragmentation |
| MF (More Fragments) | 1 = more fragments follow |
| Offset | Starting byte position ÷ 8 |
| Identification | Same for all fragments of this datagram |

### Fragmentation Example

**Original:** 4000-byte datagram, MTU = 1500 bytes, DF = 0

**Fragment 1:**
- Length: 1500 bytes (1480 data + 20 header)
- Offset: 0 (0/8)
- MF: 1

**Fragment 2:**
- Length: 1500 bytes (1480 data + 20 header)
- Offset: 185 (1480/8)
- MF: 1

**Fragment 3:**
- Length: 1040 bytes (1020 data + 20 header)
- Offset: 370 (2960/8)
- MF: 0

### DF Flag Set

- If DF = 1 and datagram exceeds MTU:
  - Router drops datagram
  - ICMP "Fragmentation Needed" message sent back

### IPv6 and Fragmentation

- IPv6 routers do NOT fragment packets
- ICMPv6 reports MTU problem
- PMTUD (Path MTU Discovery): Source learns limit and adjusts packet size

---

## 14. IP Routing

### IP Delivery Steps

1. Can whole IP datagram fit on next link? (MTU check)
2. Which next hop does forwarding table select?
3. How does packet reach that next hop? (ARP/ND)

### Routing Process

- **Local destination**: Send directly to that host
- **Remote destination**: Send to gateway on local link

### Longest-Prefix Matching

When looking up forwarding table entry:
- Use **longest** address prefix that matches destination

**Example:**
| Destination Range | Link Interface |
|-------------------|----------------|
| 11001000 00010111 00010*** ******** | 0 |
| 11001000 00010111 00011000 ******** | 1 |
| ******** 11001000 00010111 00011*** | 2 |
| otherwise | 3 |

**Questions:**
- 11001000 00010111 00010110 10100001 → Interface 0
- 11001000 00010111 00011000 10101010 → Interface 1

### Hierarchical Addressing: Route Aggregation

**Example:**
- Fly-By-Night-ISP advertises: "Send me anything with addresses beginning 200.23.16.0/20"
- This aggregates multiple customer blocks (200.23.16.0/23, 200.23.18.0/23, etc.)

**More Specific Routes:**
- If Organization 1 moves to different ISP
- New ISP advertises more specific route: "or 200.23.18.0/23"
- Longest-prefix matching ensures correct routing

---

## 15. Address Resolution Protocol (ARP)

### Purpose

- How to go from source to destination when only IP address is known but Ethernet requires MAC address?

### ARP Operation

1. **Broadcast locally**: "Who has the next-hop IPv4 address?"
2. **Target replies**: "I have that IP, here's my MAC address"
3. **ARP cache**: Later packets reuse the mapping (no broadcast needed)

---

## 16. What Changes at a Router?

### Fields That Change

- **TTL (Time To Live)**: Each router reduces it by 1
- **Destination IP address**: Does NOT change (final destination)
- **Next-hop IP address**: Changes at each router
- **Link-layer frame**: Completely new at each hop (new source/destination MAC)

---

## 17. IPv6 Local Delivery: Neighbor Discovery

### Neighbor Discovery (ND)

- Carried by ICMPv6
- Replaces ARP in IPv4

### ND Messages

- **Neighbor Solicitation**: "Who has this IPv6 address?"
- **Neighbor Advertisement**: "I have that address, here's my MAC"
- **Router Advertisements**: Identify routers and prefixes

---

## 18. ICMP: Internet Control Message Protocol

### Purpose

- Used by hosts and routers to communicate network-level information
- Error reporting
- Echo request/reply (ping)

### ICMP Message Types

| Type | Code | Description |
|------|------|-------------|
| 0 | 0 | Echo reply (ping) |
| 3 | 0 | Destination network unreachable |
| 3 | 1 | Destination host unreachable |
| 3 | 2 | Destination protocol unreachable |
| 3 | 3 | Destination port unreachable |
| 3 | 6 | Destination network unknown |
| 3 | 7 | Destination host unknown |
| 4 | 0 | Source quench (congestion control - not used) |
| 8 | 0 | Echo request (ping) |
| 9 | 0 | Route advertisement |
| 10 | 0 | Router discovery |
| 11 | 0 | TTL expired |
| 12 | 0 | Bad IP header |

### ICMP Message Format

- ICMP message includes first 8 bytes of IP datagram causing error
- Carried in IP datagrams (network-layer "above" IP)

---

## 19. Exercise: ARP and Ping Through Switch

### Scenario: Two hosts on same subnet (192.168.222.0/24)

**Host A:** 192.168.222.111, MAC: 00-24-81-AA-AA-AA  
**Host B:** 192.168.222.222, MAC: 00-24-81-BB-BB-BB

### Frame Exchange

| Frame | Source MAC | Destination MAC | Purpose | Switch Action |
|-------|------------|-----------------|---------|---------------|
| 1 | 00-24-81-AA-AA-AA | FF-FF-FF-FF-FF-FF | ARP request for 192.168.222.222 | Learn A's MAC on port 1, broadcast to ports 2,3 |
| 2 | 00-24-81-BB-BB-BB | 00-24-81-AA-AA-AA | ARP reply | Learn B's MAC on port 2, forward to port 1 |
| 3 | 00-24-81-AA-AA-AA | 00-24-81-BB-BB-BB | Ping request (ICMP echo) | Update A's entry, forward to port 2 |
| 4 | 00-24-81-BB-BB-BB | 00-24-81-AA-AA-AA | Ping reply (ICMP echo reply) | Update B's entry, forward to port 1 |

---

## 20. Exercise: ARP and Ping Through Router

### Scenario: Host A (192.168.111.111) pings Host B (192.168.222.222) through router

**Host A:** MAC 00-24-81-AA-AA-AA  
**Router interface 1:** 192.168.111.254, MAC 00-00-0C-D1-D1-D1  
**Router interface 2:** 192.168.222.254  
**Host B:** MAC 00-24-81-BB-BB-BB

### Frame Exchange

| Frame | Source MAC | Destination MAC | Purpose | Router Action |
|-------|------------|-----------------|---------|---------------|
| 1 | 00-24-81-AA-AA-AA | FF-FF-FF-FF-FF-FF | ARP request for default gateway 192.168.111.254 | Learn A's MAC in ARP cache |
| 2 | 00-00-0C-D1-D1-D1 | 00-24-81-AA-AA-AA | ARP reply | Send reply to A |
| 3 | 00-24-81-AA-AA-AA | 00-00-0C-D1-D1-D1 | Ping request for 192.168.222.222 | Broadcast ARP for 192.168.222.222 on subnet 222, learn B's MAC, forward ping |
| 4 | 00-00-0C-D1-D1-D1 | 00-24-81-AA-AA-AA | Ping reply | Receive reply, forward to A |

**Key Points:**
- IP addresses remain unchanged end-to-end
- MAC addresses change at each hop
- Router uses ARP to resolve next-hop MAC address

---

## 21. IP Delivery: Putting the Steps Together

### Complete IP Delivery Process

1. **Route selection**: Determine next hop using routing table (longest-prefix match)
2. **MTU check**: Ensure packet fits on path (fragment if needed)
3. **Address resolution**: Use ARP (IPv4) or Neighbor Discovery (IPv6) to resolve next-hop MAC
4. **Forwarding**: Router repeats process at each hop
5. **ICMP**: Supports diagnosis and error reporting

### Next Topic Preview

- **L5**: Who creates and updates the routing information?

---

## Key Concepts Summary

### Network Layer Functions

- **Forwarding**: Move packets from input to output interface
- **Routing**: Determine path from source to destination
- **Addressing**: IP addresses identify network interfaces
- **Fragmentation**: Break large datagrams to fit MTU

### Switching Techniques

| Technique | Connection Setup | Resource Allocation | Example |
|-----------|------------------|---------------------|---------|
| Circuit Switching | Yes | Dedicated | Traditional phone |
| Datagram | No | Shared, on-demand | Internet |
| Virtual Circuit | Yes | Shared, pre-planned route | X.25, ATM |

### Delay Components

**Total Delay = Processing + Queueing + Transmission + Propagation**

- Transmission delay = L/R (packet size / link rate)
- Propagation delay = d/s (distance / signal speed)

### IP Addressing Hierarchy

- **Subnet part**: High-order bits (network identifier)
- **Host part**: Low-order bits (host identifier within subnet)
- **CIDR**: a.b.c.d/x notation (x = prefix length)

### Special Addresses

- **Network address**: All host bits = 0
- **Broadcast address**: All host bits = 1
- **Private addresses**: 10/8, 172.16/12, 192.168/16

### Key Protocols

| Protocol | Purpose |
|----------|---------|
| DHCP | Dynamic IP address assignment |
| NAT | Translate private ↔ public addresses |
| ARP | Resolve IP → MAC (IPv4) |
| ND | Resolve IP → MAC (IPv6) |
| ICMP | Error reporting and diagnostics |

---

## Exam Focus Areas

### Must-Know Calculations

1. **Subnet calculations**: Given IP/prefix, find network, broadcast, usable range
2. **Delay calculations**: Transmission + propagation + pipeline effect
3. **Fragmentation**: Calculate offset, MF flag, number of fragments
4. **Subnet allocation**: VLSM - allocate subnets for different host counts

### Conceptual Understanding

1. **Circuit vs Packet switching**: Pros/cons, when to use each
2. **Datagram vs Virtual circuit**: Connection setup, routing, reliability
3. **NAT operation**: How translation table works, advantages
4. **DHCP process**: Four-message exchange, what information is provided
5. **IP delivery**: Routing + ARP + forwarding at each hop
6. **Longest-prefix matching**: How routers select forwarding entry

### Common Exam Questions

- Calculate subnet mask, network address, broadcast address
- Determine if two hosts are on same subnet
- Trace packet journey through multiple routers (what changes at each hop)
- Compare delay in circuit vs packet switching
- Explain NAT translation process with example
- Describe DHCP message exchange
