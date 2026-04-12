#!/usr/bin/env python3
"""
PDF Form Field Extractor
Reads every editable PDF from forms/editable/, extracts all fillable widget
metadata, and writes one JSON definition file per form to forms/definitions/.

Field metadata captured per widget
───────────────────────────────────
  name          – internal PDF field name
  type          – Text | CheckBox | RadioButton | ComboBox | ListBox |
                  Signature | Button
  page          – 1-based page number
  rect          – [x0, y0, x1, y1] in PDF user-space points
  label         – tooltip / field label if present in PDF
  default_value – value embedded in the PDF at authoring time
  max_length    – character limit for text fields (0 = unlimited)
  choices       – list of option strings for ComboBox / ListBox
  on_state      – on-value for CheckBox / RadioButton widgets
  multiline     – whether the text field accepts multiple lines
  required      – PDF Required flag
  read_only     – PDF ReadOnly flag
  text_font     – font name used in the field's display
  text_fontsize – font size used in the field's display
  has_calc      – whether the field has a JavaScript calculation action
  has_format    – whether the field has a JavaScript format action
  has_validate  – whether the field has a JavaScript validation action
    section_code  – inferred section identifier, e.g. '1', '2.1'
    section_title – inferred section title text
    section_level – 1 for top-level section, 2 for subsection
    checkbox_option_text   – parsed option text for checkbox/radio items
    checkbox_option_level  – hierarchy level inferred by indentation
    checkbox_option_parent – parent option text for nested checkbox items
    normalized_group       – normalized structural group, e.g. 'signature_footer'
    normalized_role        – normalized role within a group, e.g. 'signature_place'
    normalized_parent_label – human-readable parent/caption for the normalized role
"""

import json
import logging
import math
import re
from pathlib import Path

import fitz  # PyMuPDF

try:
    import numpy as np
    from rapidocr_onnxruntime import RapidOCR
except Exception:
    np = None
    RapidOCR = None

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EDITABLE_DIR = Path("forms/editable")
DEFINITIONS_DIR = Path("forms/definitions")
OCR_SCALE = 2.0

# PDF field-flag bit positions (PDF spec Table 228 / 232)
FLAG_READ_ONLY = 1 << 0
FLAG_REQUIRED  = 1 << 1
FLAG_MULTILINE = 1 << 12

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

_OCR_ENGINE = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FORM_CODE_RE = re.compile(r"^(EX\d+)", re.IGNORECASE)


def _form_code(filename: str) -> str:
    """Extract 'EX00', 'EX01', … from the filename."""
    m = _FORM_CODE_RE.match(filename)
    return m.group(1).upper() if m else Path(filename).stem


def _clean_text(text: str) -> str:
    """Normalize whitespace for candidate label text."""
    return re.sub(r"\s+", " ", (text or "").strip())


def _normalize_checkbox_marker_text(text: str) -> str:
    """Normalize OCR variations of checkbox markers to a single symbol."""
    if not text:
        return ""
    t = text
    t = t.replace("☐", "□").replace("▢", "□").replace("◻", "□")
    t = re.sub(r"\[\s*\]", "□", t)
    t = re.sub(r"\(\s*\)", "□", t)
    return t


def _get_ocr_engine():
    global _OCR_ENGINE
    if _OCR_ENGINE is not None:
        return _OCR_ENGINE
    if RapidOCR is None or np is None:
        return None
    try:
        _OCR_ENGINE = RapidOCR()
    except Exception:
        _OCR_ENGINE = None
    return _OCR_ENGINE


def _extract_ocr_lines(page: fitz.Page) -> list[dict]:
    """OCR a page and return text lines in PDF coordinate space."""
    engine = _get_ocr_engine()
    if engine is None:
        return []

    pix = page.get_pixmap(matrix=fitz.Matrix(OCR_SCALE, OCR_SCALE), alpha=False)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

    try:
        result, _ = engine(arr)
    except Exception:
        return []
    if not result:
        return []

    lines = []
    for item in result:
        box, text = item[0], item[1]
        clean = _clean_text(text)
        if not clean:
            continue
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        lines.append(
            {
                "rect": (
                    min(xs) / OCR_SCALE,
                    min(ys) / OCR_SCALE,
                    max(xs) / OCR_SCALE,
                    max(ys) / OCR_SCALE,
                ),
                "text": clean,
                "source": "ocr",
            }
        )
    return lines


def _is_noise_text(text: str) -> bool:
    """Filter out blocks that are not meaningful labels."""
    if not text:
        return True
    if text in {"-", "--", "*", "X", "* X"}:
        return True
    if re.match(r"^\d+\)\s+[A-ZÁÉÍÓÚÜÑ0-9\s,./()-]+$", text):
        return True
    if text.endswith(":") and len(text) > 20:
        return True
    if len(text) > 65:
        return True
    # Option-marker lines often seen around checkbox groups.
    if re.match(r"^[XHMSCDVSp0-9*\-\s().,]+$", text):
        return True
    # Very short lowercase fragments are usually text debris.
    if len(text) <= 3 and text == text.lower():
        return True
    # Ignore strings made mostly of separators.
    only_punct = re.sub(r"[\w\d\u00C0-\u024F]", "", text, flags=re.UNICODE)
    if text and len(only_punct) >= len(text) * 0.7:
        return True
    return False


def _has_dot_leaders(items: list[tuple]) -> bool:
    """Return True if any word token in the group is a dot-leader filler."""
    for item in items:
        word = item[4]
        non_alpha = re.sub(r"[\w\d\u00C0-\u024F]", "", word, flags=re.UNICODE)
        if len(non_alpha) >= max(3, len(word) * 0.5):
            return True
    return False


