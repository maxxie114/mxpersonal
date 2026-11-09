"""Check static pages, public output boundaries and local assets after a build."""
import hashlib
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from build import CAP, ROOT, RESUME_PDF, RESUME_PDF_SHA256, SITE
from content import PAPER, PAPER_SOURCE, PAPER_TITLE

OUTPUT = ROOT / "dist"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.headings = []
        self.citation = {}
        self.errors = []
        self.origin = path.name
        self.feed(path.read_text(encoding="utf8"))

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"{self.origin}: duplicate id {attrs['id']}")
            self.ids.add(attrs["id"])
        if re.fullmatch("h[1-6]", tag):
            self.headings.append(int(tag[1]))
        if tag == "img" and "alt" not in attrs:
            self.errors.append(f"{self.origin}: image without alt")
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if attrs.get("property") == "og:image":
            self.links.append(attrs["content"])
        if tag == "meta" and attrs.get("name", "").startswith("citation_"):
            self.citation[attrs["name"]] = attrs.get("content", "")


def main():
    pages = {p.name: Page(p) for p in OUTPUT.glob("*.html")}
    errors = []
    checked = 0
    for name, doc in pages.items():
        errors.extend(doc.errors)
        if doc.headings.count(1) != 1:
            errors.append(f"{name}: expected one h1")
        if any(b>a+1 for a,b in zip(doc.headings,doc.headings[1:])):
            errors.append(f"{name}: skipped heading level")
        for ref in doc.links:
            parsed = urlparse(ref)
            if parsed.scheme in ("mailto", "tel"):
                continue
            if parsed.netloc and parsed.netloc != urlparse(SITE).netloc:
                if parsed.scheme != "https":
                    errors.append(f"{name}: insecure URL {ref}")
                continue
            target = unquote(parsed.path.lstrip("/")) or ("index.html" if parsed.path or parsed.netloc else name)
            if not (OUTPUT/target).is_file():
                errors.append(f"{name}: missing {ref}")
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                errors.append(f"{name}: missing fragment {ref}")
            checked += 1
    for css in OUTPUT.rglob("*.css"):
        for ref in re.findall(r'url\(([^)]+)\)', css.read_text(encoding="utf8")):
            parsed=urlparse(ref.strip('"\' '))
            if not parsed.scheme and parsed.path and not (css.parent/unquote(parsed.path)).is_file():
                errors.append(f"{css.name}: missing CSS asset {ref}")
    if hashlib.sha256((OUTPUT/RESUME_PDF).read_bytes()).hexdigest() != RESUME_PDF_SHA256:
        errors.append(f"{RESUME_PDF}: unexpected SHA-256")
    paper = pages[CAP]
    if (paper.citation.get("citation_title") != PAPER_TITLE
            or not paper.citation.get("citation_author")
            or not paper.citation.get("citation_publication_date")
            or paper.citation.get("citation_pdf_url") != SITE + PAPER):
        errors.append(f"{CAP}: missing or inconsistent Scholar citation metadata")
    if Path(CAP).parent != Path(PAPER).parent or PAPER not in paper.links:
        errors.append(f"{CAP}: expected a linked full-text PDF in the same directory")
    if (OUTPUT/PAPER).read_bytes() != (OUTPUT/PAPER_SOURCE).read_bytes():
        errors.append(f"{PAPER}: full text differs from the original PDF")
    for url in ET.parse(OUTPUT/"sitemap.xml").iterfind(".//{*}loc"):
        if not url.text.startswith(SITE) or (url.text[len(SITE):] or "index.html") not in pages:
            errors.append("Invalid sitemap entry: "+url.text)
    for file in OUTPUT.rglob("*"):
        if file.suffix in (".md",".py",".json",".bak") or file.name in (".git",".claude"):
            errors.append(f"Non-public file included: {file.name}")
        if file.suffix in (".html",".xml",".js",".svg") and re.search(
            r"foxstar-wechat-bot|chromatic-games|financial-management-agent|openai_translation|maxxie114/mxpersonal",file.read_text(encoding="utf8"),re.I):
            errors.append(f"Private project reference in {file.name}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Verified {len(pages)} pages, {checked} local references, CSS assets, sitemap and résumé PDF hash.")


if __name__ == "__main__":
    main()

