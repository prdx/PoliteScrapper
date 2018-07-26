import requests
import time
from bs4 import BeautifulSoup
from engine.data_structures import Heap, Link
from engine.extractor import extract_links, extract_text
from engine.robot import polite
from engine.topic_focus import is_edit_or_delete, is_oot_wikipedia, is_oot_telegraph, is_social_media, is_also_oot_wikipedia, is_wikimedia
from engine.writer import store
from urllib.parse import urlparse

def fetch(session, url, timeout = 1):
    """Fetch the head before downloding the page
    """
    if "telegraph.co.uk" in url:
        print(url)
    try:
        # Make a head request
        r = session.head(url)
        # Make sure it accepts text/html
        headers={"accept": "text/html"}
        res = session.get(url, headers=headers, timeout=1)
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

    except requests.exceptions.RequestException as e:
        if timeout > 0:
            return fetch(session, url, timeout - 1)
    except:
        print(url)
    return ('', '', None, False)

def should_skip(url):
        # If contains facebook, twitter, or instagram skip
        if is_social_media(url): return True

        # If contains /wiki/Wikipedia:*, skip
        if is_oot_wikipedia(url): 
            print(url)
            return True
        if is_wikimedia(url): return True
        if is_also_oot_wikipedia(url): return True

        # If the link contains action to delete or edit
        if is_edit_or_delete(url): return True

        # If oot on telegraph
        if is_oot_telegraph(url): return True

        
        return False


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
        # If not polite, skip
        if not polite(robot, seed): continue

        # One request / second for the same domain
        delta_time = 1.0 - (end_time - start_time)
        if len(visited) > 0:
            last_netlock = urlparse(visited[-1])
            last_netlock = '{uri.scheme}://{uri.netloc}/'.format(uri=last_netlock)
            current_netlock = urlparse(seed)
            current_netlock = '{uri.scheme}://{uri.netloc}/'.format(uri=current_netlock)

        # No need for delay if the previous one 
        if delta_time > 0 and last_netlock == current_netlock:
            # print("Sleep for: {0}".format(delta_time))
            time.sleep(delta_time)

        start_time = time.time()

        header, html, _, ok = fetch(session, seed)
        if not ok: continue

        end_time = time.time()

        text = extract_text(html)

        links_and_text = extract_links(html, seed)
        links_and_text = dict(links_and_text)

        for link in links_and_text:
            if link not in visited:
                try:
                    queue[link].add_inlinks(link)
                except KeyError:
                    new_link = Link(link, 1, "")
                    queue[link] = new_link
                    heap.push(new_link)
                # Store the outlink in a dictionary
                outlink[seed] = links_and_text.keys()
        
        store(str(n_crawled), 0, seed, header, text, html, links_and_text.keys())
        visited.append(seed)
        n_crawled += 1

    while n_crawled < LIMIT:
        """
        """
        next_url = heap.pop()
        next_link =  next_url.url
        depth = next_url.depth
        queue.pop(next_link)
        
        if should_skip(next_link): continue

        # Check if not polite 
        if not polite(robot, next_link): continue

        try:
            # One request / second for the same domain
            delta_time = 1.0 - (end_time - start_time)
            if len(visited) > 0:
                last_netlock = urlparse(visited[-1])
                last_netlock = '{uri.scheme}://{uri.netloc}/'.format(uri=last_netlock)
                current_netlock = urlparse(next_link)
                current_netlock = '{uri.scheme}://{uri.netloc}/'.format(uri=current_netlock)
            if 0 < delta_time < 1 and last_netlock == current_netlock:
                print("Sleep for: {0}".format(delta_time))
                time.sleep(delta_time)

            start_time = time.time()

            header, html, _, ok = fetch(session, next_link)
            if not ok: continue

            text = extract_text(html)
            links_and_text = extract_links(html, next_link)
            links_and_text = dict(links_and_text)

            for link in links_and_text:
                if link not in visited:
                    try:
                        queue[link].add_inlinks(link)
                    except KeyError:
                        new_link = Link(link, depth + 1, links_and_text[link])
                        queue[link] = new_link
                        heap.push(new_link)
                    # Store the outlink in a dictionary
                    outlink[next_link] = links_and_text.keys()
            
            store(str(n_crawled), depth, next_link, header, text, html, links_and_text.keys())
            visited.append(next_link)
            n_crawled += 1
            heap.heapify()

            end_time = time.time()

        except Exception:
            print("ERROR: Could not connect to page (generic)" + next_link)
            continue
