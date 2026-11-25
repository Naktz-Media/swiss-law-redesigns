"""Builds the zanettilaw.ch redesign from _data/zl.json into zanettilaw/ (DE at the root, EN in en/)."""
import json, re, html, os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'zanettilaw')
D = json.load(open(os.path.join(ROOT, '_data/zl.json'), encoding='utf-8'))

KEYS = ['services', 'notary', 'team', 'pubs', 'contact', 'members']
SLUG = {
 'de': dict(home='', services='dienstleistung/', notary='beurkundungen/', team='team/', pubs='publikationen/',
            contact='kontakt/', members='mitgliedschaften/', imprint='impressum/', privacy='datenschutz/'),
 'en': dict(home='en/', services='en/services/', notary='en/memberships-1/', team='en/team/', pubs='en/publications/',
            contact='en/contact/', members='en/memberships/', imprint='en/imprint/', privacy='en/data-protection/'),
}
HEADIMG = dict(home='1_zanetti_home_2x-2.jpg', services='1028_zanetti_dienstleistungen_2x_neu.jpg', notary='1198_shutterstock_364368866.jpg',
               team='1029_zanetti_team_2x-2.jpg', pubs='1030_zanetti_publikationen_2x.jpg', contact='1032_zanetti_kontakt_2x-1.jpg',
               members='1033_zanetti_mitgliedschaften_2x.jpg')
ICONS = ['1045_arbeitsrecht.svg', '1048_familienrecht.svg', '1048_familienrecht.svg', '1049_vertragsrecht.svg', '1044_gesellschaftsrecht.svg',
         '1046_strafrecht.svg', '1047_steuerrecht.svg', '1050_notariat.svg', '1052_zivilprozess.svg', '1053_schuldbetreuung.svg', '1051_schiedsverfahren.svg']
AWARDS = [('1037_pme_bilanz_takch2026_logo_de_ausgabe.jpg', '2026'), ('1038_pme_bilanz_takch2025_logo_de_ausgabe_zugeschnitten.jpg', '2025'),
          ('1039_pme_bilanz_takch2024_logo_de_ausgabe.png', '2024')]
OFFICES = {
 'de': [('Head Office Zug', ['Zanetti Rechtsanwälte AG', 'Blegistrasse 9', '6340 Baar, Zug']),
        ('Office Zürich', ['Zanetti Rechtsanwälte AG', 'Allmendstrasse 2', '8105 Regensdorf, Zürich']),
        ('Office Schwyz', ['Zanetti Rechtsanwälte AG', 'Dorfplatz 2b', '6405 Immensee'])],
 'en': [('Head Office Zug', ['Zanetti Rechtsanwälte AG', 'Blegistrasse 9', '6340 Baar, Zug']),
        ('Office Zürich', ['Zanetti Rechtsanwälte AG', 'Allmendstrasse 2', '8105 Regensdorf, Zürich']),
        ('Office Schwyz', ['Zanetti Rechtsanwälte AG', 'Glorihöchi 4', '6403 Küssnacht am Rigi, Schwyz'])],
}
UI = {
 'de': dict(name='Zanetti Rechtsanwälte', menu='Menü', groups=['Beratung', 'Prozessführung'], more='Mehr', close='Schliessen',
            contact_cta='Kontakt aufnehmen', write='Schreiben Sie uns', write_sub='Ihre Nachricht öffnet sich in Ihrem E-Mail-Programm, adressiert an info@zanettilaw.ch.',
            f_name='Name', f_mail='E-Mail', f_phone='Telefon', f_msg='Ihr Anliegen', send='Nachricht vorbereiten',
            imprint='Impressum', privacy='Datenschutz', lang='Sprache', award='Top Anwaltskanzlei', award_by='Bilanz & PME',
            portrait='Porträt', team_hint='Name wählen für Werdegang, Sprachen und Kontakt', items='{n} Gebiete', pubs_n='{n} Publikationen',
            quote_by='Mahatma Gandhi (1869 – 1948)', skip='Zum Inhalt', home='Startseite', phone_l='Telefon', fax_l='Fax', all_services='Alle Dienstleistungen'),
 'en': dict(name='Zanetti Attorneys at Law', menu='Menu', groups=['Advisory', 'Litigation'], more='More', close='Close',
            contact_cta='Get in touch', write='Write to us', write_sub='Your message opens in your e-mail program, addressed to info@zanettilaw.ch.',
            f_name='Name', f_mail='E-mail', f_phone='Phone', f_msg='Your matter', send='Prepare message',
            imprint='Imprint', privacy='Data protection', lang='Language', award='Top Law Firm', award_by='Bilanz & PME',
            portrait='Portrait', team_hint='Choose a name for background, languages and contact', items='{n} areas', pubs_n='{n} publications',
            quote_by='Mahatma Gandhi (1869 – 1948)', skip='Skip to content', home='Home', phone_l='Phone', fax_l='Fax', all_services='All services'),
}

