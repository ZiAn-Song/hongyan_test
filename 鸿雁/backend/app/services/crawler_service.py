"""
网络爬虫服务 - 定期从官方网站爬取边疆相关资讯。

信源：
  1. 民政部 (www.mca.gov.cn)
  2. 新华社 (www.news.cn)
  3. 新疆政府网 (www.xinjiang.gov.cn)
  4. 国家民委 (www.neac.gov.cn)
  5. 国家发改委 (www.ndrc.gov.cn)
  6. 工信部 (www.miit.gov.cn)
  7. 中国政府网 (www.gov.cn)
  8. 边疆研究所 (bjs.cssn.cn)

每个信源从首页提取文章链接，用关键词过滤边疆相关内容，
然后逐条抓取详情页并存储到 crawled_articles 表。
"""

import re
import time
import random
import logging
import urllib3
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.crawler import CrawledArticle

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

BORDER_KEYWORDS = [
    "边疆", "边境", "援疆", "援藏", "对口支援", "东西协作",
    "民族", "少数民族", "脱贫", "乡村振兴", "对口帮扶",
    "西部", "边防", "戍边", "固边", "兴边",
    "帮扶", "支援", "兴边富民", "守边", "边民",
    "富民", "固边行动", "边境村", "边防派出所",
    "对口合作", "援外", "帮扶协作",
    # 边疆省区及核心城市
    "新疆", "西藏", "内蒙古", "广西", "宁夏",
    "乌鲁木齐", "喀什", "伊犁", "阿克苏", "塔城", "和田", "哈密",
    "拉萨", "日喀则", "林芝", "那曲",
    "南宁", "崇左", "防城港", "百色",
    "银川", "固原",
    # 边境相关概念
    "侨务", "口岸", "跨境", "边贸", "丝路",
]

CONTENT_KEYWORDS = [
    "边疆", "边境", "援疆", "援藏", "对口支援", "东西协作",
    "民族", "少数民族", "脱贫", "乡村振兴", "对口帮扶",
    "西部", "边防", "戍边", "固边", "兴边",
    "帮扶", "支援", "固边行动", "边境村",
    "新疆", "西藏", "内蒙古", "广西", "宁夏", "云南",
    "甘肃", "青海", "黑龙江", "吉林", "辽宁",
    "乌鲁木齐", "喀什", "伊犁", "拉萨", "日喀则",
    "南宁", "银川", "口岸", "跨境", "边贸",
]

SOURCES = {
    "mca": {"name": "民政部", "url": "https://www.mca.gov.cn"},
    "xinhua": {"name": "新华社", "url": "https://www.news.cn"},
    "xinjiang": {"name": "新疆政府网", "url": "https://www.xinjiang.gov.cn"},
    "neac": {"name": "国家民委", "url": "https://www.neac.gov.cn"},
    "ndrc": {"name": "国家发改委", "url": "https://www.ndrc.gov.cn"},
    "miit": {"name": "工信部", "url": "https://www.miit.gov.cn"},
    "gov": {"name": "中国政府网", "url": "https://www.gov.cn"},
    "bjs": {"name": "边疆研究所", "url": "http://bjs.cssn.cn"},
}


