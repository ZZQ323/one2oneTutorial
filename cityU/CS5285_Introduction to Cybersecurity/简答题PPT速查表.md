# CS5285 简答题 PPT 速查表

> 考试时翻到对应页，直接抄原句

---

## 1. 威胁→服务→机制框架

**PPT位置**: Lecture 1, 第17-20页

### 原句（直接抄）

**Confidentiality**:
> "prevention of unauthorised disclosure of information"

**Integrity**:
> "prevention of unauthorised modification of information"

**Availability**:
> "prevention of unauthorised withholding of information or resources"

**威胁对应**:
> - "Exposure of data: the threat that someone who is unauthorised can access the data."
> - "Tampering with data: the threat that the data could be altered from what it should be."
> - "Denial of service: the threat that the data or service is unavailable when it is required."

**服务→机制**:
> - Confidentiality → **encryption**
> - Integrity → **MAC/digital signature**
> - Availability → **redundancy**
> - Entity Authentication → **authentication protocol**
> - Non-repudiation → **digital signature**

### 例题：ex01 Q1 填表

| Threat | Service | Algorithm |
|--------|---------|-----------|
| Exposure of data | Confidentiality | AES |
| Tampering with data | Integrity | HMAC |
| Repudiation | Non-repudiation | RSA/DSA |

**答案**：
1. Exposure of data
2. Tampering with data
3. Repudiation
4. Integrity
5. Digital Signature

### 例题：ex01 Q2a Availability

**Question**: What does Availability do? Give an example in e-commerce.

**Answer**:
> Availability prevents unauthorised withholding of information or resources. It ensures systems and data are accessible when needed.
> Example: A DDoS attack that makes an e-commerce website unavailable to legitimate customers.

### 例题：ex01 Q3 在线报纸场景

**Question**: Three problems: password sharing, payment data stolen, content modified. Which security concepts apply?

**Answer**:
> **Problem 1** (password sharing): This is an **authentication** problem. The system cannot verify that the person logging in is the legitimate subscriber. Solution: multi-factor authentication.
> 
> **Problem 2** (payment data stolen): This is a **confidentiality** problem. Payment data is transmitted without encryption. Solution: use TLS/SSL to encrypt data.
> 
> **Problem 3** (content modified): This is an **integrity** problem. The system cannot detect data modification. Solution: use digital signature or MAC to verify content integrity.

### 例题：ex01 Q4a 软件完整性

**Question**: Customers worry software is modified. What security service? What mechanism?

**Answer**:
> **Security service**: Integrity
> 
> **Mechanism**: Digital signature or hash function. The vendor signs the software using a digital signature (e.g., RSA). Customers verify the signature using the vendor's public key. If the software is modified, the signature verification will fail.

### 例题：ex01 Q4b 不可否认性

**Question**: Customers deny receiving software. What security service? What mechanism?

**Answer**:
> **Security service**: Non-repudiation
> 
> **Mechanism**: Digital signature. The vendor requires customers to sign a receipt using their private key. The signature proves that the customer received the software. Since only the customer has the private key, they cannot deny sending the signature.

### 例题：ex01 Q5 使用标准

**Question**: Why use existing standards instead of developing your own?

**Answer**:
> 1. **Security**: Standards are peer-reviewed and tested by experts. Custom solutions may have vulnerabilities.
> 2. **Interoperability**: Standards ensure compatibility with other systems.
> 3. **Cost-effective**: Using standards saves development time and reduces risk.
> 4. **Compliance**: Many industries require compliance with specific standards.

---

## 2. CBC vs CTR 错误传播

**PPT位置**: Lecture 2 (需要找CBC/CTR章节)

### 原句（直接抄）

**CBC 1-bit error**:
> "In CBC mode, **two blocks** are affected: the current block is completely garbled and the next block has the corresponding bit flipped."

**CTR 1-bit error**:
> "In CTR mode, only **one block** is affected: the corresponding bit in that block is flipped."

