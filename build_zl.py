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
CAL = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="2" y="3" width="12" height="11" rx="1.5"/><path d="M2 6.5h12M5.5 1.5v3M10.5 1.5v3"/></svg>'
CHEV = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3 5l4 4 4-4"/></svg>'
PLAY = '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M5 3l8 5-8 5z"/></svg>'
I_AWARD = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10" cy="8" r="5"/><path d="M7 12.5L6 18l4-2 4 2-1-5.5"/></svg>'
I_BRIEF = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="2.5" y="6" width="15" height="10.5" rx="1.5"/><path d="M7 6V4.5A1.5 1.5 0 0 1 8.5 3h3A1.5 1.5 0 0 1 13 4.5V6M2.5 10.5h15"/></svg>'
I_SCALE = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M10 2.5v15M5 17.5h10M4 5.5h12M4 5.5l-2.5 6a2.5 2.5 0 0 0 5 0zM16 5.5l-2.5 6a2.5 2.5 0 0 0 5 0z"/></svg>'
CREDITS = json.load(open(os.path.join(OUT, 'img/credits.json'), encoding='utf-8'))
X = {
 'de': dict(offices='Standorte', team_n='Teammitglieder', areas='Rechtsgebiete', bio='Werdegang', all_team='Ganzes Team ansehen',
            pics='Bilder', site='Seiten', our_offices='Unsere Standorte', more='Mehr als Beratung', more_sub='Beurkundungen, Fachpublikationen und ein internationales Netzwerk gehören bei uns dazu.',
            read='Mehr erfahren', ready='Bereit für ein erstes Gespräch?', ready_sub='Schildern Sie uns Ihr Anliegen. Wir melden uns rasch und sagen Ihnen offen, wie wir Ihnen helfen können.',
            maps='Route planen', call='Telefon', mail='E-Mail', fax='Fax'),
 'en': dict(offices='Offices', team_n='Team members', areas='Areas of law', bio='Background', all_team='See the whole team',
            pics='Pictures', site='Pages', our_offices='Our offices', more='More than advice', more_sub='Notarial deeds, legal publications and an international network are part of our work.',
            read='Learn more', ready='Ready for a first conversation?', ready_sub='Tell us about your matter. We will get back to you quickly and tell you openly how we can help.',
            maps='Plan route', call='Phone', mail='E-mail', fax='Fax'),
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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Questrial&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pg.b}assets/site.css">
<script>document.documentElement.classList.add('js')</script>
</head>
'''


def top(pg):
    l = pg.l
    n = nav_labels(l)
    links = f'<a href="{pg.href("home")}"{" aria-current=\"page\"" if pg.key == "home" else ""}>{UI[l]["home"]}</a>'
    links += ''.join(f'<a href="{pg.href(k)}"{" aria-current=\"page\"" if k == pg.key else ""}>{e(n[k])}</a>' for k in KEYS)
    lg = ''.join(f'<a href="{pg.href(pg.key, x)}" hreflang="{x}" lang="{x}"{" aria-current=\"true\"" if x == l else ""}>{x.upper()}</a>' for x in ('de', 'en'))
    return f'''<a class="skip" href="#main">{UI[l]["skip"]}</a>
  <div class="wrap top">
    <a class="badge" href="{pg.href('home')}" aria-label="{e(UI[l]['name'])} – {UI[l]['home']}"><img src="{pg.b}img/logo-white.svg" alt="{e(UI[l]['name'])}" width="220" height="46"></a>
    <nav class="nav" id="menu" aria-label="{e(UI[l]['name'])}">{links}<span class="langs">{lg}</span></nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{UI[l]['menu']}</button>
  </div>'''


def stats(pg):
    l = pg.l
    return f'''<div class="hero-stats" data-load style="--d:3">
      <div><span>{e(X[l]['offices'])}</span><b>3</b></div>
      <div><span>{e(X[l]['team_n'])}</span><b>{len(D[l]['team'])}</b></div>
      <div><span>{e(X[l]['areas'])}</span><b>{len(services_list(l))}</b></div>
    </div>'''


def sub_hero(pg, title, lead='', img=None):
    return f'''<header class="hero sub">
  <div class="hero-bg"><img src="{pg.b}img/{img or HEADIMG['home']}" alt="" width="2000" height="833"></div>
  {top(pg)}
  <div class="wrap hero-in">
    <div class="hero-text">
      <h1 id="h1" class="h1" data-load>{e(title)}</h1>
      {f'<p class="hero-p" data-load style="--d:1">{e(lead)}</p>' if lead else ''}
    </div>
  </div>
