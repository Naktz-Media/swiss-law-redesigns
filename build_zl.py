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
            maps='Route planen', call='Telefon', mail='E-Mail', fax='Fax', links='Links', all_services='Alle Dienstleistungen',
            de_note='Dieser Abschnitt ist auf der englischen Seite der Kanzlei nur auf Deutsch verfügbar.', mail_person='E-Mail an'),
 'en': dict(about='About us', offices='Offices', bio='Background', all_team='Whole team', pics='Pictures', site='Pages',
            our_offices='Our offices', read='Learn more', ready='Ready for a first conversation?',
            ready_sub='Tell us about your matter. We will get back to you quickly and tell you openly how we can help.',
            maps='Plan route', call='Phone', mail='E-mail', fax='Fax', links='Links', all_services='All services',
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
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pg.b}assets/site.css?v={VER}">
<script>document.documentElement.classList.add('js')</script>
</head>
'''


def top(pg):
    l = pg.l
    n = nav_labels(l)
    links = ''.join(f'<a href="{pg.href(k)}"{" aria-current=\"page\"" if k == pg.key else ""}>{e(n[k])}</a>' for k in KEYS)
    lg = ''.join(f'<a href="{pg.href(pg.key, x)}" hreflang="{x}" lang="{x}"{" aria-current=\"true\"" if x == l else ""}>{x.upper()}</a>' for x in ('de', 'en'))
    return f'''<a class="skip" href="#main">{UI[l]["skip"]}</a>
<header class="bar">
  <div class="wrap bar-in">
    <a class="logo" href="{pg.href('home')}" aria-label="{e(UI[l]['name'])} – {UI[l]['home']}"><img src="{pg.b}img/logo.svg" alt="{e(UI[l]['name'])}" width="200" height="42"></a>
    <nav class="nav" id="menu" aria-label="{e(UI[l]['name'])}">{links}<span class="langs">{lg}</span></nav>
    <a class="tel" href="tel:{TEL}">{TEL_H}</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{UI[l]['menu']}</button>
  </div>
</header>'''


def page_head(pg, title, lead='', img=None, alt=''):
    pic = f'<figure class="band" data-load style="--d:2"><img src="{pg.b}img/{img}" alt="{e(alt)}" width="2000" height="833"></figure>' if img else ''
    return f'''{top(pg)}
<div class="wrap phead">
  <h1 id="h1" class="h1" data-load>{e(title)}</h1>
  {f'<p class="lead" data-load style="--d:1">{e(lead)}</p>' if lead else ''}
</div>
{pic}
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
        out += (f'<div class="off"><h3>{e(name)}</h3><p>{"<br>".join(e(x) for x in ln)}</p>'
                f'<p>T <a href="tel:{TEL}">{TEL_H}</a><br>F {FAX_H}<br><a href="mailto:{MAIL}">{MAIL}</a></p>{route}</div>')
    return f'<div class="{cls}">{out}</div>'


def contact_band(pg):
    l = pg.l
    u = UI[l]
    return f'''<section class="sec ask" aria-labelledby="cp-h"><div class="wrap ask-in">
  <div>
    <h2 id="cp-h" class="h2" data-reveal>{e(X[l]['ready'])}</h2>
    <p class="lead" data-reveal>{e(X[l]['ready_sub'])}</p>
    <p class="direct" data-reveal><a href="tel:{TEL}">{TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a></p>
  </div>
  <form class="coupon form" data-mailto="{MAIL}" data-reveal>
    <label for="cp-name">{e(u['f_name'])}<input class="inp" id="cp-name" name="name" autocomplete="name" required></label>
    <label for="cp-phone">{e(u['f_phone'])}<input class="inp" id="cp-phone" name="phone" type="tel" autocomplete="tel"></label>
    <label class="full" for="cp-mail">{e(u['f_mail'])}<input class="inp" id="cp-mail" name="email" type="email" autocomplete="email"></label>
    <label class="full" for="cp-msg">{e(u['f_msg'])}<textarea class="inp" id="cp-msg" name="message" rows="4" required></textarea></label>
    <button class="btn full" type="submit">{e(u['send'])}{ARR}</button>
    <p class="full note">{e(u['write_sub'])}</p>
  </form>
</div></section>
'''