def _split_dotted_line(items: list[tuple], include_noise: bool) -> list[dict]:
    """
    Split a word-group that mixes label text with dot-leader separator characters
    into individual short segments, each with their own bounding rect.

    The recurring pattern is rows like:
      DIRIGIDA A ……………… Código DIR3………… PROVINCIA ……
    where the full combined text is noise-filtered because it is > 65 chars.
    Splitting at dot boundaries recovers 'DIRIGIDA A', 'Código', 'DIR3',
    'PROVINCIA' as individual label candidates.
    """
    out: list[dict] = []

    # Accumulator for the current meaningful segment.
    curr_words: list[str] = []
    curr_x0 = curr_y0 = curr_x1 = curr_y1 = 0.0
    has_curr = False

    def _flush() -> None:
        nonlocal has_curr
        if not curr_words:
            return
        seg_text = _clean_text(" ".join(curr_words))
        if seg_text and (include_noise or not _is_noise_text(seg_text)):
            out.append({"rect": (curr_x0, curr_y0, curr_x1, curr_y1), "text": seg_text, "source": "pdf"})
        curr_words.clear()
        has_curr = False

    def _extend(x0: float, y0: float, x1: float, y1: float) -> None:
        nonlocal curr_x0, curr_y0, curr_x1, curr_y1, has_curr
        if not has_curr:
            curr_x0, curr_y0, curr_x1, curr_y1 = x0, y0, x1, y1
            has_curr = True
        else:
            curr_x0 = min(curr_x0, x0)
            curr_y0 = min(curr_y0, y0)
            curr_x1 = max(curr_x1, x1)
            curr_y1 = max(curr_y1, y1)

    for item in items:
        x0, y0, x1, y1, word = item[0], item[1], item[2], item[3], item[4]
        non_alpha = re.sub(r"[\w\d\u00C0-\u024F]", "", word, flags=re.UNICODE)
        dot_ratio = len(non_alpha) / max(1, len(word))
        # Meaningful alpha runs of 2+ characters within the token.
        parts = re.findall(r"\w{2,}", word)

        if dot_ratio < 0.3:
            # Mostly meaningful text – accumulate normally.
            curr_words.append(word)
            _extend(x0, y0, x1, y1)
        elif not parts:
            # Pure dot/separator cluster – flush pending segment.
            _flush()
        else:
            # Mixed token (e.g. '……Código' or 'DIR3………'):
            # flush any pending accumulation then emit each meaningful part
            # at this token's position so proximity inference can find it.
            _flush()
            for part in parts:
                if include_noise or not _is_noise_text(part):
                    out.append({"rect": (x0, y0, x1, y1), "text": part, "source": "pdf"})

    _flush()
    return out


def _build_text_lines(page: fitz.Page, include_noise: bool = False) -> list[dict]:
    """
    Build line-level text boxes from page words.
    PyMuPDF words format: (x0, y0, x1, y1, word, block_no, line_no, word_no)
    """
    words = page.get_text("words")
    grouped: dict[tuple[int, int], list[tuple]] = {}

    for w in words:
        key = (w[5], w[6])
        grouped.setdefault(key, []).append(w)

    lines = []
    for _, items in grouped.items():
        items.sort(key=lambda it: it[7])
        text = _clean_text(" ".join(it[4] for it in items))
        if (not include_noise) and _is_noise_text(text):
            # Recover label segments hidden inside dot-leader rows
            # (e.g. 'DIRIGIDA A ………… Código DIR3………… PROVINCIA ……').
            if _has_dot_leaders(items):
                lines.extend(_split_dotted_line(items, include_noise))
            continue
        x0 = min(it[0] for it in items)
        y0 = min(it[1] for it in items)
        x1 = max(it[2] for it in items)
        y1 = max(it[3] for it in items)
        lines.append({"rect": (x0, y0, x1, y1), "text": text, "source": "pdf"})

    # OCR fallback for pages with no/minimal extractable text.
    if len(lines) < 4:
        ocr_lines = _extract_ocr_lines(page)
        merged = []
        for line in ocr_lines:
            text = _normalize_checkbox_marker_text(line["text"])
            text = _clean_text(text)
            if (not include_noise) and _is_noise_text(text):
                continue
            merged.append({"rect": line["rect"], "text": text, "source": "ocr"})
        if len(merged) > len(lines):
            return merged

    return lines


def _extract_sections(page: fitz.Page, lines: list[dict]) -> list[dict]:
    """
    Extract visible section headings from page text blocks.
    Supports patterns like:
      1) DATOS ...
      2) DECLARACION ...
      2.1 Texto ...
    """
    sections: list[dict] = []

    for line in lines:
        x0, y0, x1, y1 = line["rect"]
        clean = _clean_text(line["text"])
        if not clean:
            continue

        m1 = re.match(r"^(\d+)[\)\.]\s*(.+)$", clean)
        if m1:
            sections.append(
                {
                    "code": m1.group(1),
                    "title": _clean_text(m1.group(2)),
                    "level": 1,
                    "page": page.number + 1,
                    "y0": float(y0),
                    "y1": float(y1),
                }
            )
            continue

        m2 = re.match(r"^(\d+\.\d+)[\)\.]?\s*(.+)$", clean)
        if m2:
            sections.append(
                {
                    "code": m2.group(1),
                    "title": _clean_text(m2.group(2)),
                    "level": 2,
                    "page": page.number + 1,
                    "y0": float(y0),
                    "y1": float(y1),
                }
            )

    # Deduplicate same heading repeated in adjacent blocks.
    dedup: dict[tuple[int, str, str], dict] = {}
    for sec in sections:
        key = (sec["page"], sec["code"], sec["title"])
        existing = dedup.get(key)
        if not existing or sec["y0"] < existing["y0"]:
            dedup[key] = sec

    return sorted(dedup.values(), key=lambda s: (s["page"], s["y0"], s["code"]))


