#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 EE5415 机考模拟题文档本身是否合格。

用法：
    python check_paper.py

判据：
    P1 文档存在
    P2 含 A / B / C 三段
    P3 场景数 >= 9，且总览表里的每个场景都有对应正文小节
    P4 含「验收清单」，且清单编号与 check_acceptance.py 的 CHECKS 完全一致（双向）
    P5 正文不含 java / xml / kotlin / gradle 代码块（只允许 bash / text 等命令行与模板）
    P6 正文不含明显的「答案代码」特征（如 setContentView(...) 完整调用、new SQLiteOpenHelper 实现体）
"""

from __future__ import annotations

import importlib.util
import os
import re
import sys

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(
    os.path.dirname(HERE),
    "cityU",
    "EE5415_MobileApnsDesignAndDevemt",
    "exam",
    "机考模拟题_ReadTrack.md",
)
CHECKER = os.path.join(HERE, "check_acceptance.py")

ALLOWED_FENCE_LANGS = {"", "bash", "sh", "shell", "console", "text", "cmd", "powershell"}
FORBIDDEN_FENCE_LANGS = {"java", "xml", "kotlin", "gradle", "groovy", "json", "javascript", "js"}

results: list[tuple[str, bool, str]] = []


def record(pid: str, ok: bool, detail: str) -> bool:
    results.append((pid, ok, detail))
    return ok


def load_check_ids() -> set[str]:
    spec = importlib.util.spec_from_file_location("check_acceptance", CHECKER)
    if spec is None or spec.loader is None:
        return set()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return {cid for cid, _stage, _level, _desc, _f in module.CHECKS}


def main() -> int:
    print("=" * 78)
    print(f"题目文档 : {PAPER}")
    print(f"验收脚本 : {CHECKER}")
    print("=" * 78)

    if not os.path.isfile(PAPER):
        record("P1", False, "题目文档不存在")
    else:
        record("P1", True, f"文档存在，{os.path.getsize(PAPER)} 字节")

    text = ""
    if os.path.isfile(PAPER):
        with open(PAPER, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()

    # P2 三段
    stages = [s for s in ("A", "B", "C") if re.search(r"^# " + s + r" 段", text, re.M)]
    record("P2", len(stages) == 3, f"找到的一级段落: {stages or '无'}")

    # P3 场景
    sections = re.findall(r"^## ([ABC]\d)\s+(.+)$", text, re.M)
    overview = re.findall(r"^\| ([ABC]\d) \|", text, re.M)
    ids = [cid for cid, _t in sections]
    missing_body = sorted(set(overview) - set(ids))
    missing_table = sorted(set(ids) - set(overview))
    ok3 = len(ids) >= 9 and not missing_body and not missing_table
    detail3 = f"正文小节 {len(ids)} 个: {', '.join(ids)}"
    if missing_body:
        detail3 += f"；总览表有但正文缺: {missing_body}"
    if missing_table:
        detail3 += f"；正文有但总览表缺: {missing_table}"
    record("P3", ok3, detail3)

    # P4 验收清单与脚本一致
    doc_ids = set(re.findall(r"^\| ((?:[ABC]\d|G)-\d+) \|", text, re.M))
    script_ids = load_check_ids()
    only_doc = sorted(doc_ids - script_ids)
    only_script = sorted(script_ids - doc_ids)
    ok4 = bool(script_ids) and not only_doc and not only_script
    detail4 = f"文档清单 {len(doc_ids)} 条，脚本检查 {len(script_ids)} 条"
    if only_doc:
        detail4 += f"；只在文档里: {only_doc}"
    if only_script:
        detail4 += f"；只在脚本里: {only_script}"
    record("P4", ok4, detail4)

    # P5 代码块语言
    fences = re.findall(r"^```([A-Za-z0-9_+-]*)", text, re.M)
    # 成对出现，取奇数位（开栏）的语言标记
    opens = fences[0::2]
    bad = sorted({lang.lower() for lang in opens if lang.lower() in FORBIDDEN_FENCE_LANGS})
    unknown = sorted({lang.lower() for lang in opens if lang.lower() not in ALLOWED_FENCE_LANGS})
    ok5 = not bad and not unknown
    record(
        "P5",
        ok5,
        f"代码块 {len(opens)} 个，语言标记 = {sorted(set(opens)) or '（无标记）'}"
        + (f"；禁止的语言: {bad}" if bad else "")
        + (f"；未列入白名单: {unknown}" if unknown else ""),
    )

    # P6 答案代码特征
    leak_patterns = {
        "setContentView 完整调用": r"setContentView\s*\(",
        "findViewById 完整调用": r"findViewById\s*\(\s*R\.",
        "SQLiteOpenHelper 实现体": r"public\s+\w+\s*\(\s*Context\s+\w+\s*\)\s*\{\s*super\s*\(",
        "new RecyclerView.Adapter 实现": r"new\s+RecyclerView\.Adapter",
        "onDraw 实现体": r"protected\s+void\s+onDraw\s*\(",
        "FragmentTransaction 完整链": r"beginTransaction\s*\(\s*\)\s*\.",
        "openFileOutput 完整调用": r"openFileOutput\s*\(\s*\"",
    }
    code_text = text
    for name, pat in leak_patterns.items():
        if re.search(pat, code_text):
            record("P6", False, f"文档正文疑似含实现代码: {name}")
            break
    else:
        record("P6", True, "未发现实现代码特征（仅需求描述与 grep 模式）")

    fails = 0
    for pid, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        if not ok:
            fails += 1
        print(f"[{status}] {pid}")
        print(f"         └─ {detail}")

    print("=" * 78)
    print(f"SUMMARY PASS={len(results) - fails} FAIL={fails}")
    print(f"RESULT: FAIL={fails}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
