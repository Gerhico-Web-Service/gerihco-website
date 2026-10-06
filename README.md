# Gerihco website — deployment notes

This package contains a seven-page site expanded from the original
`gerihco_homepage_concept_e.html`. It's deployed as a static site on
**GitHub Pages**, serving the repository's files directly — an earlier
version of this project targeted Google Sites' "Embed code" feature
instead, and some of this document (and a few now-removed pieces of the
HTML itself, like `target="_top"` links) reflected that. This revision
brings both fully in line with a plain GitHub Pages deployment.

## Files

| File               | Page / purpose |
|--------------------|--------------|
| `index.html`       | Home         |
| `services.html`    | Services     |
| `industries.html`  | Industries   |
| `about.html`       | About        |
| `careers.html`     | Careers      |
| `insights.html`    | Insights     |
| `contact.html`     | Contact      |
| `404.html`         | Custom not-found page; GitHub Pages serves this automatically for any unmatched URL |
| `robots.txt`        | Tells search engine crawlers everything is crawlable, and points them at the sitemap |
| `sitemap.xml`      | Lists all seven real pages, for search engines |
| `images/`          | Photography used by the pages above |
| `build_site.py`    | Generator script that produced every file above (see "Maintaining this site" below) |

Each `.html` file is a complete, self-contained document (fonts, CSS, and
markup all inline except for images) and can be opened directly in a
browser to preview it.

## Publishing to GitHub Pages

This is already how the live site works, so there's nothing new to set
up — noted here for reference or in case Pages ever needs re-enabling:

1. Push all the files in this package to the repository (`Gerhico-Web-Service/gerihco-website`),
   preserving the flat structure — every `.html` file, `robots.txt`, and
   `sitemap.xml` at the repository root, with `images/` as a real
   subfolder alongside them.
2. In the repo's **Settings → Pages**, set the source to the branch and
   folder these files live in (this repo is already configured and
   serving from `main`).
3. GitHub Pages serves each file at its own filename directly —
   `services.html` really is `.../services.html` on the live site. There
   is no separate publish step, no per-page embed box, and no URL
   remapping to do afterward, unlike the Google Sites workflow this
   project used earlier.

## SEO: already handled directly in the HTML

Because GitHub Pages serves these files as real, standalone pages rather
than through an embedding layer, the `<title>`, `<meta name="description">`,
`<link rel="canonical">`, and Open Graph / Twitter Card tags already
present in each file's `<head>` are exactly what search engines and
link-preview crawlers read — there is no separate settings panel to also
update, the way Google Sites required. Nothing further is needed here
unless the content of a page changes enough that its title or description
should change too (edit the `PAGES` list in `build_site.py` and re-run
it).

`sitemap.xml` lists all seven real pages (not `404.html`, which is
deliberately excluded and marked `noindex`, since a not-found page has no
business in search results). `robots.txt` points crawlers at it.
