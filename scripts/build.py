#!/usr/bin/env python3
"""
Build script: converts /content/*.md → /blog/*.html
Uses python-markdown for full spec compliance (bold, italic, code, lists, links, etc.).
Also generates:
  - /blog/index.html (article listing)
  - /sitemap.xml
  - /robots.txt
"""

import os
import re
import html as htmlmod
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xmlescape
import markdown

CONTENT_DIR = "content"
OUTPUT_DIR = "blog"
LANDING = "index.html"

SITE_URL = "https://mimir-intelligence.com"

MD_EXTENSIONS = ["extra", "codehilite", "sane_lists"]


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✏️  {path}")


def slug_from_filename(filename):
    return os.path.splitext(filename)[0].lstrip("0123456789-")


def parse_frontmatter(md):
    """Optional YAML frontmatter: title / date / description / excerpt."""
    meta = {}
    rest = md
    if md.startswith("---"):
        parts = md.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                m = re.match(r"(\w+):\s*(.+)", line)
                if m:
                    meta[m.group(1).strip()] = m.group(2).strip().strip('"').strip("'")
            rest = parts[2].strip()
    return meta, rest


def strip_leading_h1(text):
    """Remove the first # H1 line from body text when frontmatter has a title."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("##"):
            remaining = "\n".join(lines[i + 1:]).strip()
            return remaining
    return text


def md_to_html(text):
    """Convert markdown to HTML using python-markdown with full spec support."""
    return markdown.markdown(text, extensions=MD_EXTENSIONS)


def build_article_html(slug, meta, body_html):
    title = meta.get("title", slug.replace("-", " ").title())
    description = meta.get("description", "")
    date = meta.get("date", "")
    canonical = f"{SITE_URL}/blog/{slug}"

    date_tag = f'<time datetime="{date}">{date}</time>' if date else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{htmlmod.escape(title)} — MIMIR Intelligence</title>
    <meta name="description" content="{htmlmod.escape(description)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{htmlmod.escape(title)}">
    <meta property="og:description" content="{htmlmod.escape(description)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="MIMIR Intelligence">
    <meta name="twitter:card" content="summary_large_image">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background-color: #0a0a0f;
            color: #e0e0e0;
            font-family: system-ui, sans-serif;
            line-height: 1.8;
            overflow-x: hidden;
        }}
        h1, h2, h3 {{ font-family: Georgia, serif; color: #c8a96e; font-weight: normal; letter-spacing: 0.5px; }}
        h1 {{ font-size: 2.2rem; margin-bottom: 0.5rem; }}
        h2 {{ font-size: 1.5rem; margin-top: 2.5rem; margin-bottom: 1rem; }}
        h3 {{ font-size: 1.2rem; margin-top: 2rem; margin-bottom: 0.8rem; }}
        a {{ color: #c8a96e; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        p {{ margin-bottom: 1.5rem; }}
        ul, ol {{ margin-bottom: 1.5rem; padding-left: 1.5rem; }}
        li {{ margin-bottom: 0.5rem; }}
        hr {{ border: none; border-top: 1px solid #1a1a2e; margin: 2.5rem 0; }}
        pre {{
            background: #0d0d1a;
            border: 1px solid #1a1a2e;
            padding: 1rem;
            overflow-x: auto;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }}
        code {{ font-family: ui-monospace, monospace; }}
        code:not(pre code) {{ background: #1a1a2e; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.9em; }}
        time {{ display: block; color: #888; font-size: 0.9rem; margin-bottom: 2rem; }}
        .container {{ max-width: 700px; margin: 0 auto; padding: 0 20px; }}
        .article-header {{ padding: 80px 0 0; text-align: center; }}
        .article-body {{ padding: 20px 0 60px; }}
        .article-footer {{ border-top: 1px solid #1a1a2e; padding-top: 2rem; margin-top: 3rem; font-size: 0.9rem; color: #888; text-align: center; }}
        .nav-bar {{
            background: #0a0a0f;
            border-bottom: 1px solid #1a1a2e;
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .nav-bar .container {{ display: flex; justify-content: space-between; align-items: center; max-width: 1200px; }}
        .nav-logo {{ font-family: Georgia, serif; color: #c8a96e; font-size: 1.2rem; letter-spacing: 3px; }}
        .nav-links a {{ margin-left: 20px; font-size: 0.9rem; opacity: 0.7; }}
        .nav-links a:hover {{ opacity: 1; text-decoration: none; }}
        @media (max-width: 600px) {{
            h1 {{ font-size: 1.6rem; }}
            h2 {{ font-size: 1.3rem; }}
            .article-header {{ padding: 40px 0 0; }}
        }}
    </style>
</head>
<body>
    <nav class="nav-bar">
        <div class="container" style="max-width:700px">
            <a href="{SITE_URL}" class="nav-logo">MIMIR</a>
            <div class="nav-links">
                <a href="/blog">Blog</a>
            </div>
        </div>
    </nav>
    <header class="article-header">
        <div class="container">
            <h1>{title}</h1>
            {date_tag}
        </div>
    </header>
    <main class="article-body">
        <div class="container">
            {body_html}
            <div class="article-footer">
                <a href="/blog">← Back to all articles</a>
            </div>
        </div>
    </main>
</body>
</html>"""


