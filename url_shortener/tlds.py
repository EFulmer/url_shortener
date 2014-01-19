import requests
from tldextract.tldextract import extract


TLD_URL = 'http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1'
TLD_FILE = 'tlds.txt'


def get_tlds(tld_site=TLD_URL):
    """
    Read in Mozilla's TLD list, parse the TLDs out of it, and return
    all of the TLDs in it.

    A URL to an alternative TLD list can be provided. If it is, all 
    the lines in it should either contain TLDs (and nothing else) or 
    start with whitespace or a forward-slash ('/')
    """
    text = requests.get(tld_site).text
    tlds = { line for line in text.split('\n')[1:]
             if not line.startswith('/')  or line.startswith(' ') }
    tlds = tlds - {''}
    return frozenset(tlds)


tlds = get_tlds(TLD_URL)


def write_tlds_to_file(tlds=tlds, tld_file=TLD_FILE):
    """Write all of the TLDs to a file."""
    with open(tld_file, 'w') as f:
        f.write('\n'.join(tlds))


def has_valid_tld(url, tlds=tlds):
    url_tld = extract(url).suffix
    return url_tld in tlds