e = lambda s: html.escape(s or '', quote=True)
T = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))).strip()


def body_html(h):
    """Tidy imported rich text: demote headings, drop empty nodes and asset paths."""
    h = re.sub(r'</?(div|section|main|picture|source)[^>]*>', '', h)
    h = re.sub(r'<h1>(.*?)</h1>', r'<h3>\1</h3>', h)
    h = re.sub(r'<h4>(.*?)</h4>', r'<h3>\1</h3>', h)
    h = re.sub(r'<p>\s*(<br\s*/?>\s*)*</p>', '', h)
    h = re.sub(r'<p>\s*<img[^>]*>\s*</p>', '', h)
    h = re.sub(r'<p>(<br\s*/?>\s*)+', '<p>', h)
    h = h.replace('<ul> <li></li>', '<ul>').replace('<li></li>', '')
    h = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" rel="noopener"', h)
    return h.strip()


def section_parts(h):
    """From an imported page: (headings, body html) of the main <section>."""
    m = re.search(r'<section>(.*)</section>', h, re.S)
    s = m.group(1) if m else h
    heads = [T(x) for x in re.findall(r'<h2>(.*?)</h2>', s, re.S)]
    s = re.sub(r'<h2>.*?</h2>', '', s, flags=re.S)
    s = re.sub(r'<iframe.*?</iframe>', '', s, flags=re.S)
    s = re.sub(r'</?div>', '', s)
    return heads, body_html(s)


class Page:
    def __init__(self, l, key):
        self.l, self.key = l, key
        self.depth = SLUG[l][key].count('/')
        self.b = '../' * self.depth

    def href(self, key, l=None):
        target = SLUG[l or self.l][key]
        return (self.b + target) if target else (self.b or './')


def nav_labels(l):
    return dict(zip(KEYS, D[l]['nav']))


def head(pg, title, desc):
    l = pg.l
    alt = ''.join(f'<link rel="alternate" hreflang="{x}" href="{pg.href(pg.key, x)}">' for x in ('de', 'en'))
    return f'''<!doctype html>
<html lang="{l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc[:300])}">
{alt}
<link rel="icon" href="{pg.b}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pg.b}assets/site.css">
<script>document.documentElement.classList.add('js')</script>
</head>
'''


def langs(pg):
    out = []
    for x, lab in (('de', 'DE'), ('en', 'EN')):
        cur = ' aria-current="true"' if x == pg.l else ''
        out.append(f'<a href="{pg.href(pg.key, x)}" hreflang="{x}" lang="{x}"{cur}>{lab}</a>')
    return f'<nav class="langs" aria-label="{UI[pg.l]["lang"]}">{"".join(out)}</nav>'


def topbar(pg, home=False):
    """Header band: logo, language, and the navigation as folder tabs."""
    l = pg.l
    n = nav_labels(l)
    tabs = ''.join(f'<a class="tab" href="{pg.href(k)}"{" aria-current=\"page\"" if k == pg.key else ""}>{e(n[k])}</a>' for k in KEYS)
    return f'''<a class="skip" href="#main">{UI[l]["skip"]}</a>
<header class="band-head{' is-home' if home else ''}">
  <div class="bh-row">
    {langs(pg)}
    <a class="logo" href="{pg.href('home')}" aria-label="{e(UI[l]['name'])} – {UI[l]['home']}"><img src="{pg.b}img/logo-white.svg" alt="{e(UI[l]['name'])}" width="220" height="46"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="tabs">{UI[l]['menu']}</button>
  </div>
  <nav class="tabs" id="tabs" aria-label="{e(UI[l]['name'])}">{tabs}</nav>
</header>
'''


