# -*- coding: utf-8 -*-
"""一次性脚本：提取演讲稿 docx 与 PPTX 的文本，输出到同目录 *_extracted.txt"""
import zipfile, re, html, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))

def strip_xml_to_text(xml: str) -> str:
    xml = re.sub(r'<w:p(?: [^>]*)?>', '\n', xml)
    xml = re.sub(r'<w:tab(?: [^>]*)?/>', '\t', xml)
    xml = re.sub(r'<w:br(?: [^>]*)?/>', '\n', xml)
    xml = re.sub(r'<a:p>', '\n', xml)
    xml = re.sub(r'<[^>]+>', '', xml)
    return html.unescape(xml)

def extract_docx(path, out):
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml').decode('utf-8')
    text = strip_xml_to_text(xml)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'docx -> {out} ({len(text)} chars)')

def extract_pptx(path, out):
    lines = []
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)]
        notes = [n for n in z.namelist() if re.match(r'ppt/notesSlides/notesSlide\d+\.xml$', n)]
        def key(n):
            return int(re.search(r'(\d+)\.xml$', n).group(1))
        for n in sorted(names, key=key):
            lines.append(f'===== {n} =====')
            lines.append(strip_xml_to_text(z.read(n).decode('utf-8')))
        for n in sorted(notes, key=key):
            lines.append(f'===== NOTES {n} =====')
            lines.append(strip_xml_to_text(z.read(n).decode('utf-8')))
    text = '\n'.join(lines)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'pptx -> {out} ({len(text)} chars)')

if __name__ == '__main__':
    extract_docx(os.path.join(BASE, 'EE5609_RFBus_Group_演讲稿.docx'),
                 os.path.join(BASE, '演讲稿_extracted.txt'))
    extract_pptx(os.path.join(BASE, 'EE5609_RFBus_Group 14_zzq.pptx'),
                 os.path.join(BASE, 'pptx_zzq_extracted.txt'))
    p2 = os.path.join(BASE, 'Group14_Intro_Presentation.pptx')
    if os.path.exists(p2):
        extract_pptx(p2, os.path.join(BASE, 'pptx_intro_extracted.txt'))
