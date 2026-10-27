"""Make services.html, work.html and contact.html from site/index.html.

index.html stays the only file to edit. Each copy opens on its own view and
carries its own title, description and canonical address (from #routes), so
Google sees four real pages. It also keeps the FAQ structured data in step
with the visible questions (#faq-home on the home page, #faq-svc on
Services). Run after every change to index.html:

    python3 tools/build_pages.py
"""
import html, json, pathlib, re

SITE = 'https://stayupsocial.com'
root = pathlib.Path(__file__).resolve().parent.parent / 'site'
src = (root / 'index.html').read_text(encoding='utf-8')


def faq_ld(page, faq_id):
    """FAQPage JSON-LD built from the <details> questions inside #faq_id."""
    start = page.index('id="%s"' % faq_id)
    end = page.index('</div>', start)
    qa = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', page[start:end], re.S)
    text = lambda h: html.unescape(re.sub(r'<[^>]+>', '', h)).strip()
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": text(q), "acceptedAnswer": {"@type": "Answer", "text": text(a)}} for q, a in qa]}
    return '<script type="application/ld+json" id="ld-faq">\n' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n</script>\n'


FAQ_RE = r'<script type="application/ld\+json" id="ld-faq">.*?</script>\n'
synced = re.sub(FAQ_RE, lambda m: faq_ld(src, 'faq-home'), src, count=1, flags=re.S)
if synced != src:
    (root / 'index.html').write_text(synced, encoding='utf-8')
    src = synced
    print('updated FAQ data in site/index.html')
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
    # each page describes only the questions it shows
    page = re.sub(FAQ_RE, lambda m: faq_ld(src, 'faq-svc') if view == 'services' else '', page, count=1, flags=re.S)
    # open on this view
    page = page.replace('<section class="view" id="view-home" data-view="home">',
                        '<section class="view" id="view-home" data-view="home" hidden>', 1)
    page, n = re.subn(r'(<section class="view[^"]*" id="view-%s" data-view="%s") hidden>' % (view, view), r'\1>', page, count=1)
    assert n == 1, view
    out = root / (r['path'].strip('/') + '.html')
    out.write_text(page, encoding='utf-8')
    print('wrote', out.relative_to(root.parent))
