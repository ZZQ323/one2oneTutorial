"""EE5415 机考备考包自检脚本。

逐条核对手册关键词命中、课件覆盖对照、提取文本数量、演示工程关键 API 与 Manifest 注册数。
用法: python verify_exam_pack.py
"""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

EXAM_DIR = Path(__file__).resolve().parent
REPO = EXAM_DIR.parent                           # cityU/EE5415_MobileApnsDesignAndDevemt
DEMO = Path(r"D:\ProjectStore\AndroidDemo\app\src\main")

HANDBOOK = EXAM_DIR / "Android前端类比手册.md"
COVERAGE = EXAM_DIR / "课件覆盖对照.md"
EXTRACTED = EXAM_DIR / "extracted"

KEYWORDS = [
    "findViewById", "setOnClickListener", "drawable", "EditText", "Spinner",
    "AndroidManifest", "Intent", "生命周期", "Fragment", "RecyclerView",
    "SQLiteOpenHelper", "SharedPreferences", "Handler", "onDraw", "Menu",
]

PROJECT_SYMBOLS = [
    "RecyclerView.Adapter", "SQLiteOpenHelper", "startActivity(new Intent",
    "findViewById", "setOnClickListener", "onCreateViewHolder", "onBindViewHolder",
    "getSharedPreferences", "Handler(Looper.getMainLooper())", "onDraw(Canvas",
]

SHARED_CLASS = "GradeBarChartView"


def head(text: str, keyword: str, width: int = 96) -> str:
    for line in text.splitlines():
        if keyword in line:
            line = line.strip()
            return (line[:width] + "…") if len(line) > width else line
    return "<NOT FOUND>"


def count(text: str, keyword: str) -> int:
    return len(re.findall(re.escape(keyword), text))


def main() -> None:
    print("=" * 72)
    print("[1] 手册存在性与关键词命中")
    print("=" * 72)
    print(f"path    = {HANDBOOK}")
    print(f"exists  = {HANDBOOK.exists()}")
    handbook = HANDBOOK.read_text(encoding="utf-8") if HANDBOOK.exists() else ""
    print(f"chars   = {len(handbook)}  lines = {len(handbook.splitlines())}")
    missing = []
    for kw in KEYWORDS:
        n = count(handbook, kw)
        if n == 0:
            missing.append(kw)
        print(f"  {kw:<20} hits={n:<5} | {head(handbook, kw)}")
    print(f"MISSING_KEYWORDS = {missing if missing else 'none'}")

    print()
    print("=" * 72)
    print("[2] 课件覆盖对照表 + 提取文本")
    print("=" * 72)
    print(f"path    = {COVERAGE}")
    print(f"exists  = {COVERAGE.exists()}")
    coverage = COVERAGE.read_text(encoding="utf-8") if COVERAGE.exists() else ""
    pdfs = sorted(REPO.glob("Crouse/*.pdf")) + sorted(REPO.glob("labs/*.pdf")) + sorted(REPO.glob("*.pdf"))
    print(f"本地 PDF 总数 = {len(pdfs)}")
    not_mapped = []
    for pdf in pdfs:
        if pdf.name not in coverage:
            not_mapped.append(pdf.name)
        print(f"  {'MAPPED ' if pdf.name in coverage else 'MISSING'} {pdf.name}")
    print(f"NOT_MAPPED = {not_mapped if not_mapped else 'none'}")
    txts = sorted(EXTRACTED.glob("*.txt")) if EXTRACTED.exists() else []
    print(f"extracted/*.txt 数量 = {len(txts)}")
    for t in txts:
        print(f"  {t.name}  ({t.stat().st_size} bytes)")

    print()
    print("=" * 72)
    print("[3] 演示工程关键 API 命中")
    print("=" * 72)
    print(f"path = {DEMO}")
    sources = list(DEMO.rglob("*.java")) + list(DEMO.rglob("*.xml"))
    print(f"源文件数 = {len(sources)}")
    blob = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in sources)
    for sym in PROJECT_SYMBOLS:
        print(f"  {sym:<34} hits={count(blob, sym)}")

    print()
    print("=" * 72)
    print("[4] AndroidManifest 注册的 Activity 数")
    print("=" * 72)
    manifest = DEMO / "AndroidManifest.xml"
    mtext = manifest.read_text(encoding="utf-8") if manifest.exists() else ""
    activities = re.findall(r'<activity\s+android:name="([^"]+)"', mtext)
    print(f"manifest = {manifest}")
    print(f"activity 数量 = {len(activities)}")
    for a in activities:
        print(f"  {a}")
    print(f"LAUNCHER intent-filter 存在 = {'android.intent.category.LAUNCHER' in mtext}")

    print()
    print("=" * 72)
    print(f"[5] 特征类名 {SHARED_CLASS} 在手册与工程 .java 中同时出现")
    print("=" * 72)
    java_hits = [p for p in DEMO.rglob("*.java") if SHARED_CLASS in p.read_text(encoding="utf-8", errors="ignore")]
    xml_hits = [p for p in DEMO.rglob("*.xml") if SHARED_CLASS in p.read_text(encoding="utf-8", errors="ignore")]
    print(f"手册命中次数 = {count(handbook, SHARED_CLASS)}")
    print(f"手册命中行   = {head(handbook, SHARED_CLASS)}")
    print(f"工程 .java 命中 = {[str(p) for p in java_hits]}")
    print(f"工程 .xml  命中 = {[str(p) for p in xml_hits]}")

    print()
    print("=" * 72)
    ok = (
        HANDBOOK.exists() and not missing
        and COVERAGE.exists() and not not_mapped and len(txts) >= 14
        and all(count(blob, s) > 0 for s in PROJECT_SYMBOLS)
        and len(activities) >= 2
        and count(handbook, SHARED_CLASS) > 0 and java_hits
    )
    print(f"SELF_CHECK = {'PASS' if ok else 'FAIL'}")
    print("=" * 72)


if __name__ == "__main__":
    main()
