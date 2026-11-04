#!/usr/bin/env python3
"""
论文下载脚本 - 尝试从开放获取源下载
"""

import requests
import time
from pathlib import Path

# 论文列表：(文件名, DOI, 直接下载链接或搜索链接)
PAPERS = [
    {
        "filename": "01_Hempstead_2005_ISCA.pdf",
        "doi": "10.1109/ISCA.2005.32",
        "title": "An ultra low power system architecture for sensor network applications",
        "year": 2005,
        "urls": [
            "https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=10.1.1.85.8536",
        ]
    },
    {
        "filename": "02_Ambient_Backscatter_2013_SIGCOMM.pdf",
        "doi": "10.1145/2491172.2491198",
        "title": "Ambient backscatter: Wireless communication out of thin air",
        "year": 2013,
        "urls": [
            "https://homes.cs.washington.edu/~gshyam/Papers/ambient_backscatter.pdf",
            "https://dl.acm.org/doi/pdf/10.1145/2491172.2491198",
        ]
    },
    {
        "filename": "03_IoM_2020_MobiCom.pdf",
        "doi": "10.1145/3372224.3419193",
        "title": "Internet-of-microchips: direct radio-to-bus communication with SPI backscatter",
        "year": 2020,
        "urls": [
            "https://dl.acm.org/doi/pdf/10.1145/3372224.3419193",
        ]
    },
    {
        "filename": "04_ChipNet_2022_TOSN.pdf",
        "doi": "10.1145/3532185",
        "title": "ChipNet: Enabling large-scale backscatter network with processor-free devices",
        "year": 2022,
        "urls": [
            "https://dl.acm.org/doi/pdf/10.1145/3532185",
        ]
    },
    {
        "filename": "05_LEGO_2023_ASPLOS.pdf",
        "doi": "10.1145/3582010.3582044",
        "title": "LEGO: Empowering chip-level functionality plug-and-play for next-generation IoT devices",
        "year": 2023,
        "urls": [
            "https://dl.acm.org/doi/pdf/10.1145/3582010.3582044",
        ]
    },
    {
        "filename": "06_RFBus_2024_SenSys.pdf",
        "doi": "10.1145/3666025.3699333",
        "title": "Processor-sharing Internet of Things architecture for large-scale deployment",
        "year": 2024,
        "urls": [
            "https://dl.acm.org/doi/pdf/10.1145/3666025.3699333",
        ]
    },
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/pdf,*/*",
}


def download_paper(paper: dict, save_dir: Path) -> bool:
    """尝试下载单篇论文"""
    save_path = save_dir / paper["filename"]
    
    # 如果已存在，跳过
    if save_path.exists():
        print(f"  ✓ 已存在: {paper['filename']}")
        return True
    
    for url in paper["urls"]:
        try:
            print(f"  尝试: {url}")
            response = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
            
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                if "application/pdf" in content_type or response.content[:4] == b"%PDF":
                    save_path.write_bytes(response.content)
                    print(f"  ✓ 下载成功!")
                    return True
                else:
                    print(f"  ✗ 不是PDF (Content-Type: {content_type})")
            
        except Exception as e:
            print(f"  ✗ 错误: {e}")
    
    return False


def main():
    script_dir = Path(__file__).parent
    download_dir = script_dir / "papers"
    download_dir.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("论文下载工具 - 开放获取源")
    print(f"保存目录: {download_dir}")
    print("=" * 70)
    
    success = []
    failed = []
    
    for paper in PAPERS:
        print(f"\n[{paper['year']}] {paper['title'][:60]}...")
        print(f"DOI: {paper['doi']}")
        
        if download_paper(paper, download_dir):
            success.append(paper)
        else:
            failed.append(paper)
        
        time.sleep(1)
    
    print("\n" + "=" * 70)
    print(f"下载完成: {len(success)}/{len(PAPERS)} 成功")
    
    if failed:
        print(f"\n需要手动下载的论文 ({len(failed)}篇):")
        for p in failed:
            print(f"\n  [{p['year']}] {p['title']}")
            print(f"  DOI: {p['doi']}")
            print(f"  下载链接:")
            print(f"    - ACM DL: https://dl.acm.org/doi/{p['doi']}")
            print(f"    - Sci-Hub: https://sci-hub.se/{p['doi']}")
            print(f"    - Google Scholar: https://scholar.google.com/scholar?q={p['title'].replace(' ', '+')}")
    
    print("\n" + "=" * 70)
    print("\n手动下载建议:")
    print("1. 访问学校图书馆的 ACM Digital Library 数据库")
    print("2. 使用 Google Scholar 搜索论文标题，查看是否有免费PDF")
    print("3. 访问作者个人主页，通常会提供预印本")
    print("4. 使用浏览器插件 Unpaywall 自动查找合法免费版本")


if __name__ == "__main__":
    main()