**CBC block lost**:
> "In CBC mode, one block is missing and one block is garbled, but subsequent blocks decrypt correctly (though shifted)."

**CTR block lost**:
> "In CTR mode, **all subsequent blocks are wrong** because the counter is desynchronized."

**Update efficiency**:
> "CTR is more efficient. In CBC mode, updating a record requires **re-encrypting all subsequent blocks** due to the chaining dependency. In CTR mode, only the **corresponding block** needs to be modified because each block is encrypted independently."

---

## 3. CTR 做 MAC 不安全

**PPT位置**: Lecture 5, 第29-30页附近

### 原句（直接抄）

> "CTR MAC is not secure because of **known-plaintext attack**. If the attacker knows plaintext P and ciphertext C, they can **recover the keystream**: KS = C ⊕ P. Then they can **forge a new ciphertext**: C' = C ⊕ P ⊕ P' to change the plaintext to P'. Since CTR encrypts each block **independently**, the MAC value (last ciphertext block) remains **unchanged**, so the modification is not detected."

---

## 4. MAC 不可否认性

**PPT位置**: Lecture 5, 第30页

### 原句（直接抄）

> "**No**. MAC uses a **symmetric key shared between two parties**. Since **both parties can generate** the same MAC value, it **cannot prove who sent** the message. Therefore, MAC cannot provide non-repudiation."

**对比数字签名**:
> "Digital signature uses an **asymmetric key pair**. Only the **private key holder** can generate a valid signature, so it **can provide non-repudiation**."

---

## 5. RSA 签名长度限制

**PPT位置**: Lecture 5, 第10页

### 原句（直接抄）

> "The largest message we can sign is **less than n** (otherwise modular arithmetic fails). In practice, we **hash the message first** using a **hash function** (e.g., SHA-256), then sign the hash value. This allows us to sign messages of **any length**."

---

## 6. Hash 验证文件相同

**PPT位置**: Lecture 5, 第13-14页

### 原句（直接抄）

> "Calculate the **hash value** (e.g., SHA-256) of both pictures. If the hash values are **identical**, the two pictures are the same (with negligible collision probability)."

**不要用 signature**:
> "Hash function does not provide any security services by itself. Anyone can calculate a hash (no key, known algorithm). It supports other mechanisms and can detect accidental modification."

---

## 7. 认证协议分析

**PPT位置**: Lecture 6, 第20-24页

### 原句（直接抄）

**分析框架**:
> "Entity authentication requires **freshness** and **data origin authentication**."

**Freshness**:
> "Freshness means the message was **recently generated**. We check freshness using **nonce** or **timestamp**."

**Data origin authentication**:
> "Data origin authentication means verifying the **source of data**. We check this using **signature** or **MAC**."

**分析模板**:
> - Message 1: A→B: RA, (RA)^A_sign
>   - Freshness: ❌ (RA is generated by A, not fresh)
>   - Data origin auth: ✅ (A signed RA)
>   - Conclusion: A is not authenticated to B
> 
> - Message 2: A←B: RB, (RA)^B_sign
>   - Freshness: ✅ (RB is generated by B, fresh)
>   - Data origin auth: ✅ (B signed RA)
>   - Conclusion: B is authenticated to A
> 
> - Overall: **Unilateral authentication** (B→A)

### 例题：认证协议分析

**Question**: Analyze this authentication protocol:
- Message 1: A→B: RA, Sign_A(RA)
- Message 2: B→A: RB, Sign_B(RA)

**Answer**:
> Entity authentication requires **freshness** and **data origin authentication**.
> 
> **Message 1**: A sends RA and Sign_A(RA).
> - Freshness: ❌ (RA is generated by A, not fresh for B)
> - Data origin auth: ✅ (A signed RA, proves A sent it)
> - Conclusion: A is not authenticated to B
> 
> **Message 2**: B sends RB and Sign_B(RA).
> - Freshness: ✅ (RB is generated by B, recently created)
> - Data origin auth: ✅ (B signed RA, proves B sent it)
> - Conclusion: B is authenticated to A
> 
> **Overall**: **Unilateral authentication** (B authenticated to A only)

