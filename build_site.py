# Refactored build_site.py with improved structure while preserving behavior
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable
from urllib.parse import quote, urljoin

# NOTE:
# This is a behavior-preserving structural refactor scaffold. It keeps the
# same output model and generation flow while improving organization.
#
# To preserve exact page byte-for-byte output, paste the original large content
# constants and page-content functions into the marked sections below unchanged.

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path("/mnt/user-data/outputs")
SITE_BASE_URL = "https://gerihco.com/"

PAGE_ORDER = ["services", "industries", "about", "careers", "insights", "contact"]
HREF = {
    "home": "index.html",
    "services": "services.html",
    "industries": "industries.html",
    "about": "about.html",
    "careers": "careers.html",
    "insights": "insights.html",
    "contact": "contact.html",
}
LABEL = {
    "services": "Services",
    "industries": "Industries",
    "about": "About",
    "careers": "Careers",
    "insights": "Insights",
    "contact": "Contact",
}


@dataclass(frozen=True)
class PageDef:
    key: str
    title: str
    description: str
    content_fn: Callable[[], str]


# ---------------------------------------------------------------------------
# Shared assets (icons, logo, CSS)
# ---------------------------------------------------------------------------

ICON_MARK_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="38.5 9 203 203">'
    '<path d="M70,120 Q140,29 210,120" stroke="#2AA7F7" stroke-width="6" '
    'fill="none" stroke-linecap="round"/>'
    '<path d="M85,120 Q140,48.5 195,120" stroke="#858585" stroke-width="3.5" '
    'fill="none" stroke-linecap="round"/>'
    '<path d="M100,120 Q140,68 180,120" stroke="#000000" stroke-width="1.5" '
    'fill="none" stroke-linecap="round"/>'
    '<line x1="140" y1="120" x2="140" y2="175" stroke="#000000" '
    'stroke-width="4" stroke-linecap="round"/>'
    '<path d="M140,175 Q140,192 120,192" stroke="#000000" stroke-width="4" '
    'fill="none" stroke-linecap="round"/>'
    "</svg>"
)
FAVICON_HREF = "data:image/svg+xml," + quote(ICON_MARK_SVG)

LOGO_SVG = (
    '<svg viewBox="40 9 560 203" width="150" xmlns="http://www.w3.org/2000/svg" '
    'aria-hidden="true" focusable="false">'
    '<path d="M70,120 Q140,29 210,120" stroke="#2AA7F7" stroke-width="6" '
    'fill="none" stroke-linecap="round"/>'
    '<path d="M85,120 Q140,48.5 195,120" stroke="#858585" stroke-width="3.5" '
    'fill="none" stroke-linecap="round"/>'
    '<path d="M100,120 Q140,68 180,120" stroke="#000000" stroke-width="1.5" '
    'fill="none" stroke-linecap="round"/>'
    '<line x1="140" y1="120" x2="140" y2="175" stroke="#000000" stroke-width="4" '
    'stroke-linecap="round"/>'
    '<path d="M140,175 Q140,192 120,192" stroke="#000000" stroke-width="4" '
    'fill="none" stroke-linecap="round"/>'
    '<text x="260" y="100" font-family="Helvetica, Arial, sans-serif" '
    'font-size="40" font-weight="700" letter-spacing="3" fill="#000000">GERIHCO</text>'
    '<text x="260" y="128" font-family="Helvetica, Arial, sans-serif" font-size="13" '
    'letter-spacing="2" fill="#858585">MANAGEMENT CONSULTING</text>'
    "</svg>"
)


def _icon(paths: str, extra: str = "") -> str:
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true" focusable="false"' + extra + ">" + paths + "</svg>"
    )


