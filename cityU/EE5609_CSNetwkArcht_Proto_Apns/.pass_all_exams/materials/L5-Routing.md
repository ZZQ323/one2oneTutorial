# EE5609 Computer Networks - Lecture 5

## The Network Layer – Part II: Routing

### Learning Objectives

- Run Dijkstra's algorithm and derive next-hop forwarding entries.
- Apply distance-vector updates and explain count to infinity.
- Explain how OSPF, eBGP and iBGP support Internet routing.
- Distinguish forwarding from routing and explain distributed control.

---

## 1. Network-Layer Functions

- **Forwarding**: Move packets from router's input to appropriate router output (data plane)
- **Routing**: Determine route taken by packets from source to destination (control plane)

Individual routing algorithm components in each and every router interact in the control plane.

---

## 2. Routing Protocols

**Routing protocol goal**: Determine "good" paths (equivalently, routes), from sending hosts to receiving host, through network of routers.

- **Path**: Sequence of routers packets traverse from given initial source host to final destination host
- **"Good"**: Least "cost", "fastest", "least congested"
- Routing: a "top-10" networking challenge!

---

## 3. Routing as a Graph Problem

**Graph**: $G = (N, E)$

- $c_{a,b}$: cost of direct link connecting $a$ and $b$
  - e.g., $c_{w,z} = 5$, $c_{u,z} = \infty$
- Cost defined by network operator: could always be 1, or inversely related to bandwidth, or inversely related to congestion
- $N$: set of routers = $\{u, v, w, x, y, z\}$
- $E$: set of links = $\{(u,v), (u,x), (v,x), (v,w), (x,w), (x,y), (w,y), (w,z), (y,z)\}$

**Example graph** (node labels and edge costs):

```
        u
       / \
    2 /   \ 1
     /     \
    v---1---x
     \     / \
    3 \   /1  \ 1
       \ /     \
        w---5---z
         \     /
        1 \   / 2
           \ /
            y
```

---

## 4. Routing Algorithm Classification

| Dimension | Options |
|-----------|---------|
| **Global or decentralized information?** | **Global (link-state)**: all routers have complete topology, link cost info. **Decentralized (distance vector)**: iterative process, routers initially only know link costs to attached neighbors |
| **How fast do routes change?** | **Dynamic**: routes change more quickly (periodic updates or in response to link cost changes). **Static**: routes change slowly over time |

---

## 5. Dijkstra's Link-State Routing Algorithm

### Notation

- **Centralized**: network topology, link costs known to all nodes (accomplished via "link state broadcast")
- All nodes have same info
- Computes least cost paths from one node ("source") to all other nodes → gives forwarding table for that node
- Iterative: after $k$ iterations, know least cost path to $k$ destinations

| Symbol | Meaning |
|--------|---------|
| $c_{x,y}$ | Direct link cost from node $x$ to $y$; $= \infty$ if not direct neighbors |
| $D(v)$ | Current estimate of cost of least-cost-path from source to destination $v$ |
| $p(v)$ | Predecessor node along path from source to $v$ |
| $N'$ | Set of nodes whose least-cost-path definitively known |

### Algorithm (Pseudocode)

```
1  Initialization:
2    N' = {u}                               /* compute least cost path from u to all other nodes */
3    for all nodes v
4      if v adjacent to u                   /* u initially knows direct-path-cost only to direct neighbors */
5          then D(v) = c_{u,v}              /* but may not be minimum cost! */
6      else D(v) = ∞
7
8  Loop
9    find w not in N' such that D(w) is a minimum
10   add w to N'
11   update D(v) for all v adjacent to w and not in N':
12     D(v) = min(D(v), D(w) + c_{w,v})
13   /* new least-path-cost to v is either old least-cost-path to v
14      or known least-cost-path to w plus direct-cost from w to v */
15 until all nodes in N'
```

### Dijkstra's Algorithm: Worked Example

**Graph** (source = $u$):

```
        u
       / \
    2 /   \ 1
     /     \
    v---1---x
     \     / \
    3 \   /1  \ 1
       \ /     \
        w---5---z
         \     /
        1 \   / 2
           \ /
            y
```

**Step-by-step iteration table:**