def _section_for_widget(widget_rect: fitz.Rect, page_number: int, sections: list[dict]) -> dict:
    """Assign a widget to the closest preceding section on the same page."""
    same_page = [s for s in sections if s["page"] == page_number]
    if not same_page:
        return {"code": None, "title": None, "level": None}

    # Prefer sections appearing above the widget.
    above = [s for s in same_page if s["y0"] <= widget_rect.y0 + 3]
    if above:
        best = max(above, key=lambda s: s["y0"])
        return {"code": best["code"], "title": best["title"], "level": best["level"]}

    # Fallback to nearest by vertical distance.
    best = min(same_page, key=lambda s: abs(s["y0"] - widget_rect.y0))
    return {"code": best["code"], "title": best["title"], "level": best["level"]}


def _extract_checkbox_options_from_lines(lines: list[dict], y_start: float, y_end: float) -> list[str]:
    """
    Extract checkbox option text in visual order from a section's text blocks.
    Many forms encode checkbox lists as text containing repeated '□' markers.
    """
    candidates = []
    for line in lines:
        x0, by0, x1, by1 = line["rect"]
        text = line["text"]
        if by1 < y_start or by0 > y_end:
            continue
        clean = _normalize_checkbox_marker_text(_clean_text(text))
        if "□" not in clean:
            continue
        candidates.append((by0, x0, clean))

    candidates.sort(key=lambda t: (t[0], t[1]))

    options: list[str] = []
    for _, _, text in candidates:
        parts = text.split("□")
        for part in parts[1:]:
            option = _clean_text(part)
            if not option or len(option) < 3:
                continue
            options.append(option)

    return options


def _find_checkbox_row_text(check_field: dict, lines: list[dict], y_start: float, y_end: float) -> str | None:
    """Find nearest text to the right of a checkbox on the same row."""
    wx0, wy0, wx1, wy1 = check_field["rect"]
    wcy = (wy0 + wy1) / 2.0

    candidates = []
    for line in lines:
        lx0, ly0, lx1, ly1 = line["rect"]
        if ly1 < y_start or ly0 > y_end:
            continue
        if lx0 < wx1 - 2:
            continue
        lcy = (ly0 + ly1) / 2.0
        y_delta = abs(lcy - wcy)
        if y_delta > 16:
            continue

        text = _clean_text(_normalize_checkbox_marker_text(line["text"]))
        text = text.lstrip("□").strip()
        if _is_noise_text(text):
            continue

        score = y_delta * 2.0 + max(0.0, lx0 - wx1)
        candidates.append((score, text))

    if not candidates:
        return None
    candidates.sort(key=lambda t: t[0])
    return candidates[0][1]


def _infer_checkbox_level(x: float, base_x: float) -> int:
    """Infer hierarchy level from checkbox horizontal indentation."""
    dx = x - base_x
    if dx <= 3:
        return 1
    if dx <= 12:
        return 2
    return 3


