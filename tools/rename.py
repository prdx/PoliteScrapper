import os
import uuid

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".xml")]

for xml in files:
    os.rename(xml, str(uuid.uuid4().hex) + ".xml")
