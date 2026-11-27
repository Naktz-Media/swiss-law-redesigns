MADE_BY = {'de': 'Gestaltet von', 'fr': 'Conçu par', 'it': 'Realizzato da', 'en': 'Designed by'}
ARR = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
CHEV = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 5l4 4 4-4"/></svg>'
CREDITS = json.load(open(os.path.join(OUT, 'img/credits.json'), encoding='utf-8'))
# the original English contact page still lists an old Schwyz address; its English footer and every German page use Dorfplatz 2b
OFFICES['en'] = [('Head Office Zug', ['Zanetti Rechtsanwälte AG', 'Blegistrasse 9', '6340 Baar, Zug']),
                 ('Office Zürich', ['Zanetti Rechtsanwälte AG', 'Allmendstrasse 2', '8105 Regensdorf, Zürich']),
                 ('Office Schwyz', ['Zanetti Rechtsanwälte AG', 'Dorfplatz 2b', '6405 Immensee, Schwyz'])]
TEL, TEL_H, FAX_H, MAIL = '+41417663585', '+41 41 766 35 85', '+41 41 766 35 80', 'info@zanettilaw.ch'
X = {
 'de': dict(about='Über uns', offices='Standorte', bio='Werdegang', all_team='Ganzes Team', pics='Bilder', site='Seiten',
            our_offices='Unsere Standorte', read='Mehr erfahren', ready='Bereit für ein erstes Gespräch?',
            ready_sub='Schildern Sie uns Ihr Anliegen. Wir melden uns rasch und sagen Ihnen offen, wie wir Ihnen helfen können.',
            maps='Route planen', readmore='Weiterlesen', less='Weniger anzeigen', call='Telefon', mail='E-Mail', fax='Fax', links='Links', all_services='Alle Dienstleistungen',
            de_note='Dieser Abschnitt ist auf der englischen Seite der Kanzlei nur auf Deutsch verfügbar.', mail_person='E-Mail an'),
 'en': dict(about='About us', offices='Offices', bio='Background', all_team='Whole team', pics='Pictures', site='Pages',
            our_offices='Our offices', read='Learn more', ready='Ready for a first conversation?',
            ready_sub='Tell us about your matter. We will get back to you quickly and tell you openly how we can help.',
            maps='Plan route', readmore='Read more', less='Show less', call='Phone', mail='E-mail', fax='Fax', links='Links', all_services='All services',
            de_note='This section is only available in German.', mail_person='E-mail'),
}


def head(pg, title, desc):
    alt = ''.join(f'<link rel="alternate" hreflang="{x}" href="{pg.href(pg.key, x)}">' for x in ('de', 'en'))
    return f'''<!doctype html>
<html lang="{pg.l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc[:300])}">
{alt}
<link rel="icon" href="{pg.b}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pg.b}assets/site.css?v={VER}">
<script>document.documentElement.classList.add('js')</script>
</head>
'''


def top(pg):
    l = pg.l
    n = nav_labels(l)
    links = ''.join(f'<a href="{pg.href(k)}"{" aria-current=\"page\"" if k == pg.key else ""}>{e(n[k])}</a>' for k in KEYS)
    lg = ''.join(f'<a href="{pg.href(pg.key, x)}" hreflang="{x}" lang="{x}"{" aria-current=\"true\"" if x == l else ""}>{"D" if x == "de" else "E"}</a>' for x in ('de', 'en'))
    return f'''<a class="skip" href="#main">{UI[l]["skip"]}</a>
<header class="bar">
  <div class="wrap bar-in">
    <a class="logo" href="{pg.href('home')}" aria-label="{e(UI[l]['name'])} – {UI[l]['home']}"><img src="{pg.b}img/logo-white.svg" alt="{e(UI[l]['name'])}" width="200" height="42"></a>
    <nav class="nav" id="menu" aria-label="{e(UI[l]['name'])}">{links}<span class="langs">{lg}</span></nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu"><span></span><span></span><span class="vh">{UI[l]['menu']}</span></button>
  </div>
</header>'''


def page_head(pg, title, lead='', img=None, alt=''):
    title = title.replace('Gesellschaftsgründungen', 'Gesellschafts­gründungen')
    return f'''<div class="ph">
  <div class="ph-bg"><img src="{pg.b}img/{img or HEADIMG['home']}" alt="{e(alt)}" width="2000" height="833"></div>
  {top(pg)}
  <div class="wrap ph-in">
    <h1 id="h1" class="h1" data-load>{e(title)}</h1>
    {f'<p class="ph-lead" data-load style="--d:1">{e(lead)}</p>' if lead else ''}
  </div>
</div>
'''


