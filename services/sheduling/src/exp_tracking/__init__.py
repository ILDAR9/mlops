import json
import os
from typing import Dict

import yaml


#######
# UTILS
#######

def load_data(fpath: str) -> Dict:
    ext = os.path.basename(fpath).rsplit('.', 1)[-1]
    if ext == 'yaml' or ext == 'yml':
        with open(fpath, "r", encoding='utf8') as f:
            return yaml.safe_load(f.read())
    elif ext == 'json':
        with open(fpath, 'r') as f:
            return json.load(f)


def convert_delta_ms_hours(millis: int) -> str:
    # HH:MM:ss
    seconds = (millis // 1000) % 60
    minutes = (millis // (1000 * 60)) % 60
    hours = millis // (1000 * 60 * 60)

    s = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return s


def convert_delta_ms(millis: int) -> str:
    # MM:ss:mmm
    seconds = (millis // 1000) % 60
    minutes = millis // (1000 * 60)
    millis = millis % 1000

    s = f"{minutes:02d}:{seconds:02d}:{millis:03d}"
    return s
