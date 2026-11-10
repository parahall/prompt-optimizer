#!/usr/bin/env bash
# Builds dist/optimize-prompt.zip for uploading the skill in the Claude app
# (Customize > Skills > + > Create skill > Upload a skill). For maintainers.
#
# The ZIP holds the optimize-prompt/ folder at its top, as the Claude app expects.
# Its SKILL.md drops the Claude Code-only "argument-hint" field, which the Claude
# app's skill format does not allow. The skill in the repo is not changed.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

cp -R "$root/skills/optimize-prompt" "$work/optimize-prompt"
grep -v '^argument-hint:' "$root/skills/optimize-prompt/SKILL.md" > "$work/optimize-prompt/SKILL.md"
find "$work" -name '.DS_Store' -delete

mkdir -p "$root/dist"
rm -f "$root/dist/optimize-prompt.zip"
(cd "$work" && zip -qr "$root/dist/optimize-prompt.zip" optimize-prompt)
echo "Built dist/optimize-prompt.zip"
