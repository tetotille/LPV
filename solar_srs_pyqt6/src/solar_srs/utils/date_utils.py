from __future__ import annotations

from datetime import date, datetime


def today_iso() -> str:
    return date.today().isoformat()


def normalize_date(text: str) -> str:
    text = (text or "").strip()
    if not text:
        raise ValueError("La fecha no puede estar vacía.")
    try:
        return datetime.strptime(text, "%Y-%m-%d").date().isoformat()
    except ValueError as exc:
        raise ValueError("La fecha debe tener formato YYYY-MM-DD.") from exc
