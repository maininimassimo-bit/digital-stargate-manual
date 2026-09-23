"""Allowlisted, privacy-minimized retrieval over published DSG projections."""

from __future__ import annotations

import json
import hashlib
import re
import urllib.error
import urllib.request
from typing import Any


BASE = "https://maininimassimo-bit.github.io/digital-stargate-manual/"
METHOD_VERSION = "bkl042-static-projection-retrieval-v1"
SOURCES = {
    "observation-index": "docs/data/scientific-observation-index.json",
    "target-read-model": "docs/data/target-knowledge-read-model.json",
    "session-catalog": "docs/data/scientific-session-catalog.json",
}
MAX_SOURCE_BYTES = 1_000_000
MAX_RESULTS = 5
MAX_EVIDENCE_CHARS = 12000
TOKEN_RE = re.compile(r"[\w-]+", re.UNICODE)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _get_json(path: str) -> dict[str, Any]:
    public_url = BASE + path.removeprefix("docs/")
    request = urllib.request.Request(public_url, headers={"Accept": "application/json"})
    try:
        opener = urllib.request.build_opener(_NoRedirect)
        with opener.open(request, timeout=5) as response:
            if response.status != 200 or response.geturl() != public_url:
                raise RuntimeError("SOURCE_UNAVAILABLE")
            if response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
                raise RuntimeError("SOURCE_INVALID")
            if int(response.headers.get("Content-Length", "0") or 0) > MAX_SOURCE_BYTES:
                raise RuntimeError("SOURCE_TOO_LARGE")
            raw = response.read(MAX_SOURCE_BYTES + 1)
        if len(raw) > MAX_SOURCE_BYTES:
            raise RuntimeError("SOURCE_TOO_LARGE")
        result = json.loads(raw.decode("utf-8"))
        if not isinstance(result, dict):
            raise RuntimeError("SOURCE_INVALID")
        result["_retrieval_sha256"] = "sha256:" + hashlib.sha256(raw).hexdigest()
        return result
    except (urllib.error.URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("SOURCE_UNAVAILABLE") from exc


def _terms(value: str) -> set[str]:
    return {part.casefold() for part in TOKEN_RE.findall(value) if len(part) > 1}


def _safe_url(path: Any) -> str:
    if not isinstance(path, str):
        return ""
    if path.startswith("scientific-session-detail/?sessionId="):
        session_id = path.partition("=")[2]
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}", session_id):
            return BASE + path
    if path in {"scientific-session-catalog/", "scientific-platform-intelligence/"}:
        return BASE + path
    return ""


def _record(source_id: str, ref: str, title: str, summary: str, url: str, digest: str, freshness: str, authority: str, conflict: bool = False) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "ref": ref,
        "title": title[:180],
        "summary": summary[:700],
        "url": url,
        "digest": digest[:80],
        "freshness": freshness,
        "authority": authority,
        "conflict": conflict,
    }