| Step | $N'$ | $D(v), p(v)$ | $D(x), p(x)$ | $D(y), p(y)$ | $D(z), p(z)$ | $D(w), p(w)$ |
|------|------|--------------|--------------|--------------|--------------|--------------|
| 0 | $\{u\}$ | $2, u$ | $1, u$ | $\infty$ | $\infty$ | $5, u$ |
| 1 | $\{u, x\}$ | $2, u$ | — | $2, x$ | $4, x$ | $4, x$ |
| 2 | $\{u, x, y\}$ | $2, u$ | — | — | $3, y$ | $4, y$ |
| 3 | $\{u, x, y, v\}$ | — | — | — | $3, y$ | $4, y$ |
| 4 | $\{u, x, y, v, w\}$ | — | — | — | $4, y$ | — |
| 5 | $\{u, x, y, v, w, z\}$ | — | — | — | — | — |

**Step 0 (Initialization):** For all $a$: if $a$ adjacent to $u$ then $D(a) = c_{u,a}$

**Step 1:** Find $a \notin N'$ such that $D(a)$ is a minimum → add $a$ to $N'$ → select $x$ ($D(x)=1$).

Update $D(b)$ for all $b$ adjacent to $x$ and not in $N'$:

$$D(b) = \min(D(b),\; D(x) + c_{x,b})$$

- $D(v) = \min(D(v), D(x) + c_{x,v}) = \min(2, 1+2) = 2$
- $D(w) = \min(D(w), D(x) + c_{x,w}) = \min(5, 1+3) = 4$
- $D(y) = \min(D(y), D(x) + c_{x,y}) = \min(\infty, 1+1) = 2$

**Step 2:** Minimum is $D(v)=2$ or $D(y)=2$ → select $y$.

Update for neighbors of $y$:

- $D(w) = \min(D(w), D(y) + c_{y,w}) = \min(4, 2+1) = 3$
- $D(z) = \min(D(z), D(y) + c_{y,z}) = \min(\infty, 2+2) = 4$

**Step 3:** Minimum is $D(v)=2$ → select $v$.

- $D(w) = \min(D(w), D(v) + c_{v,w}) = \min(3, 2+3) = 3$ (no change)

**Step 4:** Minimum is $D(w)=3$ → select $w$.

**Step 5:** Minimum is $D(z)=4$ → select $z$. All nodes in $N'$.

### Resulting Least-Cost-Path Tree and Forwarding Table

**Least-cost-path tree from $u$:**

| Destination | Next-hop link | Notes |
|-------------|---------------|-------|
| $v$ | $(u, v)$ | Route from $u$ to $v$ directly |
| $x$ | $(u, x)$ | Route from $u$ to all other destinations via $x$ |
| $y$ | $(u, x)$ | via $x$ |
| $w$ | $(u, x)$ | via $x$ |
| $z$ | $(u, x)$ | via $x$ |

**Forwarding table at $u$:**

| Destination | Outgoing Link |
|-------------|---------------|
| $v$ | $(u, v)$ |
| $x$ | $(u, x)$ |
| $y$ | $(u, x)$ |
| $w$ | $(u, x)$ |
| $z$ | $(u, x)$ |

---

## 6. Distance Vector Algorithm

### Bellman-Ford Equation

Based on Bellman-Ford (BF) equation (dynamic programming):

Let $D_x(y)$: cost of least-cost path from $x$ to $y$.

Then:

$$D_x(y) = \min_{v} \{ c_{x,v} + D_v(y) \}$$

- min taken over all neighbors $v$ of $x$
- $D_v(y)$: $v$'s estimated least-cost-path cost to $y$
- $c_{x,v}$: direct cost of link from $x$ to $v$

### Bellman-Ford Example

Suppose that $u$'s neighboring nodes $x, v, w$ know that for destination $z$:

- $D_v(z) = 5$
- $D_w(z) = 3$
- $D_x(z) = 3$

Bellman-Ford equation says:

$$D_u(z) = \min \{ c_{u,v} + D_v(z),\; c_{u,x} + D_x(z),\; c_{u,w} + D_w(z) \}$$
$$= \min \{ 2 + 5,\; 1 + 3,\; 5 + 3 \} = 4$$

Node achieving minimum ($x$) is next hop on estimated least-cost path to destination ($z$).

### Distance Vector Algorithm: Key Idea

- From time-to-time, each node sends its own distance vector estimate to neighbors
- Under minor, natural conditions, the estimate $D_x(y)$ converges to the actual least cost $d_x(y)$

$$D_x(y) \leftarrow \min_v \{ c_{x,v} + D_v(y) \} \quad \text{for each node } y \in N$$

- When $x$ receives new DV estimate from any neighbor, it updates its own DV using B-F equation

### Distance Vector Algorithm: Properties

- **Iterative, asynchronous**: each local iteration caused by:
  - Local link cost change
  - DV update message from neighbor
- **Distributed, self-stopping**: each node notifies neighbors only when its DV changes
  - Neighbors then notify their neighbors – only if necessary
  - No notification received → no actions taken!

