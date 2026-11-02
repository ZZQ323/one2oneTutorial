# EE5609 Computer Networks - Lecture 7

## The Application Layer

### Learning Objectives

- Explain how a device gets its IP settings (DHCP).
- Explain how DNS finds a website's IP address.
- Explain how a browser requests and receives a Web page (HTTP).
- Explain how newer HTTP versions, caches, and CDNs reduce waiting time.

---

## 1. Dynamic Host Configuration Protocol (DHCP)

### Overview

- Application-layer protocol: to automatically configure host with IP address, default gateway, DNS, etc (echo Lecture 4)
- DHCP protocol is designed to run over UDP with server listening at well-known port 67.
- Client is required to run at well-known port 68.

### DHCP Protocol (DORA)

1. **DHCP Discover** – client requesting for DHCP server
2. **DHCP Offer** – server responding to client's request
3. **DHCP Request** – client accepting server's offer
4. **DHCP Acknowledge** – server confirming the offer

### DHCP Discover

- UDP source port 68; destination port 67
- Source IP: `0.0.0.0`; destination IP: `255.255.255.255` (IP broadcast)

### DHCP Offer

- DHCP servers send DHCP Offer via:
  - IP unicast using offered IP as destination address (possible since client's physical address is known); or
  - IP broadcast to destination address `255.255.255.255`
- The client receives the response on UDP port 68.

### DHCP Request

- Client selects one offer and sends DHCP Request which includes the selected server identifier.
- DHCP Request is sent to destination address `255.255.255.255` (IP broadcast) so that other DHCP servers will also receive it and know that their offers are being declined.
- Client still uses source IP `0.0.0.0` since the offer is not confirmed yet.

### DHCP Acknowledge

- Similar as DHCP Offer, DHCP Ack is sent via IP unicast or broadcast based on the DHCP message broadcast flag.
- Once DHCP Ack is received, the client can start using the offered IP address within the duration of the lease time.

### DHCP Release

- To extend the lease, the process of DHCP Request/Ack is repeated.
- To end the lease, the client sends DHCP Release via unicast to the server.

### DHCP Relay Across Subnets

- DHCP relay agent forwards DHCP messages between subnets.

### DHCP Message Fields

- Reference: https://www.geeksforgeeks.org/computer-networks/dynamic-host-configuration-protocol-dhcp/

---

## 2. Domain Name System (DNS)

### Overview

- DNS – to resolve domain name to IP address
- Designed to run over UDP or TCP with server listening at well-known port 53.
- Video: https://www.youtube.com/watch?v=72snZctFFtA

### DNS Hierarchy

Client wants IP address for `www.amazon.com`; 1st approximation:
- client queries root server to find .com DNS server
- client queries .com DNS server to get amazon.com DNS server
- client queries amazon.com DNS server to get IP address for `www.amazon.com`

| Level | Examples |
|-------|----------|
| Root DNS Servers | Root |
| Top Level Domain | .com DNS servers, .org DNS servers, .edu DNS servers |
| Authoritative | nyu.edu DNS servers, umass.edu DNS servers, yahoo.com DNS servers, amazon.com DNS servers, pbs.org DNS servers |

### Domain Names Are Hierarchical

- Domain names are managed hierarchically (e.g., UofT → ECE of UofT)

### DNS Root Name Servers

- 13 logical root name "servers" worldwide
- Official, contact-of-last-resort by name servers that can not resolve name
- ICANN (Internet Corporation for Assigned Names and Numbers) manages root DNS domain

### Top-Level Domain and Authoritative Servers

**Top-Level Domain (TLD) servers:**
- Responsible for .com, .org, .net, .edu, .aero, .jobs, .museums, and all top-level country domains, e.g.: .cn, .uk, .fr, .ca, .jp
- Network Solutions: authoritative registry for .com, .net TLD
- Educause: .edu TLD

**Authoritative DNS servers:**
- Organization's own DNS server(s), providing authoritative hostname to IP mappings for organization's named hosts
- Can be maintained by organization or service provider

### Local DNS Name Servers

- When host makes DNS query, it is sent to its local DNS server
- Local DNS server returns reply, answering:
  - From its local cache of recent name-to-address translation pairs (possibly out of date!)
  - Forwarding request into DNS hierarchy for resolution
- Each ISP has local DNS name server; to find yours:
  - MacOS: `% scutil --dns`
  - Windows: `> ipconfig /all`

### DNS Resolution: Iterative Queries

Example: host at `engineering.nyu.edu` wants IP address for `gaia.cs.umass.edu`

Iterated query: contacted server replies with name of server to contact

```
requesting host → local DNS server (dns.nyu.edu) → root DNS server → TLD DNS server → authoritative DNS server (dns.cs.umass.edu)
```

### DNS Resolution: Recursive Queries

Example: host at `engineering.nyu.edu` wants IP address for `gaia.cs.umass.edu`

Recursive query: puts burden of name resolution on contacted name server

### DNS Resource Records

In DNS, data are stored as Resource Records (RRs). All RRs have the same format:

- **TTL**: specifies the time interval in seconds that the RR can be cached at the client

### DNS Message Header

DNS query and reply messages, both have same format:

| Field | Size | Description |
|-------|------|-------------|
| Identification | 2 bytes | 16-bit # for query; reply to query uses same # |
| Flags | 2 bytes | query or reply, recursion desired, recursion available, reply is authoritative |
| # Questions | variable | |
| # Answer RRs | variable | answers (variable # of RRs) |
| # Authority RRs | variable | authority (variable # of RRs) |
| # Additional RRs | variable | additional "helpful" info that may be used |

---

## 3. WWW and HTTP

### Overview

- World Wide Web (WWW) is simply a network application that allows a client to access a file from a server.
- Hyper Text Transfer Protocol (HTTP) is the application layer protocol used by WWW. It is designed to run over TCP with server listening at well-known port 80.
- Basically, HTTP consists of request/response messages.

### HTTP Client/Server Model

- **Application-layer protocol**
- **Client/server model:**
  - Client: browser that requests, receives, (using HTTP protocol) and "displays" Web objects
  - Server: Web server sends (using HTTP protocol) objects in response to requests

### Non-persistent HTTP

- Individual TCP connection/termination for each pair of request/response to access one file – inefficient

### Persistent HTTP (HTTP/1.1)

- Multiple request/response messages within one TCP connection – efficient for accessing multiple files in the same server

### HTTP Methods

| Method | Description |
|--------|-------------|
| **GET** | Include user data in URL field of HTTP GET request message (following a '?'): `www.somesite.com/animalsearch?monkeys&banana` |
| **POST** | Web page often includes form input; user input sent from client to server in entity body of HTTP POST request message |
| **HEAD** | Requests headers (only) that would be returned if specified URL were requested with an HTTP GET method |
| **PUT** | Uploads new file (object) to server; completely replaces file that exists at specified URL with content in entity body of PUT |

### HTTP Response Status Codes

- Status code appears in 1st line in server-to-client response message.

| Code | Meaning |
|------|---------|
| `200 OK` | Request succeeded, requested object later in this message |
| `301 Moved Permanently` | Requested object moved, new location specified later in this message (in Location: field) |
| `400 Bad Request` | Request msg not understood by server |
| `404 Not Found` | Requested document not found on this server |
| `505 HTTP Version Not Supported` | HTTP version not supported |

---

## 4. Sockets

### Applications Use Sockets

- Process sends/receives messages to/from its socket

```
Application Layer → Socket → Transport Layer → Network Layer → Link Layer → Physical Layer → Internet
```

### A Simple Web Client Example

**1. Connect to CityUHK and send a handwritten HTTP request**

```java
import java.io.*; import java.net.*;
import javax.swing.*;
import static java.nio.charset.StandardCharsets.*;

public class CityUSocketClient {
    public static void main(String[] args) throws Exception {
        String host = System.getProperty("host", "www.cityu.edu.hk");
        int port = Integer.getInteger("port", 80);
        try (Socket sock = new Socket(host, port)) {
            sock.setSoTimeout(5000);
            String req = "GET / HTTP/1.1\r\n"
                + "Host: " + host + ":" + port + "\r\n"
                + "Connection: close\r\n"
                + "Accept-Encoding: identity\r\n\r\n";
            sock.getOutputStream().write(req.getBytes(US_ASCII));
            InputStream in = sock.getInputStream();
            ByteArrayOutputStream data = new ByteArrayOutputStream();
            byte[] block = new byte[1024];
            int n;
```

- TCP connection: Socket connects to `www.cityu.edu.hk` on port 80.
- HTTP request: GET, Host and Connection: close are written by hand.

**2. Read until EOF, separate the headers, then display HTML**

```java
            while ((n = in.read(block)) != -1)
                data.write(block, 0, n);
            byte[] all = data.toByteArray();
            String raw = new String(all, ISO_8859_1);
            int end = raw.indexOf("\r\n\r\n");
            if (end < 0) throw new IOException("Missing header end");
            String head = raw.substring(0, end);
            System.out.println(head);
            if (head.matches(
                "(?is).*\r\n(?:Transfer|Content)-Encoding:.*"))
                throw new IOException("Encoded body outside demo scope");
            String html = new String(all, end + 4,
                all.length - end - 4, UTF_8);
            SwingUtilities.invokeLater(() -> {
                JFrame f = new JFrame("CityUHK Socket Web Client");
                JEditorPane p = new JEditorPane("text/html", html);
                p.setEditable(false);
                f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
                f.add(new JScrollPane(p));
                f.setSize(600, 400); f.setVisible(true);
            });
        }
    }
}
```

- Receive bytes: `read()` may return fewer than 1024 bytes. −1 means EOF.
- Separate the header and body: `\r\n\r\n` marks the boundary.
- Decode the body last.
- Display basic HTML in a Swing window.

---

## 5. Exercise: ADSL Comprehensive Problem

### Problem Statement

A user subscribes to an ISP home broadband service and connects his computer directly to it via an ADSL modem as shown in Figure 1a. An extract of the output by the `ipconfig` command issued on the computer is shown in Figure 1b.

**(a)** Based on Figure 1a and 1b, deduce the roles performed by the ADSL modem, and briefly describe the purpose of each role.

**(b)** The user launches his web browser and requests for the default web page at `http://www.cityu.edu.hk`. Assume that all the caches of the computer are initially empty. Using a table similar to Table 1, list the sequence of frames being sent and received by the computer until the first frame containing the requested web page is received.

**Given:**
- URL: `http://www.cityu.edu.hk`
- IP: `155.69.6.163`

### Solution

**Roles performed by ADSL modem:**
- **DHCP server**: configure host with IP address, subnet mask, etc.
- **DNS server**: resolve domain name to corresponding IP address
- **Default gateway**: forward packets to outside networks not directly reachable by the host
- **NAT**: enable host to use private IP address by translating it to public IP address and vice versa

**Frame sequence:**

| Frame | MAC Src | MAC Dst | IP Src | IP Dst | Purpose |
|-------|---------|---------|--------|--------|---------|
| 1 | 00-23-26-AA-AA-AA | FF-FF-FF-FF-FF-FF | - | - | ARP request for 192.168.1.254 |
| 2 | 00-24-17-BB-BB-BB | 00-23-26-AA-AA-AA | - | - | ARP reply |
| 3 | 00-23-26-AA-AA-AA | 00-24-17-BB-BB-BB | 192.168.1.68 | 192.168.1.254 | DNS request for www.cityu.edu.hk |
| 4 | 00-24-17-BB-BB-BB | 00-23-26-AA-AA-AA | 192.168.1.254 | 192.168.1.68 | DNS reply 155.69.6.163 |
| 5 | 00-23-26-AA-AA-AA | 00-24-17-BB-BB-BB | 192.168.1.68 | 155.69.6.163 | TCP 3-way handshake |
| 6 | 00-24-17-BB-BB-BB | 00-23-26-AA-AA-AA | 155.69.6.163 | 192.168.1.68 | TCP 3-way handshake |
| 7 | 00-23-26-AA-AA-AA | 00-24-17-BB-BB-BB | 192.168.1.68 | 155.69.6.163 | TCP 3-way handshake |
| 8 | 00-23-26-AA-AA-AA | 00-24-17-BB-BB-BB | 192.168.1.68 | 155.69.6.163 | HTTP request |
| 9 | 00-24-17-BB-BB-BB | 00-23-26-AA-AA-AA | 155.69.6.163 | 192.168.1.68 | HTTP reply |

---

## 6. HTTPS and TLS

### Overview

- **Vanilla TCP & UDP sockets:** no encryption; cleartext passwords sent into socket
- **Transport Layer Security (TLS):**
  - Provides encrypted TCP connections
  - Data integrity
  - End-point authentication
- TLS implemented in application layer
  - Apps use TLS libraries, that use TCP in turn
  - Cleartext sent into "socket" traverse Internet encrypted

---

## 7. HTTP/2

### Key Goal

Decreased delay in multi-object HTTP requests

### HTTP/1.1 Problem

- HTTP/1.1: multiple, pipelined GETs over single TCP connection
- Server responds in-order (FCFS: first-come-first-served) to GET requests
- With FCFS, small object may have to wait for transmission (head-of-line (HOL) blocking) behind large object(s)
- Loss recovery (retransmitting lost TCP segments) stalls object transmission

### HTTP/1.1 Example

Client requests 1 large object (e.g., video file) and 3 smaller objects:

```
client → server: GET O1, GET O2, GET O3, GET O4
server → client: O1 (large), then O2, O3, O4
```

Objects delivered in order requested: O2, O3, O4 wait behind O1

### HTTP/2 Solution

HTTP/2: [RFC 7540, 2015] increased flexibility at server in sending objects to client:
- Methods, status codes, most header fields unchanged from HTTP 1.1
- Transmission order of requested objects based on client-specified object priority (not necessarily FCFS)
- Push unrequested objects to client
- Divide objects into frames, schedule frames to mitigate HOL blocking

### HTTP/2 Frame Interleaving

Objects divided into frames, frame transmission interleaved:

```
client → server: GET O1, GET O2, GET O3, GET O4
server → client: O2, O4, O3, O1 (interleaved frames)
```

O2, O3, O4 delivered quickly, O1 slightly delayed

---

## 8. HTTP/3 and QUIC

### From HTTP/2 to HTTP/3

HTTP/2 over single TCP connection means:
- Recovery from packet loss still stalls all object transmissions
- No security over vanilla TCP connection
- HTTP/3: adds security, per object error- and congestion-control (more pipelining) over UDP

### QUIC: Quick UDP Internet Connections

- Application-layer protocol, on top of UDP
- Increase performance of HTTP
- Error and congestion control
- Deployed on many Google servers, apps (Chrome, mobile YouTube app)

**Protocol stack comparison:**

```
HTTP/2 over TCP:   Application(HTTP/2) → Transport(TCP) → Network(IP)
HTTP/3 over QUIC:  Application(HTTP/2 slimmed) → Transport(QUIC) → Network(IP)
                                        ↑ UDP
```

### QUIC Connection Establishment

**TCP + TLS (traditional):**
- TCP handshake (transport layer) + TLS handshake (security)
- TCP (reliability, congestion control state) + TLS (authentication, crypto state)
- 2 serial handshakes

**QUIC:**
- QUIC combines reliability, congestion control, authentication, crypto state
- 1 RTT handshake

### QUIC 0-RTT

- TLS session ticket sent by server, cached at client
- End of first QUIC connection → start of second QUIC connection
- Client uses last session ticket for encryption, authentication for new connection
- **0 RTT handshake delay**

---

## 9. Web Caching

### Overview

- User configures browser to point to a (local) Web cache
- Browser sends all HTTP requests to cache
  - If object in cache: cache returns object to client
  - Else cache requests object from origin server, caches received object, then returns object to client
- **Goal**: satisfy client requests without involving origin server

### Web Caches (aka Proxy Servers)

- Web cache acts as both client and server
  - Server for original requesting client
  - Client to origin server

**Why Web caching?**
- Reduce response time for client request (cache is closer to client)
- Reduce traffic on an institution's access link
- Internet is dense with caches — enables "poor" content providers to more effectively deliver content

### Browser Caching: Conditional GET

**Goal**: don't send object if browser has up-to-date cached version (no object transmission delay or use of network resources)

- **Client**: specify date of browser-cached copy in HTTP request
  - `If-Modified-Since: <date>`
- **Server**:
  - Response contains no object if browser-cached copy is up-to-date: `HTTP/1.0 304 Not Modified`
  - Response contains object if modified after `<date>`: `HTTP/1.0 200 OK`

---

## 10. Content Distribution Networks (CDNs)

### The Challenge

How to stream content to hundreds of thousands of simultaneous users?

**Option 1: Single large "mega-server"**
- Single point of failure
- Point of network congestion
- Long (and possibly congested) path to distant clients
- This solution doesn't scale…

**Option 2: Store/serve multiple copies of videos at multiple geographically distributed sites (CDN)**
- **Enter deep**: push CDN servers deep into many access networks, close to users
  - Akamai: 240,000 servers deployed in > 120 countries (2015)
- **Bring home**: smaller number (10's) of larger clusters near access nets
  - Used by Limelight

### CDN: The Netflix Example

- Subscriber requests content, service provider returns manifest
- Netflix: stores copies of content (e.g., MADMEN) at its (worldwide) OpenConnect CDN nodes
- Using manifest, client retrieves content at highest supportable rate
- May choose different rate or copy if network path congested

---

## 11. Streaming Multimedia: DASH

### DASH: Dynamic, Adaptive Streaming over HTTP

**Server:**
- Divides video file into multiple chunks
- Each chunk encoded at multiple different rates
- Different rate encodings stored in different files
- Files replicated in various CDN nodes
- Manifest file: provides URLs for different chunks

**Client:**
- Periodically estimates server-to-client bandwidth
- Consulting manifest, requests one chunk at a time
  - Chooses maximum coding rate sustainable given current bandwidth
  - Can choose different coding rates at different points in time (depending on available bandwidth at time), and from different servers

### The Streaming Client Makes the Choices

"Intelligence" at client: client determines
- When to request chunk (so that buffer starvation, or overflow does not occur)
- What encoding rate to request (higher quality when more bandwidth available)
- Where to request chunk (can request from URL server that is "close" to client or has high available bandwidth)

---

## 12. Summary

### Summary: Application Protocols

Each application protocol has a job and uses a transport-layer service.

| Application Protocol | What It Does | Transport Used |
|---------------------|--------------|----------------|
| DHCP | Get IP settings | UDP |
| DNS | Look up names | UDP or TCP |
| HTTP/1.1 and HTTP/2 | Request Web content | TCP |
| HTTP/3 | Request Web content | QUIC over UDP |

### Summary: The Five Layers

Opening one Web page uses all five layers.

| Layer | What It Does | Examples |
|-------|-------------|----------|
| Application | Defines application messages | DHCP, DNS, HTTP |
| Transport | Delivers data between processes | TCP/UDP |
| Network | Moves packets across networks | IP addresses and routing |
| Data link | Moves frames over one link | Ethernet, Wi-Fi, MAC addresses |
| Physical | Sends bits as signals | Electrical, optical, radio signals |
