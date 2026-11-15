import subprocess
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

TARGET_DIR = r"D:\Projects\one2oneTutorial\cityU\EE8403\course_files_export"
OUTPUT_DIR = r"D:\Projects\one2oneTutorial\cityU\EE8403\extracted_texts"

def extract_pdf_text(pdf_path, output_path):
    """使用pdftotext提取PDF文本"""
    try:
        result = subprocess.run(
            ['pdftotext', '-layout', pdf_path, output_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return True, f"成功提取PDF: {os.path.basename(pdf_path)}"
        else:
            return False, f"PDF提取失败: {result.stderr}"
    except Exception as e:
        return False, f"PDF提取错误: {str(e)}"

def extract_pptx_text(pptx_path, output_path):
    """从PPTX文件中提取文本（PPTX是ZIP格式）"""
    try:
        texts = []
        with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
            # 查找所有slide XML文件
            slide_files = [f for f in zip_ref.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
            slide_files.sort()
            
            for slide_file in slide_files:
                with zip_ref.open(slide_file) as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    # 命名空间
                    ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
                    # 提取所有文本
                    for text_elem in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
                        if text_elem.text:
                            texts.append(text_elem.text)
        
        # 写入文本文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(texts))
        
        return True, f"成功提取PPTX: {os.path.basename(pptx_path)} ({len(texts)} 个文本元素)"
    except Exception as e:
        return False, f"PPTX提取错误: {str(e)}"

def main():
    results = []
    
    # 遍历目标目录
    for filename in sorted(os.listdir(TARGET_DIR)):
        filepath = os.path.join(TARGET_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        
        base_name = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == '.pdf':
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}.txt")
            success, message = extract_pdf_text(filepath, output_file)
            results.append({
                'file': filename,
                'type': 'PDF',
                'success': success,
                'message': message,
                'output': output_file if success else None
            })
            print(message)
            
        elif ext in ['.pptx', '.ppt']:
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}.txt")
            success, message = extract_pptx_text(filepath, output_file)
            results.append({
                'file': filename,
                'type': 'PPTX',
                'success': success,
                'message': message,
                'output': output_file if success else None
            })
            print(message)
    
    # 输出汇总
    print("\n" + "="*80)
    print("提取完成汇总:")
    print("="*80)
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count
    print(f"总计: {len(results)} 个文件")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    
    # 保存结果JSON
    import json
    result_file = os.path.join(OUTPUT_DIR, "extraction_results.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n详细结果已保存到: {result_file}")

if __name__ == '__main__':
    main()
