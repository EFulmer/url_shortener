import requests


TLD_URL = 'http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1'
TLD_FILE = 'tlds.txt'


def get_tlds(tld_site):
    text = requests.get(tld_site).text
    # I don't like the text.split('\n') bit.
    tlds = [ line for line in text.split('\n') 
             if not line.startswith('\n') or line.startswith('/') ]
    return set(tlds)


def write_tlds(tlds, tld_file):
    with open(tld_file, 'w') as f:
        f.write('\n'.join(tlds))


tlds = get_tlds(TLD_URL)
