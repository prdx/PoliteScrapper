import requests
from bs4 import BeautifulSoup
from engine.data_structures import Heap, Link
from engine.extractor import extract_links, extract_text
from engine.robot import polite
from engine.writer import store
from urllib.parse import urlparse

def fetch(session, url, timeout = 1):
    """Fetch the head before downloding the page
    """
    try:
        session.head(url)
        # Make sure it accepts text/html
        headers={"accept": "text/html"}
        res = session.get(url, headers=headers)
        # TODO: Use constants
        if res.status_code == 200:
            html = res.text

            # Pattern:
            # Content-Type: text/html; charset=utf-8
            # Content-Type: multipart/form-data; boundary=something
            ct_charset = res.headers["Content-Type"]
            ct_charset = ct_charset.split(";")
            content_type = ct_charset[0]
            if len(ct_charset) == 2:
                charset = ct_charset[1].split("=")[1]
            else:
                charset = "utf-8"
            soup = BeautifulSoup(html, "lxml")

            # Get only english
            if (soup.html.get("lang") == None or soup.html["lang"] == "en") and content_type == "text/html":
                return (html, charset, True)
            else: return ('', None, False)

    except requests.exceptions.RequestException as e:
        print(e)
        if timeout > 0:
            return fetch(session, url, timeout - 1)
    except:
        print(url)


def crawl(LIMIT, seeds):
    heap = Heap()
    session = requests.Session()
    n_crawled = 0
    robot = {}
    queue = {}
    visited = set()

    for seed in seeds:
        if not polite(robot, seed):
            continue

        html, charset, ok = fetch(session, seed)
        if not ok:
            continue

        text = extract_text(html)
        links = extract_links(html)
        
        for link in links:
            if link not in visited:
                try:
                    queue[link].increase_inlinks()
                except KeyError:
                    new_link = Link(link)
                    queue[link] = new_link
                    heap.push(new_link)
        
        store(str(n_crawled)+'.txt', charset, link, text, html, links)
        visited.add(seed)
        n_crawled += 1




