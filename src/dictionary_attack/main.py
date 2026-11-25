"""R.A.Z.A. 2.0 - Haupteinstiegspunkt für die grafische Oberfläche.
"""

from .gui.app import run_app, RazaApp
from .cli import main

if __name__ == "__main__":
    run_app()