def offices_html(l, cls='offices'):
    out = []
    for name, lines in OFFICES[l]:
        out.append(f'<div class="office"><h3>{e(name)}</h3><p>{"<br>".join(e(x) for x in lines)}</p></div>')
    return f'<div class="{cls}">{"".join(out)}</div>'


def coupon(pg, heading_tag='h2'):
    l = pg.l
    u = UI[l]
    return f'''<section class="coupon-wrap" aria-labelledby="cp-h">
  <form class="coupon" data-mailto="info@zanettilaw.ch" data-reveal>
    <span class="notch n1" aria-hidden="true"></span><span class="notch n2" aria-hidden="true"></span>
    <div class="cp-left">
      <{heading_tag} id="cp-h" class="cp-h">{e(u['write'])}</{heading_tag}>
      <div class="cp-contact">
        <p>Zanetti Rechtsanwälte AG<br>Blegistrasse 9, 6340 Baar</p>
        <p><a href="tel:+41417663585">T +41 41 766 35 85</a><br>F +41 41 766 35 80<br><a href="mailto:info@zanettilaw.ch">info@zanettilaw.ch</a></p>
      </div>
    </div>
    <div class="cp-right">
      <label class="vh" for="cp-name">{e(u['f_name'])}</label><input id="cp-name" name="name" placeholder="{e(u['f_name'])}" autocomplete="name" required>
      <label class="vh" for="cp-mail">{e(u['f_mail'])}</label><input id="cp-mail" name="email" type="email" placeholder="{e(u['f_mail'])}" autocomplete="email">
      <label class="vh" for="cp-phone">{e(u['f_phone'])}</label><input id="cp-phone" name="phone" type="tel" placeholder="{e(u['f_phone'])}" autocomplete="tel">
      <label class="vh" for="cp-msg">{e(u['f_msg'])}</label><textarea id="cp-msg" name="message" rows="3" placeholder="{e(u['f_msg'])}" required></textarea>
      <button class="cp-send" type="submit">{e(u['send'])}</button>
      <p class="cp-note" id="cp-note">{e(u['write_sub'])}</p>
    </div>
  </form>
</section>
'''


def footer(pg):
    l = pg.l
    n = nav_labels(l)
    letters = 'ZANETTI'
    heights = [100, 78, 92, 66, 86, 72, 96]
    blocks = ''.join(f'<span style="--h:{h}%">{c}</span>' for c, h in zip(letters, heights))
    links = ''.join(f'<a href="{pg.href(k)}">{e(n[k])}</a>' for k in KEYS)
    offs = ''.join(f'<div><b>{e(nm.replace("Head Office ", "").replace("Office ", ""))}</b><br>{"<br>".join(e(x) for x in ln[1:])}</div>' for nm, ln in OFFICES[l])
    return f'''<footer class="foot">
  <div class="blocks" aria-hidden="true">{blocks}</div>
  <div class="foot-grid">
    <nav class="foot-links" aria-label="{e(UI[l]['name'])}">{links}</nav>
    <div class="foot-offices">{offs}</div>
    <div class="foot-contact"><a href="tel:+41417663585">T +41 41 766 35 85</a><br>F +41 41 766 35 80<br><a href="mailto:info@zanettilaw.ch">info@zanettilaw.ch</a></div>
  </div>
  <div class="foot-last">
    <p>© 2026 {e(UI[l]['name'])} · <a href="{pg.href('imprint')}">{e(UI[l]['imprint'])}</a> · <a href="{pg.href('privacy')}">{e(UI[l]['privacy'])}</a></p>
    <a class="btn btn-paper" href="{pg.href('contact')}">{e(UI[l]['contact_cta'])}</a>
  </div>
</footer>
<script src="{pg.b}assets/site.js" defer></script>
</body>
</html>
'''


