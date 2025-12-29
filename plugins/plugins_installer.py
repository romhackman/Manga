import os
import sys
import json
import argparse
import requests
import zipfile
import io
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGINS_ROOT = os.path.join(BASE_DIR, "plugins")

JSON_FILE = os.path.join(PLUGINS_ROOT, "instance_plugins.json")
TEMP_JSON = os.path.join(PLUGINS_ROOT, "temp_link.json")

os.makedirs(PLUGINS_ROOT, exist_ok=True)

if os.name == "nt":
    INSTALL_SCRIPT = os.path.join(BASE_DIR, "install_requirements.bat")
else:
    INSTALL_SCRIPT = os.path.join(BASE_DIR, "install_requirements.sh")

parser = argparse.ArgumentParser()
parser.add_argument("--link")
args = parser.parse_args()

if args.link:
    lien = args.link
elif os.path.exists(TEMP_JSON):
    with open(TEMP_JSON, "r", encoding="utf-8") as f:
        lien = json.load(f).get("link")
else:
    sys.exit(1)

nom_plugin = lien.rstrip("/").split("/")[-1]
plugin_dir = os.path.join(PLUGINS_ROOT, nom_plugin)

if os.path.exists(plugin_dir):
    print("Plugin déjà installé")
    sys.exit(0)

os.makedirs(plugin_dir, exist_ok=True)

zip_url = "/".join(lien.split("/")[:5]) + "/archive/refs/heads/main.zip"
r = requests.get(zip_url)
r.raise_for_status()

with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    root = z.namelist()[0].split("/")[0]
    for file in z.namelist():
        if file.startswith(f"{root}/{nom_plugin}/"):
            dest = os.path.join(plugin_dir, os.path.relpath(file, f"{root}/{nom_plugin}"))
            if file.endswith("/"):
                os.makedirs(dest, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(z.read(file))

req = os.path.join(plugin_dir, "requirements.txt")
if os.path.exists(req):
    subprocess.run(
        ["cmd", "/c", INSTALL_SCRIPT] if os.name == "nt" else ["bash", INSTALL_SCRIPT],
        cwd=plugin_dir
    )

plugins = {}
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        plugins = json.load(f)

main_py = os.path.join(plugin_dir, f"{nom_plugin}.py")
if os.path.exists(main_py):
    plugins[nom_plugin] = main_py
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(plugins, f, indent=4)

if os.path.exists(TEMP_JSON):
    os.remove(TEMP_JSON)

print("✅ Plugin installé")
