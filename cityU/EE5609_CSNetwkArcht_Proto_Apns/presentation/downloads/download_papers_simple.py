#!/usr/bin/env python3
"""
简化版论文下载脚本 - 直接从开放获取源下载
"""

import requests
import time
import json
from pathlib import Path

# 从validated JSON读取DOI列表
def load_dois(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [(ref['id'], ref['doi']) for ref in data['references'] if ref.get('doi')]

# Sci-Hub镜像（需要自己找最新可用的）
SCI_HUB_MIRRORS = [
    "https://sci-hub.se",
    "https://sci-hub.st", 
    "https://sci-hub.ru",
]

# 直接下载链接（作者主页或开放获取）
DIRECT_URLS = {
    "10.1145/2491172.2491198": [
        "https://homes.cs.washington.edu/~gshyam/Papers/ambient_backscatter.pdf",
    ],
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/pdf,*/*",
}

def download_from_url(url, save_path, timeout=60):
    """从URL下载PDF"""
    try:
        print(f"  尝试: {url}")
        response = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        
        if response.status_code == 200:
            # 检查是否为PDF
            if response.content[:4] == b"%PDF":
                save_path.write_bytes(response.content)
                print(f"  ✓ 下载成功!")
                return True
            else:
                print(f"  ✗ 不是PDF文件")
        else:
            print(f"  ✗ HTTP {response.status_code}")
    except Exception as e:
        print(f"  ✗ 错误: {e}")
    
    return False

def download_from_scihub(doi, save_path, timeout=60):
    """从Sci-Hub下载"""
    for mirror in SCI_HUB_MIRRORS:
        url = f"{mirror}/{doi}"
        try:
            print(f"  尝试Sci-Hub: {url}")
            response = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
            
            if response.status_code == 200:
                # 检查是否为PDF
                if response.content[:4] == b"%PDF":
                    save_path.write_bytes(response.content)
                    print(f"  ✓ Sci-Hub下载成功!")
                    return True
                
                # 尝试从HTML中提取PDF链接
                if "text/html" in response.headers.get("Content-Type", ""):
                    import re
                    pdf_match = re.search(r'(https?://[^"\']+\.pdf)', response.text)
                    if pdf_match:
                        pdf_url = pdf_match.group(1)
                        print(f"  找到PDF链接: {pdf_url}")
                        pdf_response = requests.get(pdf_url, headers=HEADERS, timeout=timeout)
                        if pdf_response.status_code == 200 and pdf_response.content[:4] == b"%PDF":
                            save_path.write_bytes(pdf_response.content)
                            print(f"  ✓ Sci-Hub下载成功!")
                            return True
            
            print(f"  ✗ {mirror} 失败")
        except Exception as e:
            print(f"  ✗ {mirror} 错误: {e}")
        
        time.sleep(1)
    
    return False

def main():
    # 项目目录
    project_dir = Path("/mnt/d/ProjectStore/CityuTest/cityU/EE5609_CSNetwkArcht_Proto_Apns/presentation/rfbus_intro_refs")
    json_path = project_dir / "refs_validated.json"
    
    if not json_path.exists():
        print(f"错误: 找不到 {json_path}")
        print("请先运行 validate_refs.py")
        return
    
    # 加载DOI列表
    dois = load_dois(json_path)
    print(f"找到 {len(dois)} 个DOI")
    print("=" * 60)
    
    success = []
    failed = []
    
    for ref_id, doi in dois:
        print(f"\n[{ref_id}] DOI: {doi}")
        
        # 生成文件名
        filename = f"{ref_id:02d}_{doi.replace('/', '_')}.pdf"
        save_path = project_dir / filename
        
        # 如果已存在，跳过
        if save_path.exists():
            print(f"  ✓ 已存在: {filename}")
            success.append((ref_id, doi))
            continue
        
        # 先尝试直接链接
        downloaded = False
        if doi in DIRECT_URLS:
            for url in DIRECT_URLS[doi]:
                if download_from_url(url, save_path):
                    downloaded = True
                    break
        
        # 如果直接链接失败，尝试Sci-Hub
        if not downloaded:
            if download_from_scihub(doi, save_path):
                downloaded = True
        
        if downloaded:
            success.append((ref_id, doi))
        else:
            failed.append((ref_id, doi))
        
        time.sleep(2)  # 避免请求过快
    
    # 打印总结
    print("\n" + "=" * 60)
    print(f"下载完成: {len(success)}/{len(dois)} 成功")
    
    if failed:
        print(f"\n失败的论文 ({len(failed)}篇):")
        for ref_id, doi in failed:
            print(f"  [{ref_id}] {doi}")
            print(f"      手动下载: https://sci-hub.se/{doi}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