def pagehead(pg, title, lead='', img=None, alt=''):
    pic = (f'<figure class="ph-pic" data-load><img class="folder" src="{pg.b}img/{img}" alt="{e(alt)}" width="2000" height="833"></figure>'
           if img else '')
    return f'''<section class="phead{' has-pic' if img else ''}" aria-labelledby="h1">
  <div class="ph-text">
    <h1 id="h1" class="ph-h" data-load>{e(title)}</h1>
    {f'<p class="ph-lead" data-load>{e(lead)}</p>' if lead else ''}
  </div>
  {pic}
</section>
'''


def services_list(l):
    out = []
    for i, s in enumerate(D[l]['services']):
        if l == 'en' and s['title'] == 'Familienrecht':
            continue  # untranslated German duplicate on the original English page
        out.append(dict(s, icon=ICONS[i], uid=f"{s['id']}-{i}"))
    return out


# ------------------------------------------------------------------ home
def page_home(l):
    pg = Page(l, 'home')
    d = D[l]
    n = nav_labels(l)
    quote = T(re.search(r'<h3>(.*?)</h3>', D[l]['quote'] or '', re.S).group(1)) if re.search(r'<h3>', D[l]['quote'] or '') else ''
    if not quote:
        quote = {'de': '«Wenn du im Recht bist, kannst du es dir leisten, die Ruhe zu bewahren; und wenn du im Unrecht bist, kannst du es dir nicht leisten, sie zu verlieren.»',
                 'en': '«When you are in the right, you can afford to keep your cool; and when you are wrong, you cannot afford to lose it.»'}[l]
    w = d['widgets']
    award_txt = ''
    w0 = re.findall(r'<p>(.*?)</p>', w[0]['html'], re.S)
    w0 = [T(x) for x in w0 if T(x)]
    first_text, award_txt = w0[0], (w0[1] if len(w0) > 1 else '')
    texts = [T(' '.join(re.findall(r'<p>(.*?)</p>', x['html'], re.S))) for x in w]
    folders = [('members', '#1b4466'), ('pubs', '#2f5a80'), ('team', '#7d96ab'), ('notary', '#c9c1b1'), ('services', '#f1efea')]
    fold_html = ''
    for i, (k, col) in enumerate(folders):
        fold_html += f'<a class="folder-band f{i}" href="{pg.href(k)}" style="--c:{col}"><span class="ftab">{e(n[k])}</span></a>'
    svc = services_list(l)
    groups = [(UI[l]['groups'][0], [s for s in svc if s['group'] == 'beratung']), (UI[l]['groups'][1], [s for s in svc if s['group'] == 'prozess'])]

    def first_sentence(h):
        t = T(re.search(r'<p>(.*?)</p>', h, re.S).group(1)) if re.search(r'<p>', h) else T(h)
        m = re.match(r'(.{40,}?[a-zäöüé)][.!?])\s+[A-ZÄÖÜ«]', t)
        if m and len(m.group(1)) < 220:
            return m.group(1)
        return t[:150].rsplit(' ', 1)[0] + ' …' if len(t) > 150 else t

    s = head(pg, f"{UI[l]['name']} – Baar, Zug · Zürich · Schwyz", T(d['home_title']))
    s += '<body class="home">\n' + topbar(pg, home=True)
    s += f'''<main id="main">
<section class="hero" aria-labelledby="h1">
  <div class="hero-text">
    <h1 id="h1" class="hero-h"><span class="mask"><span>{e(UI[l]['name'])}</span></span></h1>
    <p class="hero-sub" data-load>{e(T(d['home_title']))}</p>
  </div>
  <div class="stack" aria-label="{e(UI[l]['name'])}">{fold_html}</div>
</section>

<section class="front" aria-label="{e(n['services'])}">
  <figure class="quote" data-reveal>
    <blockquote><p>{e(quote)}</p></blockquote>
    <figcaption>{e(UI[l]['quote_by'])}</figcaption>
  </figure>
  <a class="btn btn-navy" href="{pg.href('services')}" data-reveal>{e(n['services'])}</a>
</section>

<section class="awards" aria-labelledby="aw-h">
  <div class="aw-head">
    <h2 id="aw-h" class="h2" data-reveal>{e(UI[l]['award'])}</h2>
    <p data-reveal>{e(award_txt)}</p>
  </div>
  <div class="aw-tiles">
    {''.join(f'<figure class="tile t{i}" data-reveal><div class="tile-box"><img src="{pg.b}img/{f}" alt="{e(UI[l]["award"])} {y} – {UI[l]["award_by"]}" width="900" height="900" loading="lazy"></div><figcaption><b>{e(UI[l]["award"])} {y}</b><span>{e(UI[l]["award_by"])}</span></figcaption></figure>' for i, (f, y) in enumerate(AWARDS))}
  </div>
</section>

<section class="panel" aria-labelledby="pn-h">
  <div class="panel-left">
    <h2 id="pn-h" class="panel-h" data-reveal>{e(w[0]['title'].rstrip(':'))}</h2>
    <p class="panel-p" data-reveal>{e(first_text)}</p>
    <figure class="panel-pic" data-reveal><img class="folder" src="{pg.b}img/{HEADIMG['home']}" alt="" width="2000" height="1111" loading="lazy"></figure>
  </div>
  <div class="panel-right">
    {''.join(f'<div class="pblock" data-reveal><h3>{e(x["title"].rstrip(":"))}</h3><p>{e(t)}</p></div>' for x, t in zip(w[1:], texts[1:]))}
    <a class="btn btn-paper" href="{pg.href('team')}" data-reveal>{e(n['team'])}</a>
  </div>
</section>

<section class="menu-list" aria-labelledby="sv-h">
  <h2 id="sv-h" class="h2" data-reveal>{e(d['services_title'])}</h2>
  {''.join(f"""<div class="mgroup">
    <div class="mg-head" data-reveal><h3>{e(g)}</h3><span>{e(UI[l]['items'].format(n=len(items)))}</span></div>
    <ul class="mitems">
      {''.join(f'<li data-reveal><a href="{pg.href("services")}#{x["uid"]}"><img src="{pg.b}img/{x["icon"]}" alt="" width="52" height="52"><span><b>{e(x["title"])}</b><span>{e(first_sentence(x["html"]))}</span></span></a></li>' for x in items)}
    </ul>
  </div>""" for g, items in groups)}
</section>
'''
    s += coupon(pg)
    s += '</main>\n' + footer(pg)
    return s