def credits_html(pg):
    items = [f'<a href="{e(c["page"])}">{e(c["title"])}</a> · {e(c["creator"])}, {e(c["license"])}' for c in CREDITS]
    return f'<p class="credits">{X[pg.l]["pics"]}: ' + '; '.join(items) + '</p>' if items else ''


def offices_block(pg, cls='offs', maps=False):
    l = pg.l
    out = ''
    for name, ln in OFFICES[l]:
        q = '+'.join(ln[1:]).replace(' ', '+')
        route = f'<a class="route" href="https://www.google.com/maps/search/?api=1&amp;query={e(q)}" rel="noopener">{e(X[l]["maps"])}</a>' if maps else ''
        out += (f'<div class="off" data-reveal><h3>{e(name)}</h3><p>{"<br>".join(e(x) for x in ln)}</p>'
                f'<p>T <a href="tel:{TEL}">{TEL_H}</a><br>F {FAX_H}<br><a href="mailto:{MAIL}">{MAIL}</a></p>{route}</div>')
    return f'<div class="{cls}">{out}</div>'


def footer(pg):
    l = pg.l
    offs = ''.join(f'<div class="f-off"><h3>{e(nm.replace("Head Office ", "").replace("Office ", ""))}</h3><p>{"<br>".join(e(x) for x in ln)}</p>'
                   f'<p>T <a href="tel:{TEL}">{TEL_H}</a><br>F {FAX_H}<br><a href="mailto:{MAIL}">{MAIL}</a></p></div>' for nm, ln in OFFICES[l])
    other = 'en' if l == 'de' else 'de'
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      {offs}
      <div class="f-off"><h3>{e(X[l]['links'])}</h3><p><a href="{pg.href('imprint')}">{e(UI[l]['imprint'])}</a><br><a href="{pg.href('privacy')}">{e(UI[l]['privacy'])}</a><br><a href="{pg.href(pg.key, other)}" lang="{other}" hreflang="{other}">{'English' if l == 'de' else 'Deutsch'}</a></p></div>
    </div>
    <div class="foot-legal"><img src="{pg.b}img/logo-white.svg" alt="{e(UI[l]['name'])}" width="160" height="34" class="foot-logo"><p>©2026 Zanetti Rechtsanwälte</p><a class="made" href="https://naktz.com/" rel="noopener"><span>{MADE_BY[l]}</span><img src="{pg.b}img/naktz-logo.png" alt="Naktz Media" width="105" height="30"></a></div>
    {credits_html(pg)}
  </div>
