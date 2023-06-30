import hashlib


def sha1(m):
    hash_object = hashlib.sha1()
    hash_object.update(m.encode("utf-8"))
    digest_bytes = hash_object.digest()
    hash_string = digest_bytes.hex()
    return hash_string
