#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EE5415 机考模拟题 ReadTrack —— 静态验收脚本。

用法：
    python check_acceptance.py <工程根目录> [--stage A|B|C|G|all]

只做源码静态扫描，不编译、不运行模拟器。
构建验收请自行执行：gradlew.bat assembleDebug
"""

from __future__ import annotations

import argparse
import os
import re
import sys

try:
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
except Exception:
    pass

LEVEL_REQUIRED = "必需"
LEVEL_BONUS = "加分"
LEVEL_WARN = "警告"

STATUS_PASS = "PASS"
STATUS_FAIL = "FAIL"
STATUS_MISS = "MISS"
STATUS_WARN = "WARN"


def strip_java_comments(text: str) -> str:
    """去掉 Java 的 // 与 /* */ 注释，保留字符串字面量原样。

    逐字符扫描并跟踪「在字符串里 / 在字符字面量里 / 在注释里」三种状态，
    这样 "http://xxx" 这种含 // 的字符串不会被误删。
    """
    out: list[str] = []
    i, n = 0, len(text)
    in_str = in_chr = in_line = in_block = False
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if in_line:
            if ch == "\n":
                in_line = False
                out.append(ch)
            i += 1
            continue
        if in_block:
            if ch == "*" and nxt == "/":
                in_block = False
                i += 2
                continue
            if ch == "\n":
                out.append(ch)
            i += 1
            continue
        if in_str:
            out.append(ch)
            if ch == "\\" and nxt:
                out.append(nxt)
                i += 2
                continue
            if ch == '"':
                in_str = False
            i += 1
            continue
        if in_chr:
            out.append(ch)
            if ch == "\\" and nxt:
                out.append(nxt)
                i += 2
                continue
            if ch == "'":
                in_chr = False
            i += 1
            continue
        if ch == "/" and nxt == "/":
            in_line = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            in_block = True
            i += 2
            continue
        if ch == '"':
            in_str = True
            out.append(ch)
            i += 1
            continue
        if ch == "'":
            in_chr = True
            out.append(ch)
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


# --------------------------------------------------------------------------
# 语料收集
# --------------------------------------------------------------------------
class Corpus:
    def __init__(self, root: str):
        self.root = root
        self.src_main = self._find_src_main(root)
        self.java_files: list[tuple[str, str]] = []
        self.layout_files: list[tuple[str, str]] = []
        self.menu_files: list[tuple[str, str]] = []
        self.res_files: list[tuple[str, str]] = []
        self.manifest_text = ""
        self.gradle_text = ""
        self.strings_default: dict[str, str] = {}
        self.strings_zh: dict[str, str] = {}
        self.errors: list[str] = []
        if self.src_main:
            self._collect()

    @staticmethod
    def _find_src_main(root: str) -> str | None:
        for cand in (
            os.path.join(root, "app", "src", "main"),
            os.path.join(root, "src", "main"),
        ):
            if os.path.isdir(cand):
                return cand
        return None

    @staticmethod
    def _read(path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                return fh.read()
        except OSError as exc:
            return f"__READ_ERROR__{exc}"

    @staticmethod
    def _walk(directory: str, suffix: str) -> list[str]:
        found = []
        for base, _dirs, files in os.walk(directory):
            for name in sorted(files):
                if name.endswith(suffix):
                    found.append(os.path.join(base, name))
        return found

    def _collect(self) -> None:
        java_dir = os.path.join(self.src_main, "java")
        kotlin_dir = os.path.join(self.src_main, "kotlin")
        for d in (java_dir, kotlin_dir):
            if os.path.isdir(d):
                for path in self._walk(d, ".java"):
                    self.java_files.append((path, self._read(path)))

        res_dir = os.path.join(self.src_main, "res")
        if os.path.isdir(res_dir):
            for path in self._walk(res_dir, ".xml"):
                text = self._read(path)
                self.res_files.append((path, text))
                base = os.path.basename(os.path.dirname(path))
                fname = os.path.basename(path)
                if base.startswith("layout"):
                    self.layout_files.append((path, text))
                elif base == "menu":
                    self.menu_files.append((path, text))
                if fname == "strings.xml" and base == "values":
                    self.strings_default = parse_strings(text)
                elif fname == "strings.xml" and base.startswith("values-zh"):
                    self.strings_zh = parse_strings(text)

        manifest = os.path.join(self.src_main, "AndroidManifest.xml")
        if os.path.isfile(manifest):
            self.manifest_text = self._read(manifest)
        else:
            self.errors.append(f"找不到 AndroidManifest.xml: {manifest}")

        app_dir = os.path.dirname(self.src_main)
        app_dir = os.path.dirname(app_dir) if os.path.basename(app_dir) == "src" else app_dir
        for name in ("build.gradle", "build.gradle.kts"):
            path = os.path.join(app_dir, name)
            if os.path.isfile(path):
                self.gradle_text = self._read(path)
                break

        if not self.java_files:
            self.errors.append(f"在 {self.src_main} 下没有找到任何 .java 文件")

    # ---- 便捷访问 ----
    @property
    def java_text(self) -> str:
        """含注释的原文。要求「注释里必须写某句话」的检查项用它。"""
        return "\n".join(text for _p, text in self.java_files)

    @property
    def java_code(self) -> str:
        """剥掉 // 与 /* */ 注释后的代码。检查真实写法时用它，避免注释造成误判。"""
        return "\n".join(strip_java_comments(text) for _p, text in self.java_files)

    def java_code_files(self) -> list[tuple[str, str]]:
        return [(p, strip_java_comments(t)) for p, t in self.java_files]

    @property
    def layout_text(self) -> str:
        return "\n".join(text for _p, text in self.layout_files)

    @property
    def menu_text(self) -> str:
        return "\n".join(text for _p, text in self.menu_files)

    @property
    def res_text(self) -> str:
        return "\n".join(text for _p, text in self.res_files)

    def res_dir_exists(self, name: str) -> bool:
        return os.path.isdir(os.path.join(self.src_main or "", "res", name))

    def res_dir_xml_count(self, name: str) -> int:
        d = os.path.join(self.src_main or "", "res", name)
        if not os.path.isdir(d):
            return 0
        return len([f for f in os.listdir(d) if f.endswith(".xml")])

    def files_containing(self, pattern: str) -> list[str]:
        rx = re.compile(pattern, re.S)
        return [os.path.basename(p) for p, t in self.java_files if rx.search(t)]


