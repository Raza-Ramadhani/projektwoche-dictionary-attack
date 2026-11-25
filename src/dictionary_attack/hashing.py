"""Hashing utilities for cryptanalysis and dictionary attacks.
Supports SHA-1, SHA-256, and MD5 algorithms.
"""

from __future__ import annotations
import hashlib

SUPPORTED_ALGORITHMS = ["sha1", "sha256", "md5"]


def hash_text(text: str, algorithm: str = "sha1") -> str:
    """Berechnet den Hash eines Textes mit dem angegebenen Algorithmus (sha1, sha256, md5)."""
    algo = algorithm.lower().strip()
    data = text.encode("utf-8", errors="replace")

    if algo == "sha1":
        return hashlib.sha1(data).hexdigest()
    elif algo == "sha256":
        return hashlib.sha256(data).hexdigest()
    elif algo == "md5":
        return hashlib.md5(data).hexdigest()
    else:
        raise ValueError(f"Nicht unterstützter Algorithmus: {algorithm}. Erlaubt: {SUPPORTED_ALGORITHMS}")


def generate_all_hashes(text: str) -> dict[str, str]:
    """Erzeugt Hashes für SHA-1, SHA-256 und MD5 gleichzeitig."""
    return {
        "sha1": hash_text(text, "sha1"),
        "sha256": hash_text(text, "sha256"),
        "md5": hash_text(text, "md5"),
    }


def verify_hash(candidate: str, target_hash: str, algorithm: str = "sha1") -> bool:
    """Prüft, ob der Hash des Kandidaten mit dem Zielhash übereinstimmt."""
    clean_target = target_hash.strip().lower()
    return hash_text(candidate, algorithm) == clean_target