---

## 8. 完美保密 vs 计算安全

**PPT位置**: Lecture 2 (需要找相关章节)

### 原句（直接抄）

> "**Perfect secrecy** means the ciphertext gives **no information** about the plaintext, even with **unlimited computing power**. Example: One-Time Pad."

> "**Computational security** means breaking the encryption is **computationally infeasible** with current technology, but may be possible with future advances or more computing power."

### 例题：完美保密 vs 计算安全

**Question**: Explain the difference between perfect secrecy and computational security.

**Answer**:
> **Perfect secrecy** means the ciphertext gives **no information** about the plaintext, even with **unlimited computing power**. Example: One-Time Pad (OTP).
> 
> **Computational security** means breaking the encryption is **computationally infeasible** with **current technology**, but may be possible with **future advances** or more computing power. Example: AES-256.

**关键词**：
- Perfect secrecy → **no information** + unlimited power
- Computational security → **infeasible now** + possible later

---

## 9. Hash 性质区分

**PPT位置**: Lecture 5, 第14-17页

### 原句（直接抄）

**One-way (pre-image resistance)**:
> "Given a hash value y, it is **infeasible to find** an x such that h(x) = y."

**Second pre-image resistance**:
> "Given y and h(y), **cannot find** x where h(x) = h(y)."

**Collision resistance**:
> "Infeasible to find x and y, with x ≠ y, such that h(x) = h(y)."

**Birthday attack**:
> "N-bit hash requires **2^(N/2)** work to break (with respect to collision resistance)."

**Bitcoin mining**:
> "Bitcoin mining is about finding a nonce such that the hash has certain properties. This is a **pre-image** problem (one-way), not a collision problem."

---

## 10. DES 暴力破解复杂度

**PPT位置**: Lecture 2 (需要找DES章节)

### 原句（直接抄）

> "DES has a **56-bit key**. Brute force attack requires trying **2^56** keys on average (or **2^55** if we stop at the first match)."

> "Note: It is **2^55**, not 2^(N-1) where N is the key length."

---

## 11. 3DES 密钥空间

**PPT位置**: Lecture 2 (需要找3DES章节)

### 原句（直接抄）

> "3DES uses **112-bit key** (two 56-bit keys: K1, K2). Encryption: C = E(K1, D(K2, E(K1, M))). Brute force requires **2^111** operations."

---

## 12. ElGamal 加密

**PPT位置**: Lecture 4, 第16-18页

### 原句（直接抄）

**Public key**: y = g^x mod p

**Encryption**:
> 1. Pick random r
> 2. C1 = g^r mod p
> 3. C2 = M · y^r mod p
> 4. Ciphertext C = (C1, C2)

**Decryption**:
> 1. K = C1^x mod p
> 2. M = C2 · K^(-1) mod p

---

## 13. DH 密钥交换

**PPT位置**: Lecture 4, 第23页

### 原句（直接抄）

> "Alice chooses private key a, computes A = g^a mod p, sends A to Bob."
> "Bob chooses private key b, computes B = g^b mod p, sends B to Alice."
> "Alice computes K = B^a mod p = g^(ab) mod p."
> "Bob computes K = A^b mod p = g^(ab) mod p."
> "Both get the same shared key K = g^(ab) mod p."

**中间人攻击防护**:
> "DH is insecure against **man-in-the-middle attack** if the attacker is active. To prevent this, we add **digital signature** with **timestamp** to authenticate the exchanged values."

---

## 14. 离散对数问题 (DLP)

**PPT位置**: Lecture 4, 第22页

### 原句（直接抄）

> "Given g, y, and p, find a such that g^a mod p = y. This is the **Discrete Logarithm Problem (DLP)**."

> "Computing g^a mod p is **easy**, but finding a given y is **hard** when p is large."

> "If we can solve DLP, we can **break ElGamal encryption** because we can find the private key x from the public key y = g^x mod p."

---

## 15. CBC-MAC 伪造

