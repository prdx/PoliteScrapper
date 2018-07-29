from engine.crawler_from_save import crawl
from tools.config import Config
import os
import pickle

config = Config("./settings.yml")
crawl_limit = config.get("crawl_limit")
download_dir = config.get("download_dir")


def clean():
    print("Removing all files in the download folder")
    download_files = os.listdir(download_dir)
    for file_name in download_files:
        os.remove(download_dir + file_name)

def main():
    clean()
    seeds = [
            "http://en.wikipedia.org/wiki/List_of_maritime_disasters",
            "http://www.telegraph.co.uk/news/worldnews/europe/italy/10312026/Costa-Concordia-recovery-timeline-of-cruise-ship-disaster.html",
            "http://en.wikipedia.org/wiki/Costa_Concordia_disaster",
            "http://en.wikipedia.org/wiki/Costa_Concordia"]
    # TODO: Change to crawl limit
    with open("./output-2/heap-7300.p", "rb") as h:
        heap = pickle.load(h)
    with open("./output-2/outlink-7300.p", "rb") as o:
        outlink = pickle.load(o)
    with open("./output-2/queue-7300.p", "rb") as q:
        queue = pickle.load(q)
    with open("./output-2/visited-7300.p", "rb") as v:
        visited = pickle.load(v)
    crawl(21000, seeds, heap, visited, outlink, queue)


if __name__ == "__main__":
    main()
