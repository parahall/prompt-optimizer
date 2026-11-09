#!/usr/bin/env bash
# Downloads the documentation pages the skill's reference files are based on,
# and shows what changed since the last download. For maintainers only; the
# skill itself never runs this.
#
# Usage: tools/refresh-docs.sh [provider]     (default: all providers)
# Pages are saved in docs-cache/<provider>/ (ignored by git). The previous copy
# of each page is kept as <page>.prev so the diff can be shown.
# Exits with status 1 if any page failed to download.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
providers=("$@")
if [ ${#providers[@]} -eq 0 ]; then
  providers=()
  for f in "$root"/tools/sources/*.txt; do providers+=("$(basename "$f" .txt)"); done
fi

failed=0
for provider in "${providers[@]}"; do
  list="$root/tools/sources/$provider.txt"
  [ -f "$list" ] || { echo "No source list: $list" >&2; exit 1; }
  # Read the list here, not in the loop's input, so a read failure stops the script.
  urls="$(grep -vE '^\s*(#|$)' "$list")" || { echo "Cannot read URLs from: $list" >&2; exit 1; }
  dir="$root/docs-cache/$provider"
  mkdir -p "$dir"
  while read -r url; do
    # Name by the last two path parts, so pages with the same final name do not collide.
    name="$(basename "$(dirname "$url")")_$(basename "$url")"
    tmp="$(mktemp)"
    if ! curl -fsSL "$url" -o "$tmp"; then
      echo "FAILED  $url"; rm -f "$tmp"; failed=$((failed + 1)); continue
    fi
    if [ ! -f "$dir/$name" ]; then
      mv "$tmp" "$dir/$name"; echo "NEW     $provider/$name"
    elif cmp -s "$tmp" "$dir/$name"; then
      rm -f "$tmp"; echo "same    $provider/$name"
    else
      mv "$dir/$name" "$dir/$name.prev"; mv "$tmp" "$dir/$name"
      echo "CHANGED $provider/$name"
      diff -u "$dir/$name.prev" "$dir/$name" | head -200 || true
    fi
  done <<< "$urls"
done

if [ "$failed" -gt 0 ]; then
  echo "$failed page(s) failed to download; docs-cache may be out of date." >&2
  exit 1
fi
