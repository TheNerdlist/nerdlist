import requests
import hashlib
import operator
from time import sleep

NERDLIST_FILENAME = 'nerdlist.txt'
NERDLIST_HIBP_FILENAME = 'nerdlist-sorted-hibp.txt'

if __name__ == "__main__":
    passwords = []
    # open the nerdlist.txt file and collect all the passwords
    with open(NERDLIST_FILENAME, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for pword in lines[5:]:
            passwords.append(str(pword.strip()))

    indexed = {}
    for password in passwords:
        print("[*] looking up %s" % password)
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        (prefix, suffix) = (sha1[:5], sha1[5:])
        resp = requests.get('https://api.pwnedpasswords.com/range/%s' % prefix)
        hibp_line = resp.text.split("\r\n")
        count = 0
        for hibp_suffix in hibp_line:
            (hibp_suffix, hibp_count) = hibp_suffix.split(':')
            if suffix == hibp_suffix:
                count = int(hibp_count)
                break
        indexed[password] = count

        # HIBP API requires 1500 millisecond wait
        sleep(1.5)

    # sort the dictionary by keys, and then construct an array using only the first element in the tuple
    sorted_passwords = [k[0] for k in sorted(indexed.items(), key=operator.itemgetter(1))]
    with open(NERDLIST_HIBP_FILENAME, 'w', encoding='utf-8') as f:
        for password in sorted_passwords:
            f.write(password + '\n')