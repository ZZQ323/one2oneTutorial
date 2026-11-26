# EE5609 Group 14 · RFBus Presentation Q&A 准备（Simple English 版）

> 用途：12 分钟展示后的 3 分钟 Q&A。每题给「可直接念」的简单英文回答：短句、常见词、数字拼写出来。
> 每题附中文大意（帮助理解，不用念）。★ = 最可能被问 / 最该背熟的题。
> 数据来源：论文原文、`zzq_demostration.md` 已核实数据、2026-11-23 联网核实的作者背景。

---

## 万能救场句（先背这四句）

| 场景 | 英文 |
|------|------|
| 买时间 | "That's a good question. Let me think for a second." |
| 没听清 | "Sorry, could you rephrase the question?" |
| 不确定 | "I'm not one hundred percent sure, but based on the paper, ..." |
| 论文没测 | "The paper does not test this. I can only tell you what the authors suggest." |

**答题三步模板**：① 直接回答 → ② 给一个事实/数字 → ③（如果适用）诚实说局限。不要绕圈子。

---

## A. 作者团队（已联网核实，可放心讲）

### Q1 ★ Who wrote this paper? Are they an established team?

"Yes, they are a real team. / The paper comes from one lab at University of Electronic Science and Technology of China, in Chengdu. / The lab leader is Professor Li Lu. / The same group wrote four papers in five years: / Internet-of-Microchips in 2020, / ChipNet in 2022, / LEGO in 2023, / and this RFBus paper in 2024. / One author, Songfan Li, got his PhD in this lab. / He now works at HKUST. / So this is a long research line, not a one-time project."

> 中文：是固定团队——电子科大 Li Lu 教授的实验室，五年四篇一脉相承（IoM→ChipNet→LEGO→RFBus）；Songfan Li 是该实验室博士毕业，现在 HKUST。

### Q2 Is RFBus a brand-new idea in this paper?

"Not completely. / The RFBus interface first appeared in their earlier paper, LEGO, in 2023. / This paper turns RFBus into a full network design, / with processor nodes and lite nodes."

> 中文：RFBus 接口最早出现在 LEGO（ASPLOS'23），这篇是把它扩展成完整的 processor-sharing 架构。（说出这点很加分，说明我们查了前作。）

---

## B. 动机与成本（对应 Slides 1–5，Zhanquan 最可能被问）

### Q3 ★ Why is the node expensive if the sensor is so cheap?

"The sensor chip costs only twenty-five cents. / But every node also needs a processor and a radio. / Together, they push the node to about eight dollars and seventy-five cents. / So the smart parts, not the sensing part, drive the cost."

> 中文：传感器只要 25 美分，贵的是处理器和射频模块（合计 $8.75）。

### Q4 Why not just build cheaper nodes?

"Cheaper radios still need power, / and they still need a processor to run. / The paper takes a different path: / most nodes keep no radio at all. / They share one radio / through a nearby processor node."

> 中文：再便宜的射频也要供电、也要处理器驱动；论文的思路是干脆让大多数节点不带射频。

### Q5 ★ How much does RFBus actually save?

"In the tests, / RFBus used about fifteen to sixteen percent / of the energy of the conventional setup. / That is roughly six times less energy. / The average parts cost dropped by about a quarter to a third. / And collecting all ten readings was faster in both tests."

> 中文：能耗约为传统方案的 15–16%（≈6 倍节能），成本降约 24–34%，收集时间也更快（364→241 ms，1029→300 ms）。

---

## C. 技术原理

### Q6 ★ Why I2C? Why not WiFi between the nodes?

"I2C is simple and cheap. / About seventy-three percent of digital sensors already use it. / I2C also has built-in addressing, / so one bus can serve many chips. / WiFi on every node would cost more / and use much more energy. / RFBus keeps the good parts of I2C / and just makes it wireless."

> 中文：I2C 便宜简单、73% 数字传感器都用它、自带寻址；给每个节点配 WiFi 又贵又费电。

### Q7 How far can RFBus reach?

"About twenty-three meters / at two hundred kilobits per second, / with a clear path. / With an obstruction, only about five meters. / A faster bus means a shorter range. / This is fine, / because RFBus only connects nearby nodes."

> 中文：200 kbps 视距约 23 m，有遮挡约 5 m；速率越快距离越短，但设计本来就只连邻近节点。

### Q8 How does one processor talk to nine lite nodes without confusion?

"RFBus adds a two-byte header / before the normal I-squared-C message. / One byte gives the session length. / The other byte is the address of the target lite node. / Only the node with the matching address replies. / The others stay quiet."

