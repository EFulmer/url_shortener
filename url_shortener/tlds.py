import requests
from tldextract.tldextract import extract


TLD_URL = 'http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1'
TLD_FILE = 'tlds.txt'


def get_tlds(tld_site=TLD_URL):
    text = requests.get(tld_site).text
    tlds = [ line for line in text.split('\n') 
             if not line.startswith('/') or line == '' or line.startswith(' ') ]
    return set(tlds)


tlds = get_tlds(TLD_URL)


def write_tlds_to_file(tlds=tlds, tld_file=TLD_FILE):
    with open(tld_file, 'w') as f:
        f.write('\n'.join(tlds))


def has_valid_tld(url, tlds=tlds):
    # TODO: better way of making sure that has_valid_tld('') doesn't 
    # returh True
    url_tld = extract(url).suffix
    return url_tld in tlds and url_tld != ''