# ------------------------------------------------------------------ services
def page_services(l):
    pg = Page(l, 'services')
    d = D[l]
    svc = services_list(l)
    groups = [(UI[l]['groups'][0], [s for s in svc if s['group'] == 'beratung']), (UI[l]['groups'][1], [s for s in svc if s['group'] == 'prozess'])]
    idx = ''.join(f'<div class="ix-group"><h2>{e(g)}</h2><ul>' + ''.join(f'<li><a href="#{x["uid"]}">{e(x["title"])}</a></li>' for x in items) + '</ul></div>' for g, items in groups)
    secs = ''
    for x in svc:
        secs += f'''<article class="svc" id="{x['uid']}">
  <div class="svc-head" data-reveal><img src="{pg.b}img/{x['icon']}" alt="" width="56" height="56"><h2>{e(x['title'])}</h2></div>
  <div class="rich">{body_html(x['html'])}</div>
</article>
'''
    s = head(pg, f"{d['nav'][0]} · {UI[l]['name']}", d['services_title'])
    s += '<body>\n' + topbar(pg)
    s += '<main id="main">\n' + pagehead(pg, d['services_title'], ' · '.join(x['title'] for x in svc[:6]) + ' …', HEADIMG['services'])
    s += f'<section class="svc-wrap" aria-label="{e(d["services_title"])}"><nav class="index" aria-label="{e(d["services_title"])}">{idx}</nav><div class="svc-list">{secs}</div></section>\n'
    s += '</main>\n' + footer(pg)
    return s