def _enrich_checkbox_hierarchy(lines: list[dict], page_sections: list[dict], page_fields: list[dict]) -> None:
    """
    Enrich checkbox/radio fields with hierarchical option text by section.
    """
    if not page_fields:
        return

    # Keep page sections sorted top-to-bottom for boundary detection.
    sorted_sections = sorted(page_sections, key=lambda s: s["y0"])

    for i, section in enumerate(sorted_sections):
        sec_code = section["code"]
        y_start = section["y0"] - 2
        y_end = (sorted_sections[i + 1]["y0"] - 2) if i + 1 < len(sorted_sections) else 10_000

        check_fields = [
            f
            for f in page_fields
            if f.get("section_code") == sec_code and f.get("type") in {"CheckBox", "RadioButton"}
        ]
        if not check_fields:
            continue

        check_fields.sort(key=lambda f: (f["rect"][1], f["rect"][0]))
        options = _extract_checkbox_options_from_lines(lines, y_start, y_end)
        mapped = False

        # Strategy A: parse marker-separated option lists.
        if options:
            n = min(len(check_fields), len(options))
            base_x = min(f["rect"][0] for f in check_fields[:n])
            parent_by_level: dict[int, str] = {}

            for idx in range(n):
                field = check_fields[idx]
                option_text = options[idx]
                level = _infer_checkbox_level(field["rect"][0], base_x)

                parent_text = None
                for lv in range(level - 1, 0, -1):
                    if lv in parent_by_level:
                        parent_text = parent_by_level[lv]
                        break

                parent_by_level[level] = option_text
                for lv in list(parent_by_level.keys()):
                    if lv > level:
                        del parent_by_level[lv]

                field["checkbox_option_text"] = option_text
                field["checkbox_option_level"] = level
                field["checkbox_option_parent"] = parent_text
                field["checkbox_option_index"] = idx + 1

                if field.get("label_source") != "pdf_field_label":
                    field["label"] = option_text
                    field["label_inferred"] = option_text
                    field["label_source"] = "checkbox_option_list"
                    field["label_confidence"] = 0.97 if level in {1, 2} else 0.9

            mapped = True

        # Strategy B fallback: nearest row text to the right of each checkbox.
        if not mapped:
            base_x = min(f["rect"][0] for f in check_fields)
            parent_by_level: dict[int, str] = {}
            for idx, field in enumerate(check_fields, start=1):
                option_text = _find_checkbox_row_text(field, lines, y_start, y_end)
                if not option_text:
                    continue
                level = _infer_checkbox_level(field["rect"][0], base_x)

                parent_text = None
                for lv in range(level - 1, 0, -1):
                    if lv in parent_by_level:
                        parent_text = parent_by_level[lv]
                        break

                parent_by_level[level] = option_text
                for lv in list(parent_by_level.keys()):
                    if lv > level:
                        del parent_by_level[lv]

                field["checkbox_option_text"] = option_text
                field["checkbox_option_level"] = level
                field["checkbox_option_parent"] = parent_text
                field["checkbox_option_index"] = idx

                if field.get("label_source") != "pdf_field_label":
                    field["label"] = option_text
                    field["label_inferred"] = option_text
                    field["label_source"] = "checkbox_option_row"
                    field["label_confidence"] = 0.86 if level in {1, 2} else 0.78

        # Strategy C normalization: ensure every checkbox/radio has structured
        # option metadata, using existing labels where parser-based mapping was
        # not possible.
        base_x = min(f["rect"][0] for f in check_fields)
        parent_by_level: dict[int, str] = {}
        for idx, field in enumerate(check_fields, start=1):
            if field.get("checkbox_option_text"):
                level = field.get("checkbox_option_level") or _infer_checkbox_level(field["rect"][0], base_x)
                text = field.get("checkbox_option_text")
                parent_by_level[level] = text
                for lv in list(parent_by_level.keys()):
                    if lv > level:
                        del parent_by_level[lv]
                continue

            fallback_text = field.get("label")
            if not fallback_text:
                continue

            level = _infer_checkbox_level(field["rect"][0], base_x)
            parent_text = None
            for lv in range(level - 1, 0, -1):
                if lv in parent_by_level:
                    parent_text = parent_by_level[lv]
                    break

            field["checkbox_option_text"] = fallback_text
            field["checkbox_option_level"] = level
            field["checkbox_option_parent"] = parent_text
            field["checkbox_option_index"] = idx

            parent_by_level[level] = fallback_text
            for lv in list(parent_by_level.keys()):
                if lv > level:
                    del parent_by_level[lv]


def _rect_distance(a: fitz.Rect, b: fitz.Rect) -> float:
    """Euclidean distance between two rectangles (0 if they overlap)."""
    dx = max(a.x0 - b.x1, b.x0 - a.x1, 0.0)
    dy = max(a.y0 - b.y1, b.y0 - a.y1, 0.0)
    return math.hypot(dx, dy)


def _is_signature_caption(text: str) -> bool:
    normalized = re.sub(r"\s+", "", (text or "").upper())
    return "FIRMADEL" in normalized or "FIRMADELA" in normalized


def _is_signature_date_line(text: str) -> bool:
    normalized = _clean_text(text)
    if not normalized:
        return False
    if ", a " in normalized and normalized.count(" de ") >= 2:
        return True
    squashed = re.sub(r"\s+", "", normalized.lower())
    return ",a" in squashed and squashed.count("de") >= 2 and ("." in normalized or "…" in normalized)


def _find_signature_footer_lines(lines: list[dict]) -> tuple[dict | None, list[dict]]:
    """Return the footer date line and signature captions on a page."""
    date_line = None
    signature_lines: list[dict] = []

    for line in lines:
        text = line.get("text") or ""
        if _is_signature_date_line(text):
            if date_line is None or line["rect"][1] > date_line["rect"][1]:
                date_line = line
        if _is_signature_caption(text):
            signature_lines.append(line)

    signature_lines.sort(key=lambda item: (item["rect"][1], item["rect"][0]))
    return date_line, signature_lines


