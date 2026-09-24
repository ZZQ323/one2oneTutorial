![](_page_0_Figure_0.jpeg)

**EE5609 Computer Networks: Architecture, Protocols, and Applications**

![](_page_1_Picture_0.jpeg)

L3: WLAN

## **Outline**

![](_page_2_Picture_1.jpeg)

### ▪ **WLAN Overview**

- WLAN Standard
- WLAN Architecture
- WLAN Protocol Stack
- **802.11 Physical Layer**
- **802.11 MAC Layer**
  - Hidden Terminal Problem
  - CSMA/CA Protocol
  - MAC Management

# **LAN and WLAN**

![](_page_3_Picture_1.jpeg)

▪ LANs provide connectivity for interconnecting computing resources at **local levels** of an organization

### ▪ **Wired LANs**

• Limitations because of physical, hard-wired infrastructure

### ▪ **Wireless LANs**

- Flexibility
- Portability
- Mobility
- Ease of Installation

# **IEEE 802.11 WLAN Standard**

![](_page_4_Picture_1.jpeg)

- Part of the IEEE 802 set of LAN technical standards
- Scope limited to Data Link and Physical Layers
- Specifies the set of MAC and PHY protocols for implementing WLAN
- Provides basis for wireless network products using the Wi-Fi brand

| Gen. <sup>[3][4]</sup>              | IEEE<br>standard | Adopt.      | Link rate<br>(Mbit/s) | RF (GHz) |   |   |
|-------------------------------------|------------------|-------------|-----------------------|----------|---|---|
|                                     |                  |             |                       | 2.4      | 5 | 6 |
|                                     | 802.11           | 1997        | 1–2                   | ✓        |   |   |
|                                     | 802.11b          | 1999        | 1–11                  | 1        |   |   |
|                                     | 802.11a          | 1333        | 6–54                  |          | ✓ |   |
|                                     | 802.11g          | 2003        |                       | ✓        |   |   |
| Wi-Fi 4                             | 802.11n          | 2009        | 6.5–600               | ✓        | ✓ |   |
| Wi-Fi 5                             | 802.11ac         | 2013        | 6.5–6,933             | [b]      | ✓ |   |
| Wi-Fi 6                             | 802.11ax         | 2021        | 0.4–9,608             | ✓        | ✓ |   |
| Wi-Fi 6E                            |                  |             |                       | ✓        | ✓ | ✓ |
| Wi-Fi 7                             | 802.11be         | 2024<br>TBA | 0.4-23,059            | ✓        | ✓ | ✓ |
| <b>Wi-Fi 8</b> <sup>[5][6][7]</sup> | 802.11bn         |             |                       | 1        | 1 | 1 |

# **Comparison of Wireless Technologies**

![](_page_5_Picture_1.jpeg)

![](_page_5_Figure_2.jpeg)

# **WLAN Characteristics**

![](_page_6_Picture_1.jpeg)

#### ▪ **Advantages**

- Flexible deployment
- Minimal wiring difficulties
- More robust against disasters (earthquakes, etc)
- Historic buildings, conferences, trade shows,…

#### ▪ **Disadvantages**

- Low bandwidth compared to wired networks
- Need to follow wireless spectrum
- regulations

# **WLAN Characteristics**

- Decreased signal strength: radio signal attenuates as it propagates through air (path loss)
- Interference from other sources: standardized wireless network frequencies (e.g., 2.4 GHz) shared by other devices (e.g., phone)
- Multipath propagation: radio signal reflects off objects ground, arriving at destination at slightly different times

![](_page_7_Picture_5.jpeg)

# **WLAN Architecture**

![](_page_8_Picture_1.jpeg)

#### ▪ **Building Modules**

- Station (STA)
  - Mobile node
  - Smartphone, pad, laptop
- Access Point (AP)
  - Stations are connected to access points

#### ▪ **Architectural Modes**

- Infrastructure: centralized
- Ad Hoc: distributed

![](_page_8_Picture_11.jpeg)

![](_page_8_Picture_12.jpeg)

![](_page_8_Figure_13.jpeg)

# **WLAN Architecture – Service Set**

![](_page_9_Picture_1.jpeg)

#### ▪ **Basic Service Set (BSS)**

• Stations and the AP within the same radio coverage form a BSS.

#### ▪ **Extended Service Set (ESS)**

• Several BSSs connected through APs form an ESS.

![](_page_9_Figure_6.jpeg)

# **802.11 Protocol Stack**

![](_page_10_Picture_1.jpeg)

![](_page_10_Figure_2.jpeg)

![](_page_11_Picture_0.jpeg)

### **Wireless Physical Layer**

# **Wireless Radio Spectrum**

![](_page_12_Picture_1.jpeg)