**Each node:**
1. Wait for (change in local link cost or msg from neighbor)
2. Recompute DV estimates using DV received from neighbor
3. If DV to any destination has changed, notify neighbors

### Distance Vector: Example

**Network topology:**

```
    a ---8--- b
    |         |
    1         1
    |         |
    d         c
    |         |
    1         1
    |         |
    e ---1--- f
    |         |
    1         1
    |         |
    h ---1--- i
    |
    1
    |
    g
```

Note: asymmetries — missing link (a-c), larger cost (a-b = 8).

**At $t=0$:** All nodes have distance estimates to nearest neighbors (only).

DV in $a$:

| Destination | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ | $h$ | $i$ |
|-------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| $D_a$ | 0 | 8 | $\infty$ | 1 | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ |

All nodes send their local distance vector to their neighbors.

**At $t=1$:** All nodes receive DVs from neighbors, compute new local DV, send new DV to neighbors.

### Distance Vector Example: Detailed Computation

**At $t=1$, node $b$ receives DVs from $a, c, e$ and computes:**

$$D_b(a) = \min\{c_{b,a}+D_a(a),\; c_{b,c}+D_c(a),\; c_{b,e}+D_e(a)\} = \min\{8, \infty, \infty\} = 8$$

$$D_b(c) = \min\{c_{b,a}+D_a(c),\; c_{b,c}+D_c(c),\; c_{b,e}+D_e(c)\} = \min\{\infty, 1, \infty\} = 1$$

$$D_b(d) = \min\{c_{b,a}+D_a(d),\; c_{b,c}+D_c(d),\; c_{b,e}+D_e(d)\} = \min\{9, \infty, 2\} = 2$$

$$D_b(f) = \min\{c_{b,a}+D_a(f),\; c_{b,c}+D_c(f),\; c_{b,e}+D_e(f)\} = \min\{\infty, \infty, 2\} = 2$$

$$D_b(h) = \min\{c_{b,a}+D_a(h),\; c_{b,c}+D_c(h),\; c_{b,e}+D_e(h)\} = \min\{\infty, \infty, 2\} = 2$$

$$D_b(e) = \min\{c_{b,a}+D_a(e),\; c_{b,c}+D_c(e),\; c_{b,e}+D_e(e)\} = \min\{\infty, \infty, 1\} = 1$$

$$D_b(g) = \min\{c_{b,a}+D_a(g),\; c_{b,c}+D_c(g),\; c_{b,e}+D_e(g)\} = \min\{\infty, \infty, \infty\} = \infty$$

$$D_b(i) = \min\{c_{b,a}+D_a(i),\; c_{b,c}+D_c(i),\; c_{b,e}+D_e(i)\} = \min\{\infty, \infty, \infty\} = \infty$$

**Updated DV in $b$:**

| Destination | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ | $h$ | $i$ |
|-------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| $D_b$ | 8 | 0 | 1 | 2 | 1 | 2 | $\infty$ | 2 | $\infty$ |

**At $t=1$, node $c$ receives DVs from $b$ and computes:**

$$D_c(a) = \min\{c_{c,b}+D_b(a)\} = 1 + 8 = 9$$
$$D_c(b) = \min\{c_{c,b}+D_b(b)\} = 1 + 0 = 1$$
$$D_c(d) = \min\{c_{c,b}+D_b(d)\} = 1 + \infty = \infty$$
$$D_c(e) = \min\{c_{c,b}+D_b(e)\} = 1 + 1 = 2$$
$$D_c(f) = \min\{c_{c,b}+D_b(f)\} = 1 + \infty = \infty$$
$$D_c(g) = \min\{c_{c,b}+D_b(g)\} = 1 + \infty = \infty$$
$$D_c(i) = \min\{c_{c,b}+D_b(i)\} = 1 + \infty = \infty$$
$$D_c(h) = \min\{c_{c,b}+D_b(h)\} = 1 + \infty = \infty$$

**Updated DV in $c$:**

| Destination | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ | $h$ | $i$ |
|-------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| $D_c$ | 9 | 1 | 0 | 2 | 2 | $\infty$ | $\infty$ | $\infty$ | $\infty$ |

### Distance Vector: State Information Diffusion

Iterative communication, computation steps diffuses information through network:

| Time | Reach of $c$'s state at $t=0$ |
|------|-------------------------------|
| $t=0$ | $c$'s state at $t=0$ is at $c$ only |
| $t=1$ | $c$'s state may influence DV computations up to **1 hop** away (at $b$) |
| $t=2$ | Up to **2 hops** away (at $b$, $a$, $e$) |
| $t=3$ | Up to **3 hops** away (at $d$, $f$, $h$) |
| $t=4$ | Up to **4 hops** away (at $g$, $i$) |

