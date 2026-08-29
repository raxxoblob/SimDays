"""Concatenate all .rpy files from SimDays/game/ into all_code.rpy at project root."""
import os

GAME_DIR = os.path.join(os.path.dirname(__file__), "..", "SimDays", "SimDays", "game")
OUT_FILE = os.path.join(os.path.dirname(__file__), "..", "all_code.rpy")

files = sorted(f for f in os.listdir(GAME_DIR) if f.endswith(".rpy"))

with open(OUT_FILE, "w", encoding="utf-8") as out:
    for fname in files:
        path = os.path.join(GAME_DIR, fname)
        out.write("# " + "=" * 76 + "\n")
        out.write("# FILE: " + fname + "\n")
        out.write("# " + "=" * 76 + "\n\n")
        with open(path, encoding="utf-8") as f:
            out.write(f.read())
        out.write("\n\n")

print("Written %d files -> all_code.rpy" % len(files))
