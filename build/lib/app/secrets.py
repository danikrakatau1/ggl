"""Secure local credential store (cross-platform).

Replaces macOS Keychain with a secure local restricted store
compatible with Linux, Windows, and macOS.
"""

from __future__ import annotations

import json
from pathlib import Path
from .config import settings


def _path() -> Path:
    settings.ensure_dirs()
    return settings.data_dir / "secrets.json"


def _load() -> dict[str, str]:
    p = _path()
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save(data: dict[str, str]) -> None:
    p = _path()
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    try:
        p.chmod(0o600)
    except Exception:
        pass


def put(ref: str, value: str) -> None:
    data = _load()
    data[ref] = value
    _save(data)


def get(ref: str) -> str:
    data = _load()
    return data.get(ref, "")


def delete(ref: str) -> None:
    data = _load()
    if ref in data:
        del data[ref]
        _save(data)


def exists(ref: str) -> bool:
    return bool(get(ref))
