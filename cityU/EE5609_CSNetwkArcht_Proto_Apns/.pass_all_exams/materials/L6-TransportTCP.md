# EE5609 Computer Networks - Lecture 6

## Transport Layer: TCP and UDP

### Learning Objectives

- Explain and compare UDP with TCP.
- Describe TCP connection establishment and termination.
- Interpret TCP sequence numbers and acknowledgements.
- Explain TCP retransmission, flow control, and basic congestion control.
- Analyse a TCP exchange using sequence numbers, ACKs, and window limits.

---

## 1. Transport Services and Protocols

### Overview

- Provide **logical communication** between application processes running on different hosts.
- Transport protocols actions in end systems:
  - **Sender**: breaks application messages into segments, passes to network layer
  - **Receiver**: reassembles segments into messages, passes to application layer
- Two widely used Internet transport protocols: **TCP** and **UDP**

### Network Stack Context

```
application
transport
network
data link
physical
```

Hosts connect via: home network → enterprise network → regional ISP → global ISP → datacenter network → content provider network → mobile network.

---

## 2. Transport Layer: Ports

A single transport layer is used to support multiple application processes through the use of **ports**.

---

## 3. Multiplexing / Demultiplexing

### Demultiplexing (Receiver Side)

- Use header info to deliver received segments to the correct socket
- Handle data from multiple sockets, add transport header (later used for demultiplexing)

### Multiplexing (Sender Side)

- Handle data from multiple application processes
- Add transport header for later demultiplexing at receiver

### Example: HTTP Server and Client

```
client                          HTTP server
  |  HTTP msg (Ht)                |
  |------------------------------>|
  |  HTTP msg (Ht, Hn)            |
  |<------------------------------|
```

**Q:** How did transport layer know to deliver message to Firefox browser process rather than Netflix process or Skype process?

→ Through **port numbers** (demultiplexing).

---

## 4. Transport Protocols in the Internet

| Protocol | Features |
|----------|----------|
| **TCP** (Transmission Control Protocol) | Reliable, in-order delivery; congestion control; flow control; connection setup |
| **UDP** (User Datagram Protocol) | Unreliable, unordered delivery; no-frills extension of "best-effort" IP |

**Services NOT available:**
- Delay guarantees
- Bandwidth guarantees

---

## 5. UDP: Connectionless Transport

### Characteristics

- **"Best effort"** service — UDP segments may be:
  - Lost
  - Delivered out-of-order to app
- **Connectionless**: no handshaking between UDP sender and receiver
- Each UDP segment handled independently of others
- No connection establishment (which can add RTT delay)
- Simple: no connection state at sender, receiver
- Small header size
- No congestion control
- UDP can blast away as fast as desired!
- Can function in the face of congestion

### Why is there a UDP?

- Streaming multimedia apps (loss tolerant, rate sensitive)
- DNS
- SNMP
- HTTP/3
- If reliable transfer needed over UDP (e.g., HTTP/3):
  - Add needed reliability at application layer
  - Add congestion control at application layer

### UDP: Transport Layer Actions

```
SNMP client                        SNMP server
  application                         application
  transport (UDP)                     transport (UDP)
  network (IP)                        network (IP)
  link                                link
  physical                            physical
```

**UDP sender actions:**
- Is passed an application-layer message
- Determines UDP segment header fields values
- Creates UDP segment
- Passes segment to IP

### UDP Segment Format

| Field | Size | Description |
|-------|------|-------------|
| Source port # | 16 bits | Source port |
| Dest port # | 16 bits | Destination port |
| Length | 16 bits | Length in bytes of UDP segment, including header |
| Checksum | 16 bits | Error detection |
| Application data (payload) | variable | Data to/from application layer |

```
+----------+----------+
| src port | dst port |  ← 32 bits total
+----------+----------+
|  length  | checksum |
+----------+----------+
|                    |
|   application      |
|      data          |
|   (payload)        |
|                    |
+--------------------+
```

---

## 6. TCP: Connection-Oriented Transport

### Key Features

- **Reliable, in-order byte stream**: no "message boundaries"
- **Full duplex data**: bi-directional data flow in same connection
- **Point-to-point**: one sender, one receiver
- **MSS**: maximum segment size
- **Cumulative ACKs**
- **Pipelining**: TCP congestion and flow control set window size
- **Connection-oriented**: handshaking (exchange of control messages) initializes sender, receiver state before data exchange
- **Flow controlled**: sender will not overwhelm receiver

