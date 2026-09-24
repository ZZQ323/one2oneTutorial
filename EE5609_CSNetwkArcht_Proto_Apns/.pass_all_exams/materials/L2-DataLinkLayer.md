##### EE5609 Computer Networks:

##### Architecture, Protocols, and Applications

##### L2: Data Link Layer

#### Outline

- Link-layer services
- Flow control
- Stop-and-Wait
- Sliding Window
- Error control
- Error detection
- ARQ
- Local Area Networks

|•|Multiple access and MAC|
|---|---|
|•|Ethernet|
|•|IEEE 802.11 WLAN|

## Link layer introduction

Terminology: mobile network

- hosts, routers: nodes national or global ISP
- communication channels that connect adjacent node along communication path: links
- wired, wireless
- LANs
- layer-2 packet: *frame*, encapsulates datagram
datacenter network

*link layer has responsibility of* *transferring datagram from one node* enterprise network *to physically adjacent node over a link*

#### Data Link Layer Service

…

- Framing, link access:
- encapsulate datagram into frame, adding … header, trailer
Cable access

- channel access if shared medium
- "MAC" addresses in frame headers identify source, destination
cellular

Ethernet LANs

WiFi

#### Data Link Layer Service (More)

…

- Flow control:
- Control of data flow to ensure sender not … overwhelm the receiver with data
Cable access

- Error detection:
- Errors caused by signal attenuation, noise.
- Receiver detects errors, signals retransmission, or drops frame
- Error correction:
cellular

- Receiver identifies *and corrects* bit error(s) without retransmission
Ethernet LANs

- Half-duplex and full-duplex:
- with half duplex, nodes at both ends of link
WiFi can transmit, but not at same time

#### Flow Control in Data Link Layer

- Ensure transmitting station does not overwhelm a receiving station with data •**Flow-Control Mechanisms**
- Stop-and-Wait
- Sliding Window

#### Stop-and-Wait Flow Control

- Sender waits for an **ACK** of every frame it sends
- Only **one frame** in transmission at a time

#### Stop-and-Wait: Performance

𝑇𝑓𝑟𝑎𝑚𝑒 𝑇𝑓𝑟𝑎𝑚𝑒 𝑇 𝑓𝑟𝑎𝑚𝑒 : Frame Tx time Link utilization (U) = = 𝑇 𝑐𝑦𝑐𝑙𝑒 : Time needed to send a frame 𝑇𝑐𝑦𝑐𝑙𝑒 𝑇𝑓𝑟𝑎𝑚𝑒+2∗𝑇𝑝𝑟𝑜𝑝 𝑇 𝑝𝑟𝑜𝑝 : Signal propagation delay

𝑇𝑝𝑟𝑜𝑝 U =, where a = 1+2𝑎 𝑇𝑓𝑟𝑎𝑚𝑒

|Exercise|||
|---|---|---|
||A communication link connects two nodes,|X and Y. The transmission rate of the link is 4 Mbps. The distance between the nodes is 100 km, and the signal|
||propagation velocity is 2 × 10|8 without errors, and ACK transmission and processing times are negligible. Calculate the link utilization for the stop-and-wait flow-control mechanism.|m/s. Each data frame has a length of 500 bytes. Assume that stop-and-wait flow control is used, frames are transmitted|
||||11|

||U =|1 1+2𝑎||, where a =|||𝑇𝑝𝑟𝑜𝑝 𝑇𝑓𝑟𝑎𝑚𝑒||
|---|---|---|---|---|---|---|---|---|---|
|𝑇 𝑇|𝑝𝑟𝑜𝑝 𝑓𝑟𝑎𝑚𝑒|a = U =|= H/v = 100 × 10 𝑇𝑝𝑟𝑜𝑝 𝑇𝑓𝑟𝑎𝑚𝑒 1 1+2𝑎|R = 4 Mbps, L = 500 bytes = 4,000 bits, H = 100 km, v = 2 × 10 = L/R = 4,000 / 4 × 10 = =|3 0.0005 0.001 1 1+2 (0.5)|=|/ 2 × 10 6 = 0.5 1 2|8 = 0.0005 s = 0.001 s|8 m/s 12|