---

## 7. Distance Vector: Link Cost Changes

### "Good News Travels Fast"

- $t_0$: $y$ detects link-cost change, updates its DV, informs its neighbors.
- $t_1$: $z$ receives update from $y$, updates its DV, computes new least cost to $x$, sends its neighbors its DV.
- $t_2$: $y$ receives $z$'s update, updates its DV. $y$'s least costs do not change, so $y$ does not send a message to $z$.

**Link cost changes:**
- Node detects local link cost change
- Updates routing info, recalculates local DV
- If DV changes, notify neighbors

### "Bad News Travels Slow" – Count-to-Infinity Problem

When link cost increases (e.g., $c_{y,x}$ changes from 1 to 60):

- $y$ sees direct link to $x$ has new cost 60, but $z$ has said it has a path at cost of 5. So $y$ computes "my new cost to $x$ will be 6, via $z$"; notifies $z$ of new cost of 6 to $x$.
- $z$ learns that path to $x$ via $y$ has new cost 6, so $z$ computes "my new cost to $x$ will be 7 via $y$"; notifies $y$ of new cost of 7 to $x$.
- $y$ learns that path to $x$ via $z$ has new cost 7, so $y$ computes "my new cost to $x$ will be 8 via $z$"; notifies $z$ of new cost of 8 to $x$.
- $z$ learns that path to $x$ via $y$ has new cost 8, so $z$ computes "my new cost to $x$ will be 9 via $y$"; notifies $y$ of new cost of 9 to $x$.
- … (continues slowly converging)

**Distributed algorithms are tricky!**

---

## 8. Comparison of LS and DV Algorithms

| Aspect | Link-State (LS) | Distance Vector (DV) |
|--------|-----------------|----------------------|
| **Message complexity** | $n$ routers, $O(n^2)$ messages sent | Exchange between neighbors; convergence time varies |
| **Speed of convergence** | $O(n^2)$ algorithm, $O(n^2)$ messages; may have oscillations | Convergence time varies; may have routing loops; count-to-infinity problem |
| **Robustness** | Router can advertise incorrect link cost; each router computes only its own table | DV router can advertise incorrect path cost ("I have a really low-cost path to everywhere"): black-holing; each router's DV is used by others: error propagates through network |

---

## 9. Making Routing Scalable

Our routing study thus far — idealized:
- All routers identical
- Network "flat"
- … not true in practice

**Scale**: billions of destinations:
- Can't store all destinations in routing tables!
- Routing table exchange would swamp links!

**Administrative autonomy**:
- Internet: a network of networks
- Each network admin may want to control routing in its own network

---

## 10. Routing in the Internet

### Internet Approach to Scalable Routing

Aggregate routers into regions known as **"autonomous systems" (AS)** (a.k.a. "domains").

| Type | Description |
|------|-------------|
| **Intra-AS** (aka "intra-domain") | Routing among routers within same AS ("network"). All routers in AS must run same intra-domain protocol. Routers in different AS can run different intra-domain routing protocols. |
| **Inter-AS** (aka "inter-domain") | Routing among AS'es. Gateway routers at "edge" of their own AS have link(s) to router(s) in other AS'es. Gateways perform inter-domain routing (as well as intra-domain routing). |

**Gateway router**: At "edge" of its own AS, has link(s) to router(s) in other AS'es.

### Interconnected ASes

Forwarding table configured by intra- and inter-AS routing algorithms:
- Intra-AS routing determines entries for destinations within AS
- Inter-AS & intra-AS determine entries for external destinations

### Inter-AS Routing: A Role in Intradomain Forwarding

Suppose router in AS1 receives datagram destined outside of AS1: AS1 inter-domain routing must:
1. Learn which destinations reachable through AS2, which through AS3
2. Propagate this reachability info to all routers in AS1
3. Router should forward packet to gateway router in AS1, but which one?

---

## 11. Intra-AS Routing Protocols

Most common intra-AS routing protocols:

| Protocol | Type | Notes |
|----------|------|-------|
| **RIP** (Routing Information Protocol) [RFC 1723] | Distance Vector | Classic DV; DVs exchanged every 30 secs; no longer widely used |
| **EIGRP** (Enhanced Interior Gateway Routing Protocol) | Distance Vector based | Formerly Cisco-proprietary for decades (became open in 2013 [RFC 7868]) |
| **OSPF** (Open Shortest Path First) [RFC 2328] | Link-State | Classic link-state routing |
| **IS-IS** | Link-State | ISO standard, not RFC standard |