</footer>
<script src="{pg.b}assets/site.js?v={VER}" defer></script>
</body>
</html>
"""


def services_list(l):
    out = []
    for i, s in enumerate(D[l]['services']):
        out.append(dict(s, icon=ICONS[i], uid=f"{s['id']}-{i}", de_only=(l == 'en' and s['title'] == 'Familienrecht')))
    return out


def team_img(m):
    return f"{m['img'].split('/')[-2]}_{os.path.basename(m['img'])}" if m.get('img') else ''


def roles(m):
    return [x.strip() for x in re.sub(r',\s*$', '', m['role']).split(',') if x.strip()]


def teaser_lines(m):
    return [T(x) for x in re.split(r'<br\s*/?>', m.get('teaser') or '') if T(x)]


def person_card(pg, m, i, link=False):
    rs = roles(m)
    tag, attr = ('a', f'href="{pg.href("team")}#m{i}"') if link else ('button', 'type="button" aria-haspopup="dialog"')
    return (f'<{tag} class="pcard" {attr} data-open="m{i}"><span class="pc-img"><img src="{pg.b}img/{team_img(m)}" alt="" width="800" height="660" loading="lazy"></span>'
            f'<span class="pc-name">{e(m["name"])}</span><span class="pc-role">{e(rs[-1] if rs else "")}</span></{tag}>')


def svc_rows(pg, items):
    return ''.join(f'<li><a href="{pg.href("services")}#{x["uid"]}"><img src="{pg.b}img/{x["icon"]}" alt="" width="28" height="28"><span>{e(x["title"])}</span>{ARR}</a></li>' for x in items)


# ------------------------------------------------------------------ home
H = {
 'de': dict(team_n='Fachleute im Team', offices_n='Standorte', offices_l='Zug · Zürich · Schwyz', awards='Top Anwaltskanzlei', awards_l='Bilanz & PME 2024 – 2026', partners_n='Partner', ex_fields='Rechtsgebiete', ex_fields_t='Rechtsgebiete', ex_pubs='Publikationen', intro_l='Beratung und Prozessführung aus einer Hand – in Baar, Regensdorf und Immensee.',
            fields='Unsere Rechtsgebiete', fields_sub='Von der Beratung bis zur Prozessführung – wählen Sie ein Gebiet für die ausführliche Beschreibung.',
            partners='Die Partner', partners_sub='Ein gewachsener Zusammenschluss erfahrener und spezialisierter Rechtsanwälte.', see='Zum ganzen Team',
            where='Drei Standorte, ein Team', where_sub='Sie erreichen uns wie folgt:', explore='Mehr entdecken'),
 'en': dict(team_n='people on the team', offices_n='offices', offices_l='Zug · Zürich · Schwyz', awards='Top Law Firm', awards_l='Bilanz & PME 2024 – 2026', partners_n='Partners', ex_fields='areas of law', ex_fields_t='Areas of law', ex_pubs='publications', intro_l='Advice and litigation from one team – in Baar, Regensdorf and Immensee.',
            fields='Our areas of law', fields_sub='From advice to litigation – choose an area for the full description.',
            partners='The partners', partners_sub='An established association of experienced and specialised lawyers.', see='Meet the whole team',
            where='Three offices, one team', where_sub='You can reach us as follows:', explore='Explore'),
}


def excerpt(h, n=150):
    t = T(re.search(r'<p>(.*?)</p>', h, re.S).group(1)) if re.search(r'<p>(.*?)</p>', h, re.S) else T(h)
    m = re.match(r'(.+?[.!?])(\s|$)', t)
    t = m.group(1) if m and len(m.group(1)) > 40 else t
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + ' …'


def page_home(l):
    pg = Page(l, 'home')
    d = D[l]
    n = nav_labels(l)
    h = H[l]
    q = re.search(r'<h3>(.*?)</h3>', d['quote'] or '', re.S)
    q = q.group(1) if q else d['quote']
    q_lines = [T(x) for x in re.split(r'<br\s*/?>', q) if T(x)]
    w = d['widgets']
    paras = [[T(x) for x in re.findall(r'<p>(.*?)</p>', x['html'], re.S) if T(x)] for x in w]
    pages = [('services', HEADIMG['services']), ('notary', HEADIMG['notary']), ('team', HEADIMG['team']),
             ('pubs', HEADIMG['pubs']), ('contact', HEADIMG['contact']), ('members', HEADIMG['members'])]
    svc = services_list(l)
    awards = ''.join(f'<img src="{pg.b}img/{f}" alt="{e(UI[l]["award"])} {y}" width="64" height="64">' for f, y in AWARDS)
    wid = ''
    for j, (x, ps) in enumerate(zip(w, paras)):
        wid += (f'<article class="widget glass" data-reveal><span class="w-n">{j + 1:02d}</span>'
                f'<h3 class="h3">{e(x["title"].rstrip(":"))}</h3>' + ''.join(f'<p>{e(t)}</p>' for t in ps) + '</article>')
    seals = ''.join(f'<li data-reveal><img src="{pg.b}img/{f}" alt="{e(UI[l]["award"])} {y} – {UI[l]["award_by"]}" width="900" height="900" loading="lazy"><span>{y}</span></li>' for f, y in AWARDS)
    yrs = sorted(y for f, y in AWARDS)
    fields = ''.join(f'<a class="field glass" href="{pg.href("services")}#{x["uid"]}"{" lang=\"de\"" if x["de_only"] else ""} data-reveal><img src="{pg.b}img/{x["icon"]}" alt="" width="40" height="40"><b>{e(x["title"])}</b><span>{e(excerpt(x["html"]))}</span>{ARR}</a>' for x in svc)
    fields += f'<a class="field field-cta" href="{pg.href("services")}" data-reveal><b>{e(d["services_title"])}</b><span>{e(UI[l]["groups"][0])} · {e(UI[l]["groups"][1])}</span>{ARR}</a>'
    partners = [(i, m) for i, m in enumerate(d['team']) if 'Partner' in ' '.join(roles(m))]
    intro_faces = ''.join(f'<img src="{pg.b}img/{team_img(m)}" alt="" width="800" height="660" loading="lazy">' for i, m in partners)
    pcards = ''.join(f'<li data-reveal>{person_card(pg, m, i, True)}</li>' for i, m in partners)
    heads = lambda k: [T(x) for x in re.findall(r'<h2>(.*?)</h2>', d[k], re.S)]
    desc = {
        'services': f"{len(svc)} {h['ex_fields']} · {UI[l]['groups'][0]} & {UI[l]['groups'][1]}",
        'notary': heads('notary')[-1],
        'team': f"{len(d['team'])} {h['team_n']}",
        'pubs': f"{sum(len(x['items']) for x in d['pubs'])} {h['ex_pubs']}",
        'contact': f"{h['offices_l']} · {TEL_H}",
        'members': heads('members')[0],
    }
    rows = ''.join(f'<li><a href="{pg.href(k)}" data-ex="{j}"{" class=\"on\"" if j == 0 else ""}><span class="ex-n">{j + 1:02d}</span><span class="ex-t"><b>{e(n[k])}</b><small>{e(desc[k])}</small></span>'
                   f'<img class="ex-thumb" src="{pg.b}img/{im}" alt="" width="2000" height="833" loading="lazy">{ARR}</a></li>' for j, (k, im) in enumerate(pages))
    frames = ''.join(f'<img src="{pg.b}img/{im}" alt="" width="2000" height="833" loading="lazy" data-ex="{j}"{" class=\"on\"" if j == 0 else ""}>' for j, (k, im) in enumerate(pages))
    s = head(pg, f"{UI[l]['name']} – Zug · Zürich · Schwyz", T(d['home_title']))
    s += '<body class="home">\n'
    s += f"""<div class="ph home-ph">
  <div class="ph-bg"><img src="{pg.b}img/{HEADIMG['home']}" alt="" width="2000" height="1111"></div>
  {top(pg)}
  <div class="wrap ph-in">
    <blockquote class="hq"><p data-load>{e(" ".join(q_lines))}</p><footer data-load style="--d:2">{e(UI[l]['quote_by'])}</footer></blockquote>
    <div class="facts glass" data-load style="--d:3">
      <div><b>{len(d['team'])}</b><span>{e(h['team_n'])}</span></div>
      <div><b>{len(OFFICES[l])}</b><span>{e(h['offices_n'])} · {e(h['offices_l'])}</span></div>
      <div class="f-aw"><span class="aw">{awards}</span><span>{e(h['awards'])}<br>{e(h['awards_l'])}</span></div>
    </div>
  </div>