</header>
'''


def credits_html(pg):
    items = [f'<a href="{e(c["page"])}">{e(c["title"])}</a> · {e(c["creator"])}, {e(c["license"])}' for c in CREDITS]
    return f'<p class="credits">{X[pg.l]["pics"]}: ' + '; '.join(items) + '</p>' if items else ''


def cta(pg):
    l = pg.l
    u = UI[l]
    return f'''<section class="sec" aria-labelledby="cp-h"><div class="wrap">
  <div class="cta" data-reveal>
    <h2 id="cp-h" class="h2">{e(X[l]['ready'])}</h2>
    <p>{e(X[l]['ready_sub'])}</p>
    <form class="coupon cta-form" data-mailto="info@zanettilaw.ch">
      <label class="vh" for="cp-name">{e(u['f_name'])}</label><input class="inp" id="cp-name" name="name" placeholder="{e(u['f_name'])}" autocomplete="name" required>
      <label class="vh" for="cp-phone">{e(u['f_phone'])}</label><input class="inp" id="cp-phone" name="phone" type="tel" placeholder="{e(u['f_phone'])}" autocomplete="tel">
      <label class="vh" for="cp-mail">{e(u['f_mail'])}</label><input class="inp full" id="cp-mail" name="email" type="email" placeholder="{e(u['f_mail'])}" autocomplete="email">
      <label class="vh" for="cp-msg">{e(u['f_msg'])}</label><textarea class="inp full" id="cp-msg" name="message" rows="3" placeholder="{e(u['f_msg'])}" required></textarea>
      <button class="btn full" type="submit">{CAL}{e(u['send'])}</button>
    </form>
    <p class="muted" style="font-size:.85rem">{e(u['write_sub'])}</p>
  </div>
</div></section>
'''


def footer(pg):
    l = pg.l
    n = nav_labels(l)
    links = ''.join(f'<a href="{pg.href(k)}">{e(n[k])}</a>' for k in KEYS)
    offs = ''.join(f'<p><b>{e(nm.replace("Head Office ", "").replace("Office ", ""))}</b><br>{"<br>".join(e(x) for x in ln[1:])}</p>' for nm, ln in OFFICES[l])
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div><img src="{pg.b}img/logo-white.svg" alt="{e(UI[l]['name'])}" width="220" height="46" style="height:44px;width:auto;margin-bottom:18px"><p><a href="tel:+41417663585">T +41 41 766 35 85</a><br>F +41 41 766 35 80<br><a href="mailto:info@zanettilaw.ch">info@zanettilaw.ch</a></p></div>
      <nav aria-label="{e(X[l]['site'])}"><h3>{e(X[l]['site'])}</h3>{links}</nav>
      <div><h3>{e(X[l]['our_offices'])}</h3><div class="foot-offs">{offs}</div></div>
      <nav aria-label="{UI[l]['lang']}"><h3>{UI[l]['lang']}</h3><a href="{pg.href(pg.key, 'de')}" lang="de">Deutsch</a><a href="{pg.href(pg.key, 'en')}" lang="en">English</a></nav>
    </div>
    <div class="foot-legal"><p>© 2026 {e(UI[l]['name'])}</p><p><a href="{pg.href('imprint')}">{e(UI[l]['imprint'])}</a> · <a href="{pg.href('privacy')}">{e(UI[l]['privacy'])}</a></p><a class="made" href="https://naktz.com/" rel="noopener"><span>{MADE_BY[l]}</span><img src="{pg.b}img/naktz-logo.png" alt="Naktz Media" width="105" height="30"></a></div>
    {credits_html(pg)}
  </div>
</footer>
<script src="{pg.b}assets/site.js" defer></script>
</body>
</html>
'''


def services_list(l):
    out = []
    for i, s in enumerate(D[l]['services']):
        if l == 'en' and s['title'] == 'Familienrecht':
            continue  # untranslated German duplicate on the original English page
        out.append(dict(s, icon=ICONS[i], uid=f"{s['id']}-{i}"))
    return out


def first_sentence(h, n=140):
    t = T(re.search(r'<p>(.*?)</p>', h, re.S).group(1)) if re.search(r'<p>', h) else T(h)
    m = re.match(r'(.{40,}?[a-zäöüé)][.!?])\s+[A-ZÄÖÜ«]', t)
    if m and len(m.group(1)) < max(n, 120) + 60:
        return m.group(1)
    return t[:n].rsplit(' ', 1)[0] + ' …' if len(t) > n else t