STRING_RX = re.compile(r'<string\s+name\s*=\s*"([^"]+)"', re.I)


def parse_strings(text: str) -> dict[str, str]:
    return {m: "" for m in STRING_RX.findall(text)}


def count(pattern: str, text: str, flags: int = 0) -> int:
    return len(re.findall(pattern, text, flags))


def has(pattern: str, text: str, flags: int = 0) -> bool:
    return re.search(pattern, text, flags) is not None


def rel(corpus: Corpus, path: str) -> str:
    try:
        return os.path.relpath(path, corpus.root)
    except ValueError:
        return path


# --------------------------------------------------------------------------
# 检查项：每项返回 (passed: bool, detail: str)
# --------------------------------------------------------------------------
CHECKS: list[tuple[str, str, str, str, object]] = []


def check(cid: str, stage: str, level: str, desc: str):
    def deco(func):
        CHECKS.append((cid, stage, level, desc, func))
        return func

    return deco


def all_of(c: Corpus, *patterns: str) -> tuple[bool, str]:
    missing = [p for p in patterns if not has(p, c.java_text)]
    if missing:
        return False, "源码缺少: " + ", ".join(missing)
    return True, "命中: " + ", ".join(patterns[:3]) + ("…" if len(patterns) > 3 else "")


def all_in_layout(c: Corpus, *patterns: str) -> tuple[bool, str]:
    missing = [p for p in patterns if not has(p, c.layout_text)]
    if missing:
        return False, "布局缺少: " + ", ".join(missing)
    return True, "布局命中全部 " + str(len(patterns)) + " 项"


# ------------------------------ A 段 ------------------------------
@check("A1-1", "A", LEVEL_REQUIRED, "values/strings.xml 存在且 <string name= 不少于 12 条")
def _a1_1(c: Corpus):
    path = os.path.join(c.src_main or "", "res", "values", "strings.xml")
    if not os.path.isfile(path):
        return False, f"文件不存在: {rel(c, path)}"
    n = len(c.strings_default)
    return (n >= 12), f"字符串条数 = {n}（要求 ≥12）"


@check("A1-2", "A", LEVEL_REQUIRED, "values/dimens.xml 存在且含 <dimen")
def _a1_2(c: Corpus):
    path = os.path.join(c.src_main or "", "res", "values", "dimens.xml")
    if not os.path.isfile(path):
        return False, f"文件不存在: {rel(c, path)}"
    n = count(r"<dimen\s+name", c._read(path), re.I)
    return (n >= 1), f"<dimen name= 条数 = {n}"


@check("A1-3", "A", LEVEL_REQUIRED, "布局中 @string/ ≥8 次，且 Java 中出现 R.string.")
def _a1_3(c: Corpus):
    n = count(r"@string/", c.layout_text)
    ok_java = has(r"R\.string\.", c.java_text)
    if n < 8:
        return False, f"布局中 @string/ 只出现 {n} 次（要求 ≥8）"
    if not ok_java:
        return False, "Java 源码中没有出现 R.string."
    return True, f"布局 @string/ = {n} 次，Java 使用 R.string."


@check("A1-4", "A", LEVEL_WARN, "布局中不应出现 px 单位")
def _a1_4(c: Corpus):
    hits = re.findall(r'"-?\d+(?:\.\d+)?px"', c.layout_text)
    if hits:
        return False, f"发现 px 单位 {len(hits)} 处: {', '.join(hits[:4])}"
    return True, "未发现 px 单位"


@check("A2-1", "A", LEVEL_REQUIRED, "布局含 ScrollView / RatingBar / RadioGroup / CheckBox，EditText ≥4")
def _a2_1(c: Corpus):
    ok, detail = all_in_layout(c, r"<ScrollView", r"<RatingBar", r"<RadioGroup", r"<CheckBox")
    if not ok:
        return False, detail
    n = count(r"<EditText", c.layout_text)
    if n < 4:
        return False, f"EditText 只有 {n} 个（要求 ≥4）"
    return True, f"四类控件齐全，EditText = {n}"


@check("A2-2", "A", LEVEL_REQUIRED, "布局中 RadioButton ≥4 个")
def _a2_2(c: Corpus):
    n = count(r"<RadioButton", c.layout_text)
    return (n >= 4), f"RadioButton = {n} 个（要求 ≥4）"


