import json
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.json"
SETTINGS : dict = {}


def load_config():
    global SETTINGS
    try:
        with open(CONFIG_PATH, "r") as file:
            SETTINGS = json.load(file)
    except FileNotFoundError:
        sys.stderr.write("Config not found")
