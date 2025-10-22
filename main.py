from game import Game
from pathlib import Path
import sys, os

def resource_path(rel: str) -> str:

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent
    return str(base / rel)
if __name__ == "__main__":
    game = Game()
    game.run()
