#!/usr/bin/env python3
"""
Form Definitions Database Importer
Reads JSON definition files from forms/definitions/ and imports them into a
SQLite database (forms.db) using the following relational schema:

  forms
  ─────
  id           INTEGER PRIMARY KEY
  form_code    TEXT NOT NULL UNIQUE   — e.g. 'EX00'
  filename     TEXT NOT NULL
  title        TEXT
  page_count   INTEGER
  field_count  INTEGER

  form_fields
  ───────────
  id           INTEGER PRIMARY KEY
  form_id      INTEGER NOT NULL REFERENCES forms(id)
  name         TEXT NOT NULL          — internal PDF field name
  type         TEXT NOT NULL          — Text | CheckBox | RadioButton | …
  page         INTEGER
  rect_x0      REAL                   — field bounding box (PDF user-space pts)
  rect_y0      REAL
  rect_x1      REAL
  rect_y1      REAL
  label        TEXT                   — tooltip / field label
  default_value TEXT
  max_length   INTEGER                — NULL = unlimited
  choices      TEXT                   — JSON array for ComboBox / ListBox
  on_state     TEXT                   — on-value for CheckBox / RadioButton
  multiline    INTEGER                — 0 | 1
  required     INTEGER                — 0 | 1
  read_only    INTEGER                — 0 | 1
  text_font    TEXT
  text_fontsize REAL
  has_calc     INTEGER                — 0 | 1  (JavaScript calculation)
  has_format   INTEGER                — 0 | 1  (JavaScript format)
  has_validate INTEGER                — 0 | 1  (JavaScript validation)
"""

import json
import logging
import sqlite3
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFINITIONS_DIR = Path("forms/definitions")
DB_PATH = Path("forms.db")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Schema setup
# ---------------------------------------------------------------------------

DDL = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS forms (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    form_code   TEXT    NOT NULL UNIQUE,
    filename    TEXT    NOT NULL,
    title       TEXT,
    page_count  INTEGER,
    field_count INTEGER
);

CREATE TABLE IF NOT EXISTS form_fields (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    form_id       INTEGER NOT NULL REFERENCES forms(id) ON DELETE CASCADE,
    name          TEXT    NOT NULL,
    type          TEXT    NOT NULL,
    page          INTEGER,
    rect_x0       REAL,
    rect_y0       REAL,
    rect_x1       REAL,
    rect_y1       REAL,
    label         TEXT,
    label_pdf     TEXT,
    label_inferred TEXT,
    label_source  TEXT,
    label_confidence REAL,
    default_value TEXT,
    max_length    INTEGER,
    choices       TEXT,
    on_state      TEXT,
    multiline     INTEGER NOT NULL DEFAULT 0,
    required      INTEGER NOT NULL DEFAULT 0,
    read_only     INTEGER NOT NULL DEFAULT 0,
    text_font     TEXT,
    text_fontsize REAL,
    has_calc      INTEGER NOT NULL DEFAULT 0,
    has_format    INTEGER NOT NULL DEFAULT 0,
    has_validate  INTEGER NOT NULL DEFAULT 0,
    section_code  TEXT,
    section_title TEXT,
    section_level INTEGER,
    checkbox_option_text   TEXT,
    checkbox_option_level  INTEGER,
    checkbox_option_parent TEXT,
    checkbox_option_index  INTEGER,
    normalized_group       TEXT,
    normalized_role        TEXT,
    normalized_parent_label TEXT
);

