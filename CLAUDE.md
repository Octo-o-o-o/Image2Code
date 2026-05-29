# Claude Code Notes

Use this repository as a Claude Code skill source.

- The skill entrypoint is [`image2code/SKILL.md`](./image2code/SKILL.md).
- Install by copying [`image2code/`](./image2code/) to `~/.claude/skills/image2code`.
- When asked to use Image2Code, follow the decision tree in `SKILL.md` first, then load only the needed files from `references/`.
- Use the scripts in `image2code/scripts/` instead of recreating pack scaffolding or manifest logic by hand.
- Run `python3 tools/validate_skill.py` before committing or publishing skill changes.