def _enrich_signature_footer(lines: list[dict], page_fields: list[dict]) -> None:
    """
    Detect the recurring footer template:
      [place] , a [day] de [month] de [year]
      FIRMA DEL ...
      [signature box]

    and assign normalized semantic roles to the participating widgets.
    """
    if not page_fields:
        return

    date_line, signature_lines = _find_signature_footer_lines(lines)
    if not date_line or not signature_lines:
        return

    footer_top = min(date_line["rect"][1], min(line["rect"][1] for line in signature_lines)) - 18
    footer_bottom = max(line["rect"][3] for line in signature_lines) + 110

    candidate_fields = [
        field
        for field in page_fields
        if field.get("type") == "Text"
        and field["rect"][1] >= footer_top
        and field["rect"][3] <= footer_bottom
    ]
    if not candidate_fields:
        return

    date_y1 = date_line["rect"][3]
    signature_y0 = min(line["rect"][1] for line in signature_lines)

    top_row_fields = [
        field for field in candidate_fields if field["rect"][3] <= signature_y0 + 8
    ]
    top_row_fields.sort(key=lambda field: (field["rect"][0], field["rect"][1]))

    # The recurring footer pattern uses four fields: place, day, month, year.
    signature_roles = [
        "signature_place",
        "signature_day",
        "signature_month",
        "signature_year",
    ]
    role_labels = {
        "signature_place": "Lugar",
        "signature_day": "Día",
        "signature_month": "Mes",
        "signature_year": "Año",
    }
    for field, role in zip(top_row_fields[:4], signature_roles):
        field["normalized_group"] = "signature_footer"
        field["normalized_role"] = role
        field["normalized_parent_label"] = date_line["text"]
        field["label"] = role_labels[role]
        field["label_inferred"] = role_labels[role]
        field["label_source"] = "signature_footer_template"
        field["label_confidence"] = 0.99

    bottom_fields = [
        field for field in candidate_fields if field["rect"][1] >= signature_y0 - 2
    ]
    bottom_fields.sort(key=lambda field: (field["rect"][0], field["rect"][1]))

    # Large fields under the caption are signature boxes. Some forms have two.
    bottom_boxes = [
        field
        for field in bottom_fields
        if (field["rect"][2] - field["rect"][0]) >= 120 and (field["rect"][3] - field["rect"][1]) >= 35
    ]
    if not bottom_boxes:
        return

    def _nearest_signature_caption(field_rect: list[float]) -> str:
        center_x = (field_rect[0] + field_rect[2]) / 2.0
        best = min(
            signature_lines,
            key=lambda line: abs(((line["rect"][0] + line["rect"][2]) / 2.0) - center_x),
        )
        return best["text"]

    if len(bottom_boxes) == 1:
        bottom_boxes[0]["normalized_group"] = "signature_footer"
        bottom_boxes[0]["normalized_role"] = "signature_box"
        bottom_boxes[0]["normalized_parent_label"] = _nearest_signature_caption(bottom_boxes[0]["rect"])
        bottom_boxes[0]["label"] = _nearest_signature_caption(bottom_boxes[0]["rect"])
        bottom_boxes[0]["label_inferred"] = bottom_boxes[0]["label"]
        bottom_boxes[0]["label_source"] = "signature_footer_template"
        bottom_boxes[0]["label_confidence"] = 0.99
    else:
        for index, field in enumerate(bottom_boxes, start=1):
            field["normalized_group"] = "signature_footer"
            field["normalized_role"] = f"signature_box_{index}"
            field["normalized_parent_label"] = _nearest_signature_caption(field["rect"])
            field["label"] = _nearest_signature_caption(field["rect"])
            field["label_inferred"] = field["label"]
            field["label_source"] = "signature_footer_template"
            field["label_confidence"] = 0.99


def _row_center_y(line: dict) -> float:
    y0, y1 = line["rect"][1], line["rect"][3]
    return (y0 + y1) / 2.0


def _fields_near_row(
    page_fields: list[dict],
    y_center: float,
    field_types: set[str],
    y_tol: float = 14.0,
) -> list[dict]:
    """Return fields whose vertical center is close to a row center."""
    out = []
    for field in page_fields:
        if field.get("type") not in field_types:
            continue
        fy0, fy1 = field["rect"][1], field["rect"][3]
        f_center = (fy0 + fy1) / 2.0
        if abs(f_center - y_center) <= y_tol:
            out.append(field)
    return sorted(out, key=lambda item: (item["rect"][0], item["rect"][1]))


def _find_first_line(lines: list[dict], predicate) -> dict | None:
    for line in sorted(lines, key=lambda item: (item["rect"][1], item["rect"][0])):
        if predicate((line.get("text") or "")):
            return line
    return None


def _find_all_lines(lines: list[dict], predicate) -> list[dict]:
    return [
        line
        for line in sorted(lines, key=lambda item: (item["rect"][1], item["rect"][0]))
        if predicate((line.get("text") or ""))
    ]


def _set_checkbox_option(field: dict, text: str, level: int, parent: str | None, idx: int) -> None:
    field["checkbox_option_text"] = text
    field["checkbox_option_level"] = level
    field["checkbox_option_parent"] = parent
    field["checkbox_option_index"] = idx


def _clear_checkbox_mapping(field: dict) -> None:
    field["label"] = None
    field["label_inferred"] = None
    if field.get("label_source") in {"inferred_page_text", "checkbox_option_row"}:
        field["label_source"] = None
        field["label_confidence"] = 0.0
    field["checkbox_option_text"] = None
    field["checkbox_option_level"] = None
    field["checkbox_option_parent"] = None
    field["checkbox_option_index"] = None


def _cleanup_checkbox_false_short_labels(page_fields: list[dict]) -> None:
    """
    Remove common false-positive checkbox labels caused by OCR/row proximity,
    especially address tokens like 'Piso' and 'Nº' read as 'NO'.
    """
    checks = [f for f in page_fields if f.get("type") in {"CheckBox", "RadioButton"}]
    for field in checks:
        if field.get("normalized_role") in {"sex_option", "marital_status_option"}:
            continue

        label = (field.get("label") or "").strip()
        up = label.upper()

        if up == "PISO":
            _clear_checkbox_mapping(field)
            continue

        if up in {"Nº", "NO", "N."}:
            # Keep explicit yes/no rows only if a nearby checkbox has SI/SÍ label.
            y0, y1 = field["rect"][1], field["rect"][3]
            yc = (y0 + y1) / 2.0
            has_yes_neighbor = False
            for other in checks:
                if other is field:
                    continue
                oy0, oy1 = other["rect"][1], other["rect"][3]
                oyc = (oy0 + oy1) / 2.0
                if abs(oyc - yc) > 12:
                    continue
                olbl = (other.get("label") or "").strip().upper()
                if olbl in {"SI", "SÍ", "SÍ.", "SI."} or olbl.startswith("SÍ ") or olbl.startswith("SI "):
                    has_yes_neighbor = True
                    break
            if not has_yes_neighbor:
                _clear_checkbox_mapping(field)


