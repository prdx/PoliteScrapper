import requests
import time
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
        # Make a head request
        r = session.head(url)
        # Make sure it accepts text/html
        headers={"accept": "text/html"}
        res = session.get(url, headers=headers)
        # TODO: Use constants
        if res.status_code == 200:
            html = res.text
            header = res.headers

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
                return (header, html, charset, True)
            else: return ('', '', None, False)

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
    outlink = {}
    visited = []
    start_time = 0.0
    end_time = 0.0
    last_netlock = ""
    current_netlock = ""

    for seed in seeds:
        if not polite(robot, seed): continue

        # One request / second for the same domain
        delta_time = 1.0 - (end_time - start_time)
        if len(visited) > 0:
            last_netlock = urlparse(visited[-1])
            last_netlock = '{uri.scheme}://{uri.netloc}/'.format(uri=last_netlock)
            current_netlock = urlparse(seed)
            current_netlock = '{uri.scheme}://{uri.netloc}/'.format(uri=current_netlock)
        if delta_time > 0 and last_netlock == current_netlock:
            print("Sleep for: {0}".format(delta_time))
            time.sleep(delta_time)

        start_time = time.time()

        header, html, _, ok = fetch(session, seed)
        if not ok: continue

        end_time = time.time()

        text = extract_text(html)
        links = extract_links(html, seed)

        # Remove outlink that contains action such as delete or edit
        links = [ link for link in links if "edit" not in link and "delete" not in link ]

        for link in links:
            if link not in visited:
                try:
                    queue[link].add_inlinks(link)
                except KeyError:
                    new_link = Link(link, 1)
                    queue[link] = new_link
                    heap.push(new_link)
                # Store the outlink in a dictionary
                outlink[seed] = links
        
        store(str(n_crawled), 0, link, header, text, html, links)
        visited.append(seed)
        n_crawled += 1

        while n_crawled < LIMIT:
            """
            """
            next_url = heap.pop()
            next_link =  next_url.url
            depth = next_url.depth
            queue.pop(next_link)

            if not polite(robot, next_link): continue

            # One request / second for the same domain
            delta_time = 1.0 - (end_time - start_time)
            if len(visited) > 0:
                last_netlock = urlparse(visited[-1])
                last_netlock = '{uri.scheme}://{uri.netloc}/'.format(uri=last_netlock)
                current_netlock = urlparse(next_link)
                current_netlock = '{uri.scheme}://{uri.netloc}/'.format(uri=current_netlock)
            if delta_time > 0 and last_netlock == current_netlock:
                print("Sleep for: {0}".format(delta_time))
                time.sleep(delta_time)

            start_time = time.time()

            header, html, _, ok = fetch(session, next_link)
            if not ok: continue

            end_time = time.time()

            text = extract_text(html)
            links = extract_links(html, next_link)

            # Remove outlink that contains action such as delete or edit
            links = [ link for link in links if "edit" not in link and "delete" not in link ]

            for link in links:
                if link not in visited:
                    try:
                        queue[link].add_inlinks(link)
                    except KeyError:
                        new_link = Link(link, depth + 1)
                        queue[link] = new_link
                        heap.push(new_link)
                    # Store the outlink in a dictionary
                    outlink[next_link] = links
            
            store(str(n_crawled), depth, link, header, text, html, links)
            visited.append(next_link)
            n_crawled += 1
            heap.heapify()
