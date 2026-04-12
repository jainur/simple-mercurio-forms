# Simple Mercurio Forms — Python API Service

FastAPI backend for downloading Spanish immigration form PDFs, extracting field definitions, modeling domain payloads, mapping domain models to PDF widgets, and generating filled forms.

## Setup

```bash
# from services/es-immigration-forms/
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn main:app --reload
```

Key endpoints:

- `/docs`
- `/api/v1/forms`
- `/api/v1/forms/{formCode}/fields`
- `/api/v1/forms/{formCode}/validate`
- `/api/v1/forms/{formCode}/fill`
- `/api/v1/forms/{formCode}/fill-from-model`

## Core Workflow

1. Download forms

```bash
python scripts/downloader.py
```

2. Extract field definitions

```bash
python scripts/extract_fields.py
```

3. Import definitions to SQLite

```bash
python scripts/import_to_db.py
```

4. Fill from JSON input

```bash
python scripts/fill_form.py --form EX11 --input examples/ex11-input.json
```

5. Fill from domain model

```bash
python examples/ex11_domain_example.py
```

## Canonical-v3 Smoke Generators

- `examples/smoke_ex00_ex10_canonical_v3.py`
- `examples/smoke_ex01_ex30_canonical_v3.py`

These scripts generate review outputs under `data/forms/filled/canonical-v3/`.

## Project Structure

```
services/es-immigration-forms/
├── main.py                    # Entry point: uvicorn main:app --reload
├── app/
│   ├── api/                   # FastAPI application
│   │   ├── main.py            # FastAPI app initialization & middleware
│   │   ├── routers/           # API endpoints
│   │   ├── schemas/           # Pydantic request/response models
│   │   ├── services/          # Business logic (catalog, fill, validation)
│   │   └── security/          # Authentication & authorization
│   ├── models/                # Per-form domain schemas + shared canonical sections/enums
│   └── mappers/               # Per-form model-to-widget mappers + helpers
├── scripts/                   # CLI utilities for form processing
│   ├── downloader.py
│   ├── extract_fields.py
│   ├── import_to_db.py
│   └── forms_registry.py
├── data/
│   └── forms/
│       ├── definitions/       # Extracted widget metadata (JSON, committed)
│       ├── editable/          # Downloaded editable PDFs
│       ├── non-editable/      # Downloaded non-editable PDFs
│       └── filled/            # Generated output PDFs (gitignored)
├── examples/                  # Sample inputs and domain-example scripts
├── tests/                     # pytest suite
├── forms.db                   # SQLite metadata store
├── pytest.ini
├── requirements.txt
└── requirements-dev.txt
```

## Notes

- All commands must be run from `services/es-immigration-forms/` (module imports are resolved relative to that directory).
- Filled PDFs are gitignored under `services/es-immigration-forms/data/forms/filled/`.
- Some form numbers are intentionally absent by official numbering (e.g. EX05, EX08, EX12, EX14, EX15, EX27).

