#!/usr/bin/python3
import base64
import hashlib

NERDLIST_FILENAME = 'nerdlist.txt'
NERLIST_HASHED_FILENAME = 'nerdlist-hashed.tsv'


def multihash_passwords(passwords=[]):
    multihashed = []

    for password in passwords:
        bpassword = password.encode()
        multihashed.append([
            password,
            hashlib.md5(bpassword).hexdigest(),
            hashlib.sha1(bpassword).hexdigest(),
            hashlib.sha256(bpassword).hexdigest(),
            hashlib.sha512(bpassword).hexdigest(),
            str(base64.b64encode(bpassword).decode("utf-8", "ignore"))
        ])

    return multihashed


def selftest():
    multi = multihash_passwords(['password'])

    if len(multi) != 1 and len(multi[0]) != 6:
        print("[x] array length mismatch")
        exit(1)

    if '5f4dcc3b5aa765d61d8327deb882cf99' not in multi[0]:
        print("[x] md5 mismatch")
        exit(1)

    if '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8' not in multi[0]:
        print("[x] sha1 mismatch")
        exit(1)

    if '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8' not in multi[0]:
        print("[x] sha256 mismatch")
        exit(1)

    if 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86' not in multi[0]:
        print("[x] sha512 mismatch")
        exit(1)

    if 'cGFzc3dvcmQ=' not in multi[0]:
        print("[x] base64 mismatch")
        exit(1)


if __name__ == "__main__":
    selftest()

    passwords = []
    # open the nerdlist.txt file and collect all the passwords
    with open(NERDLIST_FILENAME, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for pword in lines[5:]:
            passwords.append(str(pword.strip()))

    # for each password, do md5/sha256/sha512/base64 encodings
    hash_lines = [
        "\t".join(["password", "md5", "sha1", "sha256", "sha512", "base64"])
    ]
    for multi in multihash_passwords(passwords):
        formatted_line = "\t".join(multi) + "\n"
        hash_lines.append(formatted_line)

    # write out the utf8 tsv
    with open(NERLIST_HASHED_FILENAME, "w", encoding="utf-8") as hf:
        hf.writelines(hash_lines)
