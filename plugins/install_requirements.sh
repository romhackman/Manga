#!/bin/bash
cd "$(dirname "$0")"

VENV_PYTHON="../../.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo ".venv introuvable"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "Aucun requirements.txt"
    exit 0
fi

"$VENV_PYTHON" -m pip install -r requirements.txt
