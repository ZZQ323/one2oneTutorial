
============================================================
第 1 页
============================================================
1
EE5609 Computer Networks:
Architecture, Protocols, and Applications


============================================================
第 2 页
============================================================
2
Course Overview


============================================================
第 3 页
============================================================
3
EE3315 Internet Technology 
                                 
            Overview                           
Slide 3
Course Lecturer
Name:  
Prof. Qun SONG
Office:  
YEUNG-G6403
Office Hour: 
2pm – 3pm every Wed
Phone:  
3442-6309
Email:  
qunsong@cityu.edu.hk
URL: 
 
https://www.cityu.edu.hk/stfprofile/qunsong.htm
When you email, please include “EE5609” in the subject 
line and briefly state the question or topic.


============================================================
第 4 页
============================================================
Teaching Assistants
Name
Email
KE Ye
yeke22-c@my.cityu.edu.hk
LUO Chenxiang
chenxiluo8-c@my.cityu.edu.hk
MO Yingxue
yingxuemo2-c@my.cityu.edu.hk
ZHANG Zirui
zzhang3286-c@my.cityu.edu.hk


============================================================
第 5 页
============================================================
5
Syllabus
Computer Networks and the Internet
Network layers: OSI 7-Layer, Internet 5-Layer; physical layer resilience; packet and circuit switching 
Data Link Layer 
Flow control, error control; local area network: MAC, Ethernet, wireless LAN
Network Layer: IP Routing Protocols
IP addressing and fragmentation; IPv4; IPv6; IP routing principles and practices; intra-AS and inter-AS 
routing
Transportation Layer
UDP, TCP: connection management, flow control, error control, congestion control
Application Layer
DHCP, DNS, and HTTP protocols 
Advanced Topics in Networking
Internet of Things; cloud/edge/fog computing; Artificial Intelligence of Things 


============================================================
第 6 页
============================================================
6
Assessment
• Examination (50%) 
• Two Tests (25%)
• Paper presentation (15%)
• Individual Report (10%)
    
* To pass the course, at least 30% in Exam and at least 
30% in Course Work.


============================================================
第 7 页
============================================================
7
Timetable
• Lecture: Mondays (19:00 – 20:50) 
• Group presentations: Mondays (20:50 – 21:50), starting from Week 11
• Form a group of 5-6 students
• Each group selects a full-length* paper related to computer networks, Internet of 
    Things (IoT)/cyber-physical system (CPS), AI+IoT (AIoT), or relevant topics
• Each group delivers a 12-min presentation + 3-min Q & A
• Each group member submits an individual report
* Typically 10-12 pages, double-column for conference papers. Full-length journal articles are also eligible. 
* Short papers will not be accepted. 


============================================================
第 8 页
============================================================
• Select a recent paper on an advanced topic or emerging trend in 
computer networks, IoT/CPS, AIoT, or relevant areas.
• Your presentation should:
➢Clearly define the research problem and explain why it matters.
➢Explain the paper’s key ideas, methodology, and supporting evidence.
➢Critically evaluate its assumptions, strengths, and limitations.
➢Connect the work to concepts covered in this course.
➢Offer your own critical perspectives and propose possible improvements 
or future directions.
Paper Reading and Group Presentation
8


============================================================
第 9 页
============================================================
9
Recommended publication venues include, 
but are not limited to:
- ACM SIGCOMM: Annual Conference of ACM SIGCOMM
- USENIX NSDI: USENIX Symposium on Networked Systems Design and Implementation
- ACM MobiCom: International Conference on Mobile Computing and Networking 
- ACM MobiSys: International Conference On Mobile Systems, Applications And Services
- ACM SenSys: ACM/IEEE International Conference on Embedded Artificial Intelligence and Sensing Systems
- ACM/IEEE ICCPS: International Conference on Cyber-Physical Systems
- IEEE TMC: IEEE Transactions on Mobile Computing
- ACM/IEEE TON: IEEE/ACM Transactions on Networking
- IEEE TPDS: IEEE Transactions on Parallel and Distributed Systems
- ACM TCPS: ACM Transactions on Cyber-Physical Systems
- ACM TIOT: ACM Transactions on Internet of Things
- ……


============================================================
第 10 页
============================================================
10
Individual Report
• Your report should include:
➢A concise summary of the research problem, approach, and key findings
➢An assessment of the paper’s strengths
➢An assessment of its weaknesses and limitations
➢Detailed comments on its methodology, evaluation, and presentation
➢Your own critical perspectives, proposed improvements, and future 
research directions


============================================================
第 11 页
============================================================
11
Textbook
Kurose and Ross: Computer Networking: A Top-Down Approach, 8th Edition 
(Pearson, 2020)
Additional: 
Douglas E. Comer, Computer Networks and Internets
Recent Advances in Networking, The ACM SIGCOMM ebook
Leon-Garcia and Widjaja: Communication Networks, 2nd Edition, 
(McGraw-Hill, 2003)
Tanenbaum A S: Computer Networks, (4th Edition, Prentice-Hall, 2002)


