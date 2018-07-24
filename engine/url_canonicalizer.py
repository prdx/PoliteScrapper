import os
import re
import urllib
import w3lib.url



try:
    from urllib.parse import urlsplit, urlunsplit, urljoin
except ImportError:
    from urlparse import urlsplit, urlunsplit, urljoin

def url_c14n(s, base):
    # URL C14N
    #   see also:
    #    + <http://tools.ietf.org/html/rfc3986#section-6>
    #    + <http://en.wikipedia.org/wiki/URL_normalization>

    # (Bagus) Make sure base has scheme
    scheme, netloc, path, qs, anchor = urlsplit(base)

    if scheme == "":
        # If URL starts with // or / without http
        if base.startswith("//"):
            base = base[2:]
        elif base.startswith("/"):
            base = base[1:]
        base = "http://" + base

    # (Bagus) For cases like /wiki/WhatEver, we need to combine it first
    s = urljoin(base, s)


    scheme, netloc, path, qs, anchor = urlsplit(s)

    # (Bagus) Remove the anchor
    anchor = ""

    # (Bagus) If scheme not present
    if scheme == '':
        # If URL starts with // or / without http
        if s.startswith("//"):
            s = s[2:]
        elif s.startswith("/"):
            s = s[1:]
        s = "http://" + s
        scheme, netloc, path, qs, anchor = urlsplit(s)

    return w3lib.url.canonicalize_url(s)
