from pathlib import Path

# Локальная папка
BASE_DIR = Path(__file__).resolve().parent
# Папка на диске Windows
# BASE_DIR = Path("S:\\").resolve()
SEARCH_FOLDER = BASE_DIR / "Files"

if __name__ == "__main__":
    mask = "*УД*"
    for file in Path(SEARCH_FOLDER).glob(mask):
        print(file.name)