> 中文：I2C 消息前加 2 字节帧头（会话长度 + 目标地址），地址匹配的 lite node 才应答。

### Q9 Does the lite node need a lot of hardware?

"Very little. / The lite node has no processor / and no long-range radio. / It only needs the sensor chip / and a small RFBus interface. / The header decoder uses just five logic components."

> 中文：lite node 无处理器、无远程射频，帧头解码只用 5 个逻辑元件。

---

## D. 局限与可靠性（老师最爱问；诚实回答 + 带上作者的缓解方案）

### Q10 ★ What if the processor node fails?

"Then its nine lite nodes lose contact with the gateway. / This is the single point of failure. / The authors suggest / that a nearby processor node can take over, / because RFBus supports multiple masters. / But the paper does not test this in the field."

> 中文：单点故障——processor node 挂了带的全废；作者说可让邻近 processor node 接管（RFBus 是多主），但论文没实测。

### Q11 ★ Is the communication secure?

"The paper does not discuss encryption. / In theory, an attacker could listen to / or block the RFBus signal. / The authors list security as future work, / for example a small encryption circuit. / So, no — security is not solved yet."

> 中文：论文没谈加密，信号可被窃听/干扰；作者把安全列为 future work。

### Q12 You only tested ten nodes. Can this really scale?

"The field trial used ten nodes: / one processor node and nine lite nodes. / Larger sites are not tested. / The design looks scalable, / because the gateway only schedules processor nodes, / not every sensor. / But honestly, / large-scale evidence is still missing."

> 中文：只测了 10 节点；架构上可扩展（网关只管 processor node），但缺大规模实证——主动承认这点会显得客观。

### Q13 The processor node does more work. Does its battery die faster?

"Yes. / It serves its own sensor plus nine neighbors, / so it uses more energy than a normal node. / The paper suggests two fixes: / the gateway can balance the load, / or processor nodes can get solar panels."

> 中文：是的，processor node 负载更重；缓解方案是网关均衡负载或配太阳能板。

### Q14 What about non-I2C sensors, or moving nodes?

"Today RFBus only supports I-squared-C sensors. / The authors want to extend it to SPI and CAN. / For moving nodes, / the design assumes fixed positions. / A moving lite node could leave the range of its processor. / The paper does not address this."

> 中文：目前只支持 I2C（未来想扩展 SPI/CAN）；假设节点固定，移动场景没讨论。

---

## E. 与课程的联系

### Q15 ★ How does RFBus relate to the network layers we learned?

"RFBus works at the bottom two layers: / physical and data link. / It behaves like a wireless shared bus, / similar to a small LAN. / Above it, / the processor node uses normal WiFi or LoRa / to reach the gateway. / So the stack is unchanged — / we just add a new kind of link at the bottom."

> 中文：RFBus 在物理层+链路层，相当于无线化的共享总线；上面照常用 WiFi/LoRa 到网关，协议栈分层不变。

### Q16 Is RFBus like Bluetooth or Zigbee?

"No. / Bluetooth and Zigbee are full radio protocols / with their own stacks. / RFBus is not a new network protocol. / It is a bus extension: / it copies the I-squared-C line state over the air. / The lite nodes run no protocol stack at all."

> 中文：不是。蓝牙/Zigbee 是完整协议栈；RFBus 只是把 I2C 线状态搬到无线上，lite node 不跑任何协议栈。

---

## 发音与读法提示

| 词 | 读法 |
|----|------|
| UESTC | 逐字母 U-E-S-T-C；第一次可说全称 "the University of Electronic Science and Technology of China" |
| I²C | **I-squared-C**（与组内 Speaker 3 的稿子保持一致） |
| obstruction | /əbˈstrʌkʃn/ "厄布-斯特拉克-申" |
| encryption | /ɪnˈkrɪpʃn/ "因-克里普-申" |
| conventional | /kənˈvenʃənl/ 重音在 ven |
| multiple masters | "MULTI-pull MAS-ters" |
| kilobits per second | 慢读 "KIL-o-bits per SECOND" |

## 使用建议

- 3 分钟 Q&A 一般只问 2–4 个问题，优先背 ★ 题（Q1、Q3、Q5、Q6、Q10、Q11、Q12、Q15）。
- 组内分工建议：作者团队/动机类（A、B）由 Zhanquan 答；原理类（C）由 Siyuan 答；实验与局限（D）由 ZhongYeQuan / Shuai 答；课程联系（E）谁被点到谁答。
- 答不上来时用救场句 + 转向队友："This part was covered by my teammate. Maybe he can add something."
