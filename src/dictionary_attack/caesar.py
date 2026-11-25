"""Caesar Chiffre - Ver- und Entschlüsselung sowie automatische Kryptoanalyse.

Dieses Modul bietet Funktionen zur Caesar-Verschlüsselung, -Entschlüsselung
und zum automatischen Knacken verschlüsselter Texte anhand von Worthäufigkeiten.
"""

from __future__ import annotations
import re
from typing import TypedDict

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WÖRTERLISTE: list[str] = [
    # Häufige deutsche Artikel, Pronomen & Konjunktionen
    "die", "der", "und", "in", "zu", "den", "das", "von", "mit", "ist",
    "im", "dem", "nicht", "ein", "eine", "als", "auch", "es", "an", "aus",
    "er", "dass", "sie", "nach", "bei", "einer", "um", "am", "wie", "einem",
    "einen", "so", "zum", "nur", "oder", "aber", "vor", "zur", "bis", "mehr",
    "durch", "man", "sein", "gegen", "vom", "wenn", "seine", "ihre", "dann", "unter",
    "wir", "ich", "eines", "diese", "dieser", "keine", "seiner", "zwischen", "immer", "was",
    "alle", "diesem", "doch", "ganz", "selbst", "weil", "damit", "ihm", "ihr", "andere",
    "hier", "dort", "viel", "jetzt", "sehr", "gar", "darauf", "weiter", "ohne", "beide",
    "uns", "welche", "solche", "etwas", "nichts", "alles", "dieses", "ihnen", "mich", "dich",

    # Häufige deutsche Hilfs- & Vollverben
    "werden", "hat", "wird", "sind", "war", "haben", "wurde", "sei", "hatte", "kann",
    "können", "schon", "habe", "soll", "worden", "will", "sagte", "gibt", "kommen", "wollen",
    "sehen", "lassen", "müssen", "wissen", "leben", "machen", "gehen", "stehen", "finden", "bleiben",
    "liegen", "bringen", "halten", "nehmen", "geben", "denken", "sagen", "zeigen", "dürfen", "glauben",

    # Häufige deutsche Adjektive, Adverbien & Nomen
    "jahr", "zwei", "jahren", "uhr", "millionen", "ersten", "mensch", "menschen", "wohl", "zeit",
    "neue", "neu", "gut", "lang", "weit", "recht", "arbeit", "hand", "während", "erst",
    "groß", "klein", "fall", "stadt", "land", "seite", "ende", "haus", "kind", "herr",
    "frau", "teil", "problem", "frage", "welt", "bereich", "titel", "tag", "tage",
    "ab", "bereits", "oft", "heute", "gestern", "morgen", "schnell", "hoch", "spät", "eigenen",

    # Häufige englische Artikel, Pronomen & Konjunktionen
    "the", "and", "a", "that", "i", "it", "not", "he", "as", "you",
    "this", "but", "his", "they", "we", "her", "she", "or", "an", "my",
    "one", "all", "their", "what", "so", "who", "which", "me", "him", "your",
    "them", "some", "other", "than", "then", "its", "our", "these", "any", "us",
    "those", "no", "because", "both", "each", "whoever", "myself", "everything",

    # Häufige englische Präpositionen & Adverbien
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "up",
    "out", "if", "about", "into", "over", "after", "through", "before", "under", "around",
    "now", "just", "also", "back", "well", "even", "here", "there", "how", "why",
    "when", "where", "again", "never", "always", "often", "very", "still", "already",

    # Häufige englische Verben & Hilfsverben
    "be", "have", "do", "say", "will", "would", "can", "could", "get", "go",
    "make", "know", "take", "see", "come", "think", "look", "want", "give", "use",
    "find", "tell", "ask", "work", "seem", "feel", "try", "leave", "call", "should",
    "need", "become", "mean", "keep", "let", "begin", "show", "hear", "run", "move", "resent",

    # Häufige englische Substantive & Adjektive
    "time", "year", "people", "way", "day", "man", "thing", "woman", "life", "child",
    "world", "school", "state", "family", "student", "group", "country", "problem", "hand", "part",
    "place", "case", "week", "company", "system", "program", "question", "work", "government", "number",
    "good", "new", "first", "last", "long", "great", "little", "own", "other", "old",
    "right", "big", "high", "different", "small", "large", "next", "early", "young", "important",
    "water", "money", "story", "fact", "month", "lot", "study", "book", "eye", "job",
    "guineapigs", "macaques", "soybeans"
]