</div>
<main id="main">
<section class="sec intro mesh"><div class="wrap intro-in">
  <div class="intro-l">
    <h1 id="h1" class="h2" data-reveal>{e(T(d['home_title']))}</h1>
    <p class="lead" data-reveal>{e(h['intro_l'])}</p>
    <p class="intro-acts" data-reveal><a class="btn" href="{pg.href('services')}">{e(d['services_title'])}{ARR}</a><a class="btn line" href="{pg.href('team')}">{e(h['see'])}</a></p>
  </div>
  <div class="intro-art" data-reveal>
    <div class="ia-photo"><img src="{pg.b}img/{HEADIMG['pubs']}" alt="" width="2000" height="833" loading="lazy"></div>
    <a class="ia-badge ia-team glass" href="{pg.href('team')}"><span class="ia-faces">{intro_faces}</span><span><b>{len(partners)} {e(h['partners_n'])}</b><small>{len(d['team'])} {e(h['team_n'])}</small></span></a>
    <a class="ia-badge ia-fields glass" href="{pg.href('services')}"><b>{len(svc)}</b><span><b>{e(h['ex_fields_t'])}</b><small>{e(UI[l]['groups'][0])} &amp; {e(UI[l]['groups'][1])}</small></span></a>
  </div>
</div></section>
<section class="sec photo-sec" aria-labelledby="w-h"><div class="sec-bg"><img src="{pg.b}img/{HEADIMG['services']}" alt="" width="2000" height="833" loading="lazy"></div><div class="wrap">
  <div class="aw-band glass">
    <div class="aw-copy" data-reveal><small>{e(UI[l]['award_by'])} · Statista</small><h2 id="w-h" class="h2">{e(UI[l]['award'])}</h2><p>{' · '.join(AWARD_YEARS)}</p></div>
    <ul class="aw-seals">{seals}</ul>
  </div>
  <div class="widgets">{wid}</div>
