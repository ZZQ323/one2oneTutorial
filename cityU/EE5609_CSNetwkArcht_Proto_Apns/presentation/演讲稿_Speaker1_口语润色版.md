# Speaker 1（Zhanquan Zhuang, Slides 1–5）口语润色版

> 基于 `EE5609_RFBus_Group_演讲稿.docx` 第一部分润色，**内容与数据未改动**，只调整了句子长度、语序和口语节奏，让英文念起来更顺口。
> 预计用时：2.5–3 分钟（与原稿基本一致）。

## 朗读记号说明

- `/` = 换气短停顿（半拍）
- `—` = 拖一拍，制造强调
- **加粗** = 重读这个词
- 每页最后一句念完后停 1 秒再翻页，不赶

---

## 一、带停顿记号版（练习用）

### Slide 1 · Introduction

Good morning, everyone. /
We are Group **Fourteen**. /
Today we present a paper / by Meng and colleagues. /
The paper introduces **RFBus** — /
a way for nearby sensors / to share **one** processor. /

### Slide 2 · Presentation outline

Here is our plan for today. /
**First**, / the problem. /
**Then**, / the design — / and how it works. /
**After that**, / the test results, / and where this design could be useful. /
And **finally**, / what we would check / before using RFBus / at a larger site. /

### Slide 3 · Why we need many sensors

Think about a **forest**, / a **bridge**, / and a **farm**. /
In each case, / one sensor can only tell us / about **one** place. /
To see what is happening / across the **whole** site, /
we need sensors / at **many** locations. /
For example: /
a temperature sensor / in one part of a forest /
may miss a change / in **another** part. /
More sensing points / help us see / **where** a change starts. /

### Slide 4 · A conventional sensor node

In a conventional setup, /
**every** node carries its own / sensor, / processor, / and radio. /
Now look at the **price**. /
The sensor costs / just **twenty-five cents**. /
The processor and the radio / make up **most** of the total — /
**eight dollars and seventy-five cents** / in listed parts. /
And this cost adds up, / **node after node**. /
Two small notes / on this slide: /
the radio here is **LoRa**, /
and the listed price / does **not** include the battery. /

### Slide 5 · The research question

So here is the question / this paper asks. /
Can we keep a sensor / at **every** location, /
but **share** / the more expensive parts? /
The diagram shows the idea. /
Look at the **left** side first. /
Every spot has its **own** / processor and radio. /
Now look at the **right**. /
The nearby sensors / share **one** processor /
and **one** radio / to reach the gateway. /
Same coverage — / **much less hardware**. /

### Handoff（交接给 Speaker 2）

Next, / we will look at two earlier ways / to simplify sensor nodes, /
and see / **where** RFBus puts the shared processor. /
Now I'll hand over / to my teammate. /

---

## 二、干净版（打印/提词用）

Good morning, everyone. We are Group Fourteen. Today we present a paper by Meng and colleagues. The paper introduces RFBus — a way for nearby sensors to share one processor.

Here is our plan for today. First, the problem. Then, the design — and how it works. After that, the test results, and where this design could be useful. And finally, what we would check before using RFBus at a larger site.

Think about a forest, a bridge, and a farm. In each case, one sensor can only tell us about one place. To see what is happening across the whole site, we need sensors at many locations. For example: a temperature sensor in one part of a forest may miss a change in another part. More sensing points help us see where a change starts.

In a conventional setup, every node carries its own sensor, processor, and radio. Now look at the price. The sensor costs just twenty-five cents. The processor and the radio make up most of the total — eight dollars and seventy-five cents in listed parts. And this cost adds up, node after node. Two small notes on this slide: the radio here is LoRa, and the listed price does not include the battery.

So here is the question this paper asks. Can we keep a sensor at every location, but share the more expensive parts? The diagram shows the idea. Look at the left side first. Every spot has its own processor and radio. Now look at the right. The nearby sensors share one processor and one radio to reach the gateway. Same coverage — much less hardware.

Next, we will look at two earlier ways to simplify sensor nodes, and see where RFBus puts the shared processor. Now I'll hand over to my teammate.

---

## 三、朗读要点

**改了什么、为什么更好念**

1. 长句拆短：一句话只说一件事，换气点自然落在 `/` 处，不容易读到一半没气。
2. 数字全部拼成英文读法（twenty-five cents / eight dollars and seventy-five cents），避免临场纠结 "8.75" 怎么念。
3. 加了路标词（First / Then / After that / Finally；Now look at the price；So here is the question），听众跟得上，你自己也不会忘下一句。
4. 每页结尾留了一个短句收束（如 "Same coverage — much less hardware."），念完停顿翻页，节奏干净。

**发音提示**

| 词 | 读法 |
|----|------|
| conventional | /kənˈvenʃənl/，重音在 ven |
| LoRa | /ˈlɔːrə/，"罗拉"，不是 "萝拉" 也不是 L-O-R-A |
| RFBus | 逐字母 + 词：**R-F-bus** |
| gateway | /ˈɡeɪtweɪ/，重音在前 |
| colleagues | /ˈkɒliːɡz/，"卡里格斯" |
| diagram | /ˈdaɪəɡræm/，"戴-呃-格兰姆" |

**练习建议**

- 先照着「带停顿记号版」慢读 2 遍，夸张地在 `/` 处停顿；再用「干净版」正常语速读 2 遍。
- 计时目标：2 分 30 秒 ± 20 秒。超过 3 分 10 秒就删 Slide 3 的 for example 那句（可整句跳过，不影响逻辑）。
- Slide 5 是本页的高潮（研究问题），"Can we keep a sensor at every location, but share the more expensive parts?" 放慢、加重 **share**，这是全组后面 20 页的引子。