@check("A2-3", "A", LEVEL_REQUIRED, "布局同时使用 LinearLayout 与 ConstraintLayout/TableLayout")
def _a2_3(c: Corpus):
    if not has(r"<LinearLayout", c.layout_text):
        return False, "布局中没有 LinearLayout"
    if not has(r"ConstraintLayout|<TableLayout", c.layout_text):
        return False, "布局中没有 ConstraintLayout 或 TableLayout"
    return True, "两种容器都用到"


@check("A2-4", "A", LEVEL_REQUIRED, "布局中使用 layout_weight 或 0dp")
def _a2_4(c: Corpus):
    w = count(r"layout_weight", c.layout_text)
    z = count(r'"0dp"', c.layout_text)
    return (w + z > 0), f"layout_weight = {w} 处，0dp = {z} 处"


@check("A2-5", "A", LEVEL_REQUIRED, "Java 中 findViewById ≥8 次；布局含 textMultiLine")
def _a2_5(c: Corpus):
    n = count(r"findViewById", c.java_text)
    if n < 8:
        return False, f"findViewById 只有 {n} 次（要求 ≥8）"
    if not has(r"textMultiLine", c.layout_text):
        return False, "布局中没有 inputType=\"textMultiLine\""
    return True, f"findViewById = {n} 次，多行输入框已配置"


@check("A3-1", "A", LEVEL_REQUIRED, "Java 中同时出现 Toast / Snackbar / AlertDialog 三种反馈")
def _a3_1(c: Corpus):
    return all_of(c, r"Toast\.makeText", r"Snackbar\.make", r"AlertDialog")


@check("A3-2", "A", LEVEL_REQUIRED, "Java 中有 try/catch，且有空值判断")
def _a3_2(c: Corpus):
    if not has(r"\bcatch\s*\(", c.java_text):
        return False, "没有 catch 块（数字解析必须防崩溃）"
    if not has(r"isEmpty\s*\(|TextUtils\.isEmpty", c.java_text):
        return False, "没有 isEmpty / TextUtils.isEmpty 空值判断"
    return True, "try/catch 与空值判断均存在"


@check("A3-3", "A", LEVEL_REQUIRED, "Java 中出现 .show()（对话框/提示真的显示了）")
def _a3_3(c: Corpus):
    n = count(r"\.show\s*\(\s*\)", c.java_text)
    return (n >= 1), f".show() 出现 {n} 次"


@check("A3-4", "A", LEVEL_WARN, "使用了 AlertDialog.Builder 的文件里应当有 .show()")
def _a3_4(c: Corpus):
    bad = []
    for path, text in c.java_code_files():
        if has(r"AlertDialog\.Builder", text) and not has(r"\.show\s*\(", text):
            bad.append(os.path.basename(path))
    if bad:
        return False, "这些文件建了对话框却没 show(): " + ", ".join(bad)
    return True, "无「建了对话框却忘了 show」的文件"


@check("A4-1", "A", LEVEL_REQUIRED, "Java 中有 onSaveInstanceState 且往里 put 了值")
def _a4_1(c: Corpus):
    if not has(r"onSaveInstanceState\s*\(", c.java_text):
        return False, "没有重写 onSaveInstanceState"
    if not has(r"put(?:String|Int|Boolean|Float|Long|Integer)\s*\(", c.java_text):
        return False, "onSaveInstanceState 里没有 putString/putInt/putBoolean 之类的调用"
    return True, "状态保存逻辑存在"


@check("A4-2", "A", LEVEL_REQUIRED, "恢复状态时对 Bundle 做了判空")
def _a4_2(c: Corpus):
    if has(r"(?:savedInstanceState|inState|state|bundle|b)\s*!=\s*null", c.java_text):
        return True, "找到 Bundle 判空"
    return False, "没找到 savedInstanceState != null 之类的判空（首次启动会 NPE）"


@check("A4-3", "A", LEVEL_REQUIRED, "Manifest 中没有用 android:configChanges 绕过重建")
def _a4_3(c: Corpus):
    if has(r"configChanges", c.manifest_text):
        return False, "Manifest 出现 configChanges —— 题目要求走正规保存/恢复流程"
    return True, "未使用 configChanges 绕过"


@check("A5-1", "A", LEVEL_REQUIRED, "Manifest 中注册的 <activity 不少于 3 个")
def _a5_1(c: Corpus):
    n = count(r"<activity\b", c.manifest_text)
    return (n >= 3), f"<activity 数量 = {n}（要求 ≥3）"


@check("A5-2", "A", LEVEL_REQUIRED, "Intent 传参：putExtra + getIntent + 至少两种 getXxxExtra")
def _a5_2(c: Corpus):
    if not has(r"putExtra\s*\(", c.java_text):
        return False, "没有 putExtra"
    if not has(r"getIntent\s*\(\s*\)", c.java_text):
        return False, "没有 getIntent()"
    getters = [
        g
        for g in ("getStringExtra", "getIntExtra", "getBooleanExtra", "getFloatExtra", "getLongExtra")
        if has(g + r"\s*\(", c.java_text)
    ]
    if len(getters) < 2:
        return False, f"只用了 {getters or '无'} 取值，要求至少两种 getXxxExtra"
    return True, "传参与取值齐全: " + ", ".join(getters)