class BaseCrawler:
    """爬虫基类，提供 HTTP 请求、HTML 解析和存储的通用方法。"""

    source_key: str = ""
    source_name: str = ""
    base_url: str = ""

    def __init__(self, db: Session):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch(self, url: str, retries: int = 2) -> str | None:
        for attempt in range(retries):
            try:
                resp = self.session.get(url, timeout=15, verify=False)
                resp.encoding = resp.apparent_encoding or "utf-8"
                time.sleep(random.uniform(1.0, 2.0))
                if resp.status_code == 200:
                    return resp.text
                logger.warning(f"HTTP {resp.status_code}: {url}")
            except requests.RequestException as e:
                logger.warning(f"Fetch failed (attempt {attempt+1}): {url} - {e}")
        return None

    def is_article_link(self, href: str, title: str) -> bool:
        """判断链接是否为文章详情页链接。"""
        if not href or not title or len(title) < 8:
            return False
        if "list" in href or "index" in href:
            return False
        return True

    def is_border_related(self, title: str) -> bool:
        """判断标题是否与边疆相关。"""
        return any(kw in title for kw in BORDER_KEYWORDS)

    def is_content_relevant(self, title: str, content: str) -> bool:
        """判断标题或正文是否与边疆相关（用于详情页二次筛选）。"""
        text = (title or "") + " " + (content or "")
        return any(kw in text for kw in CONTENT_KEYWORDS)

    def resolve_url(self, href: str) -> str:
        """将相对 URL 解析为绝对 URL。"""
        if href.startswith("http"):
            return href
        if href.startswith("//"):
            return "https:" + href
        return urljoin(self.base_url, href)

    def extract_date(self, text: str) -> datetime | None:
        """从文本中提取日期。"""
        if not text:
            return None
        for pattern in [
            r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})",
            r"(\d{4})年(\d{1,2})月(\d{1,2})日",
        ]:
            m = re.search(pattern, text)
            if m:
                try:
                    return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                except ValueError:
                    pass
        return None

    def save_article(self, data: dict) -> bool:
        """存储文章到数据库，跳过已存在的 URL。"""
        url = data.get("source_url", "").strip()
        if not url:
            return False
        existing = self.db.execute(
            select(CrawledArticle).where(CrawledArticle.source_url == url)
        ).scalar_one_or_none()
        if existing:
            return False
        article = CrawledArticle(
            title=data.get("title", "无标题")[:500],
            source=self.source_name,
            source_url=url,
            content=data.get("content"),
            summary=data.get("summary", ""),
            author=data.get("author"),
            publish_date=data.get("publish_date"),
            category=data.get("category"),
            region=data.get("region"),
        )
        self.db.add(article)
        self.db.commit()
        return True

    def run(self) -> tuple[int, list[str]]:
        """执行爬取流程：抓首页 -> 提取链接 -> 过滤 -> 逐条抓详情页 -> 存储。"""
        crawled = 0
        errors = []

        for list_url in self.get_list_urls():
            html = self.fetch(list_url)
            if not html:
                errors.append(f"页面获取失败: {list_url}")
                continue

            articles = self.parse_list(html)
            logger.info(f"[{self.source_name}] 解析到 {len(articles)} 条候选链接")

            seen_urls = set()
            for item in articles[:30]:
                detail_url = item.get("url", "")
                if not detail_url or detail_url in seen_urls:
                    continue
                seen_urls.add(detail_url)
                detail_url = self.resolve_url(detail_url)

                detail_html = self.fetch(detail_url)
                if not detail_html:
                    errors.append(f"详情页获取失败: {detail_url}")
                    continue

                data = self.parse_detail(detail_html, detail_url)
                if data.get("title") and len(data["title"]) > 5:
                    if not self.is_content_relevant(data["title"], data.get("content", "")):
                        logger.debug(f"[{self.source_name}] 跳过无关文章: {data['title'][:40]}")
                        continue
                    if self.save_article(data):
                        crawled += 1
                        logger.info(f"[{self.source_name}] 已保存: {data['title'][:50]}")

        return crawled, errors

    def get_list_urls(self) -> list[str]:
        raise NotImplementedError

    def parse_list(self, html: str) -> list[dict]:
        raise NotImplementedError

    def parse_detail(self, html: str, url: str) -> dict:
        raise NotImplementedError