- Radio spectrum: national asset, owned by the nation
- National government determine how spectrum is used "locally"
- Radio frequency bands are allocated to different applications
  - The use of most frequency bands needs licenses
  - IEEE 802.11 commonly uses the 2.4GHz, 5GHz, and 6 GHz (used in newer generations of the standard). Users generally do not need an individual licence, but devices and operation must comply with local regulations.

![](_page_13_Figure_2.jpeg)

![](_page_13_Figure_3.jpeg)

![](_page_13_Picture_4.jpeg)

802.11 2.4GHz & 5GHz & 6GHz

# **WiFi Spectrum Bands**

![](_page_14_Picture_1.jpeg)

#### **6** GHz range

- most recently added
- more than 250 configurable/selectable WiFi channels of different transmission rates

![](_page_14_Figure_5.jpeg)

#### **5** GHz range

▪ more than 150(configurable/selectable WiFi channels) of different transmission rates

![](_page_14_Figure_8.jpeg)

#### **2.4** GHz

▪ Divided into 11-14 channels, depending on country 802.11

![](_page_14_Picture_11.jpeg)

▪ other 802.11 WiFi spectrum bands, but not in widespread use

# **Evolution of 802.11 Standard**

![](_page_15_Picture_1.jpeg)

| IEEE Standard                                   | Generation | Year  | Representative Use Cases                                                                     | Key Features                                                                                                           | Peak Rate |
|-------------------------------------------------|------------|-------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|-----------|
| 802.11b                                         | _          | 1999  | Basic broadband: email, browsing, file sharing (home/small office)                           | 2.4 GHz, DSSS                                                                                                          | 11 Mb/s   |
| 802.11a                                         | _          | 1999  | Faster enterprise connections, early media streaming                                         | 5 GHz, OFDM                                                                                                            | 54 Mb/s   |
| 802.11g                                         | _          | 2003  | Home media, consumer electronics integration                                                 | 2.4 GHz, OFDM, backward compatible with 802.11b                                                                        | 54 Mb/s   |
| 802.11n High<br>Throughput (HT)                 | Wi-Fi 4    | 2009  | HD video, cloud access, multi-<br>device homes                                               | Up to 40 MHz channels, packet aggregation, MIMO (up to 4×4)                                                            | 600 Mb/s  |
| 802.11ac Very High<br>Throughput (VHT)          | Wi-Fi 5    | 2013  | 4K video, online gaming, mobile offload, enterprise WLANs                                    | Up to 160 MHz channels, DL MU-MIMO (up to 4×4), 256-QAM                                                                | 6.9 Gb/s  |
| 802.11ax High-<br>Efficiency (HE)               | Wi-Fi 6/6E | 2021  | Dense deployments (stadiums, campuses), IoT, teleconferencing                                | DL/UL OFDMA and MU-MIMO (up to 8×8), 1024-QAM, spatial reuse, TWT, 6 GHz band                                          | 9.6 Gb/s  |
| 802.11be Extremely-<br>High Throughput<br>(EHT) | Wi-Fi 7    | 2024  | 8K video, real-time collaboration, cloud gaming, AR/VR, IIoT pilot                           | Up to 320 MHz channels, 4096-QAM, MLO, multi-RU, enhanced QoS                                                          | 23 Gb/s   |
| 802.11bn Ultra-High<br>Reliability (UHR)        | Wi-Fi 8    | 2028+ | Robotic surgery prep, industrial automation, holography, ultra-reliable closed control loops | ELR PPDU, distributed-RU, LDPC enhancements, unequal modulation, seamless roaming, dynamic power save, NPCA, DSO, MAPC | 23 Gb/s   |

![](_page_16_Picture_0.jpeg)

### **802.11 MAC**

# **802.11 MAC Sublayer**

![](_page_17_Picture_1.jpeg)

- New challenges caused by the nature of wireless communications
  - Broadcast
  - Signal attenuation
  - Pervasive electromagnetic noise
- Three functional areas
  - Access control (random access vs controlled access)
  - Reliable data delivery (against noises and collisions)
  - Security (authentication, packet injection, …)
- Additional problem:
  - Hidden Terminal Problem

# **Access Control**

![](_page_18_Picture_1.jpeg)

- **Distributed Coordination Function (DCF)**
  - Distributed access protocol
  - Contention-based
  - Makes use of CSMA/CA
  - Suited for ad-hoc network and asynchronous traffic
- **Point Coordination Function (PCF)**
  - Alternative access method on top of DCF
  - Centralized access protocol
  - Contention-free, and works like polling
  - Suited for time-bound services like voice and multimedia

# **Reliable Data Delivery**

![](_page_19_Picture_1.jpeg)

- Loss of frames due to noise, interference and propagation effects
- Frame exchange protocol
  - Sender broadcasts data
  - Receiver responds with acknowledgement (ACK)
  - If sender does not receive ACK, it retransmits frame
