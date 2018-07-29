from bs4 import BeautifulSoup
import os

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".xml")]
urls = []

for xml in files:
    try:
        with open(xml, "rb") as f:
            soup = BeautifulSoup(f, "lxml")
            url = soup.id.value.text
            if url not in urls:
                urls.append(url)
            else:
                os.rename(xml, xml + ".duplicate")
    except:
        os.rename(xml, xml + ".fail")