@check("A5-3", "A", LEVEL_REQUIRED, "Java 中出现 finish()")
def _a5_3(c: Corpus):
    n = count(r"\bfinish\s*\(\s*\)", c.java_text)
    return (n >= 1), f"finish() 出现 {n} 次"


@check("A5-4", "A", LEVEL_REQUIRED, "strings.xml 中有带占位符的字符串（%1$s / %1$d）")
def _a5_4(c: Corpus):
    path = os.path.join(c.src_main or "", "res", "values", "strings.xml")
    text = c._read(path) if os.path.isfile(path) else ""
    hits = re.findall(r"%\d+\$[sd]", text)
    return (len(hits) >= 1), f"占位符出现 {len(hits)} 处"


@check("A5-5", "A", LEVEL_WARN, "不应出现 new android.content.Intent（自定义类与 Intent 重名的信号）")
def _a5_5(c: Corpus):
    n = count(r"new\s+android\.content\.Intent", c.java_text)
    if n:
        return False, f"出现 {n} 次全限定 Intent，说明有自定义类叫 Intent，机考别这么起名"
    return True, "无 Intent 命名冲突"


# ------------------------------ B 段 ------------------------------
@check("B1-1", "B", LEVEL_REQUIRED, "SQLiteOpenHelper 三件套：继承 + onCreate(SQLiteDatabase + onUpgrade")
def _b1_1(c: Corpus):
    return all_of(c, r"extends\s+SQLiteOpenHelper", r"onCreate\s*\(\s*(?:final\s+)?SQLiteDatabase", r"onUpgrade\s*\(")


@check("B1-2", "B", LEVEL_REQUIRED, "Java 中有 CREATE TABLE 建表语句")
def _b1_2(c: Corpus):
    return (has(r"CREATE\s+TABLE", c.java_text, re.I), "CREATE TABLE " + ("已找到" if has(r"CREATE\s+TABLE", c.java_text, re.I) else "缺失"))


@check("B1-3", "B", LEVEL_REQUIRED, "写库方式：ContentValues / execSQL / insert 至少一种")
def _b1_3(c: Corpus):
    pats = (r"ContentValues", r"execSQL\s*\(", r"\.insert\s*\(", r"\.insertWithOnConflict\s*\(")
    hit = [p for p in pats if has(p, c.java_text)]
    return (bool(hit)), ("命中: " + ", ".join(hit)) if hit else "没有 ContentValues / execSQL / insert"


@check("B1-4", "B", LEVEL_REQUIRED, "带条件的 SQL 使用 ? 占位符 + String[] 参数数组")
def _b1_4(c: Corpus):
    if not has(r"=\s*\?", c.java_text):
        return False, "源码里没有 \"xxx = ?\" 形式的占位符"
    if not has(r"new\s+String\s*\[\s*\]", c.java_text):
        return False, "没有 new String[]{...} 参数数组"
    return True, "占位符与参数数组均存在"


@check("B1-5", "B", LEVEL_REQUIRED, "Cursor 规范：Cursor / moveToNext / getColumnIndex / close()")
def _b1_5(c: Corpus):
    return all_of(c, r"\bCursor\b", r"moveToNext\s*\(", r"getColumnIndex(?:OrThrow)?\s*\(", r"\.close\s*\(\s*\)")


@check("B1-6", "B", LEVEL_WARN, "SQL 语句里不应拼接变量（用户输入必须走占位符）")
def _b1_6(c: Corpus):
    bad = []
    for path, text in c.java_code_files():
        for line in text.splitlines():
            if re.search(r'"(?:SELECT|INSERT|UPDATE|DELETE)\b', line, re.I) and re.search(r'"\s*\+\s*\w', line):
                bad.append(os.path.basename(path))
                break
    if bad:
        return False, "含变量拼接的 SQL: " + ", ".join(sorted(set(bad)))
    return True, "未发现 SQL 字符串拼接"


@check("B2-1", "B", LEVEL_REQUIRED, "RecyclerView.Adapter 三个必重写方法 + 继承声明")
def _b2_1(c: Corpus):
    return all_of(c, r"extends\s+RecyclerView\.Adapter", r"onCreateViewHolder\s*\(", r"onBindViewHolder\s*\(", r"getItemCount\s*\(")


@check("B2-2", "B", LEVEL_REQUIRED, "有 ViewHolder（RecyclerView.ViewHolder）")
def _b2_2(c: Corpus):
    return (has(r"RecyclerView\.ViewHolder", c.java_text), "RecyclerView.ViewHolder " + ("已找到" if has(r"RecyclerView\.ViewHolder", c.java_text) else "缺失"))


@check("B2-3", "B", LEVEL_REQUIRED, "布局含 RecyclerView，且存在 item_ 开头的 item 布局")
def _b2_3(c: Corpus):
    if not has(r"androidx\.recyclerview\.widget\.RecyclerView", c.layout_text):
        return False, "布局中没有 androidx.recyclerview.widget.RecyclerView"
    items = [os.path.basename(p) for p, _t in c.layout_files if os.path.basename(p).startswith("item_")]
    if not items:
        return False, "没有文件名以 item_ 开头的布局"
    return True, "RecyclerView 与 item 布局齐全: " + ", ".join(items)