CREATE INDEX IF NOT EXISTS idx_fields_form_id ON form_fields(form_id);
CREATE INDEX IF NOT EXISTS idx_fields_type    ON form_fields(type);
"""


def _table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    cur = conn.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cur.fetchall()}


def _ensure_columns(conn: sqlite3.Connection) -> None:
    """Add newly introduced columns for existing DB files."""
    existing = _table_columns(conn, "form_fields")
    needed = {
        "label_pdf": "TEXT",
        "label_inferred": "TEXT",
        "label_source": "TEXT",
        "label_confidence": "REAL",
        "section_code": "TEXT",
        "section_title": "TEXT",
        "section_level": "INTEGER",
        "checkbox_option_text": "TEXT",
        "checkbox_option_level": "INTEGER",
        "checkbox_option_parent": "TEXT",
        "checkbox_option_index": "INTEGER",
        "normalized_group": "TEXT",
        "normalized_role": "TEXT",
        "normalized_parent_label": "TEXT",
    }
    for name, sql_type in needed.items():
        if name not in existing:
            conn.execute(f"ALTER TABLE form_fields ADD COLUMN {name} {sql_type}")
    conn.commit()

# ---------------------------------------------------------------------------
# Import logic
# ---------------------------------------------------------------------------

def _bool_int(value) -> int:
    return 1 if value else 0


def import_json(conn: sqlite3.Connection, json_path: Path) -> int:
    """
    Read one form definition JSON and upsert it into the database.
    Returns the number of fields imported.
    """
    with open(json_path, encoding="utf-8") as fh:
        form_def: dict = json.load(fh)

    cur = conn.cursor()

    # Upsert form row -------------------------------------------------------
    cur.execute(
        """
        INSERT INTO forms (form_code, filename, title, page_count, field_count)
        VALUES (:form_code, :filename, :title, :page_count, :field_count)
        ON CONFLICT(form_code) DO UPDATE SET
            filename    = excluded.filename,
            title       = excluded.title,
            page_count  = excluded.page_count,
            field_count = excluded.field_count
        """,
        {
            "form_code":   form_def["form_code"],
            "filename":    form_def["filename"],
            "title":       form_def.get("title"),
            "page_count":  form_def.get("page_count"),
            "field_count": form_def.get("field_count"),
        },
    )

    cur.execute(
        "SELECT id FROM forms WHERE form_code = ?", (form_def["form_code"],)
    )
    form_id: int = cur.fetchone()[0]

    # Replace existing fields for this form ---------------------------------
    cur.execute("DELETE FROM form_fields WHERE form_id = ?", (form_id,))

    rows = []
    for field in form_def.get("fields", []):
        rect = field.get("rect") or [None, None, None, None]
        choices_raw = field.get("choices")
        choices_json = json.dumps(choices_raw, ensure_ascii=False) if choices_raw else None

        rows.append(
            (
                form_id,
                field.get("name"),
                field.get("type"),
                field.get("page"),
                rect[0] if len(rect) > 0 else None,
                rect[1] if len(rect) > 1 else None,
                rect[2] if len(rect) > 2 else None,
                rect[3] if len(rect) > 3 else None,
                field.get("label"),
                field.get("label_pdf"),
                field.get("label_inferred"),
                field.get("label_source"),
                field.get("label_confidence"),
                field.get("default_value"),
                field.get("max_length"),
                choices_json,
                field.get("on_state"),
                _bool_int(field.get("multiline")),
                _bool_int(field.get("required")),
                _bool_int(field.get("read_only")),
                field.get("text_font"),
                field.get("text_fontsize"),
                _bool_int(field.get("has_calc")),
                _bool_int(field.get("has_format")),
                _bool_int(field.get("has_validate")),
                field.get("section_code"),
                field.get("section_title"),
                field.get("section_level"),
                field.get("checkbox_option_text"),
                field.get("checkbox_option_level"),
                field.get("checkbox_option_parent"),
                field.get("checkbox_option_index"),
                field.get("normalized_group"),
                field.get("normalized_role"),
                field.get("normalized_parent_label"),
            )
        )

    cur.executemany(
        """
        INSERT INTO form_fields (
            form_id, name, type, page,
            rect_x0, rect_y0, rect_x1, rect_y1,
            label, label_pdf, label_inferred, label_source, label_confidence,
            default_value, max_length, choices, on_state,
            multiline, required, read_only,
            text_font, text_fontsize,
            has_calc, has_format, has_validate,
            section_code, section_title, section_level,
            checkbox_option_text, checkbox_option_level, checkbox_option_parent, checkbox_option_index,
            normalized_group, normalized_role, normalized_parent_label
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        rows,
    )

    conn.commit()
    return len(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    json_files = sorted(DEFINITIONS_DIR.glob("*.json"))
    if not json_files:
        log.error("No JSON definition files found in %s", DEFINITIONS_DIR)
        raise SystemExit(1)

    log.info("Connecting to database: %s", DB_PATH)
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript(DDL)
    _ensure_columns(conn)

    total_fields = 0
    for json_path in json_files:
        log.info("Importing: %s", json_path.name)
        try:
            n = import_json(conn, json_path)
        except Exception as exc:
            log.error("  Failed to import %s: %s", json_path.name, exc)
            conn.rollback()
            continue
        log.info("  → %d field(s) imported", n)
        total_fields += n

    conn.close()

    log.info(
        "Done. %d form definition(s) imported, %d total fields → %s",
        len(json_files),
        total_fields,
        DB_PATH,
    )

    # Quick verification
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM forms")
    form_rows = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM form_fields")
    field_rows = cur.fetchone()[0]
    conn.close()

    log.info("DB check → %d form row(s), %d field row(s)", form_rows, field_rows)


if __name__ == "__main__":
    main()
