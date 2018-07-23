import requests
from bs4 import BeautifulSoup
from data_structures import Heap, Link
from robot import polite

def fetch(session, url, timeout = 1):
    """Fetch the head before downloding the page
    """
    try:
        session.head(url)
        # Make sure it accepts text/html
        headers={"accept": "text/html"}
        res = session.get(url, headers=headers)
        if res.status_code == 200:
            html = res.text

            # Pattern:
            # Content-Type: text/html; charset=utf-8
            # Content-Type: multipart/form-data; boundary=something
            ct_charset = res.headers["Content-Type"]
            ct_charset = ct_charset.split(";")
            content_type = ct_charset[0]
            if len(ct_charset) == 2:
                charset = ct_charset[1]
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

def crawl(LIMIT):
    heap = Heap()
    session = requests.Session()
    n_crawled = 0
    robot = {}