def team_img(m):
    return f"{m['img'].split('/')[-2]}_{os.path.basename(m['img'])}" if m.get('img') else ''


def short_role(m):
    role = re.sub(r',\s*$', '', m['role'])
    return role.split(',')[-1].strip() if len(role) > 60 else role


def person(pg, m, i, link=False):
    tag = 'a' if link else 'button'
    attr = f'href="{pg.href("team")}#m{i}"' if link else 'type="button" aria-haspopup="dialog"'
    return (f'<{tag} class="person" {attr} data-open="m{i}"><img src="{pg.b}img/{team_img(m)}" alt="" width="800" height="660" loading="lazy">'
            f'<span class="p-name">{e(X[pg.l]["bio"])}</span><span class="play">{PLAY}</span>'
            f'<span class="p-foot"><b>{e(m["name"])}</b><span>{e(short_role(m))}</span></span></{tag}>')


def office_faq(pg):
    l = pg.l
    out = ''
    for k, (name, lines_) in enumerate(OFFICES[l]):
        q = '+'.join(lines_[1:]).replace(' ', '+')
        out += (f'<details{" open" if k == 0 else ""}><summary>{e(name)}{CHEV}</summary><div class="a"><p>{"<br>".join(e(x) for x in lines_)}</p>'
                f'<p style="margin-top:8px">T <a href="tel:+41417663585">+41 41 766 35 85</a> · <a href="https://www.google.com/maps/search/?api=1&amp;query={e(q)}" rel="noopener">{e(X[l]["maps"])}</a></p></div></details>')
    return f'<div class="faq">{out}</div>'