- Four frame exchange for enhanced reliability
  - Sender issues request-to-send (RTS)
  - Receiver responds with clear-to-send (CTS)
  - Sender transmits data
  - Receiver responds with ACK

#### **802.11 Multi -Access**

- Collision
  - A receiver hears transmissions from 2+ nodes at the same time
- 802.11: CSMA - sense before transmitting
  - Don't collide with ongoing transmission by other node
- 802.11: no collision detection!
  - Difficult to receive (sense collisions) when transmitting due to weak received signals (fading)
  - Can't sense all carriers & collisions in any case: hidden terminal problem
- 802.11: avoid collisions
  - CSMA/C(ollision)A(voidance)

![](_page_20_Picture_10.jpeg)

![](_page_20_Picture_11.jpeg)

![](_page_20_Picture_12.jpeg)

![](_page_20_Picture_13.jpeg)

# **Hidden Terminal Problem**

![](_page_21_Picture_1.jpeg)

#### Path loss causes "hidden terminals"

![](_page_21_Figure_3.jpeg)

- B, A hear each other
- B, C hear each other
- A, C can not hear each other interfering at B

#### Objects cause "hidden terminals"

![](_page_21_Picture_8.jpeg)

- B, A hear each other
- B, C hear each other
- A, C can not hear each other means A, C unaware of their interference at B

## **CSMA/CA: addressing the "hidden terminals" problem**

![](_page_22_Picture_1.jpeg)

#### Path loss causes "hidden terminals"

![](_page_22_Figure_3.jpeg)

- B, A hear each other
- B, C hear each other
- A, C can not hear each other interfering at B

#### Objects cause "hidden terminals"

![](_page_22_Picture_8.jpeg)

- B, A hear each other
- B, C hear each other
- A, C can not hear each other means A, C unaware of their interference at B

**CSMA/CA: collisions happen**

![](_page_23_Picture_1.jpeg)

![](_page_23_Figure_2.jpeg)

![](_page_23_Figure_3.jpeg)

# **IEEE 802.11 MAC Protocol: CSMA/CA**

![](_page_24_Picture_1.jpeg)

#### 802.11 sender

1 if sense channel idle for **DIFS** then transmit *entire* frame (no collision detection)

2 if sense channel busy then start random backoff time timer counts down while channel idle transmit when timer expires

3. if no ACK, increase random backoff interval, repeat 2 (see next slide)

#### 802.11 receiver

if frame received OK return ACK after **SIFS** (ACK needed due to hidden terminal problem)

![](_page_24_Picture_8.jpeg)

### CSMA/CA: randomization after collision

![](_page_25_Picture_1.jpeg)

![](_page_25_Figure_2.jpeg)

# **Collision Avoidance**

![](_page_26_Picture_1.jpeg)

idea: sender "reserves" channel use for data frames using small reservation packets

- sender first transmits *small* request-to-send (RTS) packet to BS using CSMA
  - RTSs may still collide with each other (but they're short)
  - contains duration for following data transmission
- BS broadcasts clear-to-send (CTS) packet in response to RTS
  - contains duration for following data transmission
- RTS and/or CTS heard by all nodes
  - All nodes except transmitter defer transmissions
  - transmits data frame

## **Collision Avoidance: RTS-CTS Exchange**

![](_page_27_Picture_1.jpeg)

![](_page_27_Figure_2.jpeg)

### 802.11 frame: addressing

![](_page_28_Picture_1.jpeg)

![](_page_28_Figure_2.jpeg)

Address 1: MAC address of wireless host or AP to receive this frame

Address 2: MAC address of wireless host or AP transmitting this frame

Address 4: used only in ad hoc mode

Address 3: MAC address of router interface to which AP is attached

## **802.11 frame: addressing**

![](_page_29_Picture_1.jpeg)

![](_page_29_Figure_2.jpeg)

*802.11 WiFi frame*

#### 802.11 frame

![](_page_30_Picture_1.jpeg)

![](_page_30_Figure_2.jpeg)

## **802.11 Advanced Capabilities**

![](_page_31_Picture_1.jpeg)

- Synchronization
  - finding and staying with a WLAN
  - synchronization functions
- Power Management
  - sleeping without missing any messages
  - power management functions
- Roaming
  - functions for joining a network
  - changing access points
  - scanning for access points
- Management information base

## **Learning Objectives**

![](_page_32_Picture_1.jpeg)

- Describe WLAN architecture
  - Stations, APs, BSSs and ESSs
- Explain wireless-channel challenges
  - Path loss, interference, multipath, and hidden terminals
- Understand CSMA/CA protocol

## **Questions?**

![](_page_33_Picture_1.jpeg)