from __future__ import annotations

from pathlib import Path
from typing import Any
import re

import httpx
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def _clean_text(text: str) -> str:
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


async def search_web(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """
    Web search (no API key) via DuckDuckGo HTML endpoint.
    Returns a list of {title, url, snippet}.
    """
    url = "https://duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": USER_AGENT}

    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        resp = await client.get(url, params=params, headers=headers)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    out: list[dict[str, Any]] = []

    for r in soup.select("div.result"):
        a = r.select_one("a.result__a")
        if not a:
            continue
        title = a.get_text(" ", strip=True)
        href = (a.get("href") or "").strip()
        if not href:
            continue

        snippet_el = r.select_one(".result__snippet")
        snippet = snippet_el.get_text(" ", strip=True) if snippet_el else ""

        out.append({"title": title, "url": href, "snippet": snippet})
        if len(out) >= max_results:
            break

    return out


async def fetch_url(url: str, max_chars: int = 20000) -> dict[str, Any]:
    """
    Fetch URL and return cleaned text.
    Returns: {url, status_code, content_type, text}
    """
    headers = {"User-Agent": USER_AGENT}

    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        resp = await client.get(url, headers=headers)

    content_type = resp.headers.get("content-type", "")
    text = resp.text or ""

    # HTML -> text
    if "text/html" in content_type.lower():
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            tag.decompose()
        text = soup.get_text("\n", strip=True)

    text = _clean_text(text)
    if max_chars and len(text) > max_chars:
        text = text[:max_chars] + "\n\n[TRUNCATED]"

    return {
        "url": url,
        "status_code": resp.status_code,
        "content_type": content_type,
        "text": text,
    }


def _ensure_under_src(path: str) -> Path:
    p = Path(path)
    if p.is_absolute():
        raise ValueError("Only relative paths are allowed, e.g. src/output.md")
    if not p.parts or p.parts[0] != "src":
        raise ValueError("Path must be under 'src/', e.g. src/vue-3-6-notes.md")
    return p


async def write_file(path: str, content: str, encoding: str = "utf-8") -> dict[str, Any]:
    """
    Write file content under src/ only.
    Returns: {path, bytes_written}
    """
    p = _ensure_under_src(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    data = content.encode(encoding)
    p.write_bytes(data)
    return {"path": str(p), "bytes_written": len(data)}