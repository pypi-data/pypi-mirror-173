from __future__ import annotations

from pathlib import Path
from typing import Any

from yaml import safe_load


def stat(value: int, value_max: int = 0xFFFF, low: int = 1000, high: int = 3000) -> int:
    if not (0 <= value <= value_max):
        raise ValueError("Value out of range")
    v = value / value_max
    return round(low + (high - low) * v)


def get_skill_info(file_name: str = "ko") -> dict[str, Any]:
    skill_dir = Path(__file__).parent / "skill" / f"{file_name}.yml"
    data = safe_load(skill_dir.read_text("utf-8"))
    return data
