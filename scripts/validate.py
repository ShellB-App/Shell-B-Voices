#!/usr/bin/env python3
"""Check every voice in voices/<id>/voice.json and build index.json.

A voice is a text description that HERMES (Shell:B's speech service) turns into a reference clip with Qwen3-TTS's
voice design, plus an optional tone instruction. No audio is stored here: the voice is designed on the machine that
installs it. This script checks the fields HERMES needs and keeps descriptions honest (a design, not an impression of
a real person). Standard library only; run from the repository root:

    python3 -I scripts/validate.py          # check + rebuild index.json
    python3 -I scripts/validate.py --check  # check only (CI); exits 1 on any error
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICES = ROOT / "voices"
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,39}$")
LANG_RE = re.compile(r"^[a-z]{2}(-[A-Z]{2})?$")
IMPRESSION = re.compile(r"\b(sounds? like|impression of|imitat|impersonat|in the voice of|as voiced by)\b", re.I)
FIELDS = ("name", "label", "description", "style", "language", "refText", "tags", "author", "license", "version", "homepage")
PREVIEWS = (".mp3", ".ogg", ".wav")


def check(path: Path) -> tuple[dict | None, list[str], list[str]]:
    errors, warnings = [], []
    try:
        spec = json.loads(path.read_text())
    except (OSError, ValueError) as e:
        return None, [f"not valid JSON: {e}"], []
    if not isinstance(spec, dict):
        return None, ["the file must hold one object"], []
    folder = path.parent.name
    if not ID_RE.match(folder):
        errors.append(f"folder name {folder!r}: lowercase letters, digits and dashes only")
    if spec.get("id") not in (None, folder):
        errors.append(f"id {spec.get('id')!r} doesn't match the folder name {folder!r}")
    for k in spec:
        if k not in FIELDS and k != "id":
            warnings.append(f"{k} is not a field HERMES knows and will be ignored")
    name = str(spec.get("name") or "").strip()
    if not name or len(name) > 32:
        errors.append("name: 1-32 characters")
    label = str(spec.get("label") or "").strip()
    if not label or len(label) > 60:
        errors.append("label: 1-60 characters, e.g. \"Harbor · low, calm male\"")
    desc = str(spec.get("description") or "").strip()
    if len(desc) < 40 or len(desc) > 600:
        errors.append("description: 40-600 characters; this is the voice design")
    if IMPRESSION.search(desc) or IMPRESSION.search(str(spec.get("style") or "")):
        errors.append("description reads as an impression of someone; describe a voice, not a person")
    style = spec.get("style", "")
    if not isinstance(style, str) or len(style) > 200:
        errors.append("style: a tone instruction of at most 200 characters (optional)")
    lang = spec.get("language", "en")
    if not (isinstance(lang, str) and LANG_RE.match(lang)):
        errors.append("language: a code like en, fr or en-GB")
    ref = spec.get("refText", "")
    if not isinstance(ref, str) or len(ref) > 300:
        errors.append("refText: at most 300 characters (optional; the line the reference clip reads)")
    elif ref and len(ref) < 60:
        warnings.append("refText is short; the reference clip designs better from a couple of sentences")
    for key in ("author", "license"):
        if not spec.get(key):
            errors.append(f"{key} is required (license: an SPDX id such as MIT or CC0-1.0)")
    if not spec.get("version"):
        warnings.append("no version; start at \"1.0\"")
    tags = spec.get("tags", [])
    if not (isinstance(tags, list) and all(isinstance(t, str) and t for t in tags)):
        errors.append("tags: a list of short strings")
    for f in path.parent.iterdir():
        if f.name == "voice.json" or f.name.startswith("."):
            continue
        if f.stem == "sample" and f.suffix.lower() in PREVIEWS:
            if f.stat().st_size > 400 * 1024:
                errors.append("sample: at most 400 KB")
            continue
        warnings.append(f"{f.name} is not used (only voice.json and an optional sample.mp3/ogg/wav)")
    return spec, errors, warnings


def entry(folder: str, spec: dict, path: Path) -> dict:
    sample = next((f.name for f in path.parent.iterdir() if f.stem == "sample" and f.suffix.lower() in PREVIEWS), None)
    return {"id": folder, "name": spec["name"], "label": spec["label"], "blurb": spec["description"], "style": spec.get("style", ""),
            "language": spec.get("language", "en"), "author": spec["author"], "license": spec["license"],
            "version": spec.get("version", "1.0"), "tags": spec.get("tags", []), "path": str(path.relative_to(ROOT)),
            "sample": f"voices/{folder}/{sample}" if sample else None}


def main() -> int:
    check_only = "--check" in sys.argv
    items, failed = [], 0
    files = sorted(VOICES.glob("*/voice.json"))
    if not files:
        print("no voices found under voices/<id>/voice.json")
        return 1
    for path in files:
        spec, errors, warnings = check(path)
        folder = path.parent.name
        for w in warnings:
            print(f"warning  {folder}: {w}")
        for e in errors:
            print(f"ERROR    {folder}: {e}")
        if errors or spec is None:
            failed += 1
            continue
        items.append(entry(folder, spec, path))
        print(f"ok       {folder} ({spec['label']})")
    index = {"format": 1, "kind": "voice", "items": sorted(items, key=lambda i: i["name"].lower())}
    if not check_only:
        (ROOT / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False) + "\n")
        print(f"index.json: {len(items)} voices")
    elif (ROOT / "index.json").exists() and json.loads((ROOT / "index.json").read_text()) != index:
        print("ERROR    index.json is out of date: run scripts/validate.py and commit it")
        failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