============================================================
第 12 页
============================================================
12
Schedule for EE5609
Lecture
Presentation 
Test
Week1
Week2
Week3
Week4
Week5
Week6, paper
Test 1
Week7
Week8
No class due to PH
Week9
Week10, report
Test 2
Week11
Week12
Week13
Week14
Paper and group member submission: Week 6 (Friday 11:59 pm)  
Individual report submission deadline: Week 10 (Friday 11:59 pm)  
Class Schedule 


============================================================
第 13 页
============================================================
13
Q & A


============================================================
第 14 页
============================================================
14
L1: Network layer & physical resilience


============================================================
第 15 页
============================================================
15
Outline
•
What the Internet connects
•
Devices, links, networks, and protocols
•
Why networks use layers
•
Encapsulation across hosts, switches, and routers
•
Physical resilience and network availability


============================================================
第 16 页
============================================================
Computer networks now connect:
Computer networks are everywhere
16
•  People and organizations
•  Clouds, edges, and data centers
•  Vehicles, sensors, robots, and infrastructure
•  AI services, agents, and machines
Networking has become the hidden operating system of modern society.


============================================================
第 17 页
============================================================
17
A Brief History of the Internet


============================================================
第 18 页
============================================================
18
Motivations for Layered Network Architecture
Networks are complex with many “pieces”:
▪Hosts, routers, links of various media, applications, protocols, hardware, 
software
Dealing with complex systems:
▪explicit structure allows identification, relationship of system’s pieces
• layered reference model for discussion
▪modularization eases maintenance, updating of system
• change in layer's service implementation: transparent to rest of 
system
• e.g., change in gate procedure doesn’t affect rest of system


============================================================
第 19 页
============================================================
19
Internet
mobile network
home network
enterprise
          network
national or global ISP
local or 
regional ISP
datacenter 
network
content 
provider 
network
Packet switches: forward 
packets (chunks of data)
▪routers, switches
Communication links
▪fiber, copper, radio, satellite
▪transmission rate: bandwidth
Billions of connected 
computing devices: 
▪hosts = end systems 
▪running network apps at 
Internet’s “edge”
Networks
▪collection of devices, routers, 
links: managed by an organization
Inside the Internet


============================================================
第 20 页
============================================================
20
• Internet: “network of networks”
• Interconnected ISPs
mobile network
home network
enterprise
          network
national or global ISP
local or 
regional ISP
datacenter 
network
content 
provider 
network
▪protocols are everywhere
• control sending, receiving of 
messages
• e.g., HTTP (Web), streaming video, 
Zoom, TCP, IP, WiFi, 4/5G, Ethernet
Ethernet
HTTP
Skype
IP
WiFi
4G
TCP
Streaming
video
▪Internet  standards
• RFC: Request for Comments
• IETF: Internet Engineering Task 
Force
Inside the Internet


============================================================
第 21 页
============================================================
21
Network protocols:
▪a set of rules governing communication 
between two peering parties/computers
▪all communication activity in Internet 
governed by protocols
Protocols define the format, order of 
messages sent and received among 
network entities, and actions taken on 
message transmission, receipt 
What is a protocol?
time
TCP connection
response
<file>
TCP connection
request
GET http://gaia.cs.umass.edu/kurose_ross


============================================================
第 22 页
============================================================
22
Layered Network Architecture
▪Network organized as a stack of layers
▪Purpose of layer is to offer services to the layer above it and passes 
data & control information to the layer below, using a well-defined 
interface 
▪Reducing design complexity
▪Network Architecture: 
▪A set of layers and protocols with specifications enabling 
hardware/software developers to build systems compliant with a 
particular architecture


============================================================
第 23 页
============================================================
23
Benefits of Layers
▪Simplicity
• Easy to design once layers and their interactions are defined 
clearly
▪Flexibility
• Easy to modify and develop networks by separate layers 
modifications
▪Incremental Changes
• Easy to add news layers, add new functions to a layer


============================================================
第 24 页
============================================================
24
Layered Internet protocol stack
▪application: supporting network applications
• HTTP, IMAP, SMTP, DNS
▪transport: process-process data transfer
• TCP, UDP
▪network: routing of datagrams from source to 
destination
• IP, routing protocols
▪link: data transfer between neighboring  
network elements
• Ethernet, 802.11 (WiFi), PPP
▪physical: bits “on the wire”
link
application
network
transport
physical
application
transport
network
link
physical