def build_index_html(articles_list):
    items = []
    for slug, meta in articles_list:
        title = meta.get("title", slug.replace("-", " ").title())
        date = meta.get("date", "")
        excerpt = meta.get("excerpt", meta.get("description", ""))
        date_tag = f'<time datetime="{date}">{date}</time>' if date else ""
        items.append(f"""
        <article>
            <h2><a href="/blog/{slug}">{title}</a></h2>
            {date_tag}
            <p class="excerpt">{excerpt}</p>
            <a class="read-more" href="/blog/{slug}">Read more →</a>
        </article>""")

    articles_html = "\n".join(items)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog — MIMIR Intelligence</title>
    <meta name="description" content="Essays on AI agents, reliability, memory, and failure modes in production AI systems.">
    <link rel="canonical" href="{SITE_URL}/blog">
    <meta property="og:title" content="Blog — MIMIR Intelligence">
    <meta property="og:description" content="Essays on AI agents, reliability, memory, and failure modes in production AI systems.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{SITE_URL}/blog">
    <meta name="twitter:card" content="summary_large_image">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background-color: #0a0a0f;
            color: #e0e0e0;
            font-family: system-ui, sans-serif;
            line-height: 1.8;
            overflow-x: hidden;
        }}
        h1, h2 {{ font-family: Georgia, serif; color: #c8a96e; font-weight: normal; }}
        h1 {{ font-size: 2.2rem; margin-bottom: 1rem; text-align: center; padding-top: 60px; }}
        h2 {{ font-size: 1.4rem; margin-bottom: 0.25rem; }}
        a {{ color: #c8a96e; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .container {{ max-width: 700px; margin: 0 auto; padding: 0 20px; }}
        .nav-bar {{
            background: #0a0a0f;
            border-bottom: 1px solid #1a1a2e;
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .nav-bar .container {{ display: flex; justify-content: space-between; align-items: center; max-width: 1200px; }}
        .nav-logo {{ font-family: Georgia, serif; color: #c8a96e; font-size: 1.2rem; letter-spacing: 3px; }}
        .nav-links a {{ margin-left: 20px; font-size: 0.9rem; opacity: 0.7; }}
        .nav-links a:hover {{ opacity: 1; text-decoration: none; }}
        article {{
            border-bottom: 1px solid #1a1a2e;
            padding: 30px 0;
        }}
        article:last-child {{ border-bottom: none; }}
        time {{ display: block; color: #888; font-size: 0.85rem; margin-bottom: 0.5rem; }}
        .excerpt {{ color: #b0b0b0; margin-bottom: 0.75rem; }}
        .read-more {{ font-size: 0.9rem; }}
        @media (max-width: 600px) {{
            h1 {{ font-size: 1.6rem; padding-top: 40px; }}
        }}
    </style>
</head>
<body>
    <nav class="nav-bar">
        <div class="container" style="max-width:700px">
            <a href="{SITE_URL}" class="nav-logo">MIMIR</a>
            <div class="nav-links">
                <a href="/blog">Blog</a>
            </div>
        </div>
    </nav>
    <main>
        <div class="container">
            <h1>Blog</h1>
            {articles_html}
        </div>
    </main>
</body>
</html>"""


def build_sitemap(articles_list):
    urls = [f"""
  <url>
    <loc>{SITE_URL}/</loc>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{SITE_URL}/blog</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>"""]

    for slug, meta in articles_list:
        date = meta.get("date", "")
        lastmod = f"\n    <lastmod>{date}</lastmod>" if date else ""
        urls.append(f"""
  <url>
    <loc>{SITE_URL}/blog/{slug}</loc>{lastmod}
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(urls)}
</urlset>"""


def main():
    print("📦 Build: Markdown → HTML (python-markdown)")
    print(f"   Content dir: {CONTENT_DIR}/")
    print(f"   Output dir:  {OUTPUT_DIR}/\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CONTENT_DIR, exist_ok=True)

    articles = []
    files = sorted(f for f in os.listdir(CONTENT_DIR) if f.endswith(".md"))

    if not files:
        print("   ⚠️  No .md files found in content/.")
    else:
        for fname in files:
            slug = slug_from_filename(fname)
            md = read_file(os.path.join(CONTENT_DIR, fname))
            meta, body_md = parse_frontmatter(md)
            # Strip leading H1 if title exists in frontmatter (avoids duplicate H1)
            if "title" in meta:
                body_md = strip_leading_h1(body_md)
            body_html = md_to_html(body_md)
            html = build_article_html(slug, meta, body_html)
            write_file(os.path.join(OUTPUT_DIR, f"{slug}.html"), html)
            articles.append((slug, meta))
            print(f"   ✅ {fname} → /blog/{slug}.html")

    # Sort newest first by date
    articles.sort(key=lambda x: x[1].get("date", ""), reverse=True)

    # Blog index
    write_file(os.path.join(OUTPUT_DIR, "index.html"), build_index_html(articles))
    print(f"\n   ✅ /blog/index.html ({len(articles)} article{'s' if len(articles)!=1 else ''})")

    # Sitemap
    write_file("sitemap.xml", build_sitemap(articles))

    # Robots.txt
    write_file("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")

    # Keep blog link in landing footer (build.py is idempotent — just ensure it's there)
    landing_content = read_file(LANDING)
    if '/blog"' not in landing_content:
        # Find footer and inject
        footer_start = landing_content.rfind("<footer")
        if footer_start != -1:
            link_html = '<p><a href="/blog" style="color:#c8a96e;text-decoration:none;opacity:0.7">Blog</a></p>\n        '
            insert_pos = landing_content.index(">", landing_content.index(">", footer_start) + 1) + 1
            landing_content = landing_content[:insert_pos] + "\n        " + link_html + landing_content[insert_pos:]
            write_file(LANDING, landing_content)
            print(f"\n   ✅ /index.html — blog link added to footer")
        else:
            print(f"\n   ⚠️  /index.html — could not find <footer>")
    else:
        print(f"\n   ✓ /index.html — blog link already present")

    print(f"\n🎉 Build complete. {len(files)} articles processed.")


if __name__ == "__main__":
    main()
