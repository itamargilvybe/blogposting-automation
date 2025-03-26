import requests
from bs4 import BeautifulSoup
from config import BLOG_SITEMAP_URL

def get_blog_urls_from_sitemap(sitemap_url=BLOG_SITEMAP_URL):
    try:
        res = requests.get(sitemap_url)
        soup = BeautifulSoup(res.content, 'xml')

        urls = []
        for url in soup.find_all("url"):
            loc = url.find("loc").text
            if "/blog/" in loc and "[object Object]" not in loc:
                urls.append(loc)

        return urls
    except Exception as e:
        print(f"Error reading sitemap: {e}")
        return []
