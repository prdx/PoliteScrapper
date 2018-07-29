from bs4 import BeautifulSoup
import os
import pickle

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".xml")]

outlinks = {}
inlinks = {}

def generate_outlink_file():
    print("Generating outlinks file ...")
    # Generate outlinks
    for xml in files:
        try:
            with open(xml, "rb") as f:
                soup = BeautifulSoup(f, "lxml")
                url = soup.id.value.text
                outlinks[url] = soup.outlinks.value.text.split(",")
        except Exception as e:
            print("Error processing: " + xml)
            print(e)
            os.rename(xml, xml + ".fail")

    # Dump the outlinks
    with open("../output/outlinks.p", "wb") as out:
        pickle.dump(outlinks, out, protocol=pickle.HIGHEST_PROTOCOL)
    print("Done generating outlinks file ...")
    print("Outlinks size: " + str(len(outlinks)) + " urls")

def generate_inlink_file():
    print("Generating inlinks file ...")
    # Generate inlinks
    for key in outlinks:
        for url in outlinks[key]:
            try:
                inlinks[url].append(key)
            except KeyError:
                inlinks[url] = [key]
            except Exception as e:
                print("Error processing: " + key)
                print(e)

    # Dump the inlinks
    with open("../output/inlinks.p", "wb") as out:
        pickle.dump(inlinks, out, protocol=pickle.HIGHEST_PROTOCOL)
    print("Inlinks size: " + str(len(inlinks)) + " urls")
    print("Done inlinks file ...")

generate_outlink_file()
generate_inlink_file()
