#!/usr/bin/env python3
"""Validate internal links/assets and sitemap in a built MkDocs site."""
from __future__ import annotations

import argparse
import gzip
import html.parser
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

SKIP_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data"}


class ReferenceParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"a", "link"} and values.get("href"):
            self.references.append((tag, values["href"] or ""))
        if tag in {"script", "img", "iframe", "source"} and values.get("src"):
            self.references.append((tag, values["src"] or ""))


def resolve(site: Path, page: Path, reference: str) -> Path | None:
    parsed = urllib.parse.urlsplit(reference)
    if parsed.scheme.lower() in SKIP_SCHEMES or parsed.netloc:
        return None
    raw = urllib.parse.unquote(parsed.path)
    if not raw:
        return None
    target = site / raw.lstrip("/") if raw.startswith("/") else page.parent / raw
    target = target.resolve()
    try:
        target.relative_to(site.resolve())
    except ValueError:
        return target
    if target.is_dir():
        target = target / "index.html"
    elif not target.exists() and target.suffix == "":
        directory_index = target / "index.html"
        html_file = target.with_suffix(".html")
        if directory_index.exists():
            target = directory_index
        elif html_file.exists():
            target = html_file
    return target


def validate_sitemap(site: Path) -> list[str]:
    sitemap = site / "sitemap.xml"
    compressed = site / "sitemap.xml.gz"
    if sitemap.exists():
        payload = sitemap.read_bytes()
    elif compressed.exists():
        with gzip.open(compressed, "rb") as handle:
            payload = handle.read()
    else:
        return ["sitemap.xml(.gz) missing"]
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        return [f"sitemap parse error: {exc}"]
    urls = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
    if not urls:
        return ["sitemap contains zero URLs"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", default="site")
    args = parser.parse_args()
    site = Path(args.site).resolve()
    failures: list[str] = []
    for page in sorted(site.rglob("*.html")):
        parser_html = ReferenceParser()
        parser_html.feed(page.read_text(encoding="utf-8", errors="replace"))
        for tag, reference in parser_html.references:
            target = resolve(site, page, reference)
            if target is not None and not target.exists():
                failures.append(f"{page.relative_to(site)}: <{tag}> {reference} -> missing {target}")
    failures.extend(validate_sitemap(site))
    if failures:
        print("Published-site integrity validation failed:")
        for failure in failures:
            print(f" - {failure}")
        return 1
    html_count = sum(1 for _ in site.rglob("*.html"))
    print(f"Published-site integrity OK: {html_count} HTML pages, internal references resolved, sitemap populated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