def footer(pg):
    l = pg.l
    n = nav_labels(l)
    links = ''.join(f'<a href="{pg.href(k)}">{e(n[k])}</a>' for k in KEYS)
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <img src="{pg.b}img/logo-white.svg" alt="{e(UI[l]['name'])}" width="220" height="46" class="foot-logo">
      {offices_block(pg, 'offs foot-offs')}
    </div>
    <div class="foot-mid">
      <nav aria-label="{e(X[l]['site'])}">{links}</nav>
      <nav aria-label="{e(X[l]['links'])}"><a href="{pg.href('imprint')}">{e(UI[l]['imprint'])}</a><a href="{pg.href('privacy')}">{e(UI[l]['privacy'])}</a></nav>
      <nav aria-label="{UI[l]['lang']}"><a href="{pg.href(pg.key, 'de')}" lang="de">Deutsch</a><a href="{pg.href(pg.key, 'en')}" lang="en">English</a></nav>
    </div>
    <div class="foot-legal"><p>©2026 Zanetti Rechtsanwälte</p><a class="made" href="https://naktz.com/" rel="noopener"><span>{MADE_BY[l]}</span><img src="{pg.b}img/naktz-logo.png" alt="Naktz Media" width="105" height="30"></a></div>
    {credits_html(pg)}
  </div>
</footer>
<script src="{pg.b}assets/site.js?v={VER}" defer></script>
</body>
</html>
'''


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
def page_home(l):
    pg = Page(l, 'home')
    d = D[l]
    n = nav_labels(l)
    quote = T(re.search(r'<h3>(.*?)</h3>', d['quote'] or '', re.S).group(1))
    w = d['widgets']
    paras = [[T(x) for x in re.findall(r'<p>(.*?)</p>', x['html'], re.S) if T(x)] for x in w]
    award_txt = paras[0][1] if len(paras[0]) > 1 else ''
    paras[0] = paras[0][:1]
    svc = services_list(l)
    groups = [(UI[l]['groups'][0], [s for s in svc if s['group'] == 'beratung' and not s['de_only']]),
              (UI[l]['groups'][1], [s for s in svc if s['group'] == 'prozess'])]
    notary_txt = T(section_parts(d['notary'])[1])
    more = [('notary', HEADIMG['notary'], notary_txt[:notary_txt.find('.', 120) + 1] if '.' in notary_txt[120:] else notary_txt[:180]),
            ('pubs', HEADIMG['pubs'], d['pubs_title'] + ': ' + ', '.join(p['name'] for p in d['pubs']) + '.'),
            ('members', HEADIMG['members'], ' '.join(section_parts(d['members'])[0]))]

    s = head(pg, f"{UI[l]['name']} – Zug · Zürich · Schwyz", T(d['home_title']))
    s += '<body class="home">\n' + top(pg)
    s += f'''
<main id="main">
<section class="hero" aria-labelledby="h1"><div class="wrap hero-in">
  <div class="hero-text">
    <h1 id="h1" class="h1" data-load>Zanetti<br>Rechtsanwälte</h1>
    <p class="lead" data-load style="--d:1">{e(T(d['home_title']))}</p>
    <p class="acts" data-load style="--d:2"><a class="btn" href="{pg.href('contact')}">{e(UI[l]['contact_cta'])}{ARR}</a><a class="link" href="{pg.href('services')}">{e(d['services_title'])}</a></p>
    <div class="award" data-load style="--d:3">
      <div class="award-logos">{''.join(f'<img src="{pg.b}img/{f}" alt="{e(UI[l]["award"])} {y}" width="72" height="72">' for f, y in AWARDS)}</div>
      <p>{e(award_txt)}</p>
    </div>
  </div>
  <figure class="hero-pic" data-load style="--d:1"><img src="{pg.b}img/{HEADIMG['home']}" alt="" width="2000" height="1111"></figure>
</div></section>

<section class="sec" aria-labelledby="ab-h"><div class="wrap">
  <h2 id="ab-h" class="vh">{e(X[l]['about'])}</h2>
  <div class="tri">
    {''.join(f'<article data-reveal><h3 class="h3">{e(x["title"].rstrip(":"))}</h3>' + ''.join(f'<p>{e(p)}</p>' for p in ps) + '</article>' for x, ps in zip(w, paras))}
  </div>
</div></section>

<section class="quote" aria-label="Mahatma Gandhi"><div class="wrap">
  <blockquote data-reveal><p>{e(quote)}</p><footer>{e(UI[l]['quote_by'])}</footer></blockquote>
</div></section>

