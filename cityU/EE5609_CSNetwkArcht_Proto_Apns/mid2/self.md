 Q1: Pipeline Delay (综合)

    A message of 8000 bytes is to be sent from host S to host D through 3 intermediate routers (S → R1 → R2 → R3 → D, total 4 hops). The message    is fragmented into packets, each carrying 200 bytes of data plus a 50-byte header. All links have the same transmission rate R. Propagation    delay is negligible.

    (a) How many packets are generated? What is the size of each packet (in bytes)?

    (b) Express the total end-to-end delay as a function of R. (Hint: consider the pipeline effect — how many packet-transmission times elapse
    (b) Express the total end-to-end delay as a function of R. (Hint: consider the pipeline effect — how many packet-transmission times elapse

    (c) If the total delay must not exceed 80 ms, what is the minimum transmission rate R (in kbps)?

    ────────────────────────────────────

    Q2: IP Fragmentation

    A router receives an IP datagram of 5000 bytes (including the 20-byte IP header). The outgoing link has an MTU of 1200 bytes. The DF flag is    0.

    (a) How many fragments are produced?

    (b) For each fragment, specify:

    • Total length (bytes)
    • Data length (bytes)
    • MF flag (0 or 1)
    • Fragment offset value

    (c) If the MTU were 1500 bytes instead, how would your answers change?

    ────────────────────────────────────

    Q3: ARP Through Router — Frame Exchange

    Host A (192.168.1.10, MAC: AA-AA-AA-AA-AA-AA) wants to ping Host B (192.168.2.20, MAC: BB-BB-BB-BB-BB-BB). They are connected through a    router:

      Host A ──── Switch ──── Router ──── Switch ──── Host B
                (Subnet 1)   R1: 192.168.1.1       (Subnet 2)
                       R2: 192.168.2.1

• Host A's default gateway: 192.168.1.1 (Router interface R1)
• ARP caches are empty on all devices.

List the sequence of frames (ARP requests/replies + ICMP Echo Request/Reply) exchanged until Host A receives the ping reply. For each frame,specify:

Frame  Source MAC  Dest MAC  Source IP  Dest IP  Type  Description

(Hint: there should be 6 frames total — think about what happens on each subnet.)