class CaesarResult(TypedDict):
    key: int
    score: int
    text: str
    matched_words: list[str]


def encrypt(plaintext: str, key: int) -> str:
    """Verschlüsselt einen Text mit der Caesar-Chiffre um den angegebenen Schlüssel."""
    plaintext = plaintext.upper()
    encrypted = ""
    for c in plaintext:
        code = ALPHABET.find(c)
        if code == -1:
            encrypted += c
        else:
            code = (code + key) % len(ALPHABET)
            encrypted += ALPHABET[code]
    return encrypted


def decrypt(ciphertext: str, key: int) -> str:
    """Entschlüsselt einen Text mit der Caesar-Chiffre um den angegebenen Schlüssel."""
    ciphertext = ciphertext.upper()
    decrypted = ""
    for c in ciphertext:
        code = ALPHABET.find(c)
        if code == -1:
            decrypted += c
        else:
            code = (code - key) % len(ALPHABET)
            decrypted += ALPHABET[code]
    return decrypted


def crack_caesar(
    ciphertext: str,
    wordlist: list[str] | None = None
) -> list[CaesarResult]:
    """Knackt eine Caesar-Chiffre durch systematisches Testen aller 26 Schlüssel

    und Bewerten der Treffer mit einer deutschen/englischen Wörterliste.
    Gibt die Resultate nach Trefferpunkten absteigend sortiert zurück.
    """
    words = wordlist if wordlist is not None else WÖRTERLISTE
    results: list[CaesarResult] = []

    for key in range(len(ALPHABET)):
        decrypted = decrypt(ciphertext, key)
        matched_words: list[str] = []
        score = 0

        for word in words:
            # Suche nach ganzem Wort (Regex mit Wortgrenzen oder Teilstring)
            matches = re.findall(rf"\b{re.escape(word)}\b", decrypted, re.IGNORECASE)
            if matches:
                score += len(matches)
                matched_words.append(word)

        # Falls keine ganzen Wörter gefunden wurden, auch Teilworttreffer für Wörter >= 4 Zeichen
        if score == 0:
            for word in words:
                if len(word) >= 4:
                    matches = re.findall(re.escape(word), decrypted, re.IGNORECASE)
                    if matches:
                        score += len(matches)
                        matched_words.append(word)

        results.append({
            "key": key,
            "score": score,
            "text": decrypted,
            "matched_words": matched_words
        })

    # Absteigend nach Punktzahl sortieren
    results.sort(key=lambda r: r["score"], reverse=True)
    return results


if __name__ == "__main__":
    test_plaintext = "HALLO WELT!"
    test_key = 3
    test_cipher = encrypt(test_plaintext, test_key)
    print(f"Original: {test_plaintext}")
    print(f"Verschlüsselt (Key {test_key}): {test_cipher}")
    print(f"Entschlüsselt: {decrypt(test_cipher, test_key)}")

    # Test mit Klassenbeispiel
    challenge = "JXLQLSLJV UHVHQW ZDWHU, PDFDTXHV GLVOLNH VRBEHDQV"
    cracked = crack_caesar(challenge)
    best = cracked[0]
    print("\n--- Automatisches Knacken ---")
    print(f"Bester Treffer (Key {best['key']}, Score {best['score']}):")
    print(f"Klartext: {best['text']}")
    print(f"Gefundene Wörter: {', '.join(best['matched_words'])}")
