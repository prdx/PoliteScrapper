from urllib.parse import urlparse
import urllib.robotparser

def polite(robot, url):
    host = urlparse(url).netloc
    try:
        rc = robot[host]
    except KeyError:
        rc = urllib.robotparser.RobotFileParser()
        rc.set_url("http://" + host + "/robots.txt")
        rc.read()
        robot[host] = rc
    return rc.can_fetch("*", url)