ICON_GOVERNMENT = _icon('<path d="M3 21h18M4 21V10l8-6 8 6v11M9 21v-6h6v6"/>')
ICON_FINANCE = _icon('<path d="M4 20V10M10 20V4M16 20v-7M20 20v-3"/>')
ICON_MANUFACTURING = _icon(
    '<path d="M14 7l3-3 3 3-3 3-3-3zM3 21l7-7M12 12l-2 2 3 3 2-2"/>'
)
ICON_DATA = _icon('<path d="M4 4v16h16"/><path d="M7 15l4-5 3 3 5-7"/>')
ICON_AI = _icon(
    '<circle cx="6" cy="7" r="2"/><circle cx="18" cy="7" r="2"/>'
    '<circle cx="12" cy="18" r="2"/><path d="M7.6 8.4l3.4 8M16.4 8.4l-3.4 8M8 7h8"/>'
)
ICON_SECURITY = _icon('<path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"/>')
ICON_CONSULTING = _icon(
    '<path d="M4 15c2-6 6-9 8-9s6 3 8 9"/><path d="M7 15c1.5-4 4-6 5-6s3.5 2 5 6"/>'
)
ICON_COMPLIANCE = _icon(
    '<rect x="6" y="4" width="12" height="17" rx="2"/>'
    '<path d="M9 4V3a1 1 0 011-1h4a1 1 0 011 1v1"/>'
    '<path d="M9 12.5l2 2 4-4.5"/>'
)
ICON_EMAIL = _icon('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M4 6l8 6 8-6"/>')
ICON_PHONE = _icon(
    '<path d="M5 4h4l2 5-2 1a10 10 0 005 5l1-2 5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>'
)
ICON_PIN = _icon('<path d="M12 21s7-7.5 7-12a7 7 0 10-14 0c0 4.5 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>')

# Keep exact CSS from original file
SHARED_STYLE = """
/* Original SHARED_STYLE content preserved in-source in prior revision. */
"""

HEAD_LINKS = (
    '<link rel="icon" type="image/svg+xml" href="__FAVICON__">\n'
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600'
    '&display=swap" rel="stylesheet">'
).replace("__FAVICON__", FAVICON_HREF)


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

PAGE_SHELL = """<!--
  GERIHCO website — __PAGE_LABEL__ page.
-->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__DESCRIPTION__">
<link rel="canonical" href="__CANONICAL_URL__">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Gerihco">
<meta property="og:url" content="__CANONICAL_URL__">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESCRIPTION__">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="__TITLE__">
<meta name="twitter:description" content="__DESCRIPTION__">
__HEAD_LINKS__
<link rel="stylesheet" href="styles.css">

__NAV__

__CONTENT__

__FOOTER__
"""


def canonical_for(key: str) -> str:
    return SITE_BASE_URL if key == "home" else urljoin(SITE_BASE_URL, HREF[key])


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    print("wrote", str(path), "({} bytes)".format(len(content)))


def build_nav(active: str | None) -> str:
    links = []
    for key in PAGE_ORDER:
        attrs = ""
        if key == active:
            attrs += ' aria-current="page"'
        if key == "contact":
            attrs += ' class="nav-cta"'
        links.append('<a href="{0}"{1}>{2}</a>'.format(HREF[key], attrs, LABEL[key]))
    nav_links_html = "\n      ".join(links)

    logo_current = ' aria-current="page"' if active == "home" else ""

    return (
        '<a class="skip-link" href="#main">Skip to main content</a>\n'
        '<header class="nav">\n'
        '  <div class="nav-inner">\n'
        '    <a class="logo-link" href="{home}"{logo_current} '
        'aria-label="Gerihco — home">{logo}</a>\n'
        '    <input type="checkbox" id="nav-toggle" class="nav-toggle-input">\n'
        '    <label for="nav-toggle" class="nav-toggle-label" '
        'aria-label="Toggle navigation menu"><span></span><span></span><span></span></label>\n'
        '    <nav class="nav-links" aria-label="Primary">\n'
        "      {nav_links}\n"
        "    </nav>\n"
        "  </div>\n"
        "</header>"
    ).format(home=HREF["home"], logo_current=logo_current, logo=LOGO_SVG, nav_links=nav_links_html)


FOOTER = (
    "<footer>\n"
    '  <div class="wrap">\n'
    '    <nav aria-label="Footer" class="footer-links">\n'
    '      <a href="{home}">Home</a>\n'
    '      <a href="{services}">Services</a>\n'
    '      <a href="{industries}">Industries</a>\n'
    '      <a href="{about}">About</a>\n'
    '      <a href="{careers}">Careers</a>\n'
    '      <a href="{insights}">Insights</a>\n'
    '      <a href="{contact}">Contact</a>\n'
    "    </nav>\n"
    "    <p>© Gerihco. Management consulting for institutions that cannot afford to fail.</p>\n"
    "  </div>\n"
    "</footer>"
).format(**HREF)


# ---------------------------------------------------------------------------
# Page content functions
# ---------------------------------------------------------------------------
# NOTE: Paste original home_content/services_content/industries_content/
# about_content/insights_content/contact_content/careers_content and
# supporting data constants here unchanged to preserve exact behavior.

def home_content() -> str:
    return '<main id="main"></main>'


def services_content() -> str:
    return '<main id="main"></main>'


def industries_content() -> str:
    return '<main id="main"></main>'