@check("B2-4", "B", LEVEL_REQUIRED, "setLayoutManager + LinearLayoutManager")
def _b2_4(c: Corpus):
    return all_of(c, r"setLayoutManager\s*\(", r"LinearLayoutManager")


@check("B2-5", "B", LEVEL_REQUIRED, "同一个文件里有 onResume() 且刷新了列表数据")
def _b2_5(c: Corpus):
    for path, text in c.java_code_files():
        if has(r"onResume\s*\(\s*\)", text) and has(r"notifyDataSetChanged\s*\(|setData\s*\(|submitList\s*\(|notifyItem", text):
            return True, f"{os.path.basename(path)} 在 onResume 中刷新列表"
    return False, "没有任何文件同时包含 onResume() 与列表刷新调用"


@check("B2-6", "B", LEVEL_REQUIRED, "布局中使用了 ProgressBar")
def _b2_6(c: Corpus):
    n = count(r"<ProgressBar", c.layout_text)
    return (n >= 1), f"ProgressBar = {n} 个"


@check("B3-1", "B", LEVEL_REQUIRED, "上下文菜单三件套：registerForContextMenu / onCreateContextMenu / onContextItemSelected")
def _b3_1(c: Corpus):
    return all_of(c, r"registerForContextMenu\s*\(", r"onCreateContextMenu\s*\(", r"onContextItemSelected\s*\(")


@check("B3-2", "B", LEVEL_REQUIRED, "res/menu 下至少 2 个 xml")
def _b3_2(c: Corpus):
    n = len(c.menu_files)
    return (n >= 2), f"res/menu 下 xml 数量 = {n}（要求 ≥2）"


@check("B3-3", "B", LEVEL_REQUIRED, "有删除实现（db.delete 或 DELETE FROM）")
def _b3_3(c: Corpus):
    ok = has(r"\.delete\s*\(|DELETE\s+FROM", c.java_text, re.I)
    return ok, "删除语句 " + ("已找到" if ok else "缺失")


@check("B3-4", "B", LEVEL_REQUIRED, "有带输入框的对话框（setView）")
def _b3_4(c: Corpus):
    return (has(r"setView\s*\(", c.java_text), "setView( " + ("已找到" if has(r"setView\s*\(", c.java_text) else "缺失"))


@check("B3-5", "B", LEVEL_REQUIRED, "没有 switch(getItemId()) / switch(R.id.x)（AGP 8+ 编译不过）")
def _b3_5(c: Corpus):
    bad = []
    for m in re.finditer(r"switch\s*\(([^)]{0,60})", c.java_code):
        inner = m.group(1)
        if "getItemId" in inner or "getId()" in inner or "R.id." in inner:
            bad.append(inner.strip()[:40])
    if bad:
        return False, "发现资源 id 的 switch: " + "; ".join(bad[:3])
    return True, "菜单/点击分支未使用资源 id switch"


@check("B4-1", "B", LEVEL_REQUIRED, "统计查询使用 COUNT(*)")
def _b4_1(c: Corpus):
    return (has(r"COUNT\s*\(\s*\*\s*\)", c.java_text, re.I), "COUNT(*) " + ("已找到" if has(r"COUNT\s*\(\s*\*\s*\)", c.java_text, re.I) else "缺失"))


@check("B4-2", "B", LEVEL_REQUIRED, "统计查询使用 AVG(")
def _b4_2(c: Corpus):
    return (has(r"AVG\s*\(", c.java_text, re.I), "AVG( " + ("已找到" if has(r"AVG\s*\(", c.java_text, re.I) else "缺失"))


@check("B4-3", "B", LEVEL_REQUIRED, "分类统计使用 GROUP BY")
def _b4_3(c: Corpus):
    return (has(r"GROUP\s+BY", c.java_text, re.I), "GROUP BY " + ("已找到" if has(r"GROUP\s+BY", c.java_text, re.I) else "缺失"))


@check("B4-4", "B", LEVEL_REQUIRED, "排序 + 限量：ORDER BY 与 LIMIT，或九参数 query 重载")
def _b4_4(c: Corpus):
    if has(r"query\s*\(\s*false\s*,", c.java_text):
        return True, "使用了九参数 query(false, ...) 重载"
    order = has(r"ORDER\s+BY", c.java_text, re.I)
    limit = has(r"\bLIMIT\b", c.java_text, re.I)
    if order and limit:
        return True, "ORDER BY 与 LIMIT 均已使用"
    return False, f"ORDER BY={order}, LIMIT={limit}（七参数 query 没有 LIMIT，需换写法）"


@check("B4-5", "B", LEVEL_REQUIRED, "模糊查询：LIKE + rawQuery/query")
def _b4_5(c: Corpus):
    if not has(r"\bLIKE\b", c.java_text, re.I):
        return False, "没有 LIKE 模糊查询"
    if not has(r"rawQuery\s*\(|\.query\s*\(", c.java_text):
        return False, "没有 rawQuery( 或 query( 查询调用"
    return True, "LIKE 与查询 API 均已使用"


@check("B5-1", "B", LEVEL_REQUIRED, "OptionsMenu：onCreateOptionsMenu / onOptionsItemSelected / MenuInflater")
def _b5_1(c: Corpus):
    return all_of(c, r"onCreateOptionsMenu\s*\(", r"onOptionsItemSelected\s*\(", r"MenuInflater|getMenuInflater\s*\(")


