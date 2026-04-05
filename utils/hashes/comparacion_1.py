from explorar_hashes import hash_md5, hash_sha1, hash_sha256, hash_sha3_256
from hash_utils import bits_diferentes

ALGORITHMS = [
    ("MD5",       128, hash_md5),
    ("SHA-1",     160, hash_sha1),
    ("SHA-256",   256, hash_sha256),
    ("SHA-3/256", 256, hash_sha3_256),
]

INPUT_A = "MediSoft-v2.1.0"
INPUT_B = "medisoft-v2.1.0"


def build_rows() -> list[dict]:
    rows = []
    for name, bits, fn in ALGORITHMS:
        digest_a = fn(INPUT_A)
        digest_b = fn(INPUT_B)
        delta = bits_diferentes(digest_a, digest_b)
        for text, digest in [(INPUT_A, digest_a), (INPUT_B, digest_b)]:
            rows.append({
                "input":     text,
                "algoritmo": name,
                "bits":      bits,
                "hex_len":   len(digest),
                "hash":      digest,
                "bits_delta": delta,
            })
    return rows


def print_table(rows: list[dict]) -> None:
    col = {"input": 19, "algoritmo": 10, "bits": 6, "hex_len": 7, "hash": 64, "delta": 7}
    header = (
        f"{'Input':<{col['input']}} "
        f"{'Algoritmo':<{col['algoritmo']}} "
        f"{'Bits':>{col['bits']}} "
        f"{'HexLen':>{col['hex_len']}} "
        f"{'BitsD':>{col['delta']}} "
        f"{'Hash':<{col['hash']}}"
    )
    sep = "-" * len(header)
    print(sep)
    print(header)
    print(sep)
    for r in rows:
        print(
            f"{r['input']:<{col['input']}} "
            f"{r['algoritmo']:<{col['algoritmo']}} "
            f"{r['bits']:>{col['bits']}} "
            f"{r['hex_len']:>{col['hex_len']}} "
            f"{r['bits_delta']:>{col['delta']}} "
            f"{r['hash']:<{col['hash']}}"
        )
    print(sep)


if __name__ == "__main__":
    rows = build_rows()
    print(f"\nComparación de algoritmos hash — '{INPUT_A}' vs '{INPUT_B}'\n")
    print_table(rows)