# ------------------------------------------------------------------ home
def page_home(l):
    pg = Page(l, 'home')
    d = D[l]
    n = nav_labels(l)
    quote = T(re.search(r'<h3>(.*?)</h3>', d['quote'] or '', re.S).group(1)) if re.search(r'<h3>', d['quote'] or '') else ''
    if not quote:
        quote = {'de': '«Wenn du im Recht bist, kannst du es dir leisten, die Ruhe zu bewahren; und wenn du im Unrecht bist, kannst du es dir nicht leisten, sie zu verlieren.»',
                 'en': '«When you are in the right, you can afford to keep your cool; and when you are wrong, you cannot afford to lose it.»'}[l]
    w = d['widgets']
    w0 = [T(x) for x in re.findall(r'<p>(.*?)</p>', w[0]['html'], re.S) if T(x)]
    first_text, award_txt = w0[0], (w0[1] if len(w0) > 1 else '')
    texts = [T(' '.join(re.findall(r'<p>(.*?)</p>', x['html'], re.S))) for x in w]
    svc = services_list(l)
    team = [m for m in d['team'] if m.get('img')]
    feats = [(I_BRIEF, w[1]['title'].rstrip(':'), first_sentence(w[1]['html'], 170)),
             (I_SCALE, w[2]['title'].rstrip(':'), first_sentence(w[2]['html'], 170)),
             (I_AWARD, UI[l]['award'], award_txt)]
    cards = [('notary', HEADIMG['notary'], first_sentence(section_parts(d['notary'])[1], 150)),
             ('pubs', HEADIMG['pubs'], d['pubs_title'] + ': ' + ', '.join(p['name'] for p in d['pubs']) + '.'),
             ('members', HEADIMG['members'], ' '.join(section_parts(d['members'])[0]))]

    s = head(pg, f"{UI[l]['name']} – Baar, Zug · Zürich · Schwyz", T(d['home_title']))
    s += '<body class="home">\n'
    s += f'''<header class="hero">
  <div class="hero-bg"><img src="{pg.b}img/{HEADIMG['pubs']}" alt="" width="2000" height="833"></div>
  {top(pg)}
  <div class="wrap hero-in">
    <div class="hero-text">
      <h1 id="h1" class="h1" data-load>{e(UI[l]['name'])}</h1>
      <p class="hero-p" data-load style="--d:1">{e(T(d['home_title']))} {e(first_sentence('<p>' + first_text + '</p>', 160))}</p>
      <a class="btn" href="{pg.href('contact')}" data-load style="--d:2">{e(UI[l]['contact_cta'])}</a>
    </div>
    {stats(pg)}
  </div>
</header>
<main id="main">
<section class="sec" aria-labelledby="df-h"><div class="wrap">
  <div class="sec-h center"><h2 id="df-h" class="h2" data-reveal>{e(w[0]['title'].rstrip(':'))}</h2></div>
  <div class="diff">
    <figure class="diff-pic" data-reveal><img src="{pg.b}img/{HEADIMG['home']}" alt="" width="2000" height="1111" loading="lazy"></figure>
    <ul class="feat">
      {''.join(f'<li data-reveal><span class="ico">{ic}</span><p><b>{e(t)}:</b> {e(x)}</p></li>' for ic, t, x in feats)}
    </ul>
  </div>
</div></section>

<section class="sec" aria-labelledby="ab-h" style="padding-top:0"><div class="wrap about">
  <div class="about-text">
    <h2 id="ab-h" class="h2" data-reveal>{e(UI[l]['name'])}</h2>
    <p data-reveal>{e(texts[1])}</p>
    <blockquote data-reveal><p class="h3">{e(quote)}</p><p class="muted" style="margin-top:8px;font-size:.9rem">{e(UI[l]['quote_by'])}</p></blockquote>
    <div class="awards" data-reveal>{''.join(f'<img src="{pg.b}img/{f}" alt="{e(UI[l]["award"])} {y} – {UI[l]["award_by"]}" width="84" height="84" loading="lazy">' for f, y in AWARDS)}</div>
  </div>
  <div class="duo">
    <figure data-reveal><img src="{pg.b}img/{team_img(d['team'][0])}" alt="{e(d['team'][0]['name'])}" width="800" height="660" loading="lazy"></figure>
    <figure data-reveal><img src="{pg.b}img/{HEADIMG['contact']}" alt="" width="2000" height="833" loading="lazy"></figure>
  </div>
</div></section>

<section class="sec tint" aria-labelledby="sv-h"><div class="wrap bene">
  <div class="bene-h">
    <h2 id="sv-h" class="h2" data-reveal>{e(d['services_title'])}</h2>
    <p class="muted" data-reveal>{e(UI[l]['groups'][0])} · {e(UI[l]['groups'][1])}</p>
    <a class="btn" href="{pg.href('contact')}" data-reveal>{CAL}{e(UI[l]['contact_cta'])}</a>
  </div>
  <div class="mini">
    {''.join(f'<a href="{pg.href("services")}#{x["uid"]}" data-reveal><img src="{pg.b}img/{x["icon"]}" alt="" width="34" height="34"><b>{e(x["title"])}</b><span>{e(first_sentence(x["html"], 70))}</span></a>' for x in svc)}
  </div>
</div></section>

<section class="sec" aria-labelledby="mo-h"><div class="wrap">
  <div class="sec-h center"><h2 id="mo-h" class="h2" data-reveal>{e(X[l]['more'])}</h2><p class="lead" data-reveal>{e(X[l]['more_sub'])}</p></div>
  <div class="icards">
    {''.join(f'<a class="icard" href="{pg.href(k)}" data-reveal><figure><img src="{pg.b}img/{im}" alt="" width="2000" height="833" loading="lazy"></figure><div><b>{e(n[k])}</b><p>{e(t)}</p><span class="more">{e(X[l]["read"])} →</span></div></a>' for k, im, t in cards)}
  </div>
</div></section>
'''
    s += cta(pg)
    s += f'''<section class="sec" aria-labelledby="tm-h" style="padding-top:0"><div class="wrap">
  <div class="sec-h center"><h2 id="tm-h" class="h2" data-reveal>{e(d['team_title'])}</h2><p class="lead" data-reveal>{e(UI[l]['team_hint'])}</p></div>
  <div class="people">{''.join(f'<div data-reveal>{person(pg, m, d["team"].index(m), True)}</div>' for m in team[:4])}</div>
  <p class="center" style="margin-top:32px"><a class="btn ghost" href="{pg.href('team')}">{e(X[l]['all_team'])}</a></p>
</div></section>

<section class="sec tint" aria-labelledby="of-h"><div class="wrap faq-wrap">
  <div><h2 id="of-h" class="h2" data-reveal>{e(X[l]['our_offices'])}</h2><p class="muted" style="margin-top:14px" data-reveal>Zug · Zürich · Schwyz</p></div>
  <div data-reveal>{office_faq(pg)}</div>
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
    idx = ''.join(f'<div><h2>{e(g)}</h2>' + ''.join(f'<a href="#{x["uid"]}"><img src="{pg.b}img/{x["icon"]}" alt="" width="20" height="20">{e(x["title"])}</a>' for x in items) + '</div>' for g, items in groups)
    secs = ''.join(f'''<article class="svc" id="{x['uid']}">
  <div class="svc-h"><span class="ico"><img src="{pg.b}img/{x['icon']}" alt="" width="26" height="26"></span><h2 class="h2" style="font-size:1.9rem">{e(x['title'])}</h2></div>
  <div class="rich">{body_html(x['html'])}</div>
