"""R.A.Z.A. 2.0 - Projekt-Einstiegspunkt.
Erlaubt das direkte Starten via `uv run main.py` oder `python main.py`.
"""

import sys
from pathlib import Path

# Sicherstellen, dass das src/-Verzeichnis im Suchpfad ist
src_dir = Path(__file__).resolve().parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from dictionary_attack.cli import main

if __name__ == "__main__":
    main()
