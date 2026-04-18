# Form Filling Framework

## Goal
Generate a filled editable PDF locally from:
- form code (for example `EX11`)
- input values (JSON payload)

The script picks the editable source PDF from `forms/editable/`, applies values, and writes the filled file into `forms/filled/` by default.

## CLI

```bash
python fill_form.py --form EX11 --input examples/ex11-input.json
```

Optional output path:

```bash
python fill_form.py --form EX11 --input examples/ex11-input.json --output forms/filled/EX11-demo.pdf
```

## Input Payload

The payload supports two assignment modes.

1. `field_values`: direct assignment by PDF field name.
2. `semantic_values`: assignment by extracted metadata selectors.

Example:

```json
{
  "field_values": {
    "Texto5": "GARCIA",
    "Texto6": "MARTIN"
  },
  "semantic_values": [
    {
      "selector": { "normalized_role": "passport_number" },
      "value": "P1234567"
    },
    {
      "selector": {
        "normalized_group": "identity_header",
        "normalized_role": "sex_option"
      },
      "value": "M"
    },
    {
      "selector": {
        "normalized_group": "yes_no_question",
        "normalized_parent_label_contains": "Hijas/os"
      },
      "value": "NO"
    }
  ]
}
```

## Selector Rules

`semantic_values[].selector` matches any field whose metadata satisfies all selector keys.

Supported selector styles:
- exact: `"normalized_role": "passport_number"`
- substring: `"normalized_parent_label_contains": "Hijas/os"`

You can use any extracted metadata key as a selector key, including:
- `name`, `type`, `page`
- `section_code`, `section_title`
- `label`, `label_source`
- `normalized_group`, `normalized_role`, `normalized_parent_label`
- `checkbox_option_text`, `checkbox_option_parent`, `checkbox_option_level`

## Value Behavior

- Text-like fields (`Text`, `ComboBox`, `ListBox`): value is written as string.
- Checkbox/radio fields:
  - boolean value: applies directly (`true` checks, `false` unchecks).
  - string value: treated as option token for matched checkbox groups (for example `"M"`, `"NO"`).
  - list of strings: multi-select for matched checkbox fields.

## Output

When `--output` is omitted:
- Output folder: `forms/filled/`
- Filename format: `<FORM>-filled-YYYYMMDD-HHMMSS.pdf`

## Notes

- Requires existing definition JSON in `forms/definitions/<FORM>.json`.
- Requires editable source PDF in `forms/editable/`.
- The script logs unmatched direct fields and selectors that resolve to zero fields.