### Transmission Control Protocol

- **Flow control**: keep within the receiver's capacity
- **Error control**: detect missing data and recover it
- **Congestion control**: adjust the load sent into the network
- **Connection management**: establish, use, and close the connection

---

## 7. TCP Segment Structure

```
+----------+----------+
| src port | dst port |
+----------+----------+
|     sequence number      |
+--------------------------+
|   acknowledgement number |
+------+---+---------------+
| rwnd | H |  checksum    |
+------+---+---------------+
| U A P R S F |            |
+-------------+------------+
|   urgent     |  options  |
|   pointer    | (variable)|
+--------------+-----------+
|     application data (variable length)     |
+--------------------------------------------+
```

### TCP Header Fields

| Field | Description |
|-------|-------------|
| Source port # | Source port |
| Dest port # | Destination port |
| Sequence number | Counting bytes of data into bytestream (not segments!) |
| Acknowledgement number | ACK: seq # of next expected byte; A bit: this is an ACK |
| Receive window (rwnd) | Flow control: # bytes receiver willing to accept |
| Checksum | Internet checksum |
| RST, SYN, FIN | Connection management flags |
| C, E | Congestion notification |
| Options (variable) | TCP options |
| Header length | Length of TCP header |

---

## 8. TCP Header Format: SN, AN, Window

### Sequence Number (SN)

- Each TCP connection starts with an SN called **Initial Sequence Number (ISN)**
- The position of each data byte in the byte stream is labelled from ISN+1
- SN indicates the position of the 1st byte in each segment

### Acknowledgement Number (AN)

- AN of the next data byte expected from sender
- Implies all bytes up to AN-1 have been received correctly

### Window Size (W)

- The number of bytes counted from AN that the receiver is ready to accept

---

## 9. TCP Sequence Numbers and ACKs

### Sequence Numbers (SN)

- Byte stream "number" of 1st byte in segment's data

```
        sent       sent, not-     usable       not
       ACKed       yet ACKed      but not      usable
                  ("in-flight")   yet sent

|------|------------|-------------|-----------|
       ^            ^             ^
    ACKed        last sent    window edge
                              (window size = N)
```

### Acknowledgements (AN)

- Seq # of next byte expected from other side
- **Cumulative ACK**

---

## 10. TCP Connection Management

### Connection Establishment

- Ensure both ends are ready to communicate
- Establish initial sequence number (ISN)
- Exchange parameters, e.g., window size (in bytes)
- Allocate resources, e.g., buffer space, to support connection
- Connection establishment starts with a synchronization (**SYN**) request

---

## 11. TCP: Connection Establishment (Three-Way Handshake)

```
Client                          Server
  |                                |
  |  SYN bit=1, SN=x               |  (choose ISN=x, send TCP SYN msg)
  |------------------------------->|
  |                                |  Client state: SYN_SENT → ESTAB
  |  SYN bit=1, SN=y               |  Server state: LISTEN → SYN_RCVD
  |  ACK bit=1, AN=x+1             |  (choose ISN=y, send TCP SYNACK, acking SYN)
  |<-------------------------------|
  |                                |  Server state: SYN_RCVD → ESTAB
  |  ACK bit=1, AN=y+1             |  (received SYNACK(x) indicates server is live;
  |------------------------------->|   send ACK for SYNACK; this segment may contain
  |                                |   client-to-server data)
  |                                |  Client state: SYN_SENT → ESTAB
```

### Socket Code

```python
# Client
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Server
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
connectionSocket, addr = serverSocket.accept()
```

### Why Not Just 2-Way Handshake?

```
client                          server
  |                                |
  |  req_conn(x)                   |
  |------------------------------->|
  |                                |  acc_conn(x) → ESTAB
  |  (client terminates)           |
  |                                |  req_conn(x) retransmit → ESTAB
  |                                |
  Problem: half-open connection! (no client)
```

→ Three-way handshake prevents stale connection requests from creating half-open connections.

### Why Three Handshake Messages?

To ensure both sides agree on initial sequence numbers and both are alive before data transfer.

