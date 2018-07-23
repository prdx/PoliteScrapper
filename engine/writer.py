FIELD_END = '#'.encode()

def store(results_filename, charset, url, text, html, outlinks):
    fp = open(results_filename, 'wb+')
    fp.write(url.encode() + '\n'.encode() + FIELD_END + '\n'.encode())
    fp.write(text.encode(encoding=charset, errors='ignore') + '\n'.encode() + FIELD_END + '\n'.encode())
    fp.write(html.strip().encode(charset, 'ignore') + '\n'.encode() + FIELD_END + '\n'.encode())
    fp.write(','.join(outlinks).encode(encoding=charset, errors='ignore'))

    fp.close()
