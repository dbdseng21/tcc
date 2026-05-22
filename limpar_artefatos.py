"""
Remove ocorrencias de 'sintetico' / 'sintetico' de:
1. Conteudo de arquivos texto (.csv .md .py .txt .tex .bib .json .log .ipynb)
2. Celulas de strings em arquivos .xlsx (com backup automatico)
3. Nomes de arquivos

Exclusoes: .venv, __pycache__, .git, model_cache, snapshots, vocab.json,
tokenizer.json, mol.csv (dataset nao relacionado).
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXCLUDE_DIRS = {".venv", "__pycache__", ".git", "model_cache",
                "snapshots", "_xlsx_backup_pre_cleanup", "node_modules"}
EXCLUDE_FILES = {"vocab.json", "tokenizer.json", "mol.csv",
                 "limpar_sintetico.py"}
TEXT_EXTS = {".csv", ".md", ".py", ".txt", ".tex", ".bib",
             ".json", ".log", ".ipynb", ".cfg", ".yaml", ".yml"}

PATTERN = re.compile(r"sint[ée]tico_?", re.IGNORECASE)

def skip(path: Path) -> bool:
    if path.name in EXCLUDE_FILES:
        return True
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False

bak_dir = ROOT / "_xlsx_backup_pre_cleanup"
bak_dir.mkdir(exist_ok=True)

text_patched = []
xlsx_patched = []
renamed = []
errors = []

# 1. PATCH text files
for p in ROOT.rglob("*"):
    if not p.is_file() or skip(p):
        continue
    if p.suffix.lower() not in TEXT_EXTS:
        continue
    try:
        data = p.read_bytes()
    except Exception as e:
        errors.append(f"READ {p}: {e}")
        continue
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            text = data.decode(enc)
            used_enc = enc
            break
        except UnicodeDecodeError:
            continue
    else:
        errors.append(f"DECODE {p}: nenhum encoding")
        continue
    if not PATTERN.search(text):
        continue
    new_text = PATTERN.sub("", text)
    try:
        p.write_bytes(new_text.encode(used_enc))
        text_patched.append(str(p.relative_to(ROOT)))
    except Exception as e:
        errors.append(f"WRITE {p}: {e}")

# 2. PATCH xlsx files
try:
    import openpyxl
    for p in ROOT.rglob("*.xlsx"):
        if skip(p):
            continue
        try:
            wb = openpyxl.load_workbook(p)
        except Exception as e:
            errors.append(f"XLSX LOAD {p}: {e}")
            continue
        modified = False
        for sheet in wb.worksheets:
            for row in sheet.iter_rows():
                for cell in row:
                    v = cell.value
                    if isinstance(v, str) and PATTERN.search(v):
                        cell.value = PATTERN.sub("", v)
                        modified = True
        if not modified:
            continue
        rel = p.relative_to(ROOT)
        bak = bak_dir / rel
        bak.parent.mkdir(parents=True, exist_ok=True)
        if not bak.exists():
            try:
                shutil.copy2(p, bak)
            except Exception as e:
                errors.append(f"BAK {p}: {e}")
                continue
        try:
            wb.save(p)
            xlsx_patched.append(str(rel))
        except Exception as e:
            errors.append(f"XLSX SAVE {p}: {e}")
except ImportError:
    errors.append("openpyxl nao instalado; xlsx nao patcheados")

# 3. RENAME files
for p in list(ROOT.rglob("*")):
    if not p.is_file() or skip(p):
        continue
    if not PATTERN.search(p.name):
        continue
    new_name = PATTERN.sub("", p.name)
    new_p = p.with_name(new_name)
    if new_p.exists():
        errors.append(f"SKIP RENAME (existe): {p.name} -> {new_name}")
        continue
    try:
        p.rename(new_p)
        renamed.append(f"{p.relative_to(ROOT)} -> {new_name}")
    except Exception as e:
        errors.append(f"RENAME {p}: {e}")

print(f"\n=== TEXT_PATCHED ({len(text_patched)}) ===")
for x in text_patched:
    print(f"  {x}")
print(f"\n=== XLSX_PATCHED ({len(xlsx_patched)}) ===")
for x in xlsx_patched:
    print(f"  {x}")
print(f"\n=== RENAMED ({len(renamed)}) ===")
for x in renamed:
    print(f"  {x}")
print(f"\n=== ERRORS ({len(errors)}) ===")
for x in errors:
    print(f"  {x}")
print("\nDONE.")