---

## 12. OSPF (Open Shortest Path First) Routing

- **"Open"**: publicly available
- **Classic link-state**:
  - Each router floods OSPF link-state advertisements (directly over IP rather than using TCP/UDP) to all other routers in entire AS
  - Multiple link costs metrics possible: bandwidth, delay
  - Each router has full topology, uses Dijkstra's algorithm to compute forwarding table
- **Security**: all OSPF messages authenticated (to prevent malicious intrusion)

### Hierarchical OSPF

- **Two-level hierarchy**: local area, backbone
  - Link-state advertisements flooded only in area, or backbone
  - Each node has detailed area topology; only knows direction to reach other destinations

**Router types:**

| Type | Role |
|------|------|
| **Internal routers** | Flood LS in area only; compute routing within area; forward packets to outside via area border router |
| **Area border routers** | "Summarize" distances to destinations in own area, advertise in backbone |
| **Backbone routers** | Run OSPF limited to backbone |
| **Boundary routers** | Connect to other ASes |

---

## 13. Internet Inter-AS Routing: BGP

### BGP (Border Gateway Protocol)

- The **de facto inter-domain routing protocol**
- "Glue that holds the Internet together"
- Allows subnet to advertise its existence, and the destinations it can reach, to rest of Internet: "I am here, here is who I can reach, and how"

**BGP provides each AS a means to:**
- Obtain destination network reachability info from neighboring ASes (**eBGP**)
- Determine routes to other networks based on reachability information and policy
- Propagate reachability information to all AS-internal routers (**iBGP**)
- Advertise (to neighboring networks) destination reachability info

### eBGP and iBGP Connections

- **eBGP connectivity**: between gateway routers of different ASes
- **iBGP connectivity**: among routers within the same AS
- Gateway routers run both eBGP and iBGP protocols

### BGP Basics

When AS3 gateway 3a advertises path `AS3, X` to AS2 gateway 2c:
- AS3 promises to AS2 it will forward datagrams towards X

**BGP session**: two BGP routers ("peers") exchange BGP messages over semi-permanent TCP connection:
- Advertising paths to different destination network prefixes (BGP is a "path vector" protocol)

### BGP Protocol Messages [RFC 4371]

| Message | Purpose |
|---------|---------|
| **OPEN** | Opens TCP connection to remote BGP peer and authenticates sending BGP peer |
| **UPDATE** | Advertises new path (or withdraws old) |
| **KEEPALIVE** | Keeps connection alive in absence of UPDATES; also ACKs OPEN request |
| **NOTIFICATION** | Reports errors in previous msg; also used to close connection |

### Path Attributes and BGP Routes

**BGP advertised route**: prefix + attributes

- **Prefix**: destination being advertised
- **Two important attributes**:
  - **AS-PATH**: list of ASes through which prefix advertisement has passed
  - **NEXT-HOP**: indicates specific internal-AS router to next-hop AS

**Policy-based routing:**
- Gateway receiving route advertisement uses import policy to accept/decline path (e.g., never route through AS Y)
- AS policy also determines whether to advertise path to other neighboring ASes

### BGP Path Advertisement Example

1. AS2 router 2c receives path advertisement `AS3, X` (via eBGP) from AS3 router 3a
2. Based on AS2 policy, AS2 router 2c accepts path `AS3, X`, propagates (via iBGP) to all AS2 routers
3. Based on AS2 policy, AS2 router 2a advertises (via eBGP) path `AS2, AS3, X` to AS1 router 1c
4. AS1 gateway router 1c learns path `AS2, AS3, X` from 2a
5. AS1 gateway router 1c also learns path `AS3, X` from 3a
6. Based on policy, AS1 gateway router 1c chooses path `AS3, X` and advertises path within AS1 via iBGP

### BGP: Populating Forwarding Tables

- Recall: 1a, 1b, 1d learn via iBGP from 1c: "path to X goes through 1c"
- At 1d: OSPF intra-domain routing determines how to reach 1c (e.g., use interface 1)
- At 1d: to get to X, use interface 1 (towards 1c)
- At 1a: OSPF intra-domain routing: to get to 1c, use interface 2
- At 1a: to get to X, use interface 2

---

## 14. Why Different Intra-, Inter-AS Routing?

| Factor | Inter-AS | Intra-AS |
|--------|----------|----------|
| **Policy** | Admin wants control over how its traffic routed, who routes through its network | Single admin, so policy less of an issue |
| **Scale** | Hierarchical routing saves table size, reduced update traffic | — |
| **Performance** | Policy dominates over performance | Can focus on performance |
