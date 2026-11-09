#!/usr/bin/env python3
"""Checks every server folder: metadata.json against schema.json, id = folder, logo/background images, and that no
address belongs to two servers. Exit code 1 lists every problem (the pull request check shows them)."""
import json, pathlib, sys, fnmatch
try:
    from PIL import Image
except ImportError:
    Image = None
try:
    import jsonschema
except ImportError:
    jsonschema = None

root = pathlib.Path(__file__).resolve().parent.parent
schema = json.loads((root / "schema.json").read_text())
problems, owners = [], {}
for folder in sorted((root / "servers").iterdir()):
    if not folder.is_dir():
        continue
    meta_file = folder / "metadata.json"
    if not meta_file.exists():
        problems.append(f"{folder.name}: no metadata.json"); continue
    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    except Exception as e:
        problems.append(f"{folder.name}: metadata.json isn't valid JSON ({e})"); continue
    if jsonschema:
        for err in jsonschema.Draft202012Validator(schema).iter_errors(meta):
            problems.append(f"{folder.name}: {'/'.join(map(str, err.path)) or 'metadata'}: {err.message}")
    if meta.get("id") != folder.name:
        problems.append(f"{folder.name}: id must be the folder name")
    for a in meta.get("addresses", []):
        if a != a.lower():
            problems.append(f"{folder.name}: addresses must be lower case ({a})")
        if a in owners:
            problems.append(f"{folder.name}: {a} is already used by {owners[a]}")
        owners[a] = folder.name
    if meta.get("primaryAddress") and not any(fnmatch.fnmatch(meta["primaryAddress"], p) or meta["primaryAddress"] == p for p in meta.get("addresses", [])):
        problems.append(f"{folder.name}: primaryAddress must match one of the addresses")
    for img, (lo, hi), limit in (("logo.png", (128, 1024), 512 * 1024), ("banner.png", (640, 2560), 2 * 1024 * 1024)):
        p = folder / img
        if not p.exists():
            problems.append(f"{folder.name}: {img} is missing (logo and banner are both required)")
            continue
        if p.stat().st_size > limit:
            problems.append(f"{folder.name}: {img} is larger than {limit // 1024} KB")
        if Image:
            with Image.open(p) as im:
                if im.format != "PNG":
                    problems.append(f"{folder.name}: {img} must be a PNG")
                if img == "logo.png" and (im.width != im.height or not lo <= im.width <= hi):
                    problems.append(f"{folder.name}: logo.png must be square, {lo}-{hi} px")
                if img == "banner.png" and (not 1.7 <= im.width / im.height <= 5 or not lo <= im.width <= hi):
                    problems.append(f"{folder.name}: banner.png must be wide (16:9 to 5:1), {lo}-{hi} px across")
    extra = {p.name for p in folder.iterdir()} - {"metadata.json", "logo.png", "banner.png"}
    if extra:
        problems.append(f"{folder.name}: unexpected files {sorted(extra)}")

if problems:
    print("\n".join("✗ " + p for p in problems))
    sys.exit(1)
print(f"✓ {len(list((root / 'servers').iterdir()))} servers OK")