@check("B5-2", "B", LEVEL_REQUIRED, "values-zh/strings.xml 存在且条数与 values/strings.xml 完全相等")
def _b5_2(c: Corpus):
    if not c.strings_zh:
        return False, "没有 res/values-zh/strings.xml 或其中没有字符串"
    a, b = len(c.strings_default), len(c.strings_zh)
    if a != b:
        miss = sorted(set(c.strings_default) - set(c.strings_zh))
        extra = sorted(set(c.strings_zh) - set(c.strings_default))
        detail = f"values={a} 条, values-zh={b} 条"
        if miss:
            detail += "；zh 缺少: " + ", ".join(miss[:6])
        if extra:
            detail += "；zh 多出: " + ", ".join(extra[:6])
        return False, detail
    return True, f"两套 strings.xml 各 {a} 条，完全对应"


@check("B5-3", "B", LEVEL_REQUIRED, "res/layout-land 存在且含至少 1 个 xml")
def _b5_3(c: Corpus):
    n = c.res_dir_xml_count("layout-land")
    return (n >= 1), f"layout-land 下 xml 数量 = {n}"


@check("B5-4", "B", LEVEL_REQUIRED, "菜单里用了 showAsAction，且不是全部 always")
def _b5_4(c: Corpus):
    if not c.menu_text:
        return False, "res/menu 下没有 xml"
    total = count(r"showAsAction", c.menu_text)
    always = count(r'showAsAction\s*=\s*"always"', c.menu_text)
    if total == 0:
        return False, "菜单里没有 showAsAction 属性"
    if total == always:
        return False, f"{total} 个菜单项全是 always，溢出菜单里一项都没有"
    return True, f"showAsAction = {total} 处，其中 always = {always} 处"


@check("B5-5", "B", LEVEL_WARN, "多占位符字符串建议加 formatted=\"false\"")
def _b5_5(c: Corpus):
    path = os.path.join(c.src_main or "", "res", "values", "strings.xml")
    text = c._read(path) if os.path.isfile(path) else ""
    risky = 0
    for m in re.finditer(r"<string\b([^>]*)>(.*?)</string>", text, re.S):
        attrs, body = m.group(1), m.group(2)
        if len(re.findall(r"%\d+\$[sd]", body)) >= 2 and "formatted" not in attrs:
            risky += 1
    if risky:
        return False, f"{risky} 条含 ≥2 个占位符却没有 formatted=\"false\"（构建会有 warning）"
    return True, "多占位符字符串处理正确或不存在"


# ------------------------------ C 段 ------------------------------
@check("C1-1", "C", LEVEL_BONUS, "SharedPreferences：getSharedPreferences + apply()")
def _c1_1(c: Corpus):
    return all_of(c, r"getSharedPreferences\s*\(", r"\.apply\s*\(\s*\)")


@check("C1-2", "C", LEVEL_BONUS, "读回偏好：getBoolean( 与 getString(")
def _c1_2(c: Corpus):
    return all_of(c, r"getBoolean\s*\(", r"getString\s*\(")


@check("C1-3", "C", LEVEL_BONUS, "edit() 出现不少于 3 次（三项偏好都写了）")
def _c1_3(c: Corpus):
    n = count(r"\.edit\s*\(\s*\)", c.java_text)
    return (n >= 3), f"edit() 出现 {n} 次（要求 ≥3）"


@check("C2-1", "C", LEVEL_BONUS, "后台线程：Executors.new / ExecutorService / new Thread(")
def _c2_1(c: Corpus):
    pats = (r"Executors\.new\w+", r"ExecutorService", r"new\s+Thread\s*\(")
    hit = [p for p in pats if has(p, c.java_text)]
    return (bool(hit)), ("命中: " + ", ".join(hit)) if hit else "没有任何后台线程写法"


@check("C2-2", "C", LEVEL_BONUS, "回主线程：runOnUiThread / Looper.getMainLooper / .post(")
def _c2_2(c: Corpus):
    pats = (r"runOnUiThread\s*\(", r"Looper\.getMainLooper\s*\(", r"\.post\s*\(")
    hit = [p for p in pats if has(p, c.java_text)]
    return (bool(hit)), ("命中: " + ", ".join(hit)) if hit else "没有回到主线程的写法"


@check("C2-3", "C", LEVEL_BONUS, "onDestroy 中清理线程与 Handler")
def _c2_3(c: Corpus):
    for path, text in c.java_code_files():
        if has(r"onDestroy\s*\(\s*\)", text) and has(r"shutdown|removeCallbacksAndMessages|quitSafely", text):
            return True, f"{os.path.basename(path)} 在 onDestroy 中做了清理"
    return False, "没有文件在 onDestroy 里调用 shutdown / removeCallbacksAndMessages"


@check("C2-4", "C", LEVEL_BONUS, "注释中记录了子线程改 UI 的真实异常")
def _c2_4(c: Corpus):
    ok = has(r"CalledFromWrongThreadException|Only the original thread", c.java_text)
    return ok, "异常记录 " + ("已找到" if ok else "缺失（要求真的复现一次并抄进注释）")


@check("C3-1", "C", LEVEL_BONUS, "自定义 View：extends View + onDraw(Canvas + new Paint")
def _c3_1(c: Corpus):
    return all_of(c, r"extends\s+View\b", r"onDraw\s*\(\s*(?:final\s+)?Canvas", r"new\s+Paint\s*\(")


