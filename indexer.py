from bs4 import BeautifulSoup
import os
from tools.config import Config
from tools.es import *
import pickle

"""Indexer as a slave
"""

config = Config("./settings.yml")
index_name = config.get("index_name")
download_dir = config.get("download_dir")

# delete_index()
# create_index()

with open("./output/inlinks.p", "rb") as out:
    inlinks = pickle.load(out)

if es.ping():
    
    # Go through all of the corpus and store it
    id_count = 20001
    
    for f in os.listdir(download_dir):
        if f.endswith(".xml"):
            print("Processing {0}".format(f))
            try:
                with open(download_dir + f, 'rb') as d:
                    soup = BeautifulSoup(d, "lxml")
                    url = soup.id.value.text
                    header= soup.header.value.text
                    depth = soup.depth.value.text
                    out_links = soup.outlinks.value.text.split(',')
                    try:
                        in_links = inlinks[url]
                    except KeyError:
                        print("URL not found in inlinks: {0}".format(url))
                        in_links = []

                    # Who's the stupid giving the same XML tag as BS attribute :P
                    text = soup.find_all('text')[0].value.text
                    html = soup.source.value.text

                    # And who's the stupid forget to store the title
                    soup_for_title = BeautifulSoup(html, "lxml")
                    title = soup_for_title.title.text
                    print(url)

                    res = search(url)
                    try:
                        hits = res["hits"]["hits"]
                        index = 0
                        # for hit in hits:
                            # if hit["_source"]["url"] == url:
                                # break
                            # index += 1

                        # Get everything
                        _outlinks_remote = res["hits"]["hits"][index]["_source"]["out_links"]
                        _inlinks_remote = res["hits"]["hits"][index]["_source"]["in_links"]
                        _doc_id = res["hits"]["hits"][index]["_id"]
                        _url = res["hits"]["hits"][index]["_source"]["url"]
                        _depth = res["hits"]["hits"][index]["_source"]["depth"]
                        _author = res["hits"]["hits"][index]["_source"]["author"]
                        _text = res["hits"]["hits"][index]["_source"]["text"]
                        _title = res["hits"]["hits"][index]["_source"]["title"]
                        _html = res["hits"]["hits"][index]["_source"]["html_Source"]
                        _header = res["hits"]["hits"][index]["_source"]["HTTPheader"]

                        # Merge the in - out links
                        out_links += _outlinks_remote
                        in_links += _inlinks_remote
                        # Convert to set
                        out_links = set(out_links)
                        in_links = set(in_links)

                        # Convert back to array
                        out_links = list(out_links)
                        in_links = list(in_links)

                        print("URL exists: " + _url)

                        store_document(_doc_id, _url, _header, _title, _text, _html, out_links, in_links, _depth)

                    except KeyError:
                        store_document(id_count, url, header, title, text, html, out_links, in_links, depth)
                    except Exception:
                        store_document(id_count, url, header, title, text, html, out_links, in_links, depth)
                id_count += 1
            except Exception as e:
                print("Fail for: {0}".format(f))
                os.rename(download_dir + f, download_dir + f + ".fail")
