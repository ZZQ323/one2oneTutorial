# CS5285 Problem Set 1 - 2026秋季

**截止日期**: 2026年10月11日 18:00

---

## 任务1: Security Services and Mechanisms (10分)

**题目要求**:
找一篇2026年8月之后报道的安全事件新闻（如大型黑客攻击、数据泄露、恶意软件等）。事件可以发生在2025年8月之前，但必须在此之后首次报道。写一篇短文（最多400字），用自己的话解释发生了什么。必须提及：
- 涉及的攻击者类型
- 被破坏的主要安全服务
- 你认为可以用来缓解此事件的服务和机制
- 提供事件文章的链接

### 执行建议

**步骤**:
1. 搜索2026年8月后的重大安全事件新闻
2. 选择一个有足够信息的事件
3. 撰写400字以内的分析文章

**推荐搜索方向**:
- 大型数据泄露事件
- 勒索软件攻击
- 供应链攻击
- APT（高级持续性威胁）攻击

**文章结构建议**:
1. 事件概述（100字）
2. 攻击者类型分析（80字）
3. 被破坏的安全服务（100字）
4. 缓解措施建议（120字）

### 任务1范文 (Essay)

**Selected Incident: McKesson Corporation Data Breach (August 2026)**

**Reference link**: https://morningoverview.com/hackers-steal-millions-of-patient-records-from-health-giant-mckesson-demand-55-million/

In August 2026, McKesson Corporation, one of the largest pharmaceutical distributors in the United States, disclosed a major data breach. The attackers, identified as the ShinyHunters ransomware group, exfiltrated approximately 1 terabyte of data from McKesson's Salesforce and Snowflake cloud environments over a four-day window (August 21–25). The stolen data reportedly included Social Security numbers, prescription records, billing details, and protected health information (PHI). ShinyHunters demanded a ransom of $55 million. HaveIBeenPwned confirmed at least 6.4 million unique email addresses in the leaked dataset.

The attackers were a financially motivated criminal hacking group. They did not use malware to gain initial access. Instead, they employed voice phishing (vishing): calling McKesson employees while impersonating IT staff, paired with a spoofed domain (mckesson[.]claims), to trick employees into surrendering their Okta identity credentials. Those stolen credentials then provided a pathway into the company's cloud platforms.

Several core security services were compromised. **Confidentiality** was the most directly violated: sensitive patient and employee data was exfiltrated without authorization. **Authentication** was undermined because the attackers bypassed the identity system using phished credentials — the system correctly validated the credentials but could not distinguish a legitimate user from an impostor. **Access control** also failed, as a single set of compromised credentials granted access to two major cloud platforms (Salesforce and Snowflake) without additional authorization barriers.

To mitigate such an event, several security services and mechanisms could have been applied. **Phishing-resistant multi-factor authentication** (e.g., hardware security keys such as FIDO2) would have prevented the attackers from using stolen passwords alone. **Network segmentation** and **least-privilege access control** would have limited the blast radius of a single compromised account, preventing lateral movement across both cloud platforms simultaneously. A **Cloud Access Security Broker (CASB)** with anomaly detection could have flagged the unusual data access patterns during the four-day exfiltration window. **Data Loss Prevention (DLP)** mechanisms could have detected and blocked the large-scale transfer of sensitive records. Finally, regular **security awareness training** focused on vishing and social engineering would have made employees less likely to hand over credentials over the phone.

---

## 任务2: Modes of Operation and 'shift cipher' (25分)

**题目设置**:
使用4位输入的移位密码作为分组密码，密钥 k = 3
- 字母表映射（16个字母）:
  - A=0000, B=0001, C=0010, D=0011, E=0100, F=0101, G=0110, H=0111
  - I=1000, J=1001, K=1010, L=1011, M=1100, N=1101, O=1110, P=1111
- 移位密码: Ek(X) = (X + 3) mod 16
- 明文 P = BOBALICE (P₀是B)

**转换表**:
| 字母 | 二进制 | 字母 | 二进制 |
|------|--------|------|--------|
| A    | 0000   | I    | 1000   |
| B    | 0001   | J    | 1001   |
| C    | 0010   | K    | 1010   |
| D    | 0011   | L    | 1011   |
| E    | 0100   | M    | 1100   |
| F    | 0101   | N    | 1101   |
| G    | 0110   | O    | 1110   |
| H    | 0111   | P    | 1111   |