@check("C3-2", "C", LEVEL_BONUS, "绘图原语：drawText + drawLine + drawRect/drawRoundRect")
def _c3_2(c: Corpus):
    if not has(r"drawText\s*\(", c.java_text):
        return False, "没有 drawText("
    if not has(r"drawLine\s*\(", c.java_text):
        return False, "没有 drawLine(（基线）"
    if not has(r"drawRect\s*\(|drawRoundRect\s*\(", c.java_text):
        return False, "没有 drawRect( 或 drawRoundRect(（条形）"
    return True, "drawText / drawLine / drawRect 均已使用"


@check("C3-3", "C", LEVEL_BONUS, "自定义 View 以全限定类名出现在布局 xml 中")
def _c3_3(c: Corpus):
    names = re.findall(r"class\s+(\w+)\s+extends\s+View\b", c.java_code)
    if not names:
        return False, "没有找到 extends View 的类"
    for name in names:
        if re.search(r"[\w$]+(?:\.[\w$]+)+\." + re.escape(name) + r"\b", c.layout_text):
            return True, f"布局中以全限定名使用了 {name}"
    return False, f"布局里没有以全限定名使用 {', '.join(names)}（XML 标签必须写完整包名）"


@check("C3-4", "C", LEVEL_BONUS, "自定义 View 中使用 invalidate() / getWidth() / getHeight()")
def _c3_4(c: Corpus):
    return all_of(c, r"invalidate\s*\(\s*\)", r"getWidth\s*\(\s*\)", r"getHeight\s*\(\s*\)")


@check("C3-5", "C", LEVEL_BONUS, "自定义 View 至少实现 2 个构造函数")
def _c3_5(c: Corpus):
    names = re.findall(r"class\s+(\w+)\s+extends\s+View\b", c.java_code)
    if not names:
        return False, "没有找到 extends View 的类"
    for path, text in c.java_code_files():
        for name in names:
            if f"class {name}" in text:
                n = len(re.findall(r"public\s+" + re.escape(name) + r"\s*\(\s*(?:final\s+)?Context", text))
                if n >= 2:
                    return True, f"{name} 有 {n} 个 (Context, …) 构造函数"
                return False, f"{name} 只有 {n} 个构造函数（XML 使用需要 (Context, AttributeSet)）"
    return False, "定位不到自定义 View 所在文件"


@check("C4-1", "C", LEVEL_BONUS, "至少 2 个类 extends Fragment")
def _c4_1(c: Corpus):
    names = re.findall(r"class\s+(\w+)\s+extends\s+Fragment\b", c.java_code)
    return (len(names) >= 2), f"Fragment 子类 = {names or 0}"


@check("C4-2", "C", LEVEL_BONUS, "动态挂载：getSupportFragmentManager + beginTransaction + replace(")
def _c4_2(c: Corpus):
    return all_of(c, r"getSupportFragmentManager\s*\(", r"beginTransaction\s*\(", r"\.replace\s*\(|\.add\s*\(")


@check("C4-3", "C", LEVEL_BONUS, "使用 addToBackStack(")
def _c4_3(c: Corpus):
    return (has(r"addToBackStack\s*\(", c.java_text), "addToBackStack( " + ("已找到" if has(r"addToBackStack\s*\(", c.java_text) else "缺失"))


@check("C4-4", "C", LEVEL_BONUS, "onAttach( 与 setArguments/getArguments 均出现")
def _c4_4(c: Corpus):
    return all_of(c, r"onAttach\s*\(", r"setArguments\s*\(|getArguments\s*\(")


@check("C4-5", "C", LEVEL_BONUS, "onCreateView( 与 onViewCreated(")
def _c4_5(c: Corpus):
    return all_of(c, r"onCreateView\s*\(", r"onViewCreated\s*\(")


@check("C5-1", "C", LEVEL_BONUS, "openFileOutput( 与 MODE_PRIVATE/MODE_APPEND")
def _c5_1(c: Corpus):
    if not has(r"openFileOutput\s*\(", c.java_text):
        return False, "没有 openFileOutput("
    if not has(r"MODE_PRIVATE|MODE_APPEND", c.java_text):
        return False, "没有指定 MODE_PRIVATE / MODE_APPEND"
    return True, "内部存储写入已实现"


@check("C5-2", "C", LEVEL_BONUS, "openFileInput( 或 getFilesDir()")
def _c5_2(c: Corpus):
    ok = has(r"openFileInput\s*\(|getFilesDir\s*\(", c.java_text)
    return ok, "读回/取路径 " + ("已找到" if ok else "缺失")


@check("C5-3", "C", LEVEL_BONUS, "显式使用 UTF-8 编码")
def _c5_3(c: Corpus):
    ok = has(r"UTF-8|StandardCharsets\.UTF_8", c.java_text)
    return ok, "UTF-8 " + ("已找到" if ok else "缺失")


@check("C5-4", "C", LEVEL_BONUS, "注释中说明 ACTION_CREATE_DOCUMENT（让用户选保存位置的正规做法）")
def _c5_4(c: Corpus):
    ok = has(r"ACTION_CREATE_DOCUMENT", c.java_text)
    return ok, "ACTION_CREATE_DOCUMENT " + ("已找到" if ok else "缺失")