class McaCrawler(BaseCrawler):
    """民政部爬虫 - 从 www.mca.gov.cn 首页和对口支援栏目提取边疆相关新闻。"""

    source_key = "mca"
    source_name = "民政部"
    base_url = "https://www.mca.gov.cn"

    def get_list_urls(self) -> list[str]:
        return [
            "https://www.mca.gov.cn/",
            "https://www.mca.gov.cn/n152/n164/",
            "https://www.mca.gov.cn/n152/n168/",
        ]

    def parse_list(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        seen = set()
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            title = a.get_text(strip=True)
            if not self.is_article_link(href, title):
                continue
            if "content.html" not in href and not re.search(r"/c\d+/", href):
                continue
            if not self.is_border_related(title):
                continue
            full_url = self.resolve_url(href)
            if full_url not in seen:
                seen.add(full_url)
                articles.append({"url": href, "title": title})
        return articles

    def parse_detail(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        title = ""
        for tag in soup.find_all(["h1", "h2", "h3"]):
            t = tag.get_text(strip=True)
            if t and len(t) > 5:
                title = t
                break
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True).split("-")[0].strip()

        content = ""
        for cls in ["content", "TRS_Editor", "article", "detail", "pages_content"]:
            div = soup.find("div", class_=re.compile(cls, re.I))
            if div:
                content = div.get_text("\n", strip=True)
                if len(content) > 50:
                    break
        if not content:
            for cid in ["content", "zoom", "article"]:
                div = soup.find("div", id=re.compile(cid, re.I))
                if div:
                    content = div.get_text("\n", strip=True)
                    if len(content) > 50:
                        break

        publish_date = self.extract_date(soup.get_text()[:2000])

        return {
            "title": title or "无标题",
            "source_url": url,
            "content": content[:10000] if content else "",
            "summary": content[:300] if content else "",
            "publish_date": publish_date,
            "category": "民政新闻",
            "region": "全国",
        }


class XinhuaCrawler(BaseCrawler):
    """新华社爬虫 - 从 www.news.cn 首页和时政/地方频道提取边疆相关新闻。"""

    source_key = "xinhua"
    source_name = "新华社"
    base_url = "https://www.news.cn"

    def get_list_urls(self) -> list[str]:
        return [
            "https://www.news.cn/",
            "https://www.news.cn/politics/",
            "https://www.news.cn/local/",
        ]

    def parse_list(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        seen = set()
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            title = a.get_text(strip=True)
            if not self.is_article_link(href, title):
                continue
            if "/c.html" not in href and "/c.htm" not in href:
                continue
            if not self.is_border_related(title):
                continue
            full_url = self.resolve_url(href)
            if full_url not in seen:
                seen.add(full_url)
                articles.append({"url": href, "title": title})
        return articles

    def parse_detail(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        title = ""
        title_tag = soup.find("h1")
        if title_tag:
            title = title_tag.get_text(strip=True)
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True).split("-")[0].strip()

        content = ""
        for cls in ["article", "content", "detail", "TRS_Editor", "pages_content", "xl_content"]:
            div = soup.find("div", class_=re.compile(cls, re.I))
            if div:
                content = div.get_text("\n", strip=True)
                if len(content) > 100:
                    break
        if not content:
            main = soup.find("div", class_=re.compile("main|text|body", re.I))
            if main:
                ps = main.find_all("p")
                content = "\n".join(p.get_text(strip=True) for p in ps if len(p.get_text(strip=True)) > 10)

        publish_date = self.extract_date(soup.get_text()[:3000])

        return {
            "title": title or "无标题",
            "source_url": url,
            "content": content[:10000] if content else "",
            "summary": content[:300] if content else "",
            "publish_date": publish_date,
            "category": "新闻资讯",
            "region": "边疆地区",
        }


class XinjiangGovCrawler(BaseCrawler):
    """新疆政府网爬虫 - 从 www.xinjiang.gov.cn 提取边疆相关新闻。
    使用标题关键词过滤，排除跨省转发的全国性新闻。"""

    source_key = "xinjiang"
    source_name = "新疆政府网"
    base_url = "https://www.xinjiang.gov.cn"

    def get_list_urls(self) -> list[str]:
        return [
            "https://www.xinjiang.gov.cn/",
            "https://www.xinjiang.gov.cn/xinjiang/bmdt/",
            "https://www.xinjiang.gov.cn/xinjiang/xjdt/",
        ]

    def parse_list(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        seen = set()
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            title = a.get_text(strip=True)
            if not self.is_article_link(href, title):
                continue
            if ".shtml" not in href:
                continue
            if "list" in href or "index" in href:
                continue
            if not self.is_border_related(title):
                continue
            full_url = self.resolve_url(href)
            if full_url not in seen:
                seen.add(full_url)
                articles.append({"url": href, "title": title})
        return articles

    def parse_detail(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        title = ""
        for tag in soup.find_all(["h1", "h2", "h3"]):
            t = tag.get_text(strip=True)
            if t and len(t) > 5:
                title = t
                break
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True).split("-")[0].split("_")[0].strip()

        content = ""
        for cls in ["content", "TRS_Editor", "article", "detail", "zoom", "pages_content", "main-text"]:
            div = soup.find("div", class_=re.compile(cls, re.I))
            if div:
                content = div.get_text("\n", strip=True)
                if len(content) > 50:
                    break
        if not content or len(content) < 100:
            for cid in ["content", "zoom", "article", "main-text"]:
                div = soup.find("div", id=re.compile(cid, re.I))
                if div:
                    content = div.get_text("\n", strip=True)
                    if len(content) > 50:
                        break
        if not content or len(content) < 100:
            main = soup.find("div", class_=re.compile("main|body|text", re.I))
            if main:
                ps = main.find_all("p")
                content = "\n".join(p.get_text(strip=True) for p in ps if len(p.get_text(strip=True)) > 10)

        publish_date = self.extract_date(soup.get_text()[:3000])

        return {
            "title": title or "无标题",
            "source_url": url,
            "content": content[:10000] if content else "",
            "summary": content[:300] if content else "",
            "publish_date": publish_date,
            "category": "政府公告",
            "region": "新疆",
        }


class NeacCrawler(BaseCrawler):
    """国家民委爬虫 - 从 www.neac.gov.cn 提取民族/边疆相关新闻。
    国家民委本身就是民族事务主管部门，内容天然相关，保留标题过滤排除无关内容。"""

    source_key = "neac"
    source_name = "国家民委"
    base_url = "https://www.neac.gov.cn"

    def get_list_urls(self) -> list[str]:
        return [
            "https://www.neac.gov.cn/",
            "https://www.neac.gov.cn/seac/xwzx/index.shtml",
            "https://www.neac.gov.cn/seac/xwzx/mwyw/index.shtml",
        ]

    def parse_list(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        seen = set()
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            title = a.get_text(strip=True)
            if not self.is_article_link(href, title):
                continue
            if ".shtml" not in href:
                continue
            if "list" in href or "index" in href:
                continue
            if not self.is_border_related(title):
                continue
            full_url = self.resolve_url(href)
            if full_url not in seen:
                seen.add(full_url)
                articles.append({"url": href, "title": title})
        return articles

    def parse_detail(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        title = ""
        for tag in soup.find_all(["h1", "h2", "h3"]):
            t = tag.get_text(strip=True)
            if t and len(t) > 5:
                title = t
                break
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True).split("-")[0].split("_")[0].strip()

        content = ""
        for cls in ["p3", "TRS_Editor", "content", "article", "detail", "pages_content"]:
            div = soup.find("div", class_=re.compile(cls, re.I))
            if div:
                content = div.get_text("\n", strip=True)
                if len(content) > 50:
                    break
        if not content or len(content) < 100:
            for cid in ["content", "zoom", "article"]:
                div = soup.find("div", id=re.compile(cid, re.I))
                if div:
                    content = div.get_text("\n", strip=True)
                    if len(content) > 50:
                        break

        publish_date = self.extract_date(soup.get_text()[:3000])

        return {
            "title": title or "无标题",
            "source_url": url,
            "content": content[:10000] if content else "",
            "summary": content[:300] if content else "",
            "publish_date": publish_date,
            "category": "民族事务",
            "region": "全国",
        }


class NdrcCrawler(BaseCrawler):
    """国家发改委爬虫 - 从 www.ndrc.gov.cn 提取边疆/西部/对口支援相关新闻。"""

    source_key = "ndrc"
    source_name = "国家发改委"
    base_url = "https://www.ndrc.gov.cn"

    def get_list_urls(self) -> list[str]:
        return [
            "https://www.ndrc.gov.cn/",
            "https://www.ndrc.gov.cn/xwdt/xwfb/",
            "https://www.ndrc.gov.cn/xwdt/dt/dfdt/",
        ]

    def parse_list(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        seen = set()
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            title = a.get_text(strip=True)
            if not self.is_article_link(href, title):
                continue
            if "/t" not in href or ".html" not in href:
                continue
            if "list" in href or "index" in href:
                continue
            if not self.is_border_related(title):
                continue
            full_url = self.resolve_url(href)
            if full_url not in seen:
                seen.add(full_url)
                articles.append({"url": href, "title": title})
        return articles

    def parse_detail(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        title = ""
        title_tag = soup.find("h2", class_=re.compile("article_title", re.I))
        if title_tag:
            title = title_tag.get_text(strip=True)
        if not title:
            for tag in soup.find_all(["h1", "h2", "h3"]):
                t = tag.get_text(strip=True)
                if t and len(t) > 5:
                    title = t
                    break
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True).split("-")[0].split("_")[0].strip()

        content = ""
        for cls in ["article_con", "TRS_Editor", "article", "content", "detail"]:
            div = soup.find("div", class_=re.compile(cls, re.I))
            if div:
                content = div.get_text("\n", strip=True)
                if len(content) > 50:
                    break
        if not content or len(content) < 100:
            for cid in ["content", "zoom", "article"]:
                div = soup.find("div", id=re.compile(cid, re.I))
                if div:
                    content = div.get_text("\n", strip=True)
                    if len(content) > 50:
                        break

        publish_date = self.extract_date(soup.get_text()[:3000])

        return {
            "title": title or "无标题",
            "source_url": url,
            "content": content[:10000] if content else "",
            "summary": content[:300] if content else "",
            "publish_date": publish_date,
            "category": "发改要闻",
            "region": "全国",
        }


class MiitCrawler(BaseCrawler):
    """工信部爬虫 - 从 www.miit.gov.cn 提取边疆/民族/西部相关新闻。"""

    source_key = "miit"
    source_name = "工信部"
    base_url = "https://www.miit.gov.cn"

    def get_list_urls(self) -> list[str]:
        return [
            "https://www.miit.gov.cn/",
            "https://www.miit.gov.cn/xwfb/index.html",
            "https://www.miit.gov.cn/xwfb/szyw/index.html",
        ]

    def parse_list(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        seen = set()
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            title = a.get_text(strip=True)
            if not self.is_article_link(href, title):
                continue
            if "/art/" not in href or ".html" not in href:
                continue
            if "list" in href or "index" in href:
                continue
            if not self.is_border_related(title):
                continue
            full_url = self.resolve_url(href)
            if full_url not in seen:
                seen.add(full_url)
                articles.append({"url": href, "title": title})
        return articles

    def parse_detail(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        title = ""
        title_tag = soup.find(id="con_title")
        if title_tag:
            title = title_tag.get_text(strip=True)
        if not title:
            for tag in soup.find_all(["h1", "h2", "h3"]):
                t = tag.get_text(strip=True)
                if t and len(t) > 5:
                    title = t
                    break
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True).split("-")[0].split("_")[0].strip()

        content = ""
        content_div = soup.find(id="con_con")
        if content_div:
            content = content_div.get_text("\n", strip=True)
        if not content or len(content) < 50:
            for cls in ["TRS_Editor", "ccontent", "article", "content", "detail"]:
                div = soup.find("div", class_=re.compile(cls, re.I))
                if div:
                    content = div.get_text("\n", strip=True)
                    if len(content) > 50:
                        break

        publish_date = self.extract_date(soup.get_text()[:3000])

        return {
            "title": title or "无标题",
            "source_url": url,
            "content": content[:10000] if content else "",
            "summary": content[:300] if content else "",
            "publish_date": publish_date,
            "category": "工信要闻",
            "region": "全国",
        }


class GovCrawler(BaseCrawler):
    """中国政府网爬虫 - 从 www.gov.cn 提取边疆/民族/西部相关新闻。"""

    source_key = "gov"
    source_name = "中国政府网"
    base_url = "https://www.gov.cn"

    def get_list_urls(self) -> list[str]:
        return [
            "https://www.gov.cn/",
            "https://www.gov.cn/yaowen/liebiao/",
            "https://www.gov.cn/lianbo/difang/",
        ]

    def parse_list(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        seen = set()
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            title = a.get_text(strip=True)
            if not self.is_article_link(href, title):
                continue
            if "content_" not in href or ".htm" not in href:
                continue
            if "list" in href or "index" in href:
                continue
            if not self.is_border_related(title):
                continue
            full_url = self.resolve_url(href)
            if full_url not in seen:
                seen.add(full_url)
                articles.append({"url": href, "title": title})
        return articles

    def parse_detail(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        title = ""
        for tag in soup.find_all(["h1", "h2", "h3"]):
            t = tag.get_text(strip=True)
            if t and len(t) > 5:
                title = t
                break
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True).split("-")[0].split("_")[0].strip()

        content = ""
        content_div = soup.find(id="UCAP-CONTENT")
        if content_div:
            content = content_div.get_text("\n", strip=True)
        if not content or len(content) < 50:
            for cls in ["pages_content", "TRS_Editor", "trs_editor_view", "article", "content", "detail"]:
                div = soup.find("div", class_=re.compile(cls, re.I))
                if div:
                    content = div.get_text("\n", strip=True)
                    if len(content) > 50:
                        break

        publish_date = self.extract_date(soup.get_text()[:3000])

        return {
            "title": title or "无标题",
            "source_url": url,
            "content": content[:10000] if content else "",
            "summary": content[:300] if content else "",
            "publish_date": publish_date,
            "category": "政府要闻",
            "region": "全国",
        }


class BjsCrawler(BaseCrawler):
    """边疆研究所爬虫 - 从 bjs.cssn.cn 提取边疆研究相关文章。
    边疆研究所本身就是边疆研究机构，内容天然相关。"""

    source_key = "bjs"
    source_name = "边疆研究所"
    base_url = "http://bjs.cssn.cn"

    def get_list_urls(self) -> list[str]:
        return [
            "http://bjs.cssn.cn/",
            "http://bjs.cssn.cn/top_news/news/",
        ]

    def parse_list(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        seen = set()
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            title = a.get_text(strip=True)
            if not self.is_article_link(href, title):
                continue
            if ".shtml" not in href:
                continue
            if "list" in href or "index" in href:
                continue
            full_url = self.resolve_url(href)
            if full_url not in seen:
                seen.add(full_url)
                articles.append({"url": href, "title": title})
        return articles

    def parse_detail(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        title = ""
        title_tag = soup.find("h1", class_=re.compile("article-title", re.I))
        if title_tag:
            title = title_tag.get_text(strip=True)
        if not title:
            for tag in soup.find_all(["h1", "h2", "h3"]):
                t = tag.get_text(strip=True)
                if t and len(t) > 5:
                    title = t
                    break
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True).split("-")[0].split("_")[0].strip()

        content = ""
        for cls in ["article-body", "TRS_Editor", "m-article-body", "content", "article", "detail"]:
            div = soup.find("div", class_=re.compile(cls, re.I))
            if div:
                content = div.get_text("\n", strip=True)
                if len(content) > 50:
                    break

        publish_date = self.extract_date(soup.get_text()[:3000])

        return {
            "title": title or "无标题",
            "source_url": url,
            "content": content[:10000] if content else "",
            "summary": content[:300] if content else "",
            "publish_date": publish_date,
            "category": "边疆研究",
            "region": "边疆地区",
        }


CRAWLER_MAP = {
    "mca": McaCrawler,
    "xinhua": XinhuaCrawler,
    "xinjiang": XinjiangGovCrawler,
    "neac": NeacCrawler,
    "ndrc": NdrcCrawler,
    "miit": MiitCrawler,
    "gov": GovCrawler,
    "bjs": BjsCrawler,
}


def run_crawler(db: Session, source: str | None = None) -> tuple[int, list[str]]:
    """运行爬虫。source 为 None 时运行全部信源。"""
    total_crawled = 0
    all_errors = []

    sources = [source] if source else list(CRAWLER_MAP.keys())
    for src_key in sources:
        crawler_cls = CRAWLER_MAP.get(src_key)
        if not crawler_cls:
            all_errors.append(f"未知信源: {src_key}")
            continue
        crawler = crawler_cls(db)
        try:
            crawled, errors = crawler.run()
            total_crawled += crawled
            all_errors.extend(errors)
        except Exception as e:
            logger.error(f"[{crawler.source_name}] 爬取异常: {e}")
            all_errors.append(f"{crawler.source_name} 异常: {str(e)}")

    return total_crawled, all_errors
