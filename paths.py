import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent

KEYS_FILE = PROJECT_ROOT / "keys.json"
STRINGS_FILE = PROJECT_ROOT / "strings.json"

MODULES_DIR = PROJECT_ROOT / "modules"

for path in (
    DATA_DIR := PROJECT_ROOT / ".data",
    LOGS_DIR := PROJECT_ROOT / ".logs"
):
    os.makedirs(path, exist_ok=True)