============================================================
第 25 页
============================================================
25
Services, Layering and Encapsulation
source
▪transport-layer protocol encapsulates 
application-layer message, M, with 
transport layer-layer header Ht to create a 
transport-layer segment
• Ht used by transport layer protocol to 
implement its service
application
transport
network
link
physical
destination
application
transport
network
link
physical
Transport-layer protocol transfers M (e.g., reliably) from 
one process to another, using services of network layer
Ht
M
Application exchanges messages to implement some 
application service using services of transport layer
M


============================================================
第 26 页
============================================================
26
source
Transport-layer protocol transfers M (e.g., reliably) from 
one process to another, using services of network layer
Ht
M
▪network-layer protocol encapsulates 
transport-layer segment  [Ht | M] with 
network layer-layer header Hn to create a 
network-layer datagram 
• Hn used by network layer protocol to 
implement its service
application
transport
network
link
physical
destination
M
application
transport
network
link
physical
M
Ht
Hn
Network-layer protocol transfers transport-layer segment 
[Ht | M] from one host to another, using link layer services
Services, Layering and Encapsulation


============================================================
第 27 页
============================================================
27
source
Ht
M
▪link-layer protocol encapsulates network 
datagram [Hn| [Ht |M], with link-layer header 
Hl to create a link-layer frame 
application
transport
network
link
physical
destination
M
application
transport
network
link
physical
M
Ht
Hn
Link-layer protocol transfers datagram [Hn| [Ht |M] from 
host to neighboring host, using network-layer services
M
Ht
Hn
Hl
Network-layer protocol transfers transport-layer segment 
[Ht | M] from one host to another, using link layer services
Services, Layering and Encapsulation


============================================================
第 28 页
============================================================
28
source
application
transport
network
link
physical
destination
application
transport
network
link
physical
M
Ht
Hn
Hl
M
Ht
Hn
Ht
M
M
M
message
Ht
M
segment
M
Ht
Hn
datagram
frame
M
Ht
Hn
Hl
Services, Layering and Encapsulation


============================================================
第 29 页
============================================================
29
network
link
physical
application
transport
network
link
physical
application
transport
network
link
physical
source
Ht
Hn
M
segment
Ht
datagram
destination
Ht
Hn
Hl
M
Ht
Hn
M
Ht
M
M
Ht
Hn
Hl
M
Ht
Hn
M
Ht
Hn
M
Ht
Hn
Hl
M
router
switch
message
M
Ht
M
Hn
frame
link
physical


============================================================
第 30 页
============================================================
30
Two layers not found in  Internet 
protocol stack!
▪presentation: allow applications to 
interpret meaning of data, e.g., encryption, 
compression, machine-specific conventions
▪session: synchronization, checkpointing, 
recovery of data exchange
▪Internet stack “missing” these layers!
• these services, if needed, must be 
implemented in application
• needed?
application
presentation
session
transport
network
link
physical
The seven layer OSI/ISO 
reference model
ISO/OSI reference model


============================================================
第 31 页
============================================================
OSI Model breaks encapsulation into 7 layers
https://www.networkacademy.io/ccna/network-fundamentals/understanding-the-osi-model


============================================================
第 32 页
============================================================
32
OSI vs. TCP/IP Models
https://www.networkacademy.io/ccna/network-fundamentals/understanding-the-osi-model


============================================================
第 33 页
============================================================
Layer
Name
Function
7
Application
Allows applications to request network services.
6
Presentation
Converts data so that systems that use different data 
formats can exchange information.
5
Session
Establishes sessions between network applications.
4
Transport
Provides for reliable delivery of packets.
3
Network
Handles routing of data across network segments.
2
Data Link
Provides MAC addresses to uniquely identify 
network nodes and a means for data to be sent over 
the Physical layer in the form of frames. Bridges and 
switches are layer 2 devices.
1
Physical
Governs the layout of cables (media) and devices 
such as repeaters and hubs.
OSI 7-Layer Model


============================================================
第 34 页
============================================================
Layer
Name
Function
5
Application
Acts as final endpoints at either end of a 
communication session between two network hosts
4
Transport
Manages the flow of traffic between two hosts or 
devices, ensuring that data arrives at the application 
on the host for which it is targeted
3
Internet 
(Network)
Contains all functionality that manages the 
movement of data between two network devices 
over a routed network
2
Link and Media 
Access
Deals with the network connectivity among 
neighboring devices.
1
Physical
Handles physical media and devices
Internet TCP/IP Model


============================================================
第 35 页
============================================================
35
Network Reliability
▪Probability that a network performs satisfactorily over a 
period of time
▪Parameters
• Mean Time Between Failures (MTBF)
• Mean Time to Failure (MTTF)
• Mean Time to Repair (MTTR)


============================================================
第 36 页
============================================================
36
Link Failure Probability
▪Link Failure Probability: percentage of time during which the 
link is dysfunctional
▪Link Availability: percentage of time during which the link is 
functional
*https://mimosa.co/blog/link-availability


============================================================
第 37 页
============================================================
37
Network Resilience Issues
▪What’s the probability of a link failure?
▪Are there alternative paths?
▪Is there a single point of failure?
▪What is the probability for two nodes to stay connected in 
a network?


============================================================
第 38 页
============================================================
38
Network Resilience
▪A measure of Network Fault Tolerance
▪Express in terms of probability that the network remain 
connected.
▪Assumptions
• The probabilities of link breaks are independent of each other.


============================================================
第 39 页
============================================================
39
Network Availability: Single Link
HK
SG
Given that the probability of a break is 0.05,
Link Break: bHK-SG = 0.05
Link Avail: rHK-SG = 1-0.05 = 0.95
• ri : Probability link “i” is available
• bi : Probability link “i” is broken
• ri = 1 - bi


============================================================
第 40 页
============================================================
40
Network Availability: Series
HK
SG
AU
Given that the probability of a break is 0.05, Prob that HK cannot 
communicate with AU
rHK-AU =Pr [both links survive] = rHK-SG * rSG-AU = (1-0.05)*(1-0.05) =0.9025
bP(HK-SG-AU) = 1-0.9025 = 0.0975


============================================================
第 41 页
============================================================
41
Network Availability: Parallel
HK
SG
Given that the probability of a break is 0.05,
What is the probability that HK is isolated from SG ?
Prob(break) = Pr[both links break]
= bA * bB
= 0.05 * 0.05 = 0.0025
Link A
Link B
bP(HK-SG) = 0.0025


============================================================
第 42 页
============================================================
42
Hybrid Graphs: Path-Based Approach
HK
SG
AU
Given that the probability of a break is 0.05, Calculate the Prob that HK is isolated 
from AU.
rP(HK-SG-AU) = rHK-SG * rSG-AU
= (1-0.05)*(1-0.05)
= 0.9025
bP(HK-SG-AU) = 1- rP(HK-SG-AU)
= 1-0.9025
= 0.0975
Prob. HK Disconnected from AU = bP(HK-SG-AU) * bP(HK-AU)
= 0.0975 * 0.05
= 0.004875


============================================================
第 43 页
============================================================
43
Rules for Network Availability
▪Link in series
• Calculate that probability that all links in the series are working
▪Link in parallel
• Calculate the probability that all links are broken.
▪Combination of series and parallel
• Decompose them into paths
• Calculate network availability using path-based approach


============================================================
第 44 页
============================================================
44
Exercise: 6-9’s Reliability
In network resilience, the link failure probability can be interpreted as the 
percentage of the time that the link goes down during a time window. In a 
carrier-grade network, it is often required that the network should have 6 
9’s (i.e, 99.9999%) reliability. Please calculate the duration of allowable 
downtime per year for this network? 
(hint: using the definition of failure probability)


============================================================
第 45 页
============================================================
45
• In this case, r = 99.9999%
• b=1-r = 10-6
• Failure probability = percentage of link downtime
• Assume a regular year (365 days)
• The allowable downtime per year is
    T = 365D × 24H/D × 60M/H × 60 S/M × 10-6
       = 31.5 seconds


============================================================
第 46 页
============================================================
46
Exercise: Network Resilience
Hong Kong (HK) is connected to Australia (AU), via an 
intermediate node at Singapore (SG). Two independent links 
connect between Hong Kong and Singapore, and a long-range 
link connects between Hong Kong and Australia. Assume that 
each link fails independently with probability of 0.05. Calculate 
the probability in which HK is disconnected from AU. 
HK
SG
AU


============================================================
第 47 页
============================================================
47
HK
SG
AU
Step 1: Calculate the resilience between HK and SG
bHK-SG = Pr[both upper and lower links fail]
            = 0.05 × 0.05 = 0.0025
Step 2: Calculate the resilience between HK and AU 
thru indirect link
rHK-SG-AU = Pr[both HK-SG and SG-AU survive]
            = (1-0.0025) × (1-0.05) = 0.947625


============================================================
第 48 页
============================================================
48
HK
SG
AU
Step 4: Calculate the failure between HK and AU
bSG-SF = Pr[both direct and indirect paths fail]
            = 0.05 × 0.052375 = 0.00261875
Step 3: Calculate the failure between HK and AU 
thru indirect link
bHK-SG-AU = 1- rHK-SG-AU =1- 0.947625 = 0.052375


============================================================
第 49 页
============================================================
49
Learning Objectives
▪Layered Network Architecture
•
Why layering
•
TCP/IP model and its functions
•
OSI model and its functions
•
Mapping between OSI and TCP/IP Models
▪Physical Layer Resilience
•
Definition of link availability and calculation
•
Path-based approach


============================================================
第 50 页
============================================================
50
Questions?