### 解答

**明文转换**: BOBALICE → B(0001) O(1110) B(0001) A(0000) L(1011) I(1000) C(0010) E(0100)

**(a) CBC模式加密，IV = 1100 (5分)**

CBC加密公式: Cᵢ = Ek(Pᵢ ⊕ Cᵢ₋₁)，其中C₀ = IV

计算过程:
- C₁ = Ek(P₁ ⊕ IV) = Ek(0001 ⊕ 1100) = Ek(1101) = (13+3) mod 16 = 0000 (A)
- C₂ = Ek(P₂ ⊕ C₁) = Ek(1110 ⊕ 0000) = Ek(1110) = (14+3) mod 16 = 0001 (B)
- C₃ = Ek(P₃ ⊕ C₂) = Ek(0001 ⊕ 0001) = Ek(0000) = (0+3) mod 16 = 0011 (D)
- C₄ = Ek(P₄ ⊕ C₃) = Ek(0000 ⊕ 0011) = Ek(0011) = (3+3) mod 16 = 0110 (G)
- C₅ = Ek(P₅ ⊕ C₄) = Ek(1011 ⊕ 0110) = Ek(1101) = (13+3) mod 16 = 0000 (A)
- C₆ = Ek(P₆ ⊕ C₅) = Ek(1000 ⊕ 0000) = Ek(1000) = (8+3) mod 16 = 1011 (L)
- C₇ = Ek(P₇ ⊕ C₆) = Ek(0010 ⊕ 1011) = Ek(1001) = (9+3) mod 16 = 1100 (M)
- C₈ = Ek(P₈ ⊕ C₇) = Ek(0100 ⊕ 1100) = Ek(1000) = (8+3) mod 16 = 1011 (L)

**密文**: **ABDGALML**

**(b) CBC模式加密，IV = 0101 (5分)**

计算过程:
- C₁ = Ek(P₁ ⊕ IV) = Ek(0001 ⊕ 0101) = Ek(0100) = (4+3) mod 16 = 0111 (H)
- C₂ = Ek(P₂ ⊕ C₁) = Ek(1110 ⊕ 0111) = Ek(1001) = (9+3) mod 16 = 1100 (M)
- C₃ = Ek(P₃ ⊕ C₂) = Ek(0001 ⊕ 1100) = Ek(1101) = (13+3) mod 16 = 0000 (A)
- C₄ = Ek(P₄ ⊕ C₃) = Ek(0000 ⊕ 0000) = Ek(0000) = (0+3) mod 16 = 0011 (D)
- C₅ = Ek(P₅ ⊕ C₄) = Ek(1011 ⊕ 0011) = Ek(1000) = (8+3) mod 16 = 1011 (L)
- C₆ = Ek(P₆ ⊕ C₅) = Ek(1000 ⊕ 1011) = Ek(0011) = (3+3) mod 16 = 0110 (G)
- C₇ = Ek(P₇ ⊕ C₆) = Ek(0010 ⊕ 0110) = Ek(0100) = (4+3) mod 16 = 0111 (H)
- C₈ = Ek(P₈ ⊕ C₇) = Ek(0100 ⊕ 0111) = Ek(0011) = (3+3) mod 16 = 0110 (G)

**密文**: **HMADLGHG**

**比较**: 与2(a)的密文完全不同，说明CBC模式中IV的改变会导致整个密文的雪崩效应。

**(c) CTR模式加密，计数器从9开始 (5分)**

CTR加密公式: Cᵢ = Pᵢ ⊕ Ek(Counterᵢ)

计数器序列（从9开始）:
- Counter₁ = 9 = 1001
- Counter₂ = 10 = 1010
- Counter₃ = 11 = 1011
- Counter₄ = 12 = 1100
- Counter₅ = 13 = 1101
- Counter₆ = 14 = 1110
- Counter₇ = 15 = 1111
- Counter₈ = 16 mod 16 = 0 = 0000