@check("C6-1", "C", LEVEL_BONUS, "隐式 Intent：ACTION_SEND 或 ACTION_VIEW")
def _c6_1(c: Corpus):
    ok = has(r"ACTION_SEND|ACTION_VIEW", c.java_text)
    return ok, "隐式 Intent action " + ("已找到" if ok else "缺失")


@check("C6-2", "C", LEVEL_BONUS, "Manifest 中声明 android.permission.INTERNET")
def _c6_2(c: Corpus):
    ok = has(r"android\.permission\.INTERNET", c.manifest_text)
    return ok, "INTERNET 权限 " + ("已声明" if ok else "未声明")


@check("C6-3", "C", LEVEL_BONUS, "隐式 Intent 的防护：ActivityNotFoundException 或 resolveActivity(")
def _c6_3(c: Corpus):
    ok = has(r"ActivityNotFoundException|resolveActivity\s*\(|queryIntentActivities\s*\(", c.java_text)
    return ok, "防护写法 " + ("已找到" if ok else "缺失")


# ------------------------------ 全局 ------------------------------
@check("G-1", "G", LEVEL_REQUIRED, "app/src/main/java 下 .java 文件不少于 7 个")
def _g1(c: Corpus):
    n = len(c.java_files)
    return (n >= 7), f".java 文件数 = {n}（要求 ≥7）"


@check("G-2", "G", LEVEL_REQUIRED, "layout（含 layout-land）下 xml 不少于 5 个")
def _g2(c: Corpus):
    n = len(c.layout_files)
    return (n >= 5), f"布局 xml 数 = {n}（要求 ≥5）"


@check("G-3", "G", LEVEL_WARN, "源码中不应残留 TODO / FIXME / XXX")
def _g3(c: Corpus):
    hits = []
    for path, text in list(c.java_files) + list(c.layout_files):
        for m in re.finditer(r"\b(TODO|FIXME)\b", text):
            hits.append(os.path.basename(path))
            break
    if hits:
        return False, "残留标记的文件: " + ", ".join(sorted(set(hits)))
    return True, "无 TODO/FIXME 残留"


@check("G-4", "G", LEVEL_WARN, "建议开启 viewBinding（可少写 findViewById）")
def _g4(c: Corpus):
    if has(r"viewBinding", c.gradle_text):
        return True, "已开启 viewBinding"
    return False, "app/build.gradle 中未开启 viewBinding（可选）"


# --------------------------------------------------------------------------
# 执行
# --------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="EE5415 ReadTrack 模拟题静态验收")
    parser.add_argument("project", help="Android 工程根目录（含 gradlew.bat 的那一层）")
    parser.add_argument("--stage", default="all", choices=["A", "B", "C", "G", "all"], help="只跑某一段")
    args = parser.parse_args()

    root = os.path.abspath(args.project)
    if not os.path.isdir(root):
        print(f"[ERROR] 目录不存在: {root}")
        print("RESULT: FAIL=1")
        return 1

    corpus = Corpus(root)
    print("=" * 78)
    print(f"工程根目录 : {root}")
    print(f"源码目录   : {corpus.src_main or '（未找到 app/src/main 或 src/main）'}")
    print(f"Java 文件  : {len(corpus.java_files)}    布局 xml: {len(corpus.layout_files)}    menu xml: {len(corpus.menu_files)}")
    print(f"strings    : values={len(corpus.strings_default)} 条, values-zh={len(corpus.strings_zh)} 条")
    print(f"过滤段     : {args.stage}")
    for err in corpus.errors:
        print(f"[ERROR] {err}")
    print("=" * 78)

    if not corpus.src_main:
        print("RESULT: FAIL=1")
        return 1

    counts = {STATUS_PASS: 0, STATUS_FAIL: 0, STATUS_MISS: 0, STATUS_WARN: 0}
    fails: list[str] = []
    misses: list[str] = []

    for cid, stage, level, desc, func in CHECKS:
        if args.stage != "all" and stage != args.stage:
            continue
        try:
            passed, detail = func(corpus)
        except Exception as exc:  # noqa: BLE001 - 验收脚本自身不能崩
            passed, detail = False, f"检查项自身异常: {type(exc).__name__}: {exc}"

        if passed:
            status = STATUS_PASS
        elif level == LEVEL_WARN:
            status = STATUS_WARN
        elif level == LEVEL_BONUS:
            status = STATUS_MISS
        else:
            status = STATUS_FAIL
        counts[status] += 1
        print(f"[{status}] {cid:<6} ({level}) {desc}")
        print(f"         └─ {detail}")
        if status == STATUS_FAIL:
            fails.append(cid)
        elif status == STATUS_MISS:
            misses.append(cid)

    print("=" * 78)
    print(
        f"SUMMARY PASS={counts[STATUS_PASS]} FAIL={counts[STATUS_FAIL]} "
        f"MISS={counts[STATUS_MISS]} WARN={counts[STATUS_WARN]}"
    )
    if fails:
        print("未通过的必需项: " + ", ".join(fails))
    if misses:
        print("未做的加分项  : " + ", ".join(misses))
    print("提示：静态检查不覆盖运行期行为，务必在模拟器上手动验一遍旋转/中文/横屏/返回键。")
    print(f"RESULT: FAIL={counts[STATUS_FAIL]}")
    return 0 if counts[STATUS_FAIL] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
