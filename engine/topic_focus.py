from urllib.parse import urlparse


oot_wikipedia_path_list = [
        "/wiki/Portal",
        "/wiki/Help",
        "/wiki/Wikipedia",
        "/wiki/Special",
        "/wiki/Main_Page"
        ]

oot_wikipedia_extra_path_pattern_list = "/w/"

social_media = ["facebook", "twitter", "instagram"]

def is_oot_wikipedia(url):
    r = urlparse(url)
    for l in oot_wikipedia_path_list:
        if r.path.startswith(l):
            return True
    return False

def is_social_media(url):
    r = urlparse(url)
    for socmed in social_media:
        if socmed in r.netloc:
            return True
    return False


def is_wikimedia(url):
    if "wikimedia" in url: return True
    return False

def is_also_oot_wikipedia(url):
    r = urlparse(url)
    if r.path.startswith(oot_wikipedia_extra_path_pattern_list): return True
    return False

