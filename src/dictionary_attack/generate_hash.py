"""Hash-Generator CLI Script - Erzeugt Hashes für ein eingegebenes Wort.
"""

import sys

try:
    from .hashing import generate_all_hashes
except ImportError:
    from hashing import generate_all_hashes

def main():
    wort = input("Wort eingeben: ").strip()
    if not wort:
        print("Kein Wort eingegeben.")
        return

    hashes = generate_all_hashes(wort)
    print("\n--- Generierte Hashes ---")
    print(f"Wort:    {wort}")
    print(f"SHA-1:   {hashes['sha1']}")
    print(f"SHA-256: {hashes['sha256']}")
    print(f"MD5:     {hashes['md5']}")

if __name__ == "__main__":
    main()