from urllib.parse import urlparse

keywords = [
        "costa",
        "concordia",
        "costa concordia",
        "francesco schettino",
        "maritime",
        "accident",
        "wreck",
        " ship" # To avoid %ship
        ]

oot_wikipedia_path_list = [
        "/wiki/Portal",
        "/wiki/Help",
        "/wiki/Wikipedia",
        "/wiki/Special",
        "/wiki/Main_Page"
        ]

oot_telegraph_path_list = [
        "/sponsored/",
        "/sport/",
        "/lifestyle/",
        "/advertising/",
        "/topics/",
        "/subscriptions/",
        "/promotions/",
        "/syndication/",
        "/expat",
        "/film",
        "/technology",
        "/fashion",
        "/motoring",
        "/cars",
        "/luxury",
        "/travel",
        "/women",
        "/termsandconditions",
        "/telegraphtv",
        "/football",
        "/culture",
        "/environment",
        "/business",
        "/stage",
        "/tv-and-radio",
        "/education",
        "/journalists",
        "/profile",
        "/financialservices/"
        ]

oot_telegraph_subdomains = [
        "tickets.telegraph.co.uk",
        "puzzles.telegraph.co.uk",
        "announcements.telegraph.co.uk",
        "jobs.telegraph.co.uk",
        "blogs.telegraph.co.uk",
        "subscriber.telegraph.co.uk",
        "fantasycricket.telegraph.co.uk",
        "begambleaware.org",
        "gamcare.org.uk",
        "secure.gamblingcommission.gov.uk",
        "fantasyfootball.telegraph.co.uk",
        "coffeevsgangs.telegraph.co.uk",
        "bit.ly",
        "coffeevsgangs.com",
        "coffeemadehappy.com",
        "fantasycricket.telegraph.co.uk",
        "fantasyfootballscout.co.uk",
        "workforus.theguardian.com"
        ]


oot_wikipedia_extra_path_pattern_list = "/w/"

social_media = ["facebook", "twitter", "instagram", "google", "youtube"]

def is_oot_wikipedia(url):
    r = urlparse(url)
    for oot in oot_wikipedia_path_list:
        if r.path.startswith(oot):
            return True
    return False

def is_social_media(url):
    r = urlparse(url)
    for socmed in social_media:
        if socmed in r.netloc:
            return True
    return False

def is_oot_telegraph(url):
    r = urlparse(url)
    for oot in oot_telegraph_subdomains:
        if oot in r.netloc:
            return True
    for oot in oot_telegraph_path_list:
        if r.path.startswith(oot):
            return True
    return False

def is_edit_or_delete(url):
    if "edit" in url or "delete" in url: return True
    return False

def is_wikimedia(url):
    if "wikimedia" in url: return True
    return False

def is_also_oot_wikipedia(url):
    r = urlparse(url)
    if r.path.startswith(oot_wikipedia_extra_path_pattern_list): return True
    return False