<section class="sec" aria-labelledby="sv-h"><div class="wrap">
  <div class="sec-h"><h2 id="sv-h" class="h2" data-reveal>{e(d['services_title'])}</h2><a class="link" href="{pg.href('services')}" data-reveal>{e(X[l]['all_services'])}</a></div>
  <div class="svc-cols">
    {''.join(f'<div data-reveal><h3 class="grp">{e(g)}</h3><ul class="rows">{svc_rows(pg, items)}</ul></div>' for g, items in groups)}
  </div>
</div></section>

<section class="sec tint" aria-labelledby="tm-h"><div class="wrap">
  <div class="sec-h"><h2 id="tm-h" class="h2" data-reveal>{e(d['team_title'])}</h2><a class="link" href="{pg.href('team')}" data-reveal>{e(X[l]['all_team'])} ({len(d['team'])})</a></div>
  <div class="people">{''.join(f'<div data-reveal>{person_card(pg, m, i, True)}</div>' for i, m in enumerate(d['team'][:8]))}</div>
</div></section>

<section class="sec" aria-label="{e(n['notary'])}, {e(n['pubs'])}, {e(n['members'])}"><div class="wrap">
  <div class="more">
    {''.join(f'<a class="mcard" href="{pg.href(k)}" data-reveal><span class="mc-img"><img src="{pg.b}img/{im}" alt="" width="2000" height="833" loading="lazy"></span><span class="h3">{e(n[k])}</span><span class="mc-t">{e(t)}</span><span class="link">{e(X[l]["read"])}</span></a>' for k, im, t in more)}
  </div>
</div></section>
'''
    s += contact_band(pg)
    s += f'''<section class="sec tint" aria-labelledby="of-h"><div class="wrap">
  <h2 id="of-h" class="h2" data-reveal>{e(X[l]['our_offices'])}</h2>
  <div data-reveal>{offices_block(pg, 'offs big', True)}</div>
</div></section>
</main>
'''
    s += footer(pg)
    return s


# ------------------------------------------------------------------ services
def page_services(l):
    pg = Page(l, 'services')
    d = D[l]
    svc = services_list(l)
    groups = [(UI[l]['groups'][0], [s for s in svc if s['group'] == 'beratung']), (UI[l]['groups'][1], [s for s in svc if s['group'] == 'prozess'])]
    idx = ''.join(f'<div><p class="grp">{e(g)}</p>' + ''.join(f'<a href="#{x["uid"]}"{" lang=\"de\"" if x["de_only"] else ""}>{e(x["title"])}</a>' for x in items) + '</div>' for g, items in groups)
    secs = ''
    for x in svc:
        lang = ' lang="de"' if x['de_only'] else ''
        note = f'<p class="de-note" lang="{l}">{e(X[l]["de_note"])}</p>' if x['de_only'] else ''
        secs += f'''<article class="svc" id="{x['uid']}"{lang}>
  <div class="svc-h"><img src="{pg.b}img/{x['icon']}" alt="" width="34" height="34"><h2 class="h2">{e(x['title'])}</h2></div>
  {note}<div class="rich">{body_html(x['html'])}</div>
</article>
'''
    s = head(pg, f"{d['nav'][0]} · {UI[l]['name']}", d['services_title'])
    s += '<body>\n' + page_head(pg, d['services_title'], ' · '.join(x['title'] for x in svc if not x['de_only']), HEADIMG['services'])
    s += f'<main id="main">\n<section class="sec"><div class="wrap layout"><nav class="index" aria-label="{e(d["services_title"])}">{idx}</nav><div class="svcs">{secs}</div></div></section>\n'
    s += contact_band(pg) + '</main>\n' + footer(pg)
    return s


def side_box(pg):
    l = pg.l
    return f'''<aside class="side" data-reveal>
    <h2 class="h3">{e(UI[l]['contact_cta'])}</h2>
    <p>Zanetti Rechtsanwälte AG<br>Blegistrasse 9<br>6340 Baar, Zug</p>
    <p>T <a href="tel:{TEL}">{TEL_H}</a><br>F {FAX_H}<br><a href="mailto:{MAIL}">{MAIL}</a></p>
    <a class="btn" href="{pg.href('contact')}">{e(nav_labels(l)['contact'])}{ARR}</a>
  </aside>'''


def page_generic(l, key, src, img=None):
    pg = Page(l, key)
    d = D[l]
    heads, body = section_parts(d[src])
    title = heads[0].rstrip(' –') if heads else nav_labels(l).get(key, key)
    lead = ' '.join(heads[1:]) if len(heads) > 1 else ''
    s = head(pg, f"{title} · {UI[l]['name']}", T(body)[:200])
    s += '<body>\n' + page_head(pg, title, lead, img)
    s += f'<main id="main">\n<section class="sec"><div class="wrap layout right"><div class="rich" data-reveal>{body}</div>{side_box(pg)}</div></section>\n'
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
    s += '<body>\n' + page_head(pg, d['nav'][5], title, HEADIMG['members'])
    s += f'''<main id="main">