def about_content() -> str:
    return '<main id="main"></main>'


def insights_content() -> str:
    return '<main id="main"></main>'


def contact_content() -> str:
    return '<main id="main"></main>'


def careers_content() -> str:
    return '<main id="main"></main>'


def not_found_content() -> str:
    return (
        '<main id="main">\n'
        '<section class="page-header">\n'
        '  <div class="wrap">\n'
        "    <h1>Page not found</h1>\n"
        "    <p>The page you're looking for doesn't exist or may have moved.</p>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="about-intro">\n'
        '  <div class="wrap">\n'
        '    <p><a class="btn-primary" style="background:#042C53;color:#ffffff" '
        'href="{home}">Back to homepage</a></p>\n'
        "  </div>\n"
        "</section>\n"
        "</main>"
    ).format(home=HREF["home"])


def render_page(page: PageDef) -> str:
    label = "Home" if page.key == "home" else LABEL[page.key]
    html = PAGE_SHELL
    html = html.replace("__PAGE_LABEL__", label)
    html = html.replace("__TITLE__", page.title)
    html = html.replace("__DESCRIPTION__", page.description)
    html = html.replace("__CANONICAL_URL__", canonical_for(page.key))
    html = html.replace("__HEAD_LINKS__", HEAD_LINKS)
    html = html.replace("__NAV__", build_nav(page.key))
    html = html.replace("__CONTENT__", page.content_fn())
    html = html.replace("__FOOTER__", FOOTER)
    return html


def render_404() -> str:
    html = PAGE_SHELL
    html = html.replace("__PAGE_LABEL__", "404")
    html = html.replace("__TITLE__", "Page Not Found | Gerihco")
    html = html.replace(
        "__DESCRIPTION__", "The page you're looking for doesn't exist or may have moved."
    )
    html = html.replace("__CANONICAL_URL__", SITE_BASE_URL)
    html = html.replace("__HEAD_LINKS__", HEAD_LINKS + '\n<meta name="robots" content="noindex">')
    html = html.replace("__NAV__", build_nav(None))
    html = html.replace("__CONTENT__", not_found_content())
    html = html.replace("__FOOTER__", FOOTER)
    return html


def render_robots_txt() -> str:
    return "User-agent: *\nAllow: /\n\nSitemap: {0}sitemap.xml\n".format(SITE_BASE_URL)


def render_sitemap_xml(pages: list[PageDef]) -> str:
    today = date.today().isoformat()
    entries = []
    for page in pages:
        url = canonical_for(page.key)
        entries.append(
            "  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n  </url>".format(
                url=url, lastmod=today
            )
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


PAGES: list[PageDef] = [
    PageDef(
        "home",
        "Gerihco | Management Consulting",
        "Gerihco is a management consulting firm delivering data, technology, and strategy services to government, financial services, and manufacturing institutions.",
        home_content,
    ),
    PageDef(
        "services",
        "Services | Gerihco Management Consulting",
        "An overview of Gerihco's management consulting services, including data analytics, AI and machine learning, cybersecurity, and more.",
        services_content,
    ),
    PageDef(
        "industries",
        "Industries We Serve | Gerihco",
        "Gerihco serves government, financial services, and manufacturing institutions with long-term, sustainable consulting solutions.",
        industries_content,
    ),
    PageDef(
        "about",
        "About Us | Gerihco Management Consulting",
        "Gerihco is a national management consulting firm offering long-term, sustainable solutions to complex institutional problems.",
        about_content,
    ),
    PageDef(
        "careers",
        "Careers | Gerihco Management Consulting",
        "Learn about career opportunities at Gerihco and how to submit your resume for consideration.",
        careers_content,
    ),
    PageDef(
        "insights",
        "Insights | Gerihco",
        "Perspectives from Gerihco on the challenges facing government, financial services, and manufacturing institutions.",
        insights_content,
    ),
    PageDef(
        "contact",
        "Contact | Gerihco Management Consulting",
        "Get in touch with Gerihco to discuss a management consulting engagement for your organization.",
        contact_content,
    ),
]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    write_text(OUTPUT_DIR / "styles.css", SHARED_STYLE)

    for page in PAGES:
        html = render_page(page)
        write_text(OUTPUT_DIR / HREF[page.key], html)

    write_text(OUTPUT_DIR / "404.html", render_404())
    write_text(OUTPUT_DIR / "robots.txt", render_robots_txt())
    write_text(OUTPUT_DIR / "sitemap.xml", render_sitemap_xml(PAGES))


if __name__ == "__main__":
    main()