</article>
''' for x in svc)
    s = head(pg, f"{d['nav'][0]} · {UI[l]['name']}", d['services_title'])
    s += '<body>\n' + sub_hero(pg, d['services_title'], ' · '.join(x['title'] for x in svc[:5]) + ' …', HEADIMG['services'])
    s += f'<main id="main">\n<section class="sec"><div class="wrap layout"><nav class="side index" aria-label="{e(d["services_title"])}">{idx}</nav><div>{secs}</div></div></section>\n'
    s += cta(pg) + '</main>\n' + footer(pg)
    return s


def side_box(pg):
    l = pg.l
    return f'''<aside class="side" data-reveal>
    <figure class="side-pic"><img src="{pg.b}img/{HEADIMG['contact']}" alt="" width="2000" height="833" loading="lazy"></figure>
    <div class="box">
      <h2>{e(UI[l]['contact_cta'])}</h2>
      <p>Zanetti Rechtsanwälte AG<br>Blegistrasse 9, 6340 Baar</p>
      <p><a href="tel:+41417663585">T +41 41 766 35 85</a><br><a href="mailto:info@zanettilaw.ch">info@zanettilaw.ch</a></p>
      <a class="btn white" href="{pg.href('contact')}">{e(nav_labels(l)['contact'])}</a>
    </div>
  </aside>'''


def page_generic(l, key, src, img=None):
    pg = Page(l, key)
    d = D[l]
    heads, body = section_parts(d[src])
    title = heads[0].rstrip(' –') if heads else nav_labels(l).get(key, key)
    lead = ' '.join(heads[1:]) if len(heads) > 1 else ''
    s = head(pg, f"{title} · {UI[l]['name']}", T(body)[:200])
    s += '<body>\n' + sub_hero(pg, title, lead, img or HEADIMG['members'])
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
        cards += f'<a href="{e(href)}" rel="noopener" data-reveal><img src="{pg.b}img/{logo}" alt="" width="480" height="120" loading="lazy"><b>{e(T(name))}</b><span>{e(T(a))}</span></a>'
    title = ' '.join(heads)
    lna_href = re.search(r'href="([^"]+)"', lna.group(3)).group(1)
    s = head(pg, f"{d['nav'][5]} · {UI[l]['name']}", title)
    s += '<body>\n' + sub_hero(pg, d['nav'][5], title, HEADIMG['members'])
    s += f'''<main id="main">
<section class="sec"><div class="wrap diff">
  <figure class="diff-pic" data-reveal><img src="{pg.b}img/1028_zanetti_dienstleistungen_2x_neu.jpg" alt="" width="2000" height="833" loading="lazy"></figure>
  <div class="about-text">
    <img src="{pg.b}img/1033_lna_logo_500px.180x0-is.jpg" alt="Legal Netlink Alliance" width="180" height="62" data-reveal>
    <h2 class="h2" data-reveal>{e(T(lna.group(1)))}</h2>
    <p data-reveal>{e(T(lna.group(2)))}</p>
    <p data-reveal><a class="btn" href="{e(lna_href)}" rel="noopener">{e(T(lna.group(3)))}</a></p>
  </div>
</div></section>
<section class="sec tint"><div class="wrap mem">{cards}</div></section>
'''
    s += '</main>\n' + footer(pg)
    return s


def page_team(l):
    pg = Page(l, 'team')
    d = D[l]
    cards, dialogs = '', ''
    for i, m in enumerate(d['team']):
        f = team_img(m)
        role = re.sub(r',\s*$', '', m['role'])
        mail = f'<p><a href="mailto:{e(m["email"])}">{e(m["email"])}</a></p>' if m['email'] else ''
        cards += f'<li data-reveal>{person(pg, m, i)}</li>'
        dialogs += f'''<dialog class="t-dialog" id="m{i}" aria-labelledby="m{i}-h">
  <div class="td-grid">
    <div class="td-side"><img src="{pg.b}img/{f}" alt="{e(m['name'])}" width="800" height="660" loading="lazy">
      <h2 id="m{i}-h" class="h2" style="font-size:1.7rem">{e(m['name'])}</h2><p class="muted">{e(role)}</p>{mail}</div>
    <div class="rich">{body_html(m['bio'])}</div>
  </div>
  <form method="dialog"><button class="td-close" type="submit" aria-label="{e(UI[l]['close'])}">✕</button></form>
