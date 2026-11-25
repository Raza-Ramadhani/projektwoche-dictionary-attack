"""Dictionary Attack & Cryptanalysis Package (R.A.Z.A. 2.0).
"""

from .caesar import encrypt, decrypt, crack_caesar, ALPHABET, WÖRTERLISTE
from .hashing import hash_text, generate_all_hashes, verify_hash, SUPPORTED_ALGORITHMS
from .cracker import DictionaryCracker, DEFAULT_WORDLIST
from .gui.app import RazaApp, run_app
from .cli import main

__all__ = [
    "encrypt",
    "decrypt",
    "crack_caesar",
    "ALPHABET",
    "WÖRTERLISTE",
    "hash_text",
    "generate_all_hashes",
    "verify_hash",
    "SUPPORTED_ALGORITHMS",
    "DictionaryCracker",
    "DEFAULT_WORDLIST",
    "RazaApp",
    "run_app",
    "main"
]
