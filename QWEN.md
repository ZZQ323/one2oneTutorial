# QWEN.md — one2oneTutorial（CityuTest）仓库指南

## 仓库概览

这是一个**非代码型个人学习资料仓库**（README 标题为 "CityuTest"），由 git 管理。所有者是香港城市大学（CityU）研究生 Zhanquan Zhuang（学号 60209978）。

仓库的核心用途是：**与 AI Agent 一对一协作，制作和维护课程学习笔记、备考材料（考点清单、复习计划、错题本、模拟卷、速查表），以及完成作业/演示文稿类交付物**。这里没有可构建、可测试的软件工程项目的主体，只有少量一次性的 Python 工具脚本。

内容语言约定：笔记正文为**中文**，专业术语保留**英文**原文（如 Confidentiality、Sliding Window、CRC）。

## 目录结构与内容

```
one2oneTutorial/
├── README.md                  # 仅一行标题 "# CityuTest"
├── QWEN.md                    # 本文件
├── .gitattributes             # *.onnx 走 Git LFS
├── .gitignore                 # 目前为空
├── .agent/                    # ⚠️ 多 Agent 协作手册，来自另一个项目（PetCare Android），仅作方法论参考
│   ├── mainAgent.md           # 主 Agent 工作手册（架构师+协调者定位、任务拆分原则）
│   ├── subAgent.md            # 子 Agent 工作手册
│   ├── RETROSPECTIVE.md       # 迭代复盘报告
│   └── lessons-learned-*.md   # 迭代教训记录
├── cityU/                     # 三门课程的全部资料（按课程代码组织）
│   ├── CS5285_Introduction to Cybersecurity/
│   ├── EE5609_CSNetwkArcht_Proto_Apns/
│   └── EE8403/
└── javaAgent/
    └── 学习路线.md            # Java 学习路线（Bilibili BV 号清单，非本仓库工作产物）
```

### cityU/CS5285_Introduction to Cybersecurity（信息安全导论）

| 内容 | 说明 |
|------|------|
| `复习计划.md` | 整合版复习计划：考试信息、知识体系（威胁→服务→机制框架）、考点进度（如 34/41） |
| `exam_points.jsonl` | 考点清单（JSONL，schema 见下文） |
| `简答题PPT速查表.md/.pdf`、`简答题错题本.md`、`算法框架与Q&A.md/.pdf` | 应考速查与错题材料，md 与 pdf 成对出现 |
| `.pass_all_exams/state.json` | 备考工作流状态文件 |
| `lesson_notes/1..6 主题/` | 按主题编号组织的课件 PDF/PPTX + 习题(ex0X.pdf)与解答(ex0X_sol.pdf) |
| `problem_set_1/`、`problem_set_2/` | 作业：题目 PDF/截图、解答 md、提交 PDF（文件名含学号姓名）、完成指南/最终状态 md |
| `stu-share/` | 按课次编号（01-11）的「课件扩展讲解」PDF（同学分享/自制讲义） |
| `期中考试/` | 历年真题 PDF + `MT2025_题目.md`（真题的 markdown 转录） |

### cityU/EE5609_CSNetwkArcht_Proto_Apns（计算机网络架构与协议）

| 内容 | 说明 |
|------|------|
| `知识地图.md` | 以「一个数据包的旅程」为主线串联全部考点，考点以 (P编号) 交叉引用 |
| `笔记v2.md`、`English_Cheat_Sheet.md` | 主笔记与英文速查表 |
| `.pass_all_exams/` | 最完整的备考状态目录：`state.json`、`cards.jsonl`（记忆卡）、`errors.jsonl`（错题）、`sessions.jsonl`（复习会话记录）、`materials/L1-L7.md`（按讲次整理的材料） |
| `pdf_extracted/` | 每讲课件 PDF + 提取出的文本（`*_extracted.txt` 或 `.md`） |
| `iamge/` | ⚠️ 目录名是拼写错误（应为 image），存放从 PDF 提取的插图 jpeg + `EE5609_L3_meta.json`；md 文件可能引用此路径，重命名前须全局检查 |
| `mid1/`、`mid2/`、`test2/` | 期中真题、自编模拟卷（MockHard-predict）及答案、quiz 记录 |
| `presentation/` | 小组论文演示（RFBus 主题）：PPTX、演讲稿 docx、`papers/` 原文 PDF、EndNote 库、`images/` 自制配图（原图+优化版成对）、DOI 列表、个人报告 `prepare/60209978_ZhuangZhanquan_IndividualReport.md`、`downloads/download_papers.py`（一次性下载脚本） |

