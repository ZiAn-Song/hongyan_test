import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# Try to find border-related sections on each site
sites = {
    'mca': {
        'home': 'https://www.mca.gov.cn/',
        'sections': [
            'https://www.mca.gov.cn/n152/n166/',  # 新闻
            'https://www.mca.gov.cn/n152/n183/',  # 对口支援
            'https://www.mca.gov.cn/n152/',
            'https://www.mca.gov.cn/n152/n164/',
        ],
    },
    'xinhua': {
        'home': 'https://www.news.cn/',
        'sections': [
            'https://www.news.cn/politics/',
            'https://www.news.cn/local/',
            'https://www.news.cn/fortune/',
        ],
    },
    'xinjiang': {
        'home': 'https://www.xinjiang.gov.cn/',
        'sections': [
            'https://www.xinjiang.gov.cn/xinjiang/xwtt/',  # 新闻头条
            'https://www.xinjiang.gov.cn/xinjiang/bmdt/',  # 部门动态
            'https://www.xinjiang.gov.cn/xinjiang/spxw/',  # 视频新闻
        ],
    },
}

border_keywords = ['边疆', '边境', '援疆', '援藏', '对口', '民族', '脱贫', '乡村',
                   '西部', '边防', '戍边', '固边', '兴边', '帮扶', '支援', '民生',
                   '发展', '振兴', '合作', '协作']

for site_name, site_data in sites.items():
    print(f'========== {site_name} ==========')
    for url in [site_data['home']] + site_data['sections']:
        try:
            resp = requests.get(url, headers=headers, timeout=15, verify=False)
            resp.encoding = resp.apparent_encoding or 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            links = soup.select('a[href]')
            border_links = []
            for a in links:
                title = a.get_text(strip=True)
                href = a.get('href', '')
                if title and len(title) > 8 and href:
                    if any(kw in title for kw in border_keywords):
                        border_links.append((title[:60], href[:80]))
            print(f'  URL: {url}')
            print(f'  Status: {resp.status_code}, Links: {len(links)}, Border-related: {len(border_links)}')
            for t, h in border_links[:8]:
                print(f'    {t} -> {h}')
            print()
        except Exception as e:
            print(f'  URL: {url} -> ERROR: {e}')
            print()
