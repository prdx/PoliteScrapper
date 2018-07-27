from engine.crawler import crawl
from tools.config import Config
import os

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
    seeds = ["http://www.telegraph.co.uk/news/worldnews/europe/italy/10312026/Costa-Concordia-recovery-timeline-of-cruise-ship-disaster.html",
            "http://en.wikipedia.org/wiki/List_of_maritime_disasters",
            "http://en.wikipedia.org/wiki/Costa_Concordia_disaster",
            "http://en.wikipedia.org/wiki/Costa_Concordia"]
    # TODO: Change to crawl limit
    crawl(21000, seeds)


if __name__ == "__main__":
    main()