</dialog>
'''
    s = head(pg, f"{d['nav'][2]} · {UI[l]['name']}", d['team_title'])
    s += '<body class="team-page">\n' + sub_hero(pg, d['team_title'], UI[l]['team_hint'], HEADIMG['team'])
    s += f'<main id="main">\n<section class="sec"><div class="wrap"><ol class="people team-grid">{cards}</ol></div></section>\n{dialogs}'
    s += cta(pg) + '</main>\n' + footer(pg)
    return s


def page_pubs(l):
    pg = Page(l, 'pubs')
    d = D[l]
    idx = {m['name']: i for i, m in enumerate(d['team'])}
    blocks = ''
    for p in d['pubs']:
        items = ''.join(f'<li data-reveal><span class="y">{e(y)}</span><span><b>{e(t)}</b><span>{e(src)}</span></span></li>' for y, t, src in p['items'])
        i = idx.get(p['name'])
        who = person(pg, d['team'][i], i, True) if i is not None else f'<h2 class="h3">{e(p["name"])}</h2>'
        blocks += f'<section class="pub" aria-label="{e(p["name"])}"><div data-reveal>{who}</div><ol class="plist">{items}</ol></section>'
    s = head(pg, f"{d['nav'][3]} · {UI[l]['name']}", d['pubs_title'])
    s += '<body>\n' + sub_hero(pg, d['pubs_title'], ' · '.join(p['name'] for p in d['pubs']), HEADIMG['pubs'])
    s += f'<main id="main">\n<section class="sec"><div class="wrap pubs">{blocks}</div></section>\n</main>\n' + footer(pg)
    return s


def page_contact(l):
    pg = Page(l, 'contact')
    d = D[l]
    heads, body = section_parts(d['contact'])
    intro = T(re.search(r'<p>(.*?)</p>', body, re.S).group(1))
    notes = re.findall(r'<p>\((.*?)\)</p>', body, re.S)
    note = T(notes[0]) if notes else ''
    s = head(pg, f"{d['nav'][4]} · {UI[l]['name']}", intro)
    s += '<body>\n' + sub_hero(pg, heads[0] if heads else d['nav'][4], intro, HEADIMG['contact'])
    s += f'''<main id="main">
<section class="sec"><div class="wrap">
  <div class="contact-lines">
    <a class="cl" href="tel:+41417663585" data-reveal><span>{e(X[l]['call'])}</span><b>+41 41 766 35 85</b></a>
    <a class="cl" href="mailto:info@zanettilaw.ch" data-reveal><span>{e(X[l]['mail'])}</span><b>info@zanettilaw.ch</b></a>
    <div class="cl" data-reveal><span>{e(X[l]['fax'])}</span><b>+41 41 766 35 80</b></div>
  </div>
  <p class="muted" style="margin-top:14px" data-reveal>{e(note)}</p>
</div></section>
<section class="sec tint"><div class="wrap faq-wrap">
  <div><h2 class="h2" data-reveal>{e(X[l]['our_offices'])}</h2><div data-reveal style="margin-top:24px">{office_faq(pg)}</div></div>
  <div class="map" data-reveal><iframe title="Google Maps – Zanetti Rechtsanwälte AG, Baar" src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d10840.119222836278!2d8.5708996!3d47.2159991!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xa08f4c2cdbca22ee!2sZanetti+Rechtsanw%C3%A4lte+AG!5e0!3m2!1sde!2sch!4v1552574030713" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>
'''
    s += cta(pg) + '</main>\n' + footer(pg)
    return s


def write(rel, s):
    p = os.path.join(OUT, rel, 'index.html')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


open(os.path.join(OUT, 'assets/site.css'), 'w', encoding='utf-8', newline='\n').write(open(os.path.join(ROOT, '_src/zl2.css'), encoding='utf-8').read())

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