<section class="sec"><div class="wrap lna">
  <img class="lna-logo" src="{pg.b}img/1033_lna_logo_500px.180x0-is.jpg" alt="Legal Netlink Alliance" width="180" height="62" data-reveal>
  <div>
    <h2 class="h2" data-reveal>{e(T(lna.group(1)))}</h2>
    <p class="lead" data-reveal>{e(T(lna.group(2)))}</p>
    <p data-reveal><a class="btn" href="{e(lna_href)}" rel="noopener">{e(T(lna.group(3)))}{ARR}</a></p>
  </div>
</div></section>
<section class="sec tint"><div class="wrap assocs">{cards}</div></section>
'''
    s += '</main>\n' + footer(pg)
    return s


def page_team(l):
    pg = Page(l, 'team')
    d = D[l]
    cards, dialogs = '', ''
    for i, m in enumerate(d['team']):
        f = team_img(m)
        rs = roles(m)
        tl = teaser_lines(m)
        mail = f'<p><a href="mailto:{e(m["email"])}">{e(m["email"])}</a></p>' if m['email'] else ''
        cards += f'''<li class="member" data-reveal>
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
    s += '<body class="team-page">\n' + page_head(pg, d['team_title'], UI[l]['team_hint'])
    s += f'<main id="main">\n<section class="sec" style="padding-top:0"><div class="wrap"><ol class="members">{cards}</ol></div></section>\n{dialogs}'
    s += contact_band(pg) + '</main>\n' + footer(pg)
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
        blocks += f'<section class="pub" aria-label="{e(p["name"])}"><div class="pub-who" data-reveal>{who}</div><ol class="plist">{items}</ol></section>'
    s = head(pg, f"{d['nav'][3]} · {UI[l]['name']}", d['pubs_title'])
    s += '<body>\n' + page_head(pg, d['pubs_title'], ' · '.join(p['name'] for p in d['pubs']), HEADIMG['pubs'])
    s += f'<main id="main">\n<section class="sec"><div class="wrap pubs">{blocks}</div></section>\n</main>\n' + footer(pg)
    return s


def page_contact(l):
    pg = Page(l, 'contact')
    d = D[l]
    heads, body = section_parts(d['contact'])
    intro = T(re.search(r'<p>(.*?)</p>', body, re.S).group(1))
    notes = re.findall(r'<p>\((.*?)\)</p>', body, re.S)
    note = f'({T(notes[0])})' if notes else ''
    s = head(pg, f"{d['nav'][4]} · {UI[l]['name']}", intro)
    s += '<body>\n' + page_head(pg, heads[0] if heads else d['nav'][4], intro)
    s += f'''<main id="main">
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="lines">
    <a href="tel:{TEL}" data-reveal><span>{e(X[l]['call'])}</span><b>{TEL_H}</b></a>
    <a href="mailto:{MAIL}" data-reveal><span>{e(X[l]['mail'])}</span><b>{MAIL}</b></a>
    <div data-reveal><span>{e(X[l]['fax'])}</span><b>{FAX_H}</b></div>
  </div>
  <p class="note" data-reveal>{e(note)}</p>
</div></section>
<section class="sec tint"><div class="wrap contact-grid">
  <div>{offices_block(pg, 'offs stack', True)}</div>
  <div class="map" data-reveal><iframe title="Google Maps – Zanetti Rechtsanwälte AG, Baar" src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d10840.119222836278!2d8.5708996!3d47.2159991!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xa08f4c2cdbca22ee!2sZanetti+Rechtsanw%C3%A4lte+AG!5e0!3m2!1sde!2sch!4v1552574030713" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>
'''
    s += contact_band(pg) + '</main>\n' + footer(pg)
    return s


def write(rel, s):
    p = os.path.join(OUT, rel, 'index.html')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


css = open(os.path.join(ROOT, '_src/zl3.css'), encoding='utf-8').read()
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