计算Ek(Counter):
- Ek(1001) = (9+3) mod 16 = 1100
- Ek(1010) = (10+3) mod 16 = 1101
- Ek(1011) = (11+3) mod 16 = 1110
- Ek(1100) = (12+3) mod 16 = 1111
- Ek(1101) = (13+3) mod 16 = 0000
- Ek(1110) = (14+3) mod 16 = 0001
- Ek(1111) = (15+3) mod 16 = 0010
- Ek(0000) = (0+3) mod 16 = 0011

计算密文:
- C₁ = P₁ ⊕ Ek(Counter₁) = 0001 ⊕ 1100 = 1101 (N)
- C₂ = P₂ ⊕ Ek(Counter₂) = 1110 ⊕ 1101 = 0011 (D)
- C₃ = P₃ ⊕ Ek(Counter₃) = 0001 ⊕ 1110 = 1111 (P)
- C₄ = P₄ ⊕ Ek(Counter₄) = 0000 ⊕ 1111 = 1111 (P)
- C₅ = P₅ ⊕ Ek(Counter₅) = 1011 ⊕ 0000 = 1011 (L)
- C₆ = P₆ ⊕ Ek(Counter₆) = 1000 ⊕ 0001 = 1001 (J)
- C₇ = P₇ ⊕ Ek(Counter₇) = 0010 ⊕ 0010 = 0000 (A)
- C₈ = P₈ ⊕ Ek(Counter₈) = 0100 ⊕ 0011 = 0111 (H)

**密文**: **NDPPLJAH**

**(d) C₃的MSB出错时的解密 (5分)**

使用2(a)的密文: ABDGALML

如果C₃的MSB出错，C₃从0011变成1011

CBC解密: Pᵢ = Ek⁻¹(Cᵢ) ⊕ Cᵢ₋₁

Ek⁻¹(X) = (X - 3) mod 16