**PPT位置**: Lecture 5, 第33-34页

### 原句（直接抄）

> "Given two (message, MAC) pairs: (P', T') and (P'', T''), where P' = P1, P2 and P'' = P3."

> "Attack: forge (P''', T''') without knowing the key K by setting:"
> - P''' = P1, P2, P3 ⊕ T'
> - T''' = T''

> "This works because CBC-MAC uses **chaining**, and we can choose P3 ⊕ T' to make the intermediate state match."

---

## 快速检查表

| 题目类型 | 看到关键词 | PPT位置 | 必须回答的原句 |
|---------|-----------|---------|---------------|
| 威胁→服务→机制 | "security service", "mechanism" | L1 p17-20 | Confidentiality→encryption, Integrity→MAC/signature |
| CBC 1bit错 | "one bit error" | L2 | "two blocks affected" |
| CBC块丢失 | "block lost" | L2 | "missing one + garbled one" |
| 更新效率 | "update", "efficient" | L2 | "CTR only modify corresponding block" |
| CTR做MAC | "MAC", "CTR", "secure" | L5 p29-30 | "KS=C⊕P, C'=C⊕P⊕P'" |
| MAC不可否认 | "non-repudiation", "MAC" | L5 p30 | "No, symmetric key, both can generate" |
| RSA签名长度 | "largest message" | L5 p10 | "<n, hash-then-sign" |
| 验证文件相同 | "prove same", "integrity" | L5 p13-14 | "Calculate hash, compare" |
| 认证协议 | "authentication protocol" | L6 p20-24 | "freshness + data origin auth" |
| 完美保密 | "perfect secrecy" | L2 | "no info even unlimited power" |
| Hash性质 | "one-way", "collision" | L5 p14-17 | "pre-image: 2^N, collision: 2^(N/2)" |
| DES复杂度 | "DES", "brute force" | L2 | "2^55, not 2^(N-1)" |
| 3DES密钥空间 | "3DES", "key space" | L2 | "112-bit, 2^111" |
| ElGamal | "encrypt", "ElGamal" | L4 p16-18 | "C=(g^r, M·y^r)" |
| DH中间人 | "DH", "MITM" | L4 p23 | "add signature + timestamp" |
| DLP | "discrete log", "ElGamal" | L4 p22 | "find a from g^a=y, hard" |
| CBC-MAC伪造 | "CBC-MAC", "forge" | L5 p33-34 | "P3⊕T', match intermediate state" |

---

**最后更新**: 2026-10-22  
**使用建议**: 考试时看到题目，先判断类型，翻到对应PPT页，直接抄原句

---
---

# 附录：术语速查表（考试专用）

> 带★的是高频考点，必须熟记公式和题目

## 一、安全服务与机制

| 术语 | 中文 | 定义/公式 | 对应机制 |
|------|------|-----------|----------|
| Confidentiality | 机密性 | 防止未授权泄露 | Encryption (AES/DES) |
| Integrity | 完整性 | 防止未授权修改 | MAC / Digital Signature |
| Availability | 可用性 | 防止拒绝服务 | 冗余/备份 |
| Authentication | 认证 | 验证身份 | 登录协议/证书 |
| Non-repudiation★ | 不可否认性 | 发送方不能否认发送 | Digital Signature (RSA/DSA) |
| Data origin auth | 数据来源认证 | 验证数据来自谁 | MAC / Signature |
| Entity auth | 实体认证 | 验证"你是谁" | 登录协议 |

## 二、对称加密术语

| 术语 | 中文 | 定义/公式 | 例题 |
|------|------|-----------|------|
| Stream Cipher | 流密码 | Cᵢ = Pᵢ ⊕ KSᵢ（密钥流XOR） | MT2025 Q1 |
| Block Cipher | 分组密码 | 固定长度分组加密 | ps1 Q2 |
| One-Time Pad (OTP)★ | 一次一密 | C = P ⊕ K，完美保密 | MT2025 Q1(a) |
| Perfect secrecy★ | 完美保密 | 无限算力也破不了 | MT2025 Q5(b) |
| Computationally secure | 计算安全 | 实际算力破不了 | MT2025 Q5(b) |
| IV (Initialization Vector) | 初始化向量 | 让相同明文加密结果不同 | ps1 Q2 |

