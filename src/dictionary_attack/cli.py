"""Command-Line Interface for R.A.Z.A. 2.0 / Dictionary Attack Suite.
Supports launching the GUI by default, or running interactive and batch CLI operations.
"""

from __future__ import annotations
import sys
import argparse
import time

from .caesar import encrypt, decrypt, crack_caesar
from .hashing import generate_all_hashes, hash_text, SUPPORTED_ALGORITHMS
from .cracker import DictionaryCracker, DEFAULT_WORDLIST


def run_interactive_cli() -> None:
    cracker = DictionaryCracker()
    print("=" * 60)
    print("  R.A.Z.A. 2.0 - TERMINAL KRYPTOANALYSE")
    print("=" * 60)

    while True:
        print("\nBitte Modus wählen:")
        print("  [1] Wörterbuch-Angriff (Hash knacken)")
        print("  [2] Hash-Generator (Klartext -> SHA-1/256/MD5)")
        print("  [3] Caesar Chiffre: Ver- oder Entschlüsseln")
        print("  [4] Caesar Kryptoanalyse: Automatisch knacken")
        print("  [5] GUI starten")
        print("  [0] Beenden")

        choice = input("\nAuswahl (0-5): ").strip()

        if choice == "1":
            target = input("Ziel-Hash eingeben: ").strip()
            if not target:
                continue
            algo = input("Algorithmus [sha1/sha256/md5] (Standard: sha1): ").strip().lower() or "sha1"
            wordlist = input(f"Pfad zur Wortliste (Enter für {DEFAULT_WORDLIST}): ").strip() or DEFAULT_WORDLIST

            print(f"\n[+] Starte Wörterbuch-Angriff auf {target} ({algo.upper()})...")

            def cli_progress(checked: int, speed: float, elapsed: float) -> None:
                sys.stdout.write(f"\r[*] Geprüft: {checked:,} | Tempo: {speed:,.0f} Pw/s | Dauer: {elapsed:.1f}s")
                sys.stdout.flush()

            res = cracker.crack(
                target_hash=target,
                algorithm=algo,
                wordlist_path=wordlist,
                progress_callback=cli_progress,
                update_interval=50_000
            )
            print("\n")
            if res["found"]:
                print(f"[SUCCESS] Passwort gefunden: {res['password']}")
            else:
                print(f"[-] {res['message']}")
            print(f"[*] Insgesamt {res['checked']:,} Passwörter in {res['elapsed']:.2f}s geprüft.")

        elif choice == "2":
            text = input("Wort / Text eingeben: ").strip()
            if text:
                hashes = generate_all_hashes(text)
                print(f"\nKlartext: {text}")
                print(f"SHA-1:    {hashes['sha1']}")
                print(f"SHA-256:  {hashes['sha256']}")
                print(f"MD5:      {hashes['md5']}")

        elif choice == "3":
            sub = input("Verschlüsseln (v) oder Entschlüsseln (e)? [v/e]: ").strip().lower()
            key_str = input("Schlüssel (0-25): ").strip()
            try:
                key = int(key_str) % 26
            except ValueError:
                print("Ungültiger Schlüssel!")
                continue
            text = input("Text eingeben: ").strip()
            if sub == "v":
                print(f"Ergebnis: {encrypt(text, key)}")
            else:
                print(f"Ergebnis: {decrypt(text, key)}")

        elif choice == "4":
            cipher = input("Geheimtext eingeben: ").strip()
            if not cipher:
                continue
            results = crack_caesar(cipher)
            best = results[0]
            print("\n[+] Bester Treffer:")
            print(f"    Schlüssel:         {best['key']}")
            print(f"    Trefferpunkte:     {best['score']} Wörter")
            print(f"    Gefundene Wörter:  {', '.join(best['matched_words'])}")
            print(f"    Entschlüsselt:     {best['text']}")

        elif choice == "5":
            from .gui.app import run_app
            run_app()
            break

        elif choice in ("0", "q", "exit"):
            print("Beende R.A.Z.A.")
            break


def main() -> None:
    parser = argparse.ArgumentParser(
        description="R.A.Z.A. 2.0 - Kryptoanalyse & Wörterbuch-Angriff Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--cli", "-c",
        action="store_true",
        help="Interaktives Terminal-Menü starten anstelle der GUI"
    )
    parser.add_argument(
        "--gui", "-g",
        action="store_true",
        help="Grafische Oberfläche (GUI) starten (Standard)"
    )
    parser.add_argument(
        "--hash",
        type=str,
        metavar="TEXT",
        help="Erzeugt SHA-1, SHA-256 und MD5 für den angegebenen Text"
    )
    parser.add_argument(
        "--caesar-crack",
        type=str,
        metavar="CIPHERTEXT",
        help="Knackt einen Caesar-Geheimtext automatisch mit Wörterbuch-Matching"
    )
    parser.add_argument(
        "--caesar-encrypt",
        type=str,
        metavar="TEXT",
        help="Verschlüsselt einen Text mit Caesar-Chiffre (benötigt --key)"
    )
    parser.add_argument(
        "--caesar-decrypt",
        type=str,
        metavar="TEXT",
        help="Entschlüsselt einen Text mit Caesar-Chiffre (benötigt --key)"
    )
    parser.add_argument(
        "--key", "-k",
        type=int,
        default=3,
        help="Schlüssel (0-25) für manuelle Caesar-Operationen (Standard: 3)"
    )
    parser.add_argument(
        "--crack",
        type=str,
        metavar="TARGET_HASH",
        help="Führt einen Wörterbuch-Angriff auf den angegebenen Hash durch"
    )
    parser.add_argument(
        "--algo", "-a",
        type=str,
        default="sha1",
        choices=SUPPORTED_ALGORITHMS,
        help="Hash-Algorithmus für Wörterbuch-Angriff (sha1, sha256, md5)"
    )
    parser.add_argument(
        "--wordlist", "-w",
        type=str,
        default=DEFAULT_WORDLIST,
        help="Pfad zur Passwort-Wortliste"
    )

    args = parser.parse_args()

    # CLI Flags auswerten
    if args.hash:
        hashes = generate_all_hashes(args.hash)
        print(f"Klartext: {args.hash}")
        print(f"SHA-1:    {hashes['sha1']}")
        print(f"SHA-256:  {hashes['sha256']}")
        print(f"MD5:      {hashes['md5']}")
        return

    if args.caesar_crack:
        res = crack_caesar(args.caesar_crack)
        best = res[0]
        print(f"Bester Treffer (Key {best['key']}, Score {best['score']}): {best['text']}")
        if best['matched_words']:
            print(f"Gefundene Wörter: {', '.join(best['matched_words'])}")
        return

    if args.caesar_encrypt:
        print(encrypt(args.caesar_encrypt, args.key))
        return

    if args.caesar_decrypt:
        print(decrypt(args.caesar_decrypt, args.key))
        return

    if args.crack:
        cracker = DictionaryCracker()
        print(f"[*] Starte Wörterbuch-Angriff auf {args.crack} ({args.algo.upper()})...")
        res = cracker.crack(
            target_hash=args.crack,
            algorithm=args.algo,
            wordlist_path=args.wordlist
        )
        if res["found"]:
            print(f"[SUCCESS] Passwort gefunden: {res['password']}")
        else:
            print(f"[-] {res['message']}")
        return

    if args.cli:
        run_interactive_cli()
        return

    # Standard: GUI starten
    from .gui.app import run_app
    run_app()


if __name__ == "__main__":
    main()