def _parse_yes_no_question(text: str) -> tuple[bool, str | None]:
    """Detect rows like 'SÍ NO <question>' and return question text."""
    clean = _clean_text(text)
    up = clean.upper().replace("Í", "I")

    if not re.search(r"\bSI\b", up) or not re.search(r"\bNO\b", up):
        return False, None

    # Keep the portion after the first NO token as question text.
    m = re.search(r"\bNO\b\s*(.*)$", clean, flags=re.IGNORECASE)
    question = _clean_text(m.group(1)) if m else ""
    if not question:
        return True, None
    return True, question


def _enrich_yes_no_rows(lines: list[dict], page_fields: list[dict]) -> None:
    """
    Normalize explicit SI/NO rows where two nearby checkboxes represent
    yes/no answers to a trailing question.
    """
    check_fields = [
        f for f in page_fields
        if f.get("type") in {"CheckBox", "RadioButton"}
    ]
    if not check_fields:
        return

    sorted_lines = sorted(lines, key=lambda item: (item["rect"][1], item["rect"][0]))
    consumed_rows: set[int] = set()

    for i, line in enumerate(sorted_lines):
        if i in consumed_rows:
            continue

        lx0, ly0, lx1, ly1 = line["rect"]
        yc = (ly0 + ly1) / 2.0

        # Collect co-linear fragments on the same visual row.
        row = []
        for j, other in enumerate(sorted_lines):
            oy0, oy1 = other["rect"][1], other["rect"][3]
            oyc = (oy0 + oy1) / 2.0
            if abs(oyc - yc) <= 3.0:
                row.append((j, other))
        row.sort(key=lambda t: t[1]["rect"][0])

        row_texts = [(_clean_text(item[1].get("text") or "")) for item in row]
        row_upper = [t.upper().replace("Í", "I") for t in row_texts]

        has_si = any(re.fullmatch(r"S[IÍ]", t, flags=re.IGNORECASE) for t in row_texts)
        has_no = any(re.fullmatch(r"NO", t, flags=re.IGNORECASE) for t in row_texts)

        # Primary form: SI and NO as separate tokens on the same row.
        if has_si and has_no:
            question_parts = [
                t for t in row_texts
                if not re.fullmatch(r"S[IÍ]", t, flags=re.IGNORECASE)
                and not re.fullmatch(r"NO", t, flags=re.IGNORECASE)
            ]
            question = _clean_text(" ".join(question_parts)) or "Sí/No"
            row_x0 = min(item[1]["rect"][0] for item in row)
            row_x1 = max(item[1]["rect"][2] for item in row)
            for idx, _ in row:
                consumed_rows.add(idx)

        else:
            # Secondary form: combined string 'SÍ NO <question>'.
            combined = _clean_text(" ".join(row_texts))
            ok, question = _parse_yes_no_question(combined)
            if not ok:
                continue
            row_x0, row_x1 = lx0, lx1

        candidates = []
        for f in check_fields:
            if f.get("normalized_role") in {"sex_option", "marital_status_option"}:
                continue
            fy0, fy1 = f["rect"][1], f["rect"][3]
            fyc = (fy0 + fy1) / 2.0
            if abs(fyc - yc) > 13:
                continue
            # Keep only row-local boxes close to line start; avoids matching
            # unrelated checkboxes far right on the same page.
            if f["rect"][0] > (row_x0 + 130):
                continue
            candidates.append(f)

        if len(candidates) < 2:
            continue

        candidates.sort(key=lambda item: (item["rect"][0], item["rect"][1]))
        pair = candidates[:2]
        parent = question or "Sí/No"
        values = ["SÍ", "NO"]

        for idx, (field, value) in enumerate(zip(pair, values), start=1):
            field["normalized_group"] = "yes_no_question"
            field["normalized_role"] = "yes_no_option"
            field["normalized_parent_label"] = parent
            field["label"] = f"{parent}: {value}"
            field["label_inferred"] = field["label"]
            field["label_source"] = "yes_no_row_template"
            field["label_confidence"] = 0.99
            _set_checkbox_option(field, value, 1, parent, idx)


