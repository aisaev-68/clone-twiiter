from pathlib import Path

s = Path(__file__).parent / "images"
print(s)
print(s.absolute())