|||Sliding Window Flow Control|
|---|---|---|
|• Allows ACKs|multiple frames be in transit • Sender can send up to frames • Each frame is numbered • ACK includes number of next expected frame|to N without receiving 13 [https://www.geeksforgeeks.org/computer-networks/sliding-window-protocols-summary-with-questions/|](https://www.geeksforgeeks.org/computer-networks/sliding-window-protocols-summary-with-questions/|)

#### Sliding Window: Performance

- Performance depends upon:
- Parameter a
- Window size N
- Frame transmission time = 1 (normalized to itself)
- Normalized propagation delay = a
- If 𝑁 ≥ 2𝑎 + 1: Can transmit continuously without exhausting the window -> **U = 1**
- If 𝑁 < 2𝑎 + 1: Window is exhausted at t=N -> **U = N/(1+2a)**

#### Exercise

A 128 kbps leased line connects two company offices and is used to transfer confidential data. A sliding-window link-layer protocol with a 3-bit sequence number is deployed. Determine the minimum sender window size required to ensure a throughput of at least 96 kbps. Assume that the average packet size is 160 bytes, and the one-way signal propagation delay is 15 ms. The ACK transmission and processing times are negligible and probability of packet error is negligible

|Given:|||
|---|---|---|
|Tx_rate = 128 Kbps|Propagation delay = 15 ms Packet size = 160 bytes = 1,280 bits 3 bit used for frame sequencing|Calculate Normalised propagation delay: a = Propagation delay /average frame transmission time Ave frame tx_time = ave. frame size /Tx_rate = 1,280 bit /128 K = 10 ms a = 15 ms /10 ms = 1.5|

||17|

96 The required link utilization: 𝑈 𝑚𝑖𝑛 = = 0.75 128

Utilization of the link is given by:

U = N/(1 +2a) where N is the window size

0.75 ≤ N /( 1+ 2*1.5) 𝑁 𝑚𝑖𝑛
= 3

#### Exercise

In the figure below, frames are generated at node A and sent to node C through node B. Determine the minimum transmission rate required between nodes B and C so that the buffers of node B are not flooded, based on the following:

(a) The data rate between A and B is 100 *Kbps*.
(b) The propagation delay is 10 m*sec*/*km* for both links.
(c) The lines are full duplex between the nodes.
(d) All data frames are 1000 bit long; ACK frames are separate frames of negligible length.
(e) Between A and B, a sliding-window protocol with a window size of 3 is used, and each frame is acknowledged individually.
(f) Between B and C, a stop and wait is used.
(g) There is no error, and the processing delay at the nodes is negligible.

A B: Propagation Time = 2000 *10 μsec = 20 msec 3 Transmission Time = 1000/(100*10 ) = 10 msec

B C: Propagation Time = 500 *10 μsec = 5 msec Transmission Time = x = 1000/R msec R = Data rate between B and C in kbps
A B Start sending 1st packet 00 Start sending 2nd packet 10 Start sending 3rd packet 20

Ack recd for 1st packet, start sending 4th packet 50 Ack recd for 2nd packet, start sending 5th packet 60 Ack recd for 3rd packet, start sending 6th packet 70

Ack recd for 4th packet, start sending 7th packet 100 Ack recd for 5th packet, start sending 8th packet 110

A B: Takes 50 msec to transmit 3 frames.

B C: Takes 10 + x msec to transmit one frame

Therefore, 50 = 3 (10 + x) x = 20/3

x = 1000/R R = 1000/x = 150 kbps

#### Error Control in Data Link Layer

•**Objective**

- To **detect** and **correct** errors that occur in frame transmission
•**Frame Error in DLL**

- Lost Frame: the receiver does not receive a frame (or the header was corrupted such that the frame was not recognizable)
- Damaged Frame: the receiver receives a frame, but some of its bits are in error

#### Error Detection

EDC: error detection and correction bits (e.g., redundancy) D: data protected by error checking, may include header fields

datagram datagram Error detection not 100% otherwise reliable!

||||bits in D' all|N|• protocol may miss||
|---|---|---|---|---|---|---|---|
||d data bits|||OK ?|detected error|• larger EDC field yields|some errors, but rarely|
||EDC bit-error prone link||D'|EDC'|better detection and correction|

D

#### Parity checking

Can detect *and* correct errors (without retransmission!) single bit parity:

- two-dimensional parity: detect
- detect single bit errors
*and correct* single bit errors 0111000110101011 1 <u>row parity</u>... *d* data bits d d 1,1 1,jd1,j+1... d d 2,1 2,jd2,j+1 parity bit.. ... ... .... Even/odd parity: set parity bit so <u>d... d</u> d <u>i,1 i,j</u> i,j+1 column there is an even/odd number of 1's parity... d d d i+1,1 i+1,j i+1,j+1 At receiver:

- compute parity of *d* received
detected 1 0 1 0 1 1 no errors: 1 0 1 0 1 1 bits andparity (even parity) 1 1 1 1 0 0 1 0 1 1 0 0error correctable

- compare with received parity bit
<u>0 1 1 1 0 0 1 1 1 0 1</u> single-bit – if different then error0 0 1 0 1 error: 0 0 1 0 1 0 detectedparity error

||Cyclic Redundancy Check (CRC) • more powerful error-detection coding • G: bit pattern (generator), of|• D: data bits (given, think of these as a binary number)||r+1|bits (given, specified in CRC standard)||
|---|---|---|---|---|---|---|---|
||||D: data bits (given, think of these as a binary number)||r+1|bits (given, specified in CRC standard)||
|||D: data bits (given, think of these as a binary number)||r+1|bits (given, specified in CRC standard)||
|bits to send||
|sender:|compute r • can detect all burst errors less than r+1 bits|<D,R> = D 2 • widely used in practice (Ethernet, 802.11 WiFi)|r *|XOR R CRC bits, R, such that <D,R> • receiver knows G, divides <D,R> by G. If non-zero remainder: error detected!|formula for these bits exactly|divisible by G (mod 2) 25|

#### Cyclic Redundancy Check (CRC)

<u>G</u> Sender wants to compute R <u>101 0 1 1</u> such that:1 0 0 1 1 0 1 1 1 0 0 0 0

*. r*1 0 0 1
*D 2 (here, r=3) 0 0 0 ... or equivalently (XOR R both sides): 1 0 1r D*2 (here, r=3) 0 0 0 ... or equivalently (XOR R both sides): *. r* *D 2 = nG XOR R* 1 0 1r D*2 (here, r=3) 0 0 0 ... or equivalently (XOR R both sides): *. r* *D 2 = nG XOR R* 1 0 1r D*2 (here, r=3) 0 0 0 ... or equivalently (XOR R both sides): *. r* *D 2 = nG XOR R* 1 0 0 1 1 1 0 ... which says: 0 0 0 1 1 0 0. r if we divide D 2 by G, we 1 0 0 1 want remainder R to satisfy: 1 0 1 0 1 0 0 1 *r*

|R|= remainder|[D 2.|algorithm for||||0 1 1|
|---|---|---|---|---|---|---|---|
||G|computing R||||||

*]*

R

#### Error Correction

•**Forward Error Correction (FEC)**

- Send more redundant bits in the message
- Example: Hamming code, Reed-Solomon code
•**Automatic Repeat Request (ARQ)**

- Retransmission after timeout: The source retransmits a frame when an expected ACK fails to return within a predetermined time duration
- Retransmission when requested: The destination replies a negative ACK to inform the source about an error. The source then retransmits the corrupted frames accordingly.

#### ARQ Variants

- Stop-and-Wait ARQ
- Sliding Window-Go-back-N ARQ:
- Frames are accepted strictly in the sequence.
- Sliding Window-Selective-Reject ARQ:
- Sometimes called "Selective Repeat ARQ". Frames which arrive out of sequence (but are within the open window at the receiver) are accepted.

||Stop-and-Wait ARQ|
|---|---|
||the next frame. • Only one frame can be in transit. • Use only a (0 and 1) one-bit sequence number 29 [https://www.geeksforgeeks.org/computer-networks/stop-and-wait-arq/|](https://www.geeksforgeeks.org/computer-networks/stop-and-wait-arq/|)

#### Go-Back-N ARQ

- **Source**
- Maintains a sliding window of size **N**
- Can transmit **up to N** frames without waiting for individual ACKs
- When an ACK is received, the sender slides the window forward
- If a timeout occurs for a frame, the sender retransmits that frame and all subsequent frames in the current window.
- **Destination**
- Maintains a window size of **1**
- Accepts **only the next expected** frame in sequence.
- If the expected frame is received correctly, then the receiver sends an ACK, and updates the expected sequence number.
- If an out-of-order frame is received, receiver discards the frame and resends the ACK for the **last correctly received** frame.
[https://www.geeksforgeeks.org/computer-networks/sliding-window-protocols-summary-with-questions/](https://www.geeksforgeeks.org/computer-networks/sliding-window-protocols-summary-with-questions/)

#### Selective Reject ARQ

- Only rejected frames are retransmitted
- Receiver informs transmitter of rejected frame n by sending 'NAK n'
- After receiving an erroneous frame, subsequent frames are accepted and buffered by the receiver
- More efficient than Go-back- N but requires more complex buffer management at receiver

## Local Area Networks (LANs)

- A LAN is a computer network that interconnects computers within a limited area (e.g., residence, campus, or building)
- A few kilometers
- The organization usually owns and manages the links and switches/APs.
- LAN technologies specify the physical link and how frames share/access it.
- Two dominant types of LAN today:
- **switched Ethernet** and **IEEE 802.11 wireless LANs (WLANs)**.

||LAN Protocol Architecture||
|---|---|---|---|
|• • • • • •|committee two sublayers: Logical link control and medium access|Current LANs most likely to be based on Ethernet protocols developed by IEEE 802 divides the Data Link Layer into （ interface to the Network Layer Medium access control framing, addressing, error detection, The Physical Layer defines signaling, bit transmission, medium, and topology. Different PHY/MAC technologies can offer a similar service to the upper layers.|IEEE 802 LLC ）: common （ MAC ）:|

|||33|

## LAN Topologies

- Bus/Tree: all stations hear a transmission; collisions must be controlled.
- Ring: frames circulate through repeaters; access can be passed in order.
- Hub-based Star: physical star, but logically one shared collision domain.
- Switch-based Star: independent point-to-point links; the dominant
[https://en.wikipedia.org/wiki/Local_area_network](https://en.wikipedia.org/wiki/Local_area_network) design today.

## Two types of "links":

- Point-to-point
- Point-to-point link between Ethernet switch, host
- PPP for dial-up access
- Broadcast (shared wire or medium)
- Old-school Ethernet
- Upstream HFC in cable-based access network
- 802.11 wireless LAN, 4G/5G, satellite
shared wire (e.g., humans at a cocktail party shared radio: 4G/5G shared radio: WiFi shared radio: satellite cabled Ethernet) (shared air, acoustical)

# Medium Access Control Protocols

- single shared broadcast channel
- two or more simultaneous transmissions by nodes: interference
- *collision* if node receives two or more signals at the same time
##### MAC protocol

- distributed algorithm that determines how nodes share channel,
i.e., determine when node can transmit
- communication about channel sharing must use channel itself!
- no out-of-band channel for coordination

||Ideal MAC Protocols||
|---|---|---|---|
||given:|MAC of rate|R bps|
||desiderata:||1. when one node wants to transmit, it can send at rate R.|
||2. when|M|nodes want to transmit, each can send at average|
||rate|R/M 3. fully decentralized:|• no special node to coordinate transmissions • no synchronization of clocks, slots|
||4. simple|||

|||37|

## MAC Taxonomy

## Channelization MAC Protocol: TDMA

TDMA: time division multiple access

- access to channel in "rounds"
- each station gets fixed length slot (length = packet transmission time) in each round
- unused slots go idle

## Channelization MAC Protocol: FDMA

FDMA: frequency division multiple access

- channel spectrum divided into frequency bands
- each station assigned fixed frequency band
- unused transmission time in frequency bands go idle

## Random Access Protocols

- When node has packet to send
- Transmits at full channel data rate of R
- No a-priori coordination among nodes
- Two or more transmitting nodes
- Collision
- Random access protocol specifies:
- how to detect collisions
- how to recover from collisions (e.g., via delayed retransmissions)
- Examples of random access MAC protocols:
- ALOHA, slotted ALOHA
- CSMA, CSMA/CD, CSMA/CA

|Slotted ALOHA|||||
|---|---|---|---|---|
|||Operation:|||
|t₀ t₀ +1|||• when node obtains fresh||
|Assumptions:|||frame, transmits in next slot||
|• all frames same size|•|if no collision:||node can send|
|• time divided into equal size|||new frame in next slot||
|slots (time to transmit 1 frame)|•|if collision:||node retransmits|
|• nodes start to transmit only|||frame in each subsequent||
|slot beginning|||slot with probability|p until|
|• nodes are synchronized|||success|||
|• if 2 or more nodes transmit in|||||
|slot, all nodes detect collision|||randomization –|why|?|

||||||42|

|Slotted ALOHA||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|
|node 1|1||1|||1||1|||
|node 2|2||2|2||||||C: collision S: success|
|node 3|3|||||3|||3||
|Pros: • single active node can of channel nodes need to be in sync • simple|C continuously transmit at full rate • highly decentralized: only slots in|E|C|S|E|C|E Cons:|S • idle slots|S|E: empty • collisions, wasting slots • nodes may be able to detect collision in less than time to transmit packet • clock synchronization 43|

|•|Slotted ALOHA Efficiency many frames to send) Suppose: N probability p • prob that given node has success in a slot = • prob that any node has a success = • max efficiency: find p* • for many nodes, take limit of|Efficiency: long-run fraction of successful slots (many nodes, all with nodes with many frames to send, each transmits in slot with N-1 Np(1-p) that maximizes Np(1-p) N-1 Np*(1-p*) as|N-1 p(1-p) N-1 N goes to infinity, gives:|
|---|---|---|---|
|• at best:|max efficiency = 1/e = .37|channel used for useful transmissions 37% of time!|44|

|Pure ALOHA|• Unslotted Aloha: simpler, no synchronization • frame sent at t 0 will overlap with start of i's frame|• when frame first arrives: transmit immediately • Collision probability increases with no synchronization: will overlap with end of i's frame|collides with other frames sent in [t -1,t +1] 0 0|
|---|---|---|---|
||t₀ - 1 • Pure Aloha efficiency: 18% !|t₀|t₀ + 1 48|

## Carrier Sense Multiple Access (CSMA)

simple CSMA: listen before transmit:

- if channel sensed idle: transmit entire frame
- if channel sensed busy: defer transmission
CSMA/CD: CSMA with *collision detection*

- collisions *detected* within short time
- colliding transmissions aborted, reducing channel wastage
- collision detection easy in wired, difficult with wireless

## CSMA collisions

<u>spatial layout of nodes</u>

- collisions can *still* occur with carrier sensing:
- propagation delay means two nodes may not hear each other's just- started transmission
- collision: entire packet transmission time wasted
- distance & propagation delay play role in in determining collision probability

## CSMA/CD

<u>spatial layout of nodes</u>

- CSMA/CD reduces the amount of time wasted in collisions
- transmission aborted on collision detection

## Ethernet CSMA/CD algorithm

1. Ethernet receives datagram from network layer, creates frame
2. If Ethernet senses channel: if idle: start frame transmission. if busy: wait until channel idle, then transmit
3. If entire frame transmitted without collision-done!
4. If another transmission detected while sending: abort, send jam signal
5. After aborting, enter *binary (exponential) backoff:*
***m***

- after *m*th collision, chooses *K* at random from *{0,1,2, …, 2-1}*. Ethernet waits *K*·512 bit times, returns to Step 2
- more collisions: longer backoff interval

## Exercise

The CSMA/CD specification for a medium is given below:

(a) Maximum cable length per segment is 200 meters and the propagation delay is 1 msec per 100 meters.
(b) Maximum number of repeaters between any two segments (or say, between any two stations) of a LAN is 4. Delay through each repeater is 2 msec. Determine the minimum frame size required for correct operation of the CSMA/CD protocol if the network is run at 20 Mbps.

|• Question: • of the medium|How long does it take to detect a collision? Answer: In the worst case, twice the maximum propagation delay Note: a = maximum propagation delay|
|---|---|
||55|

A round trip signal propagation time + the processing time is the minimum transmission requirement for a frame transmission to ensure a proper detection of a collision.

200 m

We must consider the "worst" case.

Minimum frame size (tx. time) = 2 x end-to-end signal propagation time + processing time (negligible)

End-to-end signal propagation time = 5 x delay in segment + 4 x delay in each repeater

200 m

|Minimum frame size (tx. time) = 2 x end-to-end signal propagation time + processing time (negligible) End-to-end signal propagation time|36us 8us = 5 x delay in segment + 4 x delay in each repeater|
|---|---|
|2us 10us > Delay per segment = 200 / 100 = 2 us > Given that the delay in each repeater = 2 us|2us Given that signal prop. time is 1us for every 100m|

Minimum frame size (tx. time) = 36 us

at 20Mb/s, for a time period of 36 us, the number of bits can be transmitted is:

36us x 20Mb/s = 720 bits

channel partitioning MAC protocols:

- share channel efficiently at high load
- inefficient at low load
random access MAC protocols

- efficient at low load: single node can fully utilize channel
- high load: collision overhead
Controlled access protocols

- look for best of both worlds!

|Polling • centralized controller "invites" other nodes to transmit in turn||||
|---|---|---|---|
|• typically used with "dumb"||data||
||||poll|
|devices||||
|• concerns:|||centralized|
|• polling overhead||data|controller|
|• latency • single point of failure (master)|||||
|• Bluetooth uses polling|client devices|61|

||Token passing|||
|---|---|---|---|
||token passing: • control token message explicitly passed from one node to next, sequentially • transmit while holding token • concerns: • token overhead • latency • single point of failure (token)|(nothing to send) T|T data|

|||62|

## Summary of MAC protocols

- channel partitioning, by time, frequency or code
- Time Division, Frequency Division
- random access (dynamic),
- ALOHA, S-ALOHA, CSMA, CSMA/CD
- carrier sensing: easy in some technologies (wire), hard in others (wireless)
- CSMA/CD used in Ethernet
- CSMA/CA used in 802.11
- Controlled access
- polling from central site, token passing
- Bluetooth, FDDI, token ring

## MAC addresses

- MAC address:
- used "**locally**" to get frame from one interface to another physically- connected interface
- 48-bit MAC address (for most LANs)
- e.g.: 1A-2F-BB-76-09-AD
*hexadecimal (base 16) notation* *(each "numeral" represents 4 bits)*

## MAC addresses

each interface on LAN has unique 48-bit MAC address

1A-2F-BB-76-09-AD

LAN (wired or wireless) 71-65-F7-2B-08-53 58-23-D7-FA-20-B0

0C-C4-11 -6F-E3-98

||Ethernet "Dominant" wired LAN technology: • first widely used LAN technology • simpler, cheap|• kept up with speed race: 10 Mbps – 400 Gbps • single chip, multiple speeds (e.g., Broadcom BCM5761)|
|---|---|
||Bob Metcalfe: Ethernet co-inventor, 2022 ACM Turing Award recipient|
|Metcalfe's Ethernet sketch|66 [https://www.uspto.gov/learning-and-resources/journeys-innovation/audio-stories/defying-doubters|](https://www.uspto.gov/learning-and-resources/journeys-innovation/audio-stories/defying-doubters|)

## Ethernet physical topology

- bus: popular through mid 90s
- all nodes in same collision domain (can collide with each other)
- switched: prevails today
- active link-layer 2 *switch* in center
- each "spoke" runs a (separate) Ethernet protocol (nodes do not collide with each other)
bus: coaxial cable switched

||Ethernet frame structure protocol packet) in Ethernet frame|sending interface encapsulates IP datagram (or other network layer type|
|---|---|---|
||dest. preamble address|source CRC data (payload) address|
||preamble:|• used to synchronize receiver, sender clock rates • 7 bytes of 10101010 followed by one byte of 10101011 68|

||Ethernet frame structure|type|
|---|---|---|
||dest. preamble address|source CRC data (payload) address|
|• otherwise, adapter discards frame • type: indicates higher layer protocol • used to demultiplex up at receiver • error detected: frame is dropped|• addresses: 6 byte source, destination MAC addresses • if adapter receives frame with matching destination address, or with broadcast address (e.g., ARP packet), it passes data in frame to network layer protocol • mostly IP but others possible, e.g., Novell IPX, AppleTalk • CRC: cyclic redundancy check at receiver 69|

## Ethernet: unreliable, connectionless

- connectionless: no handshaking between sending and receiving network interface cards (NICs)
- unreliable: receiving NIC doesn't send ACKs or NAKs to sending NIC
- Ethernet's MAC protocol: CSMA/CD

|•|many|• common MAC protocol and frame format|802.3 Ethernet standards: link & physical layers different Ethernet standards • different physical layer media: fiber, cable|• different speeds: 2 Mbps, ... 100 Mbps, 1Gbps, 10 Gbps, 40 Gbps, 80 Gbps|||
|---|---|---|---|---|---|---|
||||application transport network link physical|1000BASE-T 1000BASE-CX copper (twister pair) physical layer|1000BASE-SX 1000BASE-LX|1000BASE-LX10 1000BASE-BX10 fiber physical layer|Gigabit PHY layer standards 71|

### Learning Objectives

- Explain Link-Layer Services
- Flow-Control Protocols
- Explain Stop-and-Wait and Sliding Window
- Calculate link utilization
- Error Control
- Explain parity and CRC
- MAC Protocols
- Compare ALOHA, CSMA, and CSMA/CD
- Ethernet
- Understand MAC addresses and frame format
- Explain Ethernet topology and operation

### Questions?