---

## 12. TCP: Connection Termination

```
Client                          Server
  |                                |
  |  FIN bit=1, SN=x               |  (clientSocket.close())
  |------------------------------->|
  |                                |  Client: ESTAB → FIN_WAIT_1
  |  ACK bit=1, AN=x+1             |  Server: ESTAB → CLOSE_WAIT
  |<-------------------------------|
  |                                |  (can still send data)
  |  Client: FIN_WAIT_1 → FIN_WAIT_2
  |                                |
  |  FIN bit=1, SN=y               |  (server close)
  |<-------------------------------|  Server: CLOSE_WAIT → LAST_ACK
  |  ACK bit=1, AN=y+1             |
  |------------------------------->|  Client: FIN_WAIT_2 → TIME_WAIT
  |                                |  (timed wait for 2×max segment lifetime)
  |  Client: TIME_WAIT → CLOSED    |  Server: LAST_ACK → CLOSED
```

---

## 13. A Data-Transfer Trace

```
Host A                          Host B
  |                                |
  |  SN=42, AN=79, data = 'C'      |  (User types 'C')
  |------------------------------->|
  |                                |  Host B ACKs receipt of 'C', echoes back 'C'
  |  SN=79, AN=43, data = 'C'      |
  |<-------------------------------|
  |                                |  Host A ACKs receipt of echoed 'C'
  |  SN=43, AN=80                  |
  |------------------------------->|
```

---

## 14. TCP Flow Control

### The Problem

**Q:** What happens if network layer delivers data faster than application layer removes data from socket buffers?

```
from sender →  [ IP code → TCP socket buffers → receiver buffers ]  → application process
```

### The Solution: Receive Window

- Receiver controls sender, so sender won't overflow receiver's buffer by transmitting too much, too fast
- TCP receiver "advertises" free buffer space in **rwnd** field in TCP header
  - `RcvBuffer` size set via socket options (typical default is 4096 bytes)
  - Many operating systems auto-adjust RcvBuffer
- Sender limits amount of unACKed ("in-flight") data to received rwnd
- Guarantees receive buffer will not overflow

```
+------------------------------------------+
| RcvBuffer                                |
| [buffered data][  free buffer space  ]   |
|                |← rwnd →|                |
+------------------------------------------+
```

---

## 15. TCP Error Control

### Why?

So that TCP can guarantee reliable service to application layer even when IP is unreliable.

### Error Types

| Error Type | Detection | Recovery |
|------------|-----------|----------|
| Segments arriving out of order | Based on SN in TCP header | Re-order and ACK |
| Segments duplicated | Based on SN | Discard and ACK |
| Segments corrupted | Based on checksum in TCP header | Discard and wait for timeout retransmission |
| Segments loss | — | Wait for timeout retransmission |

---

## 16. Timeout Retransmission

### Lost ACK Scenario

```
Host A                          Host B
  |                                |
  |  Seq=92, 8 bytes of data       |
  |------------------------------->|
  |                                |
  |  ACK=100                       |
  |<-------------------------------|
  |          X (lost)              |
  |                                |
  |  timeout                       |
  |  Seq=92, 8 bytes of data       |  (retransmit)
  |------------------------------->|
  |                                |
  |  ACK=100                       |
  |<-------------------------------|
```

### How Long Should TCP Wait for the ACK?

| Term | Definition |
|------|-----------|
| **RTT** (measured) | Time from sending data to receiving its ACK |
| **SRTT** (smoothed) | A smoothed estimate from multiple RTT samples |
| **RTO** (waiting limit) | How long TCP waits before a timeout retransmission |

- Too short → unnecessary retransmissions
- Too long → slow recovery from segment loss

**Solution:** Measure Round Trip Time (RTT) and compute smoothed RTT (SRTT). The Retransmission TimeOut (RTO) is then derived from SRTT.

---

## 17. Congestion in the Network

### Congestion

- Informally: "too many sources sending too much data too fast for network to handle"
- Manifestations:
  - Long delays (queueing in router buffers)
  - Packet loss (buffer overflow at routers)

### Congestion Control vs Flow Control

| | Scope |
|---|-------|
| **Congestion control** | Too many senders, sending too fast (network-wide) |
| **Flow control** | One sender too fast for one receiver (end-to-end) |

