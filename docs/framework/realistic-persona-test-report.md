# Realistic Persona Test Report

## Goal
Use realistic, diverse test data for form-filling validation with variation in:
- countries and nationalities
- adult and child applicants
- civil status
- gender
- with and without representation

This run uses a multi-scenario matrix per form, not a single persona.

## Execution
- Runner: examples/test_realistic_personas.py
- Command: .venv/bin/python examples/test_realistic_personas.py --scenarios-per-form 4
- Output PDFs: forms/filled/realistic-personas/
- Machine-readable report: docs/framework/realistic-persona-test-report.json

## Diversity Coverage Achieved
- Forms tested: 25
- Total scenarios executed: 100
- Scenarios per form: 4
- Countries covered: Argentina, Colombia, Marruecos, Peru, Reino Unido, Senegal
- Genders covered: MALE, FEMALE, OTHER
- Civil status covered: SINGLE, MARRIED, DIVORCED, WIDOWED, SEPARATED
- Age groups covered: adult, child
- Representation split:
  - with representation: 50
  - without representation: 50

Per-form matrix coverage:
- Forms with both adult and child scenarios: 25/25
- Forms with both with/without representation scenarios: 25/25
- Forms with 4 scenarios completed: 25/25

## Quality Observations
- Execution failures: 0
- Forms with blank text fields: 25
- Total blank text values: 1090

Interpretation:
- Diversity objective is met.
- Blank text values remain high in realistic mode because this run intentionally avoids placeholder backfill and uses semantically realistic conditional data (for example, no representative when not applicable).

## Recommendation
Use this realistic suite together with reviewer-mode suite:
1. Realistic suite (this report) for scenario fidelity and demographic coverage.
2. Reviewer-mode suite for visually complete PDFs with no blank text fields.
