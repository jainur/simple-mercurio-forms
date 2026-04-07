# Simple Mercurio Forms

Toolkit for downloading Spanish immigration form PDFs, extracting field definitions, modeling domain payloads, mapping domain models to PDF widgets, and generating filled forms.

## Documentation Index

- Framework overview: [docs/framework/project-architecture.md](docs/framework/project-architecture.md)
- Form filling details: [docs/framework/form-filling.md](docs/framework/form-filling.md)

## Repository Structure

- `downloader.py`:
  Downloads official form PDFs into editable and non-editable folders.
- `extract_fields.py`:
  Extracts widget metadata from editable PDFs and writes JSON definitions in `forms/definitions`.
- `import_to_db.py`:
  Imports JSON definitions into `forms.db` (SQLite).
- `fill_form.py`:
  Fills editable PDFs from either raw payloads or domain models.
- `forms_registry.py`:
  Resolves model module -> form code -> mapper function.
- `models/`:
  Per-form domain schemas plus shared canonical section/enums.
- `mappers/`:
  Per-form model-to-widget mappers and shared helper utilities.
- `examples/`:
  Sample inputs and domain-example scripts for each available EX form.
- `docs/framework/`:
  Technical framework documentation.

## Core Workflow

1. Download forms

```bash
python downloader.py
```

2. Extract field definitions

```bash
python extract_fields.py
```

3. Import definitions to SQLite

```bash
python import_to_db.py
```

4. Fill from JSON input

```bash
python fill_form.py --form EX11 --input examples/ex11-input.json
```

5. Fill from domain model

```bash
python examples/ex11_domain_example.py
```

## Canonical-v3 Smoke Generators

- `examples/smoke_ex00_ex10_canonical_v3.py`
- `examples/smoke_ex01_ex30_canonical_v3.py`

These scripts generate review outputs under:

- `forms/filled/canonical-v3/`

They validate mapper coverage and support no-blank review outputs for available forms.

## Notes

- Filled PDFs are ignored via `.gitignore` (`forms/filled/`).
- Some forms are intentionally absent by official numbering (for example EX05, EX08, EX12, EX14, EX15, EX27 in this workspace).
