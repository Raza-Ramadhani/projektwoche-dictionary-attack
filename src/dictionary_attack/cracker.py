"""Dictionary Attack Engine - Schnelle und thread-sichere Passwort-Prüfung.
"""

from __future__ import annotations
import os
import time
import threading
from typing import Callable, Optional, TypedDict
from .hashing import hash_text, SUPPORTED_ALGORITHMS

DEFAULT_WORDLIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "passwords.txt")


class CrackResult(TypedDict):
    found: bool
    password: Optional[str]
    checked: int
    speed: float
    elapsed: float
    message: str


class DictionaryCracker:
    """Führt Wörterbuch-Angriffe gegen Hashes mit anpassbarer Wortliste und

    Fortschritts-Rückmeldungen durch.
    """

    def __init__(self, default_wordlist: str = DEFAULT_WORDLIST) -> None:
        self.default_wordlist = default_wordlist

    def crack(
        self,
        target_hash: str,
        algorithm: str = "sha1",
        wordlist_path: Optional[str] = None,
        progress_callback: Optional[Callable[[int, float, float], None]] = None,
        stop_event: Optional[threading.Event] = None,
        update_interval: int = 10_000
    ) -> CrackResult:
        path = wordlist_path or self.default_wordlist
        clean_target = target_hash.strip().lower()
        algorithm = algorithm.lower().strip()

        if not os.path.exists(path):
            return {
                "found": False,
                "password": None,
                "checked": 0,
                "speed": 0.0,
                "elapsed": 0.0,
                "message": f"Wortliste nicht gefunden: {path}"
            }

        checked = 0
        start_time = time.time()
        last_callback_time = start_time

        try:
            with open(path, "r", encoding="latin-1", errors="ignore") as file:
                for line in file:
                    if stop_event and stop_event.is_set():
                        elapsed = max(time.time() - start_time, 0.0001)
                        return {
                            "found": False,
                            "password": None,
                            "checked": checked,
                            "speed": checked / elapsed,
                            "elapsed": elapsed,
                            "message": "Prüfung durch Benutzer abgebrochen."
                        }

                    password = line.rstrip("\r\n")
                    checked += 1

                    # Prüfen
                    if hash_text(password, algorithm) == clean_target:
                        elapsed = max(time.time() - start_time, 0.0001)
                        speed = checked / elapsed
                        return {
                            "found": True,
                            "password": password,
                            "checked": checked,
                            "speed": speed,
                            "elapsed": elapsed,
                            "message": f"Passwort gefunden: {password}"
                        }

                    # GUI/CLI Feedback
                    if checked % update_interval == 0:
                        now = time.time()
                        elapsed = max(now - start_time, 0.0001)
                        speed = checked / elapsed
                        if progress_callback:
                            progress_callback(checked, speed, elapsed)

            # Ende erreicht ohne Treffer
            elapsed = max(time.time() - start_time, 0.0001)
            speed = checked / elapsed
            return {
                "found": False,
                "password": None,
                "checked": checked,
                "speed": speed,
                "elapsed": elapsed,
                "message": "Kein passendes Passwort in der Wortliste gefunden."
            }

        except Exception as e:
            elapsed = max(time.time() - start_time, 0.0001)
            return {
                "found": False,
                "password": None,
                "checked": checked,
                "speed": checked / elapsed if elapsed > 0 else 0.0,
                "elapsed": elapsed,
                "message": f"Fehler bei der Prüfung: {e}"
            }
