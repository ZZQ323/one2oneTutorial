Q6 File3 — 6位密码搜索空间 62^6 ≈ 568亿，这里跑不完。在你的 Windows 上运行：

─ cmd
hashcat -m 20 -a 3 -D 2 file3.txt -1 ?l?u?d ?1?1?1?1?1?1

（-D 2 用 GPU，约30分钟-2小时；-D 1 用 CPU 要5-10小时）

Q7 PGP 邮件 — 安装 Thunderbird → 创建密钥 → 导入 tsgexercise_cert.asc →发送加密签名邮件到 tsgexercise@gmail.com，主题含学号。