</div></section>
<section class="sec mesh" aria-labelledby="f-h"><div class="wrap">
  <div class="sec-head"><h2 id="f-h" class="h2" data-reveal>{e(h['fields'])}</h2><p class="lead" data-reveal>{e(h['fields_sub'])}</p></div>
  <div class="fields">{fields}</div>
</div></section>
<section class="sec" aria-labelledby="p-h"><div class="wrap">
  <div class="sec-head row"><div><h2 id="p-h" class="h2" data-reveal>{e(h['partners'])}</h2><p class="lead" data-reveal>{e(h['partners_sub'])}</p></div><a class="btn line" href="{pg.href('team')}" data-reveal>{e(h['see'])}{ARR}</a></div>
  <ul class="partners">{pcards}</ul>
</div></section>
<section class="sec photo-sec where" aria-labelledby="o-h"><div class="sec-bg"><img src="{pg.b}img/{HEADIMG['contact']}" alt="" width="2000" height="833" loading="lazy"></div><div class="wrap">
  <div class="sec-head light"><h2 id="o-h" class="h2" data-reveal>{e(h['where'])}</h2><p class="lead" data-reveal>{e(h['where_sub'])} <a href="tel:{TEL}">{TEL_H}</a> · <a href="mailto:{MAIL}">{MAIL}</a></p></div>
  {offices_block(pg, 'offs glassy', True)}
</div></section>
<section class="sec explore" aria-labelledby="t-h"><div class="wrap ex-in">
  <div class="ex-list"><h2 id="t-h" class="h2" data-reveal>{e(h['explore'])}</h2><ol>{rows}</ol></div>
  <div class="ex-media" aria-hidden="true" data-reveal>{frames}</div>
</div></section>
</main>
"""
    s += footer(pg)
    return s


# ------------------------------------------------------------------ services
def page_services(l):
    pg = Page(l, 'services')
    d = D[l]
    svc = services_list(l)
    groups = [(UI[l]['groups'][0], [x for x in svc if x['group'] == 'beratung']), (UI[l]['groups'][1], [x for x in svc if x['group'] == 'prozess'])]
    idx = ''
    for g, items in groups:
        for x in items:
            lang = ' lang="de"' if x['de_only'] else ''
            idx += f'<a href="#{x["uid"]}"{lang}><span class="ix-ic"><img src="{pg.b}img/{x["icon"]}" alt="" width="40" height="40"></span><span class="ix-t"><b>{e(x["title"])}</b><small lang="{l}">{e(g)}</small></span>{ARR}</a>'
    idx += f'<a class="ix-cta" href="{pg.href("contact")}"><span class="ix-t"><b>{e(UI[l]["contact_cta"])}</b><small>{TEL_H}</small></span>{ARR}</a>'
    secs = ''
    for x in svc:
        lang = ' lang="de"' if x['de_only'] else ''
        note = f'<p class="de-note" lang="{l}">{e(X[l]["de_note"])}</p>' if x['de_only'] else ''
        secs += f"""<article class="svc" id="{x['uid']}"{lang}>
  <div class="svc-h"><img src="{pg.b}img/{x['icon']}" alt="" width="40" height="40"><h2 class="h3">{e(x['title'])}</h2></div>
  <div class="svc-b" id="{x['uid']}-b">{note}<div class="rich">{body_html(x['html'])}</div></div>
  <button class="svc-more" type="button" aria-expanded="false" aria-controls="{x['uid']}-b" data-less="{e(X[l]['less'])}">{e(X[l]['readmore'])}</button>
