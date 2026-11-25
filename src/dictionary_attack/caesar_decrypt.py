"""Caesar Decrypt - Script zum Knacken der Caesar-Chiffre anhand von Worthäufigkeiten.
"""

import sys
try:
    from .caesar import crack_caesar, decrypt, encrypt, ALPHABET, WÖRTERLISTE
except ImportError:
    from caesar import crack_caesar, decrypt, encrypt, ALPHABET, WÖRTERLISTE

ciphertext = "JXLQLSLJV UHVHQW ZDWHU, PDFDTXHV GLVOLNH VRBEHDQV"

def main():
    print("=" * 60)
    print("CAESAR-KRYPTOANALYSE")
    print("=" * 60)
    print(f"Geheimtext: {ciphertext}\n")

    results = crack_caesar(ciphertext)
    best = results[0]

    print(f"Bester Treffer:")
    print(f"  Schlüssel:         {best['key']}")
    print(f"  Gefundene Wörter:  {best['score']} ({', '.join(best['matched_words'])})")
    print(f"  Entschlüsselt:     {best['text']}\n")

    print("Top 3 Schlüssel-Kandidaten:")
    for i, res in enumerate(results[:3], start=1):
        print(f"  #{i}: Key {res['key']:02d} | Score: {res['score']:02d} | Text: {res['text']}")

if __name__ == "__main__":
    main()