---

## 18. The Congestion Window

### TCP Sender Limits Transmission

$$\text{LastByteSent} - \text{LastByteAcked} \leq \min(\text{cwnd}, \text{rwnd})$$

- **cwnd** (congestion window) is dynamically adjusted in response to observed network congestion (implementing TCP congestion control)

```
        last byte    last byte
         ACKed        sent
           |           |
           v           v
|----------|===========|----------|
           |←  cwnd  →|
           | available |
           | but not   |
           | used      |
```

### TCP Sending Behavior

- Roughly: send cwnd bytes, wait RTT for ACKs, then send more bytes
- TCP rate ≈ `cwnd / RTT` bytes/sec

---

## 19. TCP Slow Start

- When connection begins, increase rate **exponentially** until first loss event:
  - Initially `cwnd = 1 MSS`
  - Double cwnd every RTT
  - Done by incrementing cwnd for every ACK received

```
cwnd
  |                          /
  |                        /
  |                      /
  |                    /
  |                  /
  |                /
  |              /
  |            /
  |          /
  |        /
  |      /
  |    /
  |  /
  |/
  +--------------------------------→ time (RTT)
```

- Summary: initial rate is slow, but ramps up exponentially fast

---

## 20. TCP Exercise

### Exercise Statement

Figure Q1 shows an extract of a Client program and a Server program (in pseudo code) interacting with their TCP layers. Fill in the minimum number of TCP segments that must be exchanged between the Client TCP and Server TCP, in an ideal communication situation without error retransmission. Indicate clearly the Sequence Number (SN) and the Acknowledgement Number (AN) in each segment. Include SYN or FIN flags if they are set.

**Assumptions:**
- ISN for Client TCP = **100**
- ISN for Server TCP = **600**
- Both window sizes fixed at **2048 bytes**
- Maximum Segment Size (MSS) = **536 bytes**
- Initial congestion window size = **1 MSS**

### Pseudo Code

```
Client TCP                          Server TCP
c = new Socket()                    svr = new ServerSocket()
c.write(30 bytes)                   s = svr.accept()
c.read(3000 bytes)                  s.read(30 bytes)
c.close()                           s.write(3000 bytes)
                                    s.close()
```

### Phase 1: Connection Establishment

```
Client (ISN=100)                   Server (ISN=600)
  |                                    |
  |  SYN: SN=100                       |
  |----------------------------------->|
  |  SYN+ACK: SN=600, AN=101           |
  |<-----------------------------------|
  |  ACK: AN=601                       |
  |----------------------------------->|
```

### Phase 2: Data Transfer (Flow & Congestion Control)

**Client writes 30 bytes → Server reads 30 bytes:**
- Client sends 1 data segment: SN=101, 30 bytes of data, AN=601
- Server ACKs: SN=601, AN=131

**Server writes 3000 bytes → Client reads 3000 bytes:**
- MSS = 536 bytes, so 3000 bytes = ⌈3000/536⌉ = 6 segments
- Initial cwnd = 1 MSS = 536 bytes
- Slow start: cwnd = 1 → 2 → 4 → ...
- Round 1: send 1 segment (536 bytes), receive 1 ACK → cwnd = 2
- Round 2: send 2 segments (1072 bytes), receive 2 ACKs → cwnd = 4
- Round 3: send 3 segments (remaining 3000 - 536 - 1072 = 1392 bytes → 3 segments of 536, 536, 320)

**Window size constraint:** rwnd = 2048 bytes, so at most 2048 bytes can be in flight.

### Phase 3: Connection Termination

```
Client                              Server
  |                                    |
  |  FIN: SN=131, AN=3601              |  (c.close())
  |----------------------------------->|
  |  ACK: SN=3601, AN=132              |
  |<-----------------------------------|
  |  FIN: SN=3601, AN=132              |  (s.close())
  |<-----------------------------------|  (or combined FIN+ACK above)
  |  ACK: SN=132, AN=3602              |
  |----------------------------------->|
```

### Notes

- A SYN and FIN segment does not carry data but **consumes one sequence number**
- A SYN+ACK, FIN+ACK does not carry data but **consumes one sequence number**
- ACK segment, carrying no data, **does not consume any sequence number**