</article>
"""
    s = head(pg, f"{d['nav'][0]} · {UI[l]['name']}", d['services_title'])
    s += '<body class="has-over">\n' + page_head(pg, d['services_title'], '', HEADIMG['services'])
    s += f'<main id="main">\n<section class="over"><div class="wrap"><nav class="index glass-light" aria-label="{e(d["services_title"])}">{idx}</nav></div></section>\n<section class="sec tint"><div class="wrap svcs">{secs}</div></section>\n'
    s += '</main>\n' + footer(pg)
    return s


def doc_blocks(body):
    """Split an imported text page into (intro html, [(title, html)], closing line)."""
    body = re.sub(r'<li>\s*<ul>(.*?)</ul>\s*</li>', r'\1', body, flags=re.S)
    body = re.sub(r'<p><strong>([^<]+)</strong>\s*<br\s*/?>\s*', r'<p><strong>\1</strong></p><p>', body)
    parts = re.split(r'<p><strong>([^<]+)</strong></p>', body)
    intro, blocks, closing = parts[0].strip(), [], ''
    for t, h in zip(parts[1::2], parts[2::2]):
        t = T(t).rstrip(':').strip()
        blocks.append([t, h.strip()])
    if blocks and not blocks[-1][1]:
        closing = blocks.pop()[0]
    if blocks:
        last = blocks[-1][1]
        m = re.search(r'<p>([^<]{8,80})</p>\s*$', last)
        if m and '</ul>' in last:
            closing, blocks[-1][1] = T(m.group(1)), last[:m.start()].strip()
    return intro, blocks, closing


def page_generic(l, key, src, img=None):
    pg = Page(l, key)
    d = D[l]
    heads, body = section_parts(d[src])
    title = heads[0].rstrip(' –') if heads else nav_labels(l).get(key, key)
    lead = ' '.join(heads[1:]) if len(heads) > 1 else ''
    intro, blocks, closing = doc_blocks(body)
    s = head(pg, f"{title} · {UI[l]['name']}", T(body)[:200])
    if key == 'notary':
        label = next((t for t, h in blocks if not h), '')
        blocks = [(t, h) for t, h in blocks if h]
        icons = ['1044_gesellschaftsrecht.svg', '1048_familienrecht.svg', '1050_notariat.svg']
        paras = re.findall(r'<p>(.*?)</p>', intro, re.S)
        kicker = T(paras[0]) if paras and len(T(paras[0])) < 110 else ''
        paras = paras[1:] if kicker else paras
        cards = ''.join(f'<article class="nb glass-light" data-reveal><img src="{pg.b}img/{icons[i % 3]}" alt="" width="48" height="48"><h3 class="h3">{e(t)}</h3><div class="rich">{h}</div></article>' for i, (t, h) in enumerate(blocks))
        s += '<body>\n' + page_head(pg, title, lead, img)
        s += f"""<main id="main">
<section class="sec"><div class="wrap n-intro">
  <div class="n-lead" data-reveal>{f'<p class="n-kicker">{e(kicker)}</p>' if kicker else ''}{''.join(f'<p>{e(T(x))}</p>' for x in paras)}</div>
  <aside class="n-side glass" data-reveal><img src="{pg.b}img/1050_notariat.svg" alt="" width="56" height="56"><p class="n-close">{e(closing)}</p><a class="btn white" href="{pg.href('contact')}">{e(UI[l]['contact_cta'])}{ARR}</a><a class="link light" href="{pg.href('team')}">{e(nav_labels(l)['team'])}</a></aside>
</div></section>
<section class="sec tint"><div class="wrap">
  {f'<h2 class="h2 sec-head" data-reveal>{e(label)}</h2>' if label else ''}
  <div class="nbs">{cards}</div>
