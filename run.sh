#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

PY=$(command -v python3.13 || command -v python3 || command -v python || true)
if [ -z "$PY" ]; then
  echo "Python 3 tidak ditemukan." >&2
  exit 1
fi

PYTHON_BIN=".venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN=".venv/Scripts/python"
fi

if [ ! -x "$PYTHON_BIN" ]; then
  "$PY" -m venv .venv
  if [ -x .venv/bin/python ]; then
    PYTHON_BIN=".venv/bin/python"
  else
    PYTHON_BIN=".venv/Scripts/python"
  fi
  "$PYTHON_BIN" -m pip install --upgrade pip
  "$PYTHON_BIN" -m pip install .
fi

export GAI_BIND_PORT="${PORT:-8765}"

exec "$PYTHON_BIN" -m uvicorn app.main:app --host 127.0.0.1 --port "$GAI_BIND_PORT" --log-level warning
