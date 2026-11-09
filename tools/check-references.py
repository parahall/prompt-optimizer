#!/usr/bin/env python3
"""Maintainer check for the skill's reference files. The skill never runs this.

For every provider folder in skills/optimize-prompt/reference/ (anthropic, openai, ...):
1. Every block marked "Quoted from <Provider>" appears word for word in the
   downloaded docs (docs-cache/<provider>/, made by tools/refresh-docs.sh).
   Whitespace and line breaks are ignored, because the docs wrap lines.
2. Every model page in the provider's source list is covered by a model file.
3. Every docs link answers HTTP 200.

Usage: python3 tools/check-references.py [--no-network]
Exit code 1 if any check fails.
"""
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF_ROOT = ROOT / "skills/optimize-prompt/reference"

PROVIDERS = {
    "anthropic": {"name": "Anthropic", "link": r"https://platform\.claude\.com/docs/[^)#\s]+"},
    "openai": {"name": "OpenAI", "link": r"https://developers\.openai\.com/[^)#\s]+"},
}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def quoted_blocks(path: Path, name: str):
    """Yield (line_number, block_text) for each code block right after a 'Quoted from <name>' line."""
    lines = path.read_text().splitlines()
    marker = f"> Quoted from {name}"
    i = 0
    while i < len(lines):
        if lines[i].startswith(marker):
            j = i + 1
            if j >= len(lines) or not lines[j].startswith("```"):
                yield i + 1, ""  # the block must start on the next line; an empty block is reported as missing
                i += 1
                continue
            start = j + 1
            k = start
            while k < len(lines) and not lines[k].startswith("```"):
                k += 1
            yield i + 1, "\n".join(lines[start:k])
            i = k
        i += 1


def check_coverage(provider: str, ref: Path, sources: str) -> int:
    failures = 0
    models_text = "\n".join(p.read_text() for p in (ref / "models").glob("*.md")).lower()
    if provider == "anthropic":
        for slug in re.findall(r"prompting-claude-([a-z0-9-]+)\.md", sources):
            if not (ref / "models" / f"{slug}.md").exists():
                failures += 1
                print(f"MISSING MODEL FILE  anthropic/models/{slug}.md")
        cache = ROOT / "docs-cache/anthropic"
        guide_path = cache / "prompt-engineering_claude-prompting-best-practices.md"  # the name refresh-docs.sh gives the current guide
        if not guide_path.exists():
            print(f"GUIDE NOT DOWNLOADED (run tools/refresh-docs.sh): {guide_path.name}")
            return failures + 1
        guide = guide_path.read_text()
        for slug in sorted(set(re.findall(r"prompting-claude-([a-z0-9-]+)\)", guide))):
            if f"prompting-claude-{slug}.md" not in sources:
                failures += 1
                print(f"GUIDE LISTS A MODEL PAGE NOT IN tools/sources/anthropic.txt: {slug}")
    elif provider == "openai":
        # Every "Using GPT-X" page must map to a model file whose title names that family.
        # Families without their own file belong in legacy.md. A new family in the docs
        # fails this check until it is added here and to a file.
        family_files = {
            "gpt-6-astra": "gpt-6.md",  # the GPT-6 page is named after Astra but covers the family
            "gpt-5.6": "gpt-5-6.md",
            "gpt-5.5": "gpt-5-5.md",
            "gpt-5.4": "gpt-5-4.md",
            "gpt-5.3-codex": "legacy.md",
            "gpt-5.2": "legacy.md",
            "gpt-5.1": "legacy.md",
            "gpt-5": "legacy.md",
            "gpt-4.1": "legacy.md",
        }
        for slug in re.findall(r"/latest-model/([a-z0-9.-]+)\.md", sources):
            if slug not in family_files:
                failures += 1
                print(f"NEW OPENAI FAMILY IN THE SOURCE LIST, NOT MAPPED TO A MODEL FILE: {slug}")
                continue
            path = ref / "models" / family_files[slug]
            family = slug.replace("-astra", "").upper()
            title = path.read_text().splitlines()[0].upper() if path.exists() else ""
            if family not in title:
                failures += 1
                print(f"OPENAI FAMILY {family} NOT NAMED IN THE TITLE OF models/{family_files[slug]}")
        # Every model page on the source list must be named in a reference file, so a new
        # model added to the list fails until the skill covers it.
        known = (models_text + (ref / "api-settings.md").read_text()).lower()
        for model_id in re.findall(r"/models/([a-z0-9.-]+)\.md", sources):
            if model_id not in known:
                failures += 1
                print(f"OPENAI MODEL {model_id} IS ON THE SOURCE LIST BUT NOT NAMED IN ANY REFERENCE FILE")
    return failures


def cache_corpus(provider: str, sources: str) -> str:
    """Text of the cached pages that are on the current source list only, so pages
    dropped from the list (or left over from an older naming scheme) cannot vouch for a quote."""
    cache = ROOT / "docs-cache" / provider
    texts, missing = [], 0
    for url in re.findall(r"^\s*(https://\S+)", sources, re.M):
        parts = url.rstrip("/").split("/")
        path = cache / f"{parts[-2]}_{parts[-1]}"
        if path.exists():
            texts.append(path.read_text())
        else:
            missing += 1
            print(f"NOT DOWNLOADED (run tools/refresh-docs.sh): {url}")
    return norm("\n".join(texts)), missing


def main() -> int:
    failures = 0
    network = "--no-network" not in sys.argv
    for provider, info in PROVIDERS.items():
        ref = REF_ROOT / provider
        if not ref.exists():
            continue
        cache = ROOT / "docs-cache" / provider
        if not cache.exists():
            print(f"docs-cache/{provider} is missing; run tools/refresh-docs.sh first")
            return 1
        sources = (ROOT / f"tools/sources/{provider}.txt").read_text()
        corpus, missing = cache_corpus(provider, sources)
        failures += missing

        count = 0
        for path in sorted(ref.rglob("*.md")):
            for line, block in quoted_blocks(path, info["name"]):
                count += 1
                if not norm(block) or norm(block) not in corpus:  # an empty block means the code fence is missing
                    failures += 1
                    print(f"QUOTE NOT FOUND  {path.relative_to(ROOT)}:{line}  {norm(block)[:80]}...")
        print(f"{provider}: checked {count} quoted blocks")

        failures += check_coverage(provider, ref, sources)

        if network:
            links = set()
            for path in ref.rglob("*.md"):
                links |= set(re.findall(r"\((" + info["link"] + r")", path.read_text()))
            for url in sorted(links):
                target = url if url.endswith(".md") else url + ".md"
                try:
                    req = urllib.request.Request(target, headers={"User-Agent": "prompt-optimizer-link-check"})
                    with urllib.request.urlopen(req, timeout=20) as r:
                        ok = r.status == 200
                except Exception:
                    ok = False
                if not ok:
                    failures += 1
                    print(f"BROKEN LINK  {url}")
            print(f"{provider}: checked {len(links)} links")

    print("OK" if failures == 0 else f"{failures} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