def _enrich_identity_rows(lines: list[dict], page_fields: list[dict]) -> None:
    """
    Normalize the recurring personal-identity rows found in most forms:
      - PASAPORTE / N.I.E.
      - Sexo(1) ... H M
      - Estado civil(3) ... S C V D Sp
    """
    if not page_fields:
        return

    # ---- PASAPORTE / N.I.E. segmented row ---------------------------------
    nie_lines = _find_all_lines(lines, lambda text: "N.I.E" in text.upper())
    for nie_line in nie_lines:
        y_center = _row_center_y(nie_line)
        nie_x0 = nie_line["rect"][0]
        row_text_fields = [
            f for f in _fields_near_row(page_fields, y_center, {"Text"}, y_tol=14)
            if not f.get("normalized_role")
        ]
        if len(row_text_fields) >= 3:
            # Typical layout: [passport][nie_part1][nie_part2][nie_part3], where
            # PASAPORTE and N.I.E. captions may appear as separate text lines.
            passport_candidates = [f for f in row_text_fields if f["rect"][2] <= (nie_x0 + 8)]
            passport_field = None
            if passport_candidates:
                passport_field = max(
                    passport_candidates,
                    key=lambda f: (f["rect"][2] - f["rect"][0]),
                )

            if passport_field:
                passport_field["normalized_group"] = "identity_header"
                passport_field["normalized_role"] = "passport_number"
                passport_field["normalized_parent_label"] = "PASAPORTE"
                passport_field["label"] = "PASAPORTE"
                passport_field["label_inferred"] = "PASAPORTE"
                passport_field["label_source"] = "identity_row_template"
                passport_field["label_confidence"] = 0.99

            nie_candidates = [
                f for f in row_text_fields
                if f is not passport_field and f["rect"][0] >= (nie_x0 - 24)
            ]
            nie_candidates.sort(key=lambda f: f["rect"][0])
            for idx, field in enumerate(nie_candidates[:3], start=1):
                label = f"N.I.E. segmento {idx}"
                field["normalized_group"] = "identity_header"
                field["normalized_role"] = f"nie_segment_{idx}"
                field["normalized_parent_label"] = "N.I.E."
                field["label"] = label
                field["label_inferred"] = label
                field["label_source"] = "identity_row_template"
                field["label_confidence"] = 0.99

    # ---- Sexo row ----------------------------------------------------------
    sexo_lines = _find_all_lines(lines, lambda text: "SEXO" in text.upper())
    for sexo_line in sexo_lines:
        y_center = _row_center_y(sexo_line)
        sexo_boxes = [
            f for f in _fields_near_row(page_fields, y_center, {"CheckBox", "RadioButton"}, y_tol=16)
            if not f.get("normalized_role")
        ]
        if len(sexo_boxes) >= 2:
            # In rows combining sexo + estado civil there are typically 8 boxes.
            if len(sexo_boxes) >= 8:
                sexo_boxes = sexo_boxes[:3]
                options = ["X", "H", "M"]
            else:
                options = ["X", "H", "M"] if len(sexo_boxes) >= 3 else ["H", "M"]
            for idx, (field, opt) in enumerate(zip(sexo_boxes, options), start=1):
                field["normalized_group"] = "identity_header"
                field["normalized_role"] = "sex_option"
                field["normalized_parent_label"] = "Sexo"
                field["label"] = f"Sexo: {opt}"
                field["label_inferred"] = field["label"]
                field["label_source"] = "identity_row_template"
                field["label_confidence"] = 0.99
                _set_checkbox_option(field, opt, 1, "Sexo", idx)

    # ---- Estado civil row --------------------------------------------------
    civil_lines = _find_all_lines(lines, lambda text: "ESTADO CIVIL" in text.upper())
    for civil_line in civil_lines:
        y_center = _row_center_y(civil_line)
        civil_boxes = [
            f for f in _fields_near_row(page_fields, y_center, {"CheckBox", "RadioButton"}, y_tol=16)
            if not f.get("normalized_role")
        ]
        if len(civil_boxes) >= 5:
            # If row has both sexo and estado civil, marital options are the right-most 5.
            if len(civil_boxes) >= 8:
                civil_boxes = civil_boxes[-5:]
            options = ["S", "C", "V", "D", "Sp"]
            for idx, (field, opt) in enumerate(zip(civil_boxes, options), start=1):
                field["normalized_group"] = "identity_header"
                field["normalized_role"] = "marital_status_option"
                field["normalized_parent_label"] = "Estado civil"
                field["label"] = f"Estado civil: {opt}"
                field["label_inferred"] = field["label"]
                field["label_source"] = "identity_row_template"
                field["label_confidence"] = 0.99
                _set_checkbox_option(field, opt, 1, "Estado civil", idx)

    _cleanup_checkbox_false_short_labels(page_fields)


def _infer_label(widget_rect: fitz.Rect, lines: list[dict]) -> tuple[str | None, float]:
    """
    Infer semantic label using nearest meaningful text line around the widget.
    Returns (label, confidence in [0, 1]).
    """
    left_row: list[tuple[float, str]] = []
    above_overlap: list[tuple[float, str]] = []
    right_row: list[tuple[float, str]] = []
    nearest: list[tuple[float, str]] = []

    for line in lines:
        lx0, ly0, lx1, ly1 = line["rect"]
        line_rect = fitz.Rect(lx0, ly0, lx1, ly1)
        distance = _rect_distance(widget_rect, line_rect)
        if distance > 95:
            continue

        overlap_x = max(0.0, min(widget_rect.x1, lx1) - max(widget_rect.x0, lx0))
        overlap_y = max(0.0, min(widget_rect.y1, ly1) - max(widget_rect.y0, ly0))
        y_center_delta = abs(((ly0 + ly1) / 2.0) - ((widget_rect.y0 + widget_rect.y1) / 2.0))

        is_left_same_row = lx1 <= widget_rect.x0 + 8 and y_center_delta <= 10
        is_right_same_row = lx0 >= widget_rect.x1 - 4 and y_center_delta <= 10
        x_overlap_ratio = overlap_x / max(1.0, min(widget_rect.width, (lx1 - lx0)))
        is_above_overlap = ly1 <= widget_rect.y0 + 4 and x_overlap_ratio >= 0.20

        if is_left_same_row:
            left_gap = widget_rect.x0 - lx1
            left_row.append((left_gap, line["text"]))
            continue

        if is_above_overlap:
            up_gap = widget_rect.y0 - ly1
            above_overlap.append((up_gap, line["text"]))
            continue

        if is_right_same_row:
            right_gap = lx0 - widget_rect.x1
            right_row.append((right_gap, line["text"]))
            continue

        nearest.append((distance, line["text"]))

    # Priority order tuned for these forms: left row > above overlap > right row > nearest.
    if left_row:
        left_row.sort(key=lambda t: t[0])
        return left_row[0][1], 0.92 if left_row[0][0] <= 35 else 0.76

    if above_overlap:
        above_overlap.sort(key=lambda t: t[0])
        return above_overlap[0][1], 0.84 if above_overlap[0][0] <= 18 else 0.69

    if right_row:
        right_row.sort(key=lambda t: t[0])
        return right_row[0][1], 0.66

    if nearest:
        nearest.sort(key=lambda t: t[0])
        best_dist, text = nearest[0]
        confidence = max(0.15, min(0.52, 1.0 / (1.0 + best_dist)))
        return text, round(confidence, 3)

    return None, 0.0


