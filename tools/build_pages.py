"""Make services.html, work.html and contact.html from site/index.html.

index.html stays the only file to edit. Each copy opens on its own view and
carries its own title, description and canonical address (from #routes), so
Google sees four real pages. Run after every change to index.html:

    python3 tools/build_pages.py
"""
import html, json, pathlib, re

SITE = 'https://stayupsocial.com'
root = pathlib.Path(__file__).resolve().parent.parent / 'site'
src = (root / 'index.html').read_text(encoding='utf-8')
routes = json.loads(re.search(r'<script type="application/json" id="routes">(.*?)</script>', src, re.S).group(1))


def swap_attr(page, pattern, value):
    page, n = re.subn(pattern, lambda m: m.group(1) + value + m.group(2), page, count=1)
    assert n == 1, pattern
    return page


for view, r in routes.items():
    if view == 'home':
        continue
    title, desc, url = html.escape(r['title'], quote=False), html.escape(r['desc']), SITE + r['path']
    page = src
    page = swap_attr(page, r'(<title>).*?(</title>)', title)
    page = swap_attr(page, r'(<meta name="description" content=").*?(">)', desc)
    page = swap_attr(page, r'(<link rel="canonical" href=").*?(">)', url)
    page = swap_attr(page, r'(<meta property="og:url" content=").*?(">)', url)
    page = swap_attr(page, r'(<meta property="og:title" content=").*?(">)', title)
    page = swap_attr(page, r'(<meta property="og:description" content=").*?(">)', desc)
    page = swap_attr(page, r'(<meta name="twitter:title" content=").*?(">)', title)
    page = swap_attr(page, r'(<meta name="twitter:description" content=").*?(">)', desc)
    # the FAQ lives on the home page only
    page = re.sub(r'<script type="application/ld\+json" id="ld-faq">.*?</script>\n', '', page, flags=re.S)
    # open on this view
    page = page.replace('<section class="view" id="view-home" data-view="home">',
                        '<section class="view" id="view-home" data-view="home" hidden>', 1)
    page, n = re.subn(r'(<section class="view[^"]*" id="view-%s" data-view="%s") hidden>' % (view, view), r'\1>', page, count=1)
    assert n == 1, view
    out = root / (r['path'].strip('/') + '.html')
    out.write_text(page, encoding='utf-8')
    print('wrote', out.relative_to(root.parent))