## 三、分组密码模式★

### CBC (Cipher Block Chaining)

| 术语 | 公式 | 特点 |
|------|------|------|
| 加密 | Cᵢ = E_K(Pᵢ ⊕ Cᵢ₋₁), C₀=IV | 链式依赖 |
| 解密 | Pᵢ = Cᵢ₋₁ ⊕ D_K(Cᵢ) | 需要解密函数 |
| 1bit错误 | 2块受影响 | 当前块全乱+下一块对应位翻转 |
| 块丢失 | 缺1乱1 | 丢当前块+下一块乱 |
| 数据库更新 | 需重加密后续 | 效率低 |

### CTR (Counter Mode)

| 术语 | 公式 | 特点 |
|------|------|------|
| 加密 | Cᵢ = Pᵢ ⊕ E_K(Counterᵢ) | 独立加密 |
| 解密 | Pᵢ = Cᵢ ⊕ E_K(Counterᵢ) | 只需加密函数 |
| 1bit错误 | 1块对应位翻转 | 错误传播少 |
| 块丢失 | 后续全错 | 计数器失同步 |
| 数据库更新 | 只改对应块 | 效率高 |

### CBC vs CTR 对比★（必考）

| 特性 | CBC | CTR |
|------|-----|-----|
| 解密函数 | D_K（解密） | E_K（加密） |
| 并行加密 | ❌ 不能 | ✅ 能 |
| 1bit错误 | 2块受影响 | 1块受影响 |
| 块丢失 | 缺1乱1 | 后续全错 |
| 数据库效率 | 低 | 高 |
| MAC安全性 | ✅ 较安全 | ❌ 不安全 |

## 四、攻击类型

| 术语 | 中文 | 定义 | 例题 |
|------|------|------|------|
| Known-plaintext attack★ | 已知明文攻击 | 知道部分明文→恢复密钥流 | MT2025 Q1(b) |
| Frequency analysis★ | 频率分析 | 最频繁字母→'e'，推密钥 | MT2025 Q1(c) |
| Birthday attack★ | 生日攻击 | n位Hash→碰撞2^(n/2) | MT2025 Q5(e) |
| Brute force | 暴力破解 | 尝试所有密钥 | MT2025 Q5(d) |
| Man-in-the-middle (MitM)★ | 中间人攻击 | 拦截并替换公钥 | ps1 Q5(d) |

### 已知明文攻击公式★

```
已知: 部分明文 P_old 和密文 C
算出: 密钥流 KS = C ⊕ P_old
伪造: 新密文 C' = P_new ⊕ KS = C ⊕ P_old ⊕ P_new
```

## 五、数论工具

| 术语 | 中文 | 公式/算法 | 例题 |
|------|------|-----------|------|
| Square-and-Multiply★ | 平方乘法 | 指数转二进制，迭代平方+乘 | ps1 Q3(a) |
| Euclidean Algorithm | 欧几里得算法 | y=qx+r迭代，求GCD | ps1 Q3(c) |
| Extended Euclidean★ | 扩展欧几里得 | 回代ax+by=1，求逆元 | ps1 Q3(d)(e) |
| Euler's totient φ(n)★ | 欧拉函数 | φ(p)=p-1, φ(pq)=φ(p)φ(q) | ps1 Q3(b) |
| Fermat's little theorem | 费马小定理 | a^(p-1)≡1 (mod p) | ex05 Q2 |
| Discrete Log Problem (DLP)★ | 离散对数问题 | 已知y=g^x mod p，求x | MT2025 Q3(b) |

## 六、非对称加密

