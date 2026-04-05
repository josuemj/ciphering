import hashlib


def hash_md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def hash_sha1(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()


def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def hash_sha3_256(text: str) -> str:
    return hashlib.sha3_256(text.encode()).hexdigest()