### cityU/EE8403（机器学习在信号处理中的应用）

| 内容 | 说明 |
|------|------|
| `README_EE8403课程总结.md`、`course_summary.md` | 完整课程总结（师资、逐讲内容、作业与考试要求） |
| `course_analysis.json`、`assignments_and_exams.md` | 课程结构分析与作业/考试说明 |
| `extract_text.py` | 一次性 PDF/PPTX 文本提取脚本 |
| `course_files_export/` | 各讲课件原件（PDF/PPTX） |
| `extracted_texts/` | 课件提取文本（每讲一个 .txt + `extraction_results.json`） |
| `hw1_export/` | HMM/Viterbi 作业：数据文件（.hmm/.fa/.positions）、`viterbi_parser.py`、提交物 `zhuang-zhanquan-60209978-hw4.ipynb/.html`、`my_output.txt`；含 PyCharm 的 `.idea/` 目录 |

## 关键数据格式：`.pass_all_exams` 备考工作流

每门课可有 `.pass_all_exams/` 目录（CS5285 的考点清单放在课程根目录的 `exam_points.jsonl`），这是「通过所有考试」备考流程的状态存储：

**考点条目 schema**（`exam_points.jsonl` 每行一个 JSON，或 `state.json` 的 `points` 字段）：

```json
{"id":"P1","topic":"考点主题","formula":"公式/结论速记","source":"PPT1/Ex2/L2 等来源",
 "priority":"high|medium|low","type":"calculation|concept","status":"pending|done"}
```

**`state.json` 顶层字段**：`course`、`slug`、`created_at`/`updated_at`、`mode`、`stage`（如 review）、`exam_type`（闭卷/开卷、题型）、`exam_date`、`counts`（points_total/points_done/errors/stubborn/cards/materials 汇总）、`points`（P编号 → 考点对象）。

配套文件：`cards.jsonl`（记忆卡）、`errors.jsonl`（错题记录）、`sessions.jsonl`（复习会话日志）、`materials/L*.md`（分讲材料）。

**维护规则**：更新考点状态、新增错题或完成复习会话时，必须同步更新 `state.json` 的 `counts` 与 `updated_at`，保持汇总与明细一致。

## 使用方式（Agent 在此仓库的典型任务）

1. **备考材料迭代**：更新复习计划/知识地图/速查表；将真题、课件、习题整理为带 (P编号) 交叉引用的考点；出模拟卷并附答案；把做错的题记入错题本（`errors.jsonl` / `简答题错题本.md`）并更新 state。
2. **课件文本化**：用 `extract_text.py` 类脚本或 marker 等工具把 PDF/PPTX 提取到 `extracted_texts/`、`pdf_extracted/`，供后续整理引用；插图提取到 `iamge/`（EE5609）。
3. **作业交付**：在对应 `problem_set_*/`、`hw1_export/`、`presentation/` 目录内完成解答 md → 导出提交 PDF；提交文件命名遵循 **`学号_姓名` 前缀**（如 `60209978_Zhanquan Zhuang.pdf`、`zhuang-zhanquan-60209978-hw4.ipynb`）。
4. **新增课程**：在 `cityU/` 下新建 `课程代码_课程名/` 目录，沿用上述结构（课件、考点、真题、作业分目录；必要时建 `.pass_all_exams/`）。

## 注意事项与约定

- **没有构建/测试命令**。Python 脚本（`extract_text.py`、`viterbi_parser.py`、`download_papers.py` 等）都是一次性工具，按需直接 `python <脚本>` 运行，无依赖清单文件。
- **大量二进制文件**（PDF/PPTX/DOCX/jpeg）是原始课件与提交物，属于用户资产：不要改写、重新生成或"优化"它们；md 与 pdf 成对的文件（如 速查表.md/.pdf）更新 md 后如需同步 pdf，先询问用户。
- **`.agent/` 手册描述的是另一个项目（PetCare Android 作业）的多 Agent 工作流**，其中项目结构、Gradle 命令、高德 SDK 教训均与本仓库无关，只借鉴其方法论（任务拆分、迭代文档、教训记录）。
- `iamge/`（EE5609）是既成事实的拼写错误目录，笔记中可能已有相对路径引用，不要擅自重命名。
- **Git 约定**：提交信息为简短中文短语（如 "识别 EE8403"、"信息安全最后兵器"、"ps2"）；`*.onnx` 使用 Git LFS；`.gitignore` 目前为空，新增敏感文件（token 等）前先补 ignore 条目。
- 会话产生的中间产物（脚本、日志、截图）一律放在本仓库目录树内，禁止写入系统 Temp/C 盘路径。