</div></section>
"""
    else:
        toc = ''.join(f'<a href="#b{i}">{e(t)}</a>' for i, (t, h) in enumerate(blocks))
        secs = ''.join(f'<section class="db" id="b{i}" data-reveal><h2 class="h3">{e(t)}</h2><div class="rich">{h}</div></section>' for i, (t, h) in enumerate(blocks))
        long = len(T(body)) > 900
        s += '<body>\n' + page_head(pg, title, lead, img)
        if long:
            s += f'<main id="main">\n<section class="sec tint"><div class="wrap doc">{"<nav class=\"doc-toc\" aria-label=\"" + e(title) + "\">" + toc + "</nav>" if len(blocks) > 1 else ""}<div class="doc-body glass-light">{f"<div class=\"rich\">{intro}</div>" if intro else ""}{secs}</div></div></section>\n'
        else:
            s += f'<main id="main">\n<section class="sec tint"><div class="wrap"><div class="dcards">{"".join(f"<section class=\"db glass-light\" data-reveal><h2 class=\"h3\">{e(t)}</h2><div class=\"rich\">{h}</div></section>" for t, h in blocks)}</div></div></section>\n'
    s += '</main>\n' + footer(pg)
    return s


def page_notary(l):
    return page_generic(l, 'notary', 'notary', HEADIMG['notary'])


def page_members(l):
    pg = Page(l, 'members')
    d = D[l]
    heads, body = section_parts(d['members'])
    lna = re.search(r'<p><strong>(.*?)</strong>(.*?)</p>\s*<p>(<a.*?</a>)</p>', body, re.S)
    rest = re.findall(r'<p>([^<]+)</p>\s*<p>(<a [^>]*>[^<]*</a>)</p>', body)
    logos = {'advokaten': '1114_advokatenverein_500px.jpg', 'sav': '1115_sav_fsa_logo_500px.jpg', 'zav': '1116_zuercher_anwaltsverband_500px.jpg'}
    cards = ''
    for name, a in rest:
        href = re.search(r'href="([^"]+)"', a).group(1)
        logo = next((v for k, v in logos.items() if k in href), '')
        cards += f'<a class="assoc" href="{e(href)}" rel="noopener" data-reveal><span class="as-logo"><img src="{pg.b}img/{logo}" alt="" width="480" height="120" loading="lazy"></span><b>{e(T(name))}</b><span class="link">{e(T(a))}</span></a>'
    title = ' '.join(heads)
    lna_href = re.search(r'href="([^"]+)"', lna.group(3)).group(1)
    s = head(pg, f"{d['nav'][5]} · {UI[l]['name']}", title)
    s += '<body class="has-over">\n' + page_head(pg, d['nav'][5], title, HEADIMG['members'])
    s += f'''<main id="main">
<section class="over"><div class="wrap"><div class="lna glass-light">
  <span class="lna-tile"><img class="lna-logo" src="{pg.b}img/1033_lna_logo_500px.180x0-is.jpg" alt="Legal Netlink Alliance" width="180" height="62"></span>
  <div>
    <h2 class="h2">{e(T(lna.group(1)))}</h2>
    <p class="lead">{e(T(lna.group(2)))}</p>
    <p><a class="btn" href="{e(lna_href)}" rel="noopener">{e(T(lna.group(3)))}{ARR}</a></p>
  </div>
</div></div></section>
<section class="sec tint"><div class="wrap assocs">{cards}</div></section>
'''
    s += '</main>\n' + footer(pg)
    return s


TEAM_G = {'de': ['Partner', 'Rechtsanwältinnen und Rechtsanwälte', 'Fachleute und Mitarbeitende'],
          'en': ['Partners', 'Attorneys', 'Specialists and staff']}


def page_team(l):
    pg = Page(l, 'team')
    d = D[l]
    groups = {k: '' for k in TEAM_G[l]}
    dialogs = ''
    for i, m in enumerate(d['team']):
        f = team_img(m)
        rs = roles(m)
        tl = teaser_lines(m)
        mail = f'<p><a href="mailto:{e(m["email"])}">{e(m["email"])}</a></p>' if m['email'] else ''
        g = 0 if 'Partner' in ' '.join(roles(m)) else 1 if re.search(r'Rechtsanw|Attorney|Lawyer', m['role']) else 2
        groups[list(TEAM_G[l])[g]] += f'''<li class="member" data-reveal>
  <button class="m-pic" type="button" data-open="m{i}" aria-haspopup="dialog" aria-label="{e(X[l]['bio'])}: {e(m['name'])}"><img src="{pg.b}img/{f}" alt="" width="800" height="660" loading="lazy"></button>
  <h2 class="h3">{e(m['name'])}</h2>
  <p class="m-role">{e(', '.join(rs))}</p>
  {f'<ul class="m-cv">' + ''.join(f'<li>{e(x)}</li>' for x in tl) + '</ul>' if tl else ''}
  <p class="m-acts"><button class="link" type="button" data-open="m{i}" aria-haspopup="dialog">{e(X[l]['bio'])}</button>{f'<a class="link" href="mailto:{e(m["email"])}">{e(X[l]["mail_person"])}</a>' if m['email'] else ''}</p>
</li>'''
        dialogs += f'''<dialog class="t-dialog" id="m{i}" aria-labelledby="m{i}-h">
  <div class="td-grid">
    <div class="td-side"><img src="{pg.b}img/{f}" alt="{e(m['name'])}" width="800" height="660" loading="lazy">
      <h2 id="m{i}-h" class="h3">{e(m['name'])}</h2><p class="m-role">{e(', '.join(rs))}</p>{mail}</div>
    <div class="rich">{body_html(m['bio'])}</div>
  </div>
  <form method="dialog"><button class="td-close" type="submit" aria-label="{e(UI[l]['close'])}">✕</button></form>
</dialog>
'''
    s = head(pg, f"{d['nav'][2]} · {UI[l]['name']}", d['team_title'])
    s += '<body class="team-page">\n' + page_head(pg, d['team_title'], UI[l]['team_hint'], HEADIMG['team'])
    body = ''.join(f'<section class="tg" aria-labelledby="tg{j}"><h2 id="tg{j}" class="tg-h" data-reveal>{e(t)}<span>{c.count("<li class=")}</span></h2><ul class="members">{c}</ul></section>' for j, (t, c) in enumerate(groups.items()) if c)
    s += f'<main id="main">\n<section class="sec tint team-sec"><div class="wrap">{body}</div></section>\n{dialogs}'
    s += '</main>\n' + footer(pg)
    return s


def page_pubs(l):
    pg = Page(l, 'pubs')
    d = D[l]
    idx = {m['name']: i for i, m in enumerate(d['team'])}
    blocks = ''
    for p in d['pubs']:
        items = ''.join(f'<li data-reveal><span class="y">{e(y)}</span><span><b>{e(t)}</b><span>{e(src)}</span></span></li>' for y, t, src in p['items'])
        i = idx.get(p['name'])
        who = person_card(pg, d['team'][i], i, True) if i is not None else f'<h2 class="h3">{e(p["name"])}</h2>'
        blocks += f'<section class="pub glass-light" aria-label="{e(p["name"])}"><div class="pub-who" data-reveal>{who}</div><ol class="plist">{items}</ol></section>'
    s = head(pg, f"{d['nav'][3]} · {UI[l]['name']}", d['pubs_title'])
    s += '<body>\n' + page_head(pg, d['pubs_title'], ' · '.join(p['name'] for p in d['pubs']), HEADIMG['pubs'])
    s += f'<main id="main">\n<section class="sec tint"><div class="wrap pubs">{blocks}</div></section>\n</main>\n' + footer(pg)
    return s


def page_contact(l):
    pg = Page(l, 'contact')
    d = D[l]
    heads, body = section_parts(d['contact'])
    intro = T(re.search(r'<p>(.*?)</p>', body, re.S).group(1))
    notes = re.findall(r'<p>\((.*?)\)</p>', body, re.S)
    note = f'({T(notes[0])})' if notes else ''
    s = head(pg, f"{d['nav'][4]} · {UI[l]['name']}", intro)
    s += '<body class="has-over">\n' + page_head(pg, heads[0] if heads else d['nav'][4], intro, HEADIMG['contact'])
    s += f'''<main id="main">
<section class="over"><div class="wrap">
  <div class="lines glass-light">
    <a href="tel:{TEL}" data-reveal><span>{e(X[l]['call'])}</span><b>{TEL_H}</b></a>
    <a href="mailto:{MAIL}" data-reveal><span>{e(X[l]['mail'])}</span><b>{MAIL}</b></a>
    <div data-reveal><span>{e(X[l]['fax'])}</span><b>{FAX_H}</b></div>
  </div>
  <p class="note">{e(note)}</p>
</div></section>
<section class="sec tint"><div class="wrap contact-grid">
  <div>{offices_block(pg, 'offs stack', True)}</div>
  <div class="map" data-reveal><iframe title="Google Maps – Zanetti Rechtsanwälte AG, Baar" src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d10840.119222836278!2d8.5708996!3d47.2159991!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xa08f4c2cdbca22ee!2sZanetti+Rechtsanw%C3%A4lte+AG!5e0!3m2!1sde!2sch!4v1552574030713" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>
'''
    s += '</main>\n' + footer(pg)
    return s


def write(rel, s):
    p = os.path.join(OUT, rel, 'index.html')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


css = open(os.path.join(ROOT, '_src/zl4.css'), encoding='utf-8').read()
VER = __import__('hashlib').md5((css + open(os.path.join(OUT, 'assets/site.js'), encoding='utf-8').read() + open(__file__, encoding='utf-8').read()).encode()).hexdigest()[:8]
open(os.path.join(OUT, 'assets/site.css'), 'w', encoding='utf-8', newline='\n').write(css)

for l in ('de', 'en'):
    write(SLUG[l]['home'], page_home(l))
    write(SLUG[l]['services'], page_services(l))
    write(SLUG[l]['notary'], page_notary(l))
    write(SLUG[l]['team'], page_team(l))
    write(SLUG[l]['pubs'], page_pubs(l))
    write(SLUG[l]['contact'], page_contact(l))
    write(SLUG[l]['members'], page_members(l))
    write(SLUG[l]['imprint'], page_generic(l, 'imprint', 'imprint'))
    write(SLUG[l]['privacy'], page_generic(l, 'privacy', 'privacy'))
print('built zanettilaw')
