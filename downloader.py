#!/usr/bin/env python3
"""
Spanish Immigration Forms Downloader
Fetches all official forms from:
  https://www.inclusion.gob.es/en/web/migraciones/modelos-generales

Saves:
  forms/editable/        — fillable PDF versions
  forms/non-editable/    — static PDF versions
"""

import logging
import os
import re
import time
from urllib.parse import unquote, urljoin

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = "https://www.inclusion.gob.es"
FORMS_PAGE_URL = f"{BASE_URL}/en/web/migraciones/modelos-generales"

EDITABLE_DIR = os.path.join("forms", "editable")
NON_EDITABLE_DIR = os.path.join("forms", "non-editable")

REQUEST_DELAY = 1.0  # polite delay between downloads (seconds)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# HTTP session
# ---------------------------------------------------------------------------

def make_session() -> requests.Session:
    import urllib3

    # The inclusion.gob.es site uses a Spanish-government CA that is not
    # included in the default system trust store.  We disable certificate
    # verification only for this specific, well-known government endpoint.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    log.warning(
        "SSL certificate verification is disabled because the site uses a "
        "Spanish-government CA that is not in the default trust bundle. "
        "All downloads are from the verified domain inclusion.gob.es."
    )

    session = requests.Session()
    session.verify = False
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,*/*;q=0.8"
            ),
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        }
    )
    return session


# ---------------------------------------------------------------------------
# Link discovery and classification
# ---------------------------------------------------------------------------

def _is_migraciones_form_link(href: str) -> bool:
    """True when the href points to a migraciones form document."""
    return "/documents/d/migraciones/" in href


def _is_editable(href: str, surrounding_text: str) -> bool:
    """
    An editable form is identified by 'editable' in its URL path, or by the
    word 'editable' appearing in the text block that contains the link.
    """
    if "editable" in href.lower():
        return True
    return "editable" in surrounding_text.lower()


def extract_form_links(page_html: str) -> tuple[list, list]:
    """
    Parse the forms page and return two lists:
      editable_forms     -> [(name, url), ...]
      non_editable_forms -> [(name, url), ...]

    Deduplication is applied so the same URL is not downloaded twice.
    """
    soup = BeautifulSoup(page_html, "html.parser")
    editable: list[tuple[str, str]] = []
    non_editable: list[tuple[str, str]] = []
    seen_urls: set[str] = set()

    for a_tag in soup.find_all("a", href=True):
        href: str = a_tag["href"]
        if not _is_migraciones_form_link(href):
            continue

        full_url = urljoin(BASE_URL, href)
        if full_url in seen_urls:
            continue
        seen_urls.add(full_url)

        link_text = a_tag.get_text(strip=True)

        # Use the parent element's full text to catch "Editable" labels that
        # sit as plain text nodes adjacent to the <a> tag (e.g. EX02, EX10).
        surrounding = ""
        if a_tag.parent:
            surrounding = a_tag.parent.get_text(separator=" ", strip=True)

        name = link_text or href.rstrip("/").split("/")[-1]

        if _is_editable(href, surrounding):
            editable.append((name, full_url))
        else:
            non_editable.append((name, full_url))

    return editable, non_editable


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------

def _filename_from_response(resp: requests.Response) -> str:
    """
    Derive a safe filename from the Content-Disposition header or the final
    (post-redirect) URL.
    """
    cd = resp.headers.get("Content-Disposition", "")
    if cd:
        # RFC 5987 encoded filename
        match = re.search(r"filename\*=UTF-8''([^\s;]+)", cd, re.IGNORECASE)
        if not match:
            match = re.search(r'filename=["\']?([^"\';\r\n]+)', cd, re.IGNORECASE)
        if match:
            name = unquote(match.group(1)).strip().strip("\"'")
            if name:
                return _ensure_pdf_ext(name)

    # Fall back to the path component of the final URL
    path = resp.url.split("?")[0]
    name = path.rstrip("/").split("/")[-1]
    return _ensure_pdf_ext(unquote(name))


def _ensure_pdf_ext(name: str) -> str:
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    return name


def _unique_filepath(directory: str, filename: str) -> str:
    """Return a filepath that does not collide with existing files."""
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(directory, filename)
    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(directory, f"{base}_{counter}{ext}")
        counter += 1
    return candidate


def download_form(url: str, dest_dir: str, session: requests.Session) -> bool:
    """
    Download a single form (following redirects) and save it to dest_dir.
    Returns True on success.
    """
    os.makedirs(dest_dir, exist_ok=True)
    try:
        resp = session.get(url, allow_redirects=True, timeout=60)
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "")
        if "pdf" not in content_type.lower() and not resp.url.lower().endswith(".pdf"):
            log.warning(
                "Unexpected Content-Type '%s' for %s — saving anyway", content_type, url
            )

        filename = _filename_from_response(resp)
        filepath = _unique_filepath(dest_dir, filename)

        with open(filepath, "wb") as fh:
            fh.write(resp.content)

        log.info("  Saved %-55s  (%d KB)", filename, len(resp.content) // 1024)
        return True

    except requests.RequestException as exc:
        log.error("  FAILED %s — %s", url, exc)
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    session = make_session()

    log.info("Fetching forms index: %s", FORMS_PAGE_URL)
    try:
        page = session.get(FORMS_PAGE_URL, timeout=30)
        page.raise_for_status()
    except requests.RequestException as exc:
        log.error("Could not fetch forms page: %s", exc)
        raise SystemExit(1)

    editable_forms, non_editable_forms = extract_form_links(page.text)

    log.info(
        "Discovered %d non-editable and %d editable form links.",
        len(non_editable_forms),
        len(editable_forms),
    )

    # ---------- non-editable ----------
    log.info("")
    log.info("=== Non-editable forms → %s ===", NON_EDITABLE_DIR)
    ok, fail = 0, 0
    for name, url in non_editable_forms:
        log.info("  %s", url)
        if download_form(url, NON_EDITABLE_DIR, session):
            ok += 1
        else:
            fail += 1
        time.sleep(REQUEST_DELAY)
    log.info("Non-editable: %d downloaded, %d failed.", ok, fail)

    # ---------- editable ----------
    log.info("")
    log.info("=== Editable forms → %s ===", EDITABLE_DIR)
    ok, fail = 0, 0
    for name, url in editable_forms:
        log.info("  %s", url)
        if download_form(url, EDITABLE_DIR, session):
            ok += 1
        else:
            fail += 1
        time.sleep(REQUEST_DELAY)
    log.info("Editable: %d downloaded, %d failed.", ok, fail)

    log.info("")
    log.info(
        "Done. PDFs saved under '%s/' and '%s/'.",
        NON_EDITABLE_DIR,
        EDITABLE_DIR,
    )


if __name__ == "__main__":
    main()
