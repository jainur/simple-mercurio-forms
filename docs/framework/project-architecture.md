# Project Architecture Reference

This document explains the core technical components of the repository and how they fit together end to end.

Scope covered:
- Downloader
- Field extractor
- SQLite schema
- Canonical and form models
- Mappers

---

## 1) Downloader

Implementation: downloader.py

### Purpose
The downloader fetches official Spanish immigration form PDFs from the public migration forms page and separates them into editable and non-editable sets.

- Source page: https://www.inclusion.gob.es/en/web/migraciones/modelos-generales
- Editable output directory: forms/editable
- Non-editable output directory: forms/non-editable

### How it works
1. Builds an HTTP session with browser-like headers.
2. Fetches the forms index page.
3. Parses links and keeps only migraciones document URLs.
4. Classifies each link as editable or non-editable.
5. Downloads each PDF with polite delay and collision-safe filenames.

### Notable design decisions
- Domain-specific SSL handling:
  - Certificate verification is disabled for this endpoint because the site uses a CA not present in default trust bundles.
  - This is intentionally scoped to the known government domain and clearly logged.
- Link deduplication:
  - The same URL is downloaded only once.
- Editable classification strategy:
  - Checks for the word editable in URL and surrounding text context, not only anchor text.
- Filename resolution:
  - Uses Content-Disposition first (including RFC 5987 filename*), then final URL path fallback.
  - Adds a numeric suffix on collisions.

### Operational notes
- This script is network-dependent.
- If the source page HTML changes significantly, link detection logic may need updates.

---

## 2) Field Extractor

Implementation: extract_fields.py

### Purpose
The extractor reads every editable PDF and creates normalized JSON form definitions in forms/definitions. These definitions are the canonical source for widget names, geometry, labels, section metadata, and semantic hints.

### Output shape
One JSON file per form, typically EXNN.json, containing:
- Form metadata (form code, filename, page count, field count)
- Field records with widget attributes such as:
  - name, type, page, rect
  - label and default value
  - choice/on-state data for list or checkbox widgets
  - text limits and style flags
  - inferred section and semantic classification metadata

### Extraction strategy
The extractor combines multiple signals:
1. Native PDF text extraction via PyMuPDF words/blocks.
2. OCR fallback via RapidOCR when native text is too sparse.
3. Post-processing to recover labels from dotted leader lines.
4. Checkbox/radio option parsing and hierarchy inference.
5. Section heading inference with patterns like 1) and 2.1.
6. Role normalization for downstream semantic matching.

### Why this matters
- Mapper code can stay stable against PDF UI wording differences because it targets widget names.
- Semantic filling can match normalized groups/roles (via fill_form.py selectors).
- Database import can index rich metadata for analysis and tooling.

### Operational notes
- OCR dependencies are optional; extractor degrades gracefully when unavailable.
- OCR improves extraction quality on low-text or difficult PDFs but adds runtime cost.

---

## 3) SQLite Database Schema

Implementation: import_to_db.py
Database file: forms.db

### Purpose
Imports JSON definitions into a relational schema for querying, analytics, audits, and tooling support.

### Tables

#### forms
Stores one row per form.

Columns:
- id (PK)
- form_code (unique)
- filename
- title
- page_count
- field_count

#### form_fields
Stores one row per widget field.

Core columns:
- id (PK)
- form_id (FK to forms.id)
- name
- type
- page
- rect_x0, rect_y0, rect_x1, rect_y1
- label
- default_value
- max_length
- choices (JSON text)
- on_state
- multiline, required, read_only
- text_font, text_fontsize
- has_calc, has_format, has_validate

Extended normalization columns:
- label_pdf
- label_inferred
- label_source
- label_confidence
- section_code
- section_title
- section_level
- checkbox_option_text
- checkbox_option_level
- checkbox_option_parent
- checkbox_option_index
- normalized_group
- normalized_role
- normalized_parent_label

### Import behavior
- Upserts form rows by form_code.
- Replaces all form_fields for that form on each import.
- Uses WAL mode and foreign keys.
- Includes migration-safe column backfill for older DB files.

### Useful query examples
- Count widgets by type per form.
- Find all checkbox groups with normalized_role.
- Identify missing labels or low-confidence inferred labels.

---

## 4) Canonical and Form Models

Primary model locations:
- models/common_sections.py
- models/shared_enums.py
- models/shared_request_enums.py
- models/exNN.py files

### Canonical model layer
The project has a shared canonical layer used by many form-specific schemas.

#### Shared identity/contact section bases
In models/common_sections.py, reusable generic bases define the recurring applicant/foreigner blocks:
- Core identity fields (passport/NIE, name, birth data, nationality)
- Address and contact fields
- Optional legal guardian/legal representative variants
- Optional children-related variants

This reduces drift across EX models and enforces consistent field semantics.

#### Shared enums
In models/shared_enums.py:
- GenderEnum with canonical values X/H/M
- MaritalStatusEnum with canonical values S/C/V/D/Sp

In models/shared_request_enums.py:
- Shared request-category style enums used by multiple forms.

### Form-specific model layer
Each form still has a dedicated root schema in models/exNN.py.

Typical pattern:
- EXNNFormSchema root object
- Section-specific nested objects for foreigner/applicant, request details, office, signature, etc.
- Form-specific enums where domain values are unique to that form

### Modeling intent
- Shared pieces capture cross-form invariants.
- Per-form models preserve official form-specific semantics.
- The mapper layer then converts model semantics to PDF widget key-value payloads.

---

## 5) Mappers

Primary locations:
- mappers/exNN.py files
- mappers/helpers.py
- forms_registry.py

### Purpose
Each mapper converts a domain model instance into field_values: a flat dictionary keyed by PDF widget name.

Example contract:
- Input: EXNNFormSchema instance
- Output: dict where keys are PDF widget names and values are strings or booleans

### Shared helper strategy
mappers/helpers.py contains canonical helper primitives used across forms:
- coerce_str: None to empty string normalization
- split_nie: NIE segment splitting for multi-box fields
- normalize_enum_semantic and apply_enum_registry:
  - semantic enum normalization
  - compact registry-driven checkbox mapping
- map_identity_person_block:
  - standard person block mapping (identity, dates, gender, marital)
- map_optional_object_fields:
  - optional section mapping to text widgets
- map_notification_block:
  - notification fields and optional consent checkbox

### Mapper registry
forms_registry.py resolves:
- model module name to form code
- form code to mapper function

This allows fill_form_from_model in fill_form.py to dynamically route any EXNN model instance to the correct mapper.

### Current design benefits
- Large duplication reduction across mappers.
- Consistent enum checkbox behavior via normalized registries.
- Easier audits and safer refactoring (widget keys remain explicit in mappers).

---

## End-to-End Flow Summary

1. downloader.py fetches source PDFs.
2. extract_fields.py builds JSON field definitions from editable PDFs.
3. import_to_db.py loads definitions into forms.db.
4. models/exNN.py defines the form domain payload.
5. mappers/exNN.py converts domain model to widget field_values.
6. fill_form.py writes values into widgets and saves filled PDFs.

---

## Practical Extension Guidance

When adding or refactoring a form:
1. Confirm its definition exists in forms/definitions.
2. Create or update models/exNN.py using shared bases/enums when applicable.
3. Implement mapper in mappers/exNN.py using helper functions first, custom logic second.
4. Ensure forms_registry.py includes the form code.
5. Run smoke generation scripts and verify:
   - no missing mapper keys
   - no unexpected extra keys
   - no blank review fields (for canonical-v3 outputs)
