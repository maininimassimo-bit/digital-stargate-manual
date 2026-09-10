#!/usr/bin/env python3
"""Regression coverage for the homepage runtime-projection shell contract."""
from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "homepage" / "refresh_homepage.py"
spec = importlib.util.spec_from_file_location("refresh_homepage", MODULE_PATH)
assert spec and spec.loader
homepage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(homepage)


def sample_block(detail: str = "Projection scientifica non ancora disponibile") -> str:
    return f'''{homepage.START_MARKER}
<section data-dsg-home-snapshot>
  <span data-home-freshness>Caricamento projection…</span>
  <strong data-home-current-package>—</strong>
  <p data-home-current-detail>Stato roadmap non ancora disponibile</p>
  <strong data-home-latest-session>—</strong>
  <p data-home-latest-detail>{detail}</p>
  <a data-home-latest-link href="./scientific-session-catalog/">Dettaglio</a>
  <strong data-home-session-count>—</strong>
  <p data-home-session-totals>Conteggi non ancora disponibili</p>
</section>
{homepage.END_MARKER}'''


def test_dynamic_shell_accepts_complete_fail_closed_contract() -> None:
    homepage.validate_dynamic_shell(sample_block())


def test_dynamic_shell_rejects_missing_binding() -> None:
    content = sample_block().replace("data-home-session-count", "data-missing-session-count")
    try:
        homepage.validate_dynamic_shell(content)
    except RuntimeError as error:
        assert "data-home-session-count" in str(error)
    else:
        raise AssertionError("Missing homepage binding was accepted")


def test_dynamic_shell_rejects_known_stale_fallback() -> None:
    try:
        homepage.validate_dynamic_shell(sample_block("AP-013 in corso · 31,83 h"))
    except RuntimeError as error:
        assert "stale fallback" in str(error)
    else:
        raise AssertionError("Stale homepage fallback was accepted")


def test_repository_homepage_matches_contract() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    homepage.validate_dynamic_shell((repo_root / "docs" / "index.md").read_text(encoding="utf-8"))
    consumer = (repo_root / "docs" / "javascripts" / "homepage-effects.js").read_text(encoding="utf-8")
    assert "data/roadmap.json" in consumer
    assert "data/scientific-session-catalog.json" in consumer
    assert "data/realtime/latest-observation.json" in consumer
    assert "cache: 'no-store'" in consumer


if __name__ == "__main__":
    test_dynamic_shell_accepts_complete_fail_closed_contract()
    test_dynamic_shell_rejects_missing_binding()
    test_dynamic_shell_rejects_known_stale_fallback()
    test_repository_homepage_matches_contract()
    print("Homepage runtime-projection shell regression tests PASS")