def page_generic(l, key, src, img=None, extra=''):
    pg = Page(l, key)
    d = D[l]
    heads, body = section_parts(d[src])
    title = heads[0].rstrip(' –') if heads else nav_labels(l).get(key, key)
    lead = ' '.join(heads[1:]) if len(heads) > 1 else ''
    s = head(pg, f"{title} · {UI[l]['name']}", T(body)[:200])
    s += '<body>\n' + topbar(pg)
    s += '<main id="main">\n' + pagehead(pg, title, lead, img)
    card = f'''<aside class="card" data-reveal>
    <img class="folder" src="{pg.b}img/{HEADIMG['contact']}" alt="" width="2000" height="833" loading="lazy">
    <h2>{e(UI[l]['contact_cta'])}</h2>
    <p>Zanetti Rechtsanwälte AG<br>Blegistrasse 9, 6340 Baar</p>
    <p><a href="tel:+41417663585">T +41 41 766 35 85</a><br><a href="mailto:info@zanettilaw.ch">info@zanettilaw.ch</a></p>
    <a class="btn btn-paper" href="{pg.href('contact')}">{e(nav_labels(l)['contact'])}</a>
  </aside>'''
    s += f'<section class="textpage"><div class="rich">{body}</div>{extra}{card}</section>\n'
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
    rows = ''
    for name, a in rest:
        href = re.search(r'href="([^"]+)"', a).group(1)
        logo = next((v for k, v in logos.items() if k in href), '')
        rows += f'<li data-reveal><a href="{e(href)}" rel="noopener"><span class="m-logo"><img src="{pg.b}img/{logo}" alt="" width="480" height="120" loading="lazy"></span><span class="m-name">{e(T(name))}</span><span class="m-url">{e(T(a))}</span></a></li>'
    title = ' '.join(heads)
    s = head(pg, f"{d['nav'][5]} · {UI[l]['name']}", title)
    s += '<body>\n' + topbar(pg)
    s += '<main id="main">\n' + pagehead(pg, d['nav'][5], title, HEADIMG['members'])
    s += f'''<section class="lna" aria-labelledby="lna-h">
  <div class="lna-text"><h2 id="lna-h" class="h2" data-reveal>{e(T(lna.group(1)))}</h2><p data-reveal>{e(T(lna.group(2)))}</p><p data-reveal>{lna.group(3).replace('<a ', '<a rel="noopener" ')}</p></div>
  <figure class="lna-logo" data-reveal><img src="{pg.b}img/1033_lna_logo_500px.180x0-is.jpg" alt="Legal Netlink Alliance" width="180" height="62"></figure>
</section>
<section class="assoc" aria-label="{e(d['nav'][5])}"><ul>{rows}</ul></section>
'''
    s += '</main>\n' + footer(pg)
    return s


def page_team(l):
    pg = Page(l, 'team')
    d = D[l]
    rows, dialogs = '', ''
    for i, m in enumerate(d['team']):
        imgf = os.path.basename(m['img']).split('/')[-1]
        num = m['img'].split('/')[-2]
        fname = f'{num}_{imgf}'
        role = re.sub(r',\s*$', '', m['role'])
        mail = f'<p class="t-mail"><a href="mailto:{e(m["email"])}">{e(m["email"])}</a></p>' if m['email'] else ''
        rows += f'''<li data-reveal><button type="button" class="t-row" data-img="{pg.b}img/{fname}" data-dialog="m{i}" aria-haspopup="dialog">
  <img class="t-inline" src="{pg.b}img/{fname}" alt="" width="800" height="660" loading="lazy">
  <span class="t-name">{e(m['name'])}</span><span class="t-role">{e(role)}</span></button></li>'''
        dialogs += f'''<dialog class="t-dialog" id="m{i}" aria-labelledby="m{i}-h">
  <div class="td-grid">
    <div class="td-side"><img class="folder" src="{pg.b}img/{fname}" alt="{e(m['name'])}" width="800" height="660" loading="lazy">
      <h2 id="m{i}-h">{e(m['name'])}</h2><p>{e(role)}</p>{mail}</div>
    <div class="td-body rich">{body_html(m['bio'])}</div>
  </div>
  <form method="dialog"><button class="td-close" type="submit">{e(UI[l]['close'])}</button></form>
</dialog>
'''
    first = d['team'][0]
    ff = f"{first['img'].split('/')[-2]}_{os.path.basename(first['img'])}"
    s = head(pg, f"{d['nav'][2]} · {UI[l]['name']}", d['team_title'])
    s += '<body class="team-page">\n' + topbar(pg)
    s += '<main id="main">\n' + pagehead(pg, d['team_title'], UI[l]['team_hint'], HEADIMG['team'])
    s += f'''<section class="team" aria-label="{e(d['team_title'])}">
  <ol class="t-list">{rows}</ol>
  <figure class="t-frame" aria-hidden="true"><img class="folder" id="t-preview" src="{pg.b}img/{ff}" alt="" width="800" height="660"></figure>
</section>
{dialogs}'''
    s += '</main>\n' + footer(pg)
    return s


