# AzzieL3MTools
# utils.py
# Hillman
# March 2026

from pathlib import Path
import json
from datetime import datetime
import tiktoken

import re
import unicodedata
from decimal import Decimal, InvalidOperation
import psutil
import platform


## file handling functions  follow (housekeeping)
keep_alive = "30m"

def loadjson(fname):
    with open(fname, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def savejson(fname,jdata):
    with open(fname, 'w', encoding="utf-8") as file:
        json.dump(jdata,file,indent=2, ensure_ascii=False)
    return

def loadtext (fname):
    with open(fname,"r", encoding='utf-8') as file:
        return file.read()

def savetext (fname:str,fdata:str, fmode="w"):
    with open(fname, fmode) as file:
        file.write(fdata)

def parse_json(text: str):
    try:
        obj = json.loads(text)
        if isinstance(obj, (dict, list)):
            return obj
        else:
            return None
    except json.JSONDecodeError:
        return None

def getprompts(pp=""):
    plist = loadjson('config/llmprompts.json')
    pnames = []
    for i in plist:
        if pp == i["preprompt"]["qryid"]:
            pnames = [i]
            return pnames
        pnames.append((i["preprompt"]["qryid"], i["preprompt"]["qryname"]))   #list, list
    return pnames

reslog = "log/resfile.jsonl"
def saveresults(res,model,pp):
    newres = [str(datetime.now()), model, pp, res]
    # savetext(reslog,str(newres) + "\n",fmode="a")
    with open(reslog, "a", encoding="utf-8") as f:
        json.dump(newres, f, ensure_ascii=False)
        f.write("\n")


def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:

    try:
        enc = tiktoken.get_encoding(encoding_name)
    except Exception:
        # fallback to the most common tokenizer
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def find_filenames_by_name(
    root_dir: str,
    substring: str,
    ext: str,
    recursive: bool = False):

    root = Path(root_dir)
    pattern = f"*{substring}*.{ext}"

    paths = root.rglob(pattern) if recursive else root.glob(pattern)
    return [p.name for p in paths]
    
def extract_json_from_markdown(text: str):
    try:
        text = text.strip()

        if text.startswith("```"):
            # Remove opening fence
            text = text.split("\n", 1)[1]
            # Remove closing fence
            text = text.rsplit("```", 1)[0]

        return json.loads(text)
    except:
        return text



def safe_filename_ascii(name: str, replacement="_") -> str:
    # Normalize Unicode → ASCII
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")

    # Keep only safe characters
    name = re.sub(r"[^A-Za-z0-9._-]", replacement, name)

    # Collapse duplicates
    name = re.sub(rf"{re.escape(replacement)}+", replacement, name)

    return name.strip("._-")



_SUFFIXES = {
    "":   Decimal("1"),
    "K":  Decimal("1e3"),
    "M":  Decimal("1e6"),
    "B":  Decimal("1e9"),
    "T":  Decimal("1e12"),
}

_NUM_RE = re.compile(
    r"""
    ^\s*
    (?P<num>[-+]?(?:\d+(?:\.\d+)?|\.\d+))
    \s*
    (?P<suf>[kKmMbBtT])?
    """,
    re.VERBOSE
)

def parse_compact_number(s, as_int=False):

    # --- NEW: handle blanks / alpha strings ---
    if s is None:
        return 0

    s = str(s).strip()

    if s == "" or not any(c.isdigit() for c in s):
        return 0
    # ------------------------------------------

    m = _NUM_RE.search(s)
    if not m:
        return 0

    num = Decimal(m.group("num"))
    suf = (m.group("suf") or "").upper()

    val = num * _SUFFIXES.get(suf, 1)

    return int(val) if as_int else float(val)


def get_system_info():
    info = {}

    # CPU
    info["cpu_name"] = platform.processor()
    info["cpu_cores_physical"] = psutil.cpu_count(logical=False)
    info["cpu_cores_logical"] = psutil.cpu_count(logical=True)
    info["cpu_freq_mhz"] = psutil.cpu_freq().max

    # RAM
    mem = psutil.virtual_memory()
    info["ram_total_gb"] = round(mem.total / (1024**3), 2)
    info["ram_available_gb"] = round(mem.available / (1024**3), 2)

    # OS
    info["os"] = platform.system()
    info["os_version"] = platform.version()

    return info

