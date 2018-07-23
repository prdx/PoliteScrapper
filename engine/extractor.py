from bs4 import BeautifulSoup
from url_canonicalizer import url_c14n

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.title
    try:
        text = title_tag.string + " "
    except AttributeError:
        text = ""

    text += " ".join([ x.text.strip() for x in soup.find_all("p")])
    return text

def extract_links(html):
    soup =  BeautifulSoup(html, "html.parser")
    return list(map(lambda x: url_c14n(x['href']), filter(lambda x: x.has_attr('href') and x.text != '', soup.find_all('a'))))