def page_pubs(l):
    pg = Page(l, 'pubs')
    d = D[l]
    photos = {m['name']: f"{m['img'].split('/')[-2]}_{os.path.basename(m['img'])}" for m in d['team']}
    blocks = ''
    for p in d['pubs']:
        items = ''.join(f'<li data-reveal><span class="p-year">{e(y)}</span><span class="p-t"><b>{e(t)}</b><span>{e(src)}</span></span></li>' for y, t, src in p['items'])
        ph = photos.get(p['name'])
        blocks += f'''<section class="pub" aria-labelledby="pb-{len(blocks)}">
  <div class="pub-who" data-reveal>{f'<img class="folder" src="{pg.b}img/{ph}" alt="" width="800" height="660" loading="lazy">' if ph else ''}<h2 id="pb-{len(blocks)}">{e(p['name'])}</h2><p>{e(UI[l]['pubs_n'].format(n=len(p['items'])))}</p></div>
  <ol class="pub-list">{items}</ol>
</section>
'''
    s = head(pg, f"{d['nav'][3]} · {UI[l]['name']}", d['pubs_title'])
    s += '<body>\n' + topbar(pg)
    s += '<main id="main">\n' + pagehead(pg, d['pubs_title'], ' · '.join(p['name'] for p in d['pubs']), HEADIMG['pubs'])
    s += blocks + '</main>\n' + footer(pg)
    return s


def page_contact(l):
    pg = Page(l, 'contact')
    d = D[l]
    heads, body = section_parts(d['contact'])
    intro = T(re.search(r'<p>(.*?)</p>', body, re.S).group(1))
    note = T(re.findall(r'<p>\((.*?)\)</p>', body, re.S)[0]) if re.findall(r'<p>\((.*?)\)</p>', body, re.S) else ''
    rows = ''
    for name, lines in OFFICES[l]:
        q = '+'.join(lines[1:]).replace(' ', '+')
        rows += f'''<li data-reveal><h2>{e(name)}</h2><a class="o-addr" href="https://www.google.com/maps/search/?api=1&amp;query={e(q)}" rel="noopener">{"<br>".join(e(x) for x in lines[1:])}</a></li>'''
    s = head(pg, f"{d['nav'][4]} · {UI[l]['name']}", intro)
    s += '<body>\n' + topbar(pg)
    s += '<main id="main">\n' + pagehead(pg, heads[0] if heads else d['nav'][4], intro, HEADIMG['contact'])
    s += f'''<section class="phones" aria-label="{e(d['nav'][4])}">
  <a class="big-line" href="tel:+41417663585" data-reveal>T +41 41 766 35 85</a>
  <a class="big-line" href="mailto:info@zanettilaw.ch" data-reveal>info@zanettilaw.ch</a>
  <p class="small-line" data-reveal>F +41 41 766 35 80 · ({e(note)})</p>
</section>
<section class="office-rows" aria-label="{e(heads[0] if heads else '')}"><ul>{rows}</ul>
  <div class="map" data-reveal><iframe title="Google Maps – Zanetti Rechtsanwälte AG, Baar" src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d10840.119222836278!2d8.5708996!3d47.2159991!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xa08f4c2cdbca22ee!2sZanetti+Rechtsanw%C3%A4lte+AG!5e0!3m2!1sde!2sch!4v1552574030713" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</section>
'''
    s += coupon(pg)
    s += '</main>\n' + footer(pg)
    return s


def write(rel, s):
    p = os.path.join(OUT, rel, 'index.html')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


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