def retrieve(question: str, fetch=_get_json) -> dict[str, Any]:
    """Return ranked, field-allowlisted source records; fail closed on any missing source."""
    qterms = _terms(question)
    if not qterms:
        return {"state": "INSUFFICIENT_EVIDENCE", "records": [], "sources": [], "method_version": METHOD_VERSION}
    docs: list[dict[str, str]] = []
    source_meta: list[dict[str, str]] = []
    source_data = {source_id: fetch(path) for source_id, path in SOURCES.items()}
    required_lists = {
        "observation-index": ("catalogItems", "searchDocuments"),
        "target-read-model": ("targets",),
        "session-catalog": ("sessions",),
    }
    for source_id, keys in required_lists.items():
        if any(not isinstance(source_data[source_id].get(key), list) for key in keys):
            raise RuntimeError("SOURCE_INVALID")
    for source_id, path in SOURCES.items():
        data = source_data[source_id]
        source_digest = str(data.get("_retrieval_sha256", ""))[:80]
        source_meta.append({"source_id": source_id, "path": path, "status": "AVAILABLE", "digest": source_digest})
        if source_id == "observation-index":
            catalog_items = data.get("catalogItems", [])
            item_by_id = {item.get("catalogItemId"): item for item in catalog_items[:100] if isinstance(item, dict)} if isinstance(catalog_items, list) else {}
            search_terms: dict[str, str] = {}
            entries = data.get("searchDocuments", [])
            for entry in entries[:100] if isinstance(entries, list) else []:
                if not isinstance(entry, dict):
                    continue
                item = item_by_id.get(entry.get("catalogItemId"), {})
                entity_id = item.get("entityId") if isinstance(item, dict) else None
                if not isinstance(entity_id, str):
                    continue
                title = str(entry.get("title", ""))
                keywords = entry.get("keywords", [])
                search_terms[entity_id] = title + " " + " ".join(str(k) for k in keywords[:30] if isinstance(k, str)) if isinstance(keywords, list) else title
            # Index text influences recall only; it is never sent as factual evidence.
            source_data["_search_terms"] = search_terms
        elif source_id == "target-read-model":
            entries = data.get("targets", [])
            for entry in entries[:20] if isinstance(entries, list) else []:
                if not isinstance(entry, dict):
                    continue
                # Never forward internal target keys, identifiers, coordinates, or provenance refs.
                title = str(entry.get("canonical_name", ""))[:160]
                aliases = entry.get("aliases", [])
                identity = str(entry.get("identity_state", "UNKNOWN"))
                if identity not in {"validated", "candidate", "conflicted", "unknown"}:
                    identity = "UNKNOWN"
                conflicts = entry.get("conflict_refs", [])
                conflict = identity == "conflicted" or (isinstance(conflicts, list) and bool(conflicts))
                summary = "Target: " + title + "; identity state: " + identity + ("; conflict requires review" if conflict else "")
                if isinstance(aliases, list):
                    summary += "; aliases: " + ", ".join(str(item)[:100] for item in aliases[:10] if isinstance(item, str))
                docs.append(_record(source_id, title, title, summary, BASE + "scientific-platform-intelligence/", source_digest, "VERSIONED_PROJECTION", "IDENTITY_PROJECTION", conflict))
        else:
            entries = data.get("sessions", [])
            for entry in entries[:100] if isinstance(entries, list) else []:
                if not isinstance(entry, dict):
                    continue
                # Allowlist excludes RA/Dec, paths, equipment serials, and detailed telemetry.
                fields = ("observationDate", "target", "analyticsState", "metadataState", "evidenceState", "integrationHours", "completionPct", "severity")
                selected = {key: entry[key] for key in fields if key in entry and isinstance(entry[key], (str, int, float))}
                session_id = str(entry.get("sessionId", ""))
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}", session_id):
                    continue
                title = "Session " + str(selected.get("observationDate", "unknown")) + " · " + str(selected.get("target", "unknown target"))
                summary = "; ".join(f"{key}: {value}" for key, value in selected.items())
                url = _safe_url("scientific-session-detail/?sessionId=" + session_id) or BASE + "scientific-session-catalog/"
                docs.append(_record(source_id, session_id, title, summary, url, source_digest, "HISTORICAL_PROJECTION", "PRIMARY_SESSION_PROJECTION"))
    ranked = []
    for doc in docs:
        discovery = source_data.get("_search_terms", {}).get(doc["ref"], "") if doc["source_id"] == "session-catalog" else ""
        matched = len(qterms & _terms(doc["title"] + " " + doc["summary"] + " " + discovery))
        if matched:
            ranked.append((matched / len(qterms), doc))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["source_id"], pair[1]["ref"]))
    records = [doc for score, doc in ranked[:MAX_RESULTS] if score > 0]
    evidence = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    if len(evidence) > MAX_EVIDENCE_CHARS:
        records = records[:2]
    state = "CONFLICT_REQUIRES_REVIEW" if any(record["conflict"] for record in records) else "EVIDENCE_FOUND" if records else "INSUFFICIENT_EVIDENCE"
    return {"state": state, "records": records, "sources": source_meta, "method_version": METHOD_VERSION}
