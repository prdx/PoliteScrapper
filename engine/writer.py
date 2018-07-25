from tools.config import Config
from lxml import etree

config = Config("./settings.yml")
download_dir = config.get("download_dir")


def store(doc_id, depth, url, header, text, html, outlinks):
    with open(download_dir + doc_id + ".xml", 'wb') as xml:
        _doc_id_value.text = url
        _depth_value.text = depth
        _text_value.text = text
        _header_value.text = str(header)
        _source_value.text = html
        _outlinks_value.text = ','.join(outlinks)
        xml.write(etree.tostring(_root, pretty_print=True))

_root = etree.Element("items")
_item = etree.SubElement(_root, "item")
_doc_id = etree.SubElement(_item, "id")
_doc_id_value = etree.SubElement(_doc_id, "value")
_depth = etree.SubElement(_item, "depth")
_depth_value = etree.SubElement(_depth, "value")
_text = etree.SubElement(_item, "text")
_text_value = etree.SubElement(_text, "value")
_source = etree.SubElement(_item, "source")
_source_value = etree.SubElement(_source, "value")
_header = etree.SubElement(_item, "header")
_header_value = etree.SubElement(_header, "value")
_outlinks = etree.SubElement(_item, "outlinks")
_outlinks_value = etree.SubElement(_outlinks, "value")