def _widget_to_dict(
    widget: fitz.Widget,
    page_number: int,
    lines: list[dict],
    sections: list[dict],
) -> dict:
    """Convert a PyMuPDF Widget to a plain dict with all relevant metadata."""
    flags = widget.field_flags or 0
    rect = [round(v, 3) for v in widget.rect]
    pdf_label = widget.field_label or None
    inferred_label, label_confidence = _infer_label(widget.rect, lines)

    if pdf_label:
        final_label = pdf_label
        label_source = "pdf_field_label"
        label_confidence = 1.0
    else:
        final_label = inferred_label
        label_source = "inferred_page_text" if inferred_label else None

    section = _section_for_widget(widget.rect, page_number, sections)

    return {
        "name":          widget.field_name,
        "type":          widget.field_type_string,
        "page":          page_number,
        "rect":          rect,
        "label":         final_label,
        "label_pdf":     pdf_label,
        "label_inferred": inferred_label,
        "label_source":  label_source,
        "label_confidence": label_confidence,
        "default_value": widget.field_value or None,
        "max_length":    widget.text_maxlen if widget.text_maxlen else None,
        "choices":       widget.choice_values or None,
        "on_state":      widget.on_state() if callable(widget.on_state) else widget.on_state,
        "multiline":     bool(flags & FLAG_MULTILINE),
        "required":      bool(flags & FLAG_REQUIRED),
        "read_only":     bool(flags & FLAG_READ_ONLY),
        "text_font":     widget.text_font or None,
        "text_fontsize": widget.text_fontsize or None,
        "has_calc":      bool(widget.script_calc),
        "has_format":    bool(widget.script_format),
        "has_validate":  bool(widget.script_stroke),
        "section_code":  section["code"],
        "section_title": section["title"],
        "section_level": section["level"],
        "checkbox_option_text": None,
        "checkbox_option_level": None,
        "checkbox_option_parent": None,
        "checkbox_option_index": None,
        "normalized_group": None,
        "normalized_role": None,
        "normalized_parent_label": None,
    }


# ---------------------------------------------------------------------------
# Per-form extraction
# ---------------------------------------------------------------------------

def extract_form(pdf_path: Path) -> dict:
    """Open a PDF and return the full form definition as a dict."""
    doc = fitz.open(str(pdf_path))
    filename = pdf_path.name
    form_code = _form_code(filename)

    # PDF title from metadata
    meta = doc.metadata or {}
    title = meta.get("title") or filename
    page_count = doc.page_count  # capture before close

    fields: list[dict] = []
    seen_widget_ids: set[int] = set()

    form_sections: list[dict] = []

    for page in doc:
        page_no = page.number + 1
        lines_all = _build_text_lines(page, include_noise=True)
        lines = _build_text_lines(page, include_noise=False)
        page_sections = _extract_sections(page, lines_all)
        form_sections.extend(page_sections)
        page_fields: list[dict] = []
        for widget in page.widgets():
            # fitz sometimes yields the same widget on adjacent pages; skip dups
            wid = widget.xref
            if wid in seen_widget_ids:
                continue
            seen_widget_ids.add(wid)
            field = _widget_to_dict(widget, page_no, lines, page_sections)
            fields.append(field)
            page_fields.append(field)

        _enrich_checkbox_hierarchy(lines_all, page_sections, page_fields)
        _enrich_yes_no_rows(lines_all, page_fields)
        _enrich_identity_rows(lines_all, page_fields)
        _enrich_signature_footer(lines_all, page_fields)

    doc.close()

    return {
        "form_code":   form_code,
        "filename":    filename,
        "title":       title,
        "page_count":  page_count,
        "field_count": len(fields),
        "sections":    form_sections,
        "fields":      fields,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    DEFINITIONS_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(EDITABLE_DIR.glob("*.pdf"))
    if not pdf_files:
        log.error("No PDF files found in %s", EDITABLE_DIR)
        raise SystemExit(1)

    log.info("Found %d editable PDF(s) in %s", len(pdf_files), EDITABLE_DIR)

    total_fields = 0
    for pdf_path in pdf_files:
        log.info("Extracting: %s", pdf_path.name)
        try:
            form_def = extract_form(pdf_path)
        except Exception as exc:
            log.error("  Failed to process %s: %s", pdf_path.name, exc)
            continue

        json_name = f"{form_def['form_code']}.json"
        json_path = DEFINITIONS_DIR / json_name

        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(form_def, fh, ensure_ascii=False, indent=2)

        log.info(
            "  → %s  (%d fields, %d pages)",
            json_path,
            form_def["field_count"],
            form_def["page_count"],
        )
        total_fields += form_def["field_count"]

    log.info(
        "Done. %d form(s) processed, %d total fields. "
        "Definitions saved to %s/",
        len(pdf_files),
        total_fields,
        DEFINITIONS_DIR,
    )


if __name__ == "__main__":
    main()