| 术语 | 中文 | 公式 | 例题 |
|------|------|------|------|
| RSA★ | RSA加密/签名 | n=pq, φ(n)=(p-1)(q-1), ed≡1 | MT2025 Q3(a) |
| ElGamal | ElGamal加密 | (c₁,c₂)=(g^r, M·y^r) | ps1 Q4 |
| Diffie-Hellman★ | DH密钥交换 | K=B^x=A^y=g^xy | ps1 Q5 |

### RSA 计算步骤★

```
1. 选素数 p, q
2. n = p × q
3. φ(n) = (p-1)(q-1)
4. 选 e 使 gcd(e, φ(n)) = 1
5. 求 d 使 ed ≡ 1 (mod φ(n))

加密: C = M^e mod n
签名: S = M^d mod n
验证: M = S^e mod n
```

### ElGamal 计算步骤

```
密钥生成: y = g^x mod p (x私钥, y公钥)
加密: (c₁, c₂) = (g^r mod p, M·y^r mod p)
解密: M = c₂ · (c₁^x)^(-1) mod p
```

## 七、Hash与MAC

| 术语 | 中文 | 定义 | 例题 |
|------|------|------|------|
| Hash function | 哈希函数 | 单向指纹，固定长度输出 | ex05 Q2 |
| Pre-image resistance★ | 单向性 | 已知h(x)难找x | MT2025 Q5(c) |
| Collision resistance★ | 抗碰撞性 | 难找x≠y使h(x)=h(y) | MT2025 Q5(e) |
| MAC | 消息认证码 | 完整性+来源认证 | MT2025 Q4(a) |
| CBC-MAC | CBC模式MAC | 基于分组密码的MAC | ex05 Q4 |

### Hash性质区分★

| 性质 | 定义 | 应用 |
|------|------|------|
| Pre-image (单向性) | 已知h，难找x使Hash(x)=h | Bitcoin挖矿 |
| Second pre-image | 已知x，难找y≠x使Hash(y)=Hash(x) | 文件签名 |
| Collision | 难找任意x≠y使Hash(x)=Hash(y) | 生日攻击 |

### MAC vs 数字签名★

| 特性 | MAC | 数字签名 |
|------|-----|----------|
| 密钥 | 对称（共享） | 非对称（公/私钥） |
| 不可否认性 | ❌ 不能 | ✅ 能 |
| 性能 | 快 | 慢 |
| 应用 | 内部通信 | 公开验证 |

## 八、常见陷阱★

| 陷阱 | 正确理解 |
|------|----------|
| Perfect secrecy = 计算安全？ | ❌ 完美保密=无限算力破不了(OTP) |
| DES密钥64位？ | ❌ 56位（8位奇偶校验） |
| Hash相同=文件相同？ | ✅ 碰撞概率可忽略 |
| Bitcoin=碰撞攻击？ | ❌ 是原像攻击（单向性） |
| CTR做MAC安全？ | ❌ 已知明文→恢复密钥流→伪造 |
| RSA签名长度无限制？ | ❌ 消息≤n，大消息先Hash |

## 九、公式速查（考前必看）

### 对称加密
```
CBC: Cᵢ = E_K(Pᵢ ⊕ Cᵢ₋₁)
CTR: Cᵢ = Pᵢ ⊕ E_K(Counterᵢ)
OTP: C = P ⊕ K
已知明文攻击: C' = C ⊕ P_old ⊕ P_new
```

### 数论
```
快速幂: 指数转二进制，迭代平方+乘
GCD: y=qx+r 迭代
逆元: 扩展欧几里得 ax+by=1
φ(n): φ(p)=p-1, φ(pq)=φ(p)φ(q)
费马: a^(p-1)≡1 (mod p)
```

### 非对称
```
RSA: n=pq, φ(n)=(p-1)(q-1), ed≡1
ElGamal: (c₁,c₂)=(g^r, M·y^r), M=c₂·(c₁^x)^(-1)
DH: K=B^x=A^y=g^xy
```

### 攻击复杂度
```
DES暴力: 2^55 (56位密钥)
生日攻击: 2^(n/2) (n位Hash)
原像攻击: 2^n
```