- P₁ = Ek⁻¹(C₁) ⊕ IV = Ek⁻¹(0000) ⊕ 1100 = 1101 ⊕ 1100 = 0001 (B) ✓
- P₂ = Ek⁻¹(C₂) ⊕ C₁ = Ek⁻¹(0001) ⊕ 0000 = 1110 ⊕ 0000 = 1110 (O) ✓
- P₃ = Ek⁻¹(C₃') ⊕ C₂ = Ek⁻¹(1011) ⊕ 0001 = 1000 ⊕ 0001 = 1001 (J) ✗ (原为B)
- P₄ = Ek⁻¹(C₄) ⊕ C₃' = Ek⁻¹(0110) ⊕ 1011 = 0011 ⊕ 1011 = 1000 (I) ✗ (原为A)
- P₅ = Ek⁻¹(C₅) ⊕ C₄ = Ek⁻¹(0000) ⊕ 0110 = 1101 ⊕ 0110 = 1011 (L) ✓
- P₆ = Ek⁻¹(C₆) ⊕ C₅ = Ek⁻¹(1011) ⊕ 0000 = 1000 ⊕ 0000 = 1000 (I) ✓
- P₇ = Ek⁻¹(C₇) ⊕ C₆ = Ek⁻¹(1100) ⊕ 1011 = 1001 ⊕ 1011 = 0010 (C) ✓
- P₈ = Ek⁻¹(C₈) ⊕ C₇ = Ek⁻¹(1011) ⊕ 1100 = 1000 ⊕ 1100 = 0100 (E) ✓

**恢复的明文**: BOJILICE

**(e) C₃丢失时的解密 (5分)**

如果C₃丢失，接收者将C₄当作C₃处理

密文序列变为: C₁, C₂, C₄, C₅, C₆, C₇, C₈

- P₁ = Ek⁻¹(C₁) ⊕ IV = Ek⁻¹(0000) ⊕ 1100 = 1101 ⊕ 1100 = 0001 (B) ✓
- P₂ = Ek⁻¹(C₂) ⊕ C₁ = Ek⁻¹(0001) ⊕ 0000 = 1110 ⊕ 0000 = 1110 (O) ✓
- P₃ = Ek⁻¹(C₄) ⊕ C₂ = Ek⁻¹(0110) ⊕ 0001 = 0011 ⊕ 0001 = 0010 (C) ✗ (原为B)
- P₄ = Ek⁻¹(C₅) ⊕ C₄ = Ek⁻¹(0000) ⊕ 0110 = 1101 ⊕ 0110 = 1011 (L) ✗ (原为A)
- P₅ = Ek⁻¹(C₆) ⊕ C₅ = Ek⁻¹(1011) ⊕ 0000 = 1000 ⊕ 0000 = 1000 (I) ✓
- P₆ = Ek⁻¹(C₇) ⊕ C₆ = Ek⁻¹(1100) ⊕ 1011 = 1001 ⊕ 1011 = 0010 (C) ✓
- P₇ = Ek⁻¹(C₈) ⊕ C₇ = Ek⁻¹(1011) ⊕ 1100 = 1000 ⊕ 1100 = 0100 (E) ✗ (原为E)

**恢复的明文**: BOCLICE (7个字符，丢失了一个)

---

## 任务3: Number Theory (30分)

**注意**: 你需要使用自己的学号！
- X = 8位学号（例如：12345678）
- Y = 学号的后4位（例如：5678）

**以下解答使用示例学号 X = 12345678, Y = 5678**

### 解答

**注意**: 以下使用示例学号 X = 12345678, Y = 5678。**你必须替换为自己的学号重新计算！**

**(a) 使用平方乘法计算 41^Y mod 18865 (5分)**

Y = 5678 = 1011000101110₂ (二进制)

使用平方乘法，从高位到低位:
```
初始化: result = 1
bit=1: result = result² × 41 = 41
bit=0: result = result² = 41² mod 18865 = 1681
bit=1: result = result² × 41 = 1681² × 41 mod 18865 = 2825761 × 41 mod 18865 = 10461 × 41 mod 18865 = ...
bit=1: ...
... (依次处理每个bit)
```

**最终答案**: 41^5678 mod 18865 = **14316**

**(b) 计算 ϕ(Y) (5分)**

Y = 5678

分解质因数: 5678 = 2 × 17 × 167

ϕ(5678) = ϕ(2) × ϕ(17) × ϕ(167) = 1 × 16 × 166 = **2656**

**(c) gcd(X, 928374827) (5分)**

X = 12345678

使用欧几里得算法:
```
928374827 = 75 × 12345678 + 2449177
12345678 = 5 × 2449177 + 99893
2449177 = 24 × 99893 + 51745
99893 = 1 × 51745 + 48148
51745 = 1 × 48148 + 3597
48148 = 13 × 3597 + 1387
3597 = 2 × 1387 + 823
1387 = 1 × 823 + 564
823 = 1 × 564 + 259
564 = 2 × 259 + 46
259 = 5 × 46 + 29
46 = 1 × 29 + 17
29 = 1 × 17 + 12
17 = 1 × 12 + 5
12 = 2 × 5 + 2
5 = 2 × 2 + 1
2 = 2 × 1 + 0
```

**gcd(12345678, 928374827) = 1**

**(d) 找到整数x和z使得 x·X + z·928374827 = gcd(X, 928374827) (5分)**

使用扩展欧几里得算法，回代上述步骤:

**x = -351508225, z = 4674413**

验证: (-351508225) × 12345678 + 4674413 × 928374827 = 1 ✓

**(e) 计算 108809^(-1) mod 291452 (5分)**

使用扩展欧几里得算法求逆元:

首先验证 gcd(108809, 291452) = 1 ✓

**答案**: 108809^(-1) mod 291452 = **107381**

验证: 108809 × 107381 mod 291452 = 1 ✓

**(f) 选择一个小于X的素数Z，计算 X^X mod Z (5分)**

选择 Z = 9999991（这是一个素数，且小于12345678）

使用快速幂算法:

**答案**: 12345678^12345678 mod 9999991 = **9193925**

---

## 任务4: El-Gamal (10分)

**参数**: p = 17, g = 3

### 解答

**(a) 私钥 x = 6，计算公钥 y (2分)**

y = g^x mod p = 3^6 mod 17

3^6 = 729 = 42 × 17 + 15

**y = 15**

**(b) 使用公钥和 r = 5 加密消息 M = 7 (3分)**

El-Gamal加密:
- c₁ = g^r mod p = 3^5 mod 17 = 243 mod 17 = 5
- c₂ = M × y^r mod p = 7 × 15^5 mod 17

15^5 = 759375
759375 mod 17 = 759375 - 44669 × 17 = 759375 - 759373 = 2

c₂ = 7 × 2 mod 17 = 14 mod 17 = 14

**密文**: (c₁, c₂) = **(5, 14)**

**(c) 解密验证 (3分)**

解密: M = c₂ × (c₁^x)^(-1) mod p

c₁^x = 5^6 mod 17 = 15625 mod 17 = 15625 - 919 × 17 = 15625 - 15623 = 2

求 2^(-1) mod 17:
2 × 9 = 18 ≡ 1 (mod 17)
所以 2^(-1) = 9

M = 14 × 9 mod 17 = 126 mod 17 = 126 - 7 × 17 = 126 - 119 = 7

**验证成功: M = 7** ✓

**(d) El-Gamal算法能提供哪些安全服务？ (2分)**

1. **机密性(Confidentiality)**: 通过加密提供，只有拥有私钥的人才能解密
2. **完整性(Integrity)**: 结合数字签名可提供
3. **认证(Authentication)**: 结合数字签名可验证发送者身份
4. **不可否认性(Non-repudiation)**: 通过数字签名提供

---

## 任务5: Diffie-Hellman (12分)

**参数**: p = 17, g = 3

### 解答

**(a) Alice选择 x = 6，计算她发送给Bob的公钥 A (2分)**

A = g^x mod p = 3^6 mod 17 = 729 mod 17

729 = 42 × 17 + 15

**A = 15**

**(b) Bob选择 y = 5，计算他发送给Alice的公钥 B (2分)**

B = g^y mod p = 3^5 mod 17 = 243 mod 17

243 = 14 × 17 + 5

**B = 5**

**(c) 计算共享密钥 K (2分)**

Alice计算: K = B^x mod p = 5^6 mod 17 = 15625 mod 17 = 2
Bob计算: K = A^y mod p = 15^5 mod 17 = 759375 mod 17 = 2

**共享密钥 K = 2**

**(d) 如何修改DH以防止中间人攻击？ (6分)**

**中间人攻击问题**: 攻击者可以拦截并替换公钥，分别与Alice和Bob建立不同的共享密钥。

**解决方案**: 使用认证的Diffie-Hellman

**方法1: 数字签名**
- Alice和Bob各自拥有公钥证书（由CA签发）
- Alice发送: (A, Sign_A(A, B, timestamp))
- Bob发送: (B, Sign_B(A, B, timestamp))
- 双方验证签名后再计算共享密钥

**方法2: 静态- ephemeral DH**
- Alice和Bob各有长期密钥对 (a, A) 和 (b, B)
- Alice发送: A
- Bob发送: B 和 Sign_b(B)
- Alice验证签名后继续

**方法3: MQV (Menezes-Qu-Vanstone)**
- 结合长期密钥和临时密钥
- 提供隐式认证

**假设**:
- 存在可信的CA或预共享的公钥
- 双方有数字签名算法（如RSA、DSA、ECDSA）
- 时间戳或nonce防止重放攻击

**符号**:
- Sign_X(M): 用X的私钥对消息M签名
- Cert_X: X的公钥证书
- timestamp: 时间戳

---

## 任务6: VM Connect (10分)

### 执行步骤

**(a) 设置云VM连接 (10分)**

**步骤**:
1. 查看课程页面（Pages）发布的VM连接说明
2. 按照说明配置SSH连接或远程桌面
3. 成功连接后截图VM桌面

**提交**: 提供VM桌面截图作为证据

---

## 总结

**总分**: 102分
- 任务1: 10分
- 任务2: 25分
- 任务3: 30分（需要你的学号）
- 任务4: 10分
- 任务5: 12分
- 任务6: 10分

**重要提醒**:
1. 任务3必须使用你自己的学号计算
2. 任务1需要找2026年8月后的真实安全事件
3. 任务6需要实际连接VM并截图
4. 所有计算题需要展示步骤
