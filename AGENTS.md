# AGENTS

## Start Here

- Read [`image2code/SKILL.md`](./image2code/SKILL.md) before changing the skill behavior.
- Keep the skill folder itself lean: `SKILL.md`, `agents/`, `references/`, and `scripts/`.
- Human-facing setup notes belong in [`README.md`](./README.md), not inside the skill folder.

## Validation

Before committing changes, run:

```bash
python3 tools/validate_skill.py
```

The validation must pass before pushing.
