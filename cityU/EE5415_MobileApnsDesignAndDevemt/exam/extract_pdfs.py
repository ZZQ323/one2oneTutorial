"""把 EE5415 本地课件 PDF 提取成 txt，供手册编写与覆盖对照使用。

用法: python extract_pdfs.py
输出: exam/extracted/<同名>.txt
"""

from pathlib import Path

from pypdf import PdfReader

BASE = Path(__file__).resolve().parent.parent  # EE5415_MobileApnsDesignAndDevemt
OUT = Path(__file__).resolve().parent / "extracted"

TARGETS = [
    BASE / "EE5415-Lab Setup & Getting Started Instructions.pdf",
    *sorted((BASE / "Crouse").glob("*.pdf")),
    *sorted((BASE / "labs").glob("*.pdf")),
]


def extract(pdf: Path) -> str:
    reader = PdfReader(str(pdf))
    chunks = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks.append(f"----- page {i} -----\n{text.strip()}")
    return "\n\n".join(chunks)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for pdf in TARGETS:
        if not pdf.exists():
            print(f"[MISS] {pdf}")
            continue
        text = extract(pdf)
        dest = OUT / (pdf.stem + ".txt")
        dest.write_text(text, encoding="utf-8")
        total += 1
        print(f"[OK] {pdf.name} -> {dest.name}  chars={len(text)}")
    print(f"TOTAL={total} OUT={OUT}")


if __name__ == "__main__":
    main()
