from tools.config import Config
from lxml import etree

config = Config("./settings.yml")
download_dir = config.get("download_dir")


def store(doc_id, url, header, text, html, outlinks):
    with open(download_dir + doc_id + ".xml", 'wb') as xml:
        _doc_id_value.text = url
        _text_value.text = text
        _header_value.text = str(header)
        _source_value.text = html
        _outlinks_value.text = ','.join(outlinks)
        xml.write(etree.tostring(root, pretty_print=True))

_root = etree.Element("items")
_item = etree.SubElement(root, "item")
_doc_id = etree.SubElement(item, "id")
_doc_id_value = etree.SubElement(doc_id, "value")
_text = etree.SubElement(item, "text")
_text_value = etree.SubElement(text, "value")
_source = etree.SubElement(item, "source")
_source_value = etree.SubElement(source, "value")
_header = etree.SubElement(item, "header")
_header_value = etree.SubElement(header, "value")
_outlinks = etree.SubElement(item, "outlinks")
_outlinks_value = etree.SubElement(outlinks, "value")
