ARR = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3 11L11 3M4.5 3H11v6.5"/></svg>'
PHONE = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3.5 1.8h2.6l1.2 3.2-1.8 1.2a8.6 8.6 0 0 0 4.3 4.3l1.2-1.8 3.2 1.2v2.6a1.6 1.6 0 0 1-1.7 1.6A12.6 12.6 0 0 1 1.9 3.5a1.6 1.6 0 0 1 1.6-1.7z"/></svg>'
LEFT = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M9 2L4 7l5 5"/></svg>'
RIGHT = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 2l5 5-5 5"/></svg>'
CREDITS = json.load(open(os.path.join(OUT, 'img/credits.json'), encoding='utf-8'))
X = {
 'de': dict(offices='Standorte', lawyers='Juristinnen und Juristen', areas='Rechtsgebiete', bio='Werdegang', all_team='Ganzes Team',
            pics='Bilder', site='Seiten', office='Büros', call='Anrufen', write_l='E-Mail schreiben', maps='Karte öffnen', years='Ausgezeichnet 2024 · 2025 · 2026'),
 'en': dict(offices='Offices', lawyers='Lawyers and legal staff', areas='Areas of law', bio='Background', all_team='Whole team',
            pics='Pictures', site='Pages', office='Offices', call='Call', write_l='Send an e-mail', maps='Open map', years='Awarded 2024 · 2025 · 2026'),
}


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
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&display=swap" rel="stylesheet">
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


def bar(pg):
    l = pg.l
    n = nav_labels(l)
    tabs = ''.join(f'<a href="{pg.href(k)}"{" aria-current=\"page\"" if k == pg.key else ""}>{e(n[k])}</a>' for k in KEYS)
    return f'''<div class="bar">
    <a class="brand" href="{pg.href('home')}" aria-label="{e(UI[l]['name'])} – {UI[l]['home']}"><img src="{pg.b}img/logo-white.svg" alt="{e(UI[l]['name'])}" width="220" height="46"></a>
    <nav class="pills" id="menu" aria-label="{e(UI[l]['name'])}">{tabs}</nav>
    <div class="bar-right">
      {langs(pg)}
      <a class="btn small light" href="{pg.href('contact')}">{e(UI[l]['contact_cta'])}<span class="arr">{ARR}</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{UI[l]['menu']}</button>
    </div>
  </div>'''


def lines(t):
    w = t.split()
    n = 1 if len(t) < 20 else 2 if len(t) < 44 else 3
    per = -(-len(w) // n)
    out = [' '.join(w[i:i + per]) for i in range(0, len(w), per)]
    return ''.join(f'<span class="l"><span style="--i:{i}">{e(x)}</span></span>' for i, x in enumerate(out))


def page_hero(pg, title, lead='', img=None, right=''):
    return f'''<a class="skip" href="#main">{UI[pg.l]["skip"]}</a>
<header class="hero sub">
  <div class="hero-bg"><img src="{pg.b}img/{img or HEADIMG['home']}" alt="" width="2000" height="833"></div>
  {bar(pg)}
  <div class="hero-main"><h1 id="h1" class="hero-h h-xl">{lines(title)}</h1></div>
  <div class="hero-foot">
    <p class="hero-sub" data-load>{e(lead)}</p>
    {right}
  </div>
</header>
'''


def credits_html(pg):
    items = [f'<a href="{e(c["page"])}">{e(c["title"])}</a> · {e(c["creator"])}, {e(c["license"])}' for c in CREDITS]
    return f'<p class="credits">{X[pg.l]["pics"]}: ' + '; '.join(items) + '</p>'


def contact_form(pg):
    l = pg.l
    u = UI[l]
    return f'''<section class="panel contact-panel" aria-labelledby="cp-h">
  <div class="form-panel">
    <div class="sec-head left" style="margin:0">
      <h2 id="cp-h" class="h-l" data-reveal>{e(u['write'])}</h2>
      <p class="lead" data-reveal>{e(u['write_sub'])}</p>
      <div class="cinfo" data-reveal>
        <a href="tel:+41417663585"><span class="circ">{PHONE}</span><span><small>{e(X[l]['call'])}</small>+41 41 766 35 85</span></a>
        <a href="mailto:info@zanettilaw.ch"><span class="circ">{ARR}</span><span><small>{e(X[l]['write_l'])}</small>info@zanettilaw.ch</span></a>
      </div>
    </div>
    <form class="coupon fields" data-mailto="info@zanettilaw.ch" data-reveal>
      <label class="vh" for="cp-name">{e(u['f_name'])}</label><input class="inp" id="cp-name" name="name" placeholder="{e(u['f_name'])}" autocomplete="name" required>
      <label class="vh" for="cp-phone">{e(u['f_phone'])}</label><input class="inp" id="cp-phone" name="phone" type="tel" placeholder="{e(u['f_phone'])}" autocomplete="tel">
      <label class="vh" for="cp-mail">{e(u['f_mail'])}</label><input class="inp full" id="cp-mail" name="email" type="email" placeholder="{e(u['f_mail'])}" autocomplete="email">
      <label class="vh" for="cp-msg">{e(u['f_msg'])}</label><textarea class="inp full" id="cp-msg" name="message" rows="4" placeholder="{e(u['f_msg'])}" required></textarea>
      <div class="full"><button class="btn" type="submit">{e(u['send'])}<span class="arr">{ARR}</span></button></div>
    </form>
  </div>
</section>
'''


def footer(pg):
    l = pg.l
    n = nav_labels(l)
    links = ''.join(f'<a href="{pg.href(k)}">{e(n[k])}</a>' for k in KEYS)
    offs = ''.join(f'<p><b>{e(nm.replace("Head Office ", "").replace("Office ", ""))}</b><br>{"<br>".join(e(x) for x in ln[1:])}</p>' for nm, ln in OFFICES[l])
    return f'''<footer class="foot">
  <div class="foot-cta">
    <h2 class="h-l" data-reveal>{e(D[l]['widgets'][0]['title'].rstrip(':'))}</h2>
    <a class="btn light" href="{pg.href('contact')}" data-reveal>{e(UI[l]['contact_cta'])}<span class="arr">{ARR}</span></a>
  </div>
  <div class="foot-grid">
    <div><img src="{pg.b}img/logo-white.svg" alt="{e(UI[l]['name'])}" width="220" height="46" style="height:44px;width:auto;margin-bottom:18px"><p><a href="tel:+41417663585">T +41 41 766 35 85</a>F +41 41 766 35 80<br><a href="mailto:info@zanettilaw.ch">info@zanettilaw.ch</a></p></div>
    <nav aria-label="{e(X[l]['site'])}"><h3>{e(X[l]['site'])}</h3>{links}</nav>
    <div class="foot-offs"><h3>{e(X[l]['office'])}</h3>{offs}</div>
    <nav aria-label="{UI[l]['lang']}"><h3>{UI[l]['lang']}</h3><a href="{pg.href(pg.key, 'de')}" lang="de">Deutsch</a><a href="{pg.href(pg.key, 'en')}" lang="en">English</a></nav>
  </div>
  <div class="foot-legal"><p>© 2026 {e(UI[l]['name'])}</p><p><a href="{pg.href('imprint')}">{e(UI[l]['imprint'])}</a> · <a href="{pg.href('privacy')}">{e(UI[l]['privacy'])}</a></p></div>
  {credits_html(pg)}
  <p class="foot-word" aria-hidden="true">Zanetti</p>
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


def first_sentence(h):
    t = T(re.search(r'<p>(.*?)</p>', h, re.S).group(1)) if re.search(r'<p>', h) else T(h)
    m = re.match(r'(.{40,}?[a-zäöüé)][.!?])\s+[A-ZÄÖÜ«]', t)
    if m and len(m.group(1)) < 200:
        return m.group(1)
    return t[:140].rsplit(' ', 1)[0] + ' …' if len(t) > 140 else t


def team_img(m):
    return f"{m['img'].split('/')[-2]}_{os.path.basename(m['img'])}" if m.get('img') else ''


def member_card(pg, m, i, tag=True):
    f = team_img(m)
    role = re.sub(r',\s*$', '', m['role'])
    short = role.split(',')[-1].strip() if len(role) > 60 else role
    return (f'<a class="photo person" href="{pg.href("team")}#m{i}" data-open="m{i}"><img src="{pg.b}img/{f}" alt="" width="800" height="660" loading="lazy">'
            + (f'<span class="tag">{e(X[pg.l]["bio"])}<i>{ARR}</i></span>' if tag else '')
            + f'<span class="ph-in"><span class="ph-name">{e(m["name"])}</span><span class="ph-role">{e(short)}</span></span></a>')


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
    badges = ''.join(f'<img src="{pg.b}img/{f}" alt="{e(UI[l]["award"])} {y}" width="38" height="38">' for f, y in AWARDS)
    groups = [(UI[l]['groups'][0], [s for s in svc if s['group'] == 'beratung']), (UI[l]['groups'][1], [s for s in svc if s['group'] == 'prozess'])]

    s = head(pg, f"{UI[l]['name']} – Baar, Zug · Zürich · Schwyz", T(d['home_title']))
    s += f'<body class="home">\n<a class="skip" href="#main">{UI[l]["skip"]}</a>\n'
    s += f'''<header class="hero">
  <div class="hero-bg"><img src="{pg.b}img/handshake3.jpg" alt="" width="1920" height="1280"></div>
  {bar(pg)}
  <div class="hero-main"><h1 id="h1" class="hero-h h-xl">{lines(UI[l]['name'])}</h1></div>
  <div class="hero-foot">
    <p class="hero-sub" data-load>{e(T(d['home_title']))}</p>
    <div class="widget-wrap" data-load>
      <div class="widget glass">
        <a class="w-row" href="{pg.href('services')}">{e(n['services'])}{ARR}</a>
        <a class="w-row w-main" href="{pg.href('contact')}"><span class="ic">{PHONE}</span><span class="t">{e(UI[l]['contact_cta'])}</span>{ARR}</a>
        <a class="w-row" href="{pg.href('team')}">{e(n['team'])}{ARR}</a>
        <a class="w-row w-tel" href="tel:+41417663585"><span>T +41 41 766 35 85</span>{PHONE}</a>
      </div>
    </div>
    <div class="hero-right" data-load>
      <div class="avatars glass chip"><span class="faces badges">{badges}</span><span>{e(UI[l]['award'])}</span></div>
      <p>{e(X[l]['years'])} · {e(UI[l]['award_by'])}</p>
    </div>
  </div>
</header>
<main id="main">
<section class="panel" aria-labelledby="ab-h">
  <div class="sec-head">
    <h2 id="ab-h" class="h-l" data-reveal>{e(w[0]['title'].rstrip(':'))}</h2>
    <p class="lead center" data-reveal>{e(first_text)}</p>
  </div>
  <div class="bento">
    <figure class="photo" data-reveal><img src="{pg.b}img/{HEADIMG['home']}" alt="" width="2000" height="1111" loading="lazy">
      <div class="stats">
        <div class="stat glass"><b>3</b><span>{e(X[l]['offices'])}</span></div>
        <div class="stat glass"><b>{len(d['team'])}</b><span>{e(X[l]['lawyers'])}</span></div>
        <div class="stat glass"><b>{len(svc)}</b><span>{e(X[l]['areas'])}</span></div>
      </div>
    </figure>
    <div class="quote-card" data-reveal>
      <blockquote><p>{e(quote)}</p></blockquote>
      <div class="who"><span class="mono">MG</span><span><b>Mahatma Gandhi</b><span>1869 – 1948</span></span></div>
    </div>
    <div data-reveal style="display:grid">{member_card(pg, d['team'][0], 0)}</div>
  </div>
</section>

<section class="panel" aria-labelledby="st-h">
  <div class="steps">
    <figure class="photo" data-reveal><img src="{pg.b}img/{HEADIMG['contact']}" alt="" width="2000" height="833" loading="lazy"></figure>
    <div class="steps-mid">
      <div class="sec-head left" style="margin:0">
        <h2 id="st-h" class="h-m" data-reveal>{e(UI[l]['award'])} {e(UI[l]['award_by'])}</h2>
        <p class="muted" data-reveal>{e(award_txt)}</p>
      </div>
      <div class="awards" data-reveal>{''.join(f'<figure><img src="{pg.b}img/{f}" alt="{e(UI[l]["award"])} {y} – {UI[l]["award_by"]}" width="300" height="300" loading="lazy"><figcaption>{y}</figcaption></figure>' for f, y in AWARDS)}</div>
    </div>
    <div class="acc" data-reveal>
      {''.join(f'<details{" open" if k == 0 else ""}><summary>{e(x["title"].rstrip(":"))}<span class="pm" aria-hidden="true"></span></summary><div class="acc-body"><p>{e(t)}</p></div></details>' for k, (x, t) in enumerate(zip(w[1:], texts[1:])))}
    </div>
  </div>
</section>

<section class="panel dark" aria-labelledby="tm-h">
  <div class="row-head">
    <h2 id="tm-h" class="h-l" data-reveal>{e(d['team_title'])}</h2>
    <div class="rail-ctl"><button type="button" data-rail="-1" aria-label="‹">{LEFT}</button><button type="button" data-rail="1" aria-label="›">{RIGHT}</button></div>
  </div>
  <div class="rail" id="rail">{''.join(member_card(pg, m, d['team'].index(m)) for m in team[1:])}</div>
  <p style="margin-top:28px"><a class="btn light" href="{pg.href('team')}">{e(X[l]['all_team'])}<span class="arr">{ARR}</span></a></p>
</section>

<section class="panel" aria-labelledby="sv-h">
  <div class="row-head">
    <h2 id="sv-h" class="h-l" data-reveal>{e(d['services_title'])}</h2>
    <a class="btn" href="{pg.href('services')}" data-reveal>{e(UI[l]['all_services'])}<span class="arr">{ARR}</span></a>
  </div>
  {''.join(f"""<div class="sgroup"><h3 class="h-s" data-reveal>{e(g)} <span class="muted">· {e(UI[l]['items'].format(n=len(items)))}</span></h3><div class="cards">
    {''.join(f'<a class="acard" href="{pg.href("services")}#{x["uid"]}" data-reveal><span class="ac-top"><span class="ac-ico"><img src="{pg.b}img/{x["icon"]}" alt="" width="34" height="34"></span><span class="circ">{ARR}</span></span><h3>{e(x["title"])}</h3><p>{e(first_sentence(x["html"]))}</p></a>' for x in items)}
  </div></div>""" for g, items in groups)}
</section>
'''
    s += contact_form(pg)
    s += '</main>\n' + footer(pg)
    return s


# ------------------------------------------------------------------ services
def page_services(l):
    pg = Page(l, 'services')
    d = D[l]
    svc = services_list(l)
    groups = [(UI[l]['groups'][0], [s for s in svc if s['group'] == 'beratung']), (UI[l]['groups'][1], [s for s in svc if s['group'] == 'prozess'])]
    idx = ''.join(f'<div class="ix-group"><h2 class="ix-h">{e(g)}</h2><ul>' + ''.join(f'<li><a href="#{x["uid"]}"><img src="{pg.b}img/{x["icon"]}" alt="" width="22" height="22">{e(x["title"])}</a></li>' for x in items) + '</ul></div>' for g, items in groups)
    secs = ''.join(f'''<article class="svc" id="{x['uid']}">
  <div class="svc-head"><span class="ac-ico"><img src="{pg.b}img/{x['icon']}" alt="" width="34" height="34"></span><h2 class="h-m">{e(x['title'])}</h2></div>
  <div class="rich">{body_html(x['html'])}</div>
</article>
''' for x in svc)
    s = head(pg, f"{d['nav'][0]} · {UI[l]['name']}", d['services_title'])
    s += '<body>\n' + page_hero(pg, d['services_title'], ' · '.join(x['title'] for x in svc[:5]) + ' …', HEADIMG['services'],
                                 f'<a class="btn light" href="{pg.href("contact")}" data-load>{e(UI[l]["contact_cta"])}<span class="arr">{ARR}</span></a>')
    s += f'<main id="main">\n<section class="panel svc-wrap" aria-label="{e(d["services_title"])}"><nav class="index" aria-label="{e(d["services_title"])}">{idx}</nav><div class="svc-list">{secs}</div></section>\n'
    s += contact_form(pg) + '</main>\n' + footer(pg)
    return s


def aside_card(pg):
    l = pg.l
    return f'''<aside class="aside" data-reveal>
    <figure class="photo"><img src="{pg.b}img/{HEADIMG['contact']}" alt="" width="2000" height="833" loading="lazy"></figure>
    <div class="infocard">
      <h2 class="h-s">{e(UI[l]['contact_cta'])}</h2>
      <p>Zanetti Rechtsanwälte AG<br>Blegistrasse 9, 6340 Baar</p>
      <p><a href="tel:+41417663585">T +41 41 766 35 85</a><br><a href="mailto:info@zanettilaw.ch">info@zanettilaw.ch</a></p>
      <a class="btn small light" href="{pg.href('contact')}">{e(nav_labels(l)['contact'])}<span class="arr">{ARR}</span></a>
    </div>
  </aside>'''


def page_generic(l, key, src, img=None):
    pg = Page(l, key)
    d = D[l]
    heads, body = section_parts(d[src])
    title = heads[0].rstrip(' –') if heads else nav_labels(l).get(key, key)
    lead = ' '.join(heads[1:]) if len(heads) > 1 else UI[l]['name']
    s = head(pg, f"{title} · {UI[l]['name']}", T(body)[:200])
    s += '<body>\n' + page_hero(pg, title, lead, img or HEADIMG['members'])
    s += f'<main id="main">\n<section class="panel"><div class="textgrid"><div class="rich" data-reveal>{body}</div>{aside_card(pg)}</div></section>\n'
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
        cards += f'<a class="acard mcard" href="{e(href)}" rel="noopener" data-reveal><span class="ac-top"><span class="m-logo"><img src="{pg.b}img/{logo}" alt="" width="480" height="120" loading="lazy"></span><span class="circ">{ARR}</span></span><h3>{e(T(name))}</h3><span class="ac-meta">{e(T(a))}</span></a>'
    title = ' '.join(heads)
    lna_href = re.search(r'href="([^"]+)"', lna.group(3)).group(1)
    s = head(pg, f"{d['nav'][5]} · {UI[l]['name']}", title)
    s += '<body>\n' + page_hero(pg, d['nav'][5], title, HEADIMG['members'])
    s += f'''<main id="main">
<section class="panel" aria-labelledby="lna-h">
  <div class="split">
    <div class="sec-head left" style="margin:0">
      <img src="{pg.b}img/1033_lna_logo_500px.180x0-is.jpg" alt="Legal Netlink Alliance" width="180" height="62" data-reveal>
      <h2 id="lna-h" class="h-l" data-reveal>{e(T(lna.group(1)))}</h2>
      <p class="lead" data-reveal>{e(T(lna.group(2)))}</p>
      <a class="btn" href="{e(lna_href)}" rel="noopener" data-reveal>{e(T(lna.group(3)))}<span class="arr">{ARR}</span></a>
    </div>
    <figure class="photo" data-reveal><img src="{pg.b}img/1028_zanetti_dienstleistungen_2x_neu.jpg" alt="" width="2000" height="833" loading="lazy"></figure>
  </div>
</section>
<section class="panel soft" aria-label="{e(d['nav'][5])}"><div class="cards">{cards}</div></section>
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
        mail = f'<p><a class="btn small" href="mailto:{e(m["email"])}">{e(m["email"])}<span class="arr">{ARR}</span></a></p>' if m['email'] else ''
        cards += f'''<li data-reveal><button type="button" class="photo person" data-open="m{i}" aria-haspopup="dialog"><img src="{pg.b}img/{f}" alt="" width="800" height="660" loading="lazy"><span class="tag">{e(X[l]['bio'])}<i>{ARR}</i></span><span class="ph-in"><span class="ph-name">{e(m['name'])}</span><span class="ph-role">{e(role)}</span></span></button></li>'''
        dialogs += f'''<dialog class="t-dialog" id="m{i}" aria-labelledby="m{i}-h">
  <div class="td-grid">
    <div class="td-side"><img src="{pg.b}img/{f}" alt="{e(m['name'])}" width="800" height="660" loading="lazy">
      <h2 id="m{i}-h" class="h-m">{e(m['name'])}</h2><p class="muted">{e(role)}</p>{mail}</div>
    <div class="td-body rich">{body_html(m['bio'])}</div>
  </div>
  <form method="dialog"><button class="td-close" type="submit" aria-label="{e(UI[l]['close'])}">✕</button></form>
</dialog>
'''
    s = head(pg, f"{d['nav'][2]} · {UI[l]['name']}", d['team_title'])
    s += '<body class="team-page">\n' + page_hero(pg, d['team_title'], UI[l]['team_hint'], HEADIMG['team'])
    s += f'''<main id="main">
<section class="panel" aria-label="{e(d['team_title'])}"><ol class="team-grid">{cards}</ol></section>
{dialogs}'''
    s += '</main>\n' + footer(pg)
    return s


def page_pubs(l):
    pg = Page(l, 'pubs')
    d = D[l]
    photos = {m['name']: (team_img(m), i) for i, m in enumerate(d['team'])}
    blocks = ''
    for k, p in enumerate(d['pubs']):
        items = ''.join(f'<li class="acard pubcard" data-reveal><span class="ac-top"><span class="p-year">{e(y)}</span></span><h3>{e(t)}</h3><p>{e(src)}</p></li>' for y, t, src in p['items'])
        ph, idx = photos.get(p['name'], ('', 0))
        who = (f'<a class="photo person" href="{pg.href("team")}#m{idx}"><img src="{pg.b}img/{ph}" alt="" width="800" height="660" loading="lazy"><span class="tag">{e(X[l]["bio"])}<i>{ARR}</i></span>'
               f'<span class="ph-in"><span class="ph-name">{e(p["name"])}</span><span class="ph-role">{e(UI[l]["pubs_n"].format(n=len(p["items"])) if len(p["items"]) > 1 else ("1 Publikation" if l == "de" else "1 publication"))}</span></span></a>') if ph else f'<h2 class="h-m">{e(p["name"])}</h2>'
        blocks += f'''<section class="panel{' soft' if k % 2 else ''}" aria-label="{e(p['name'])}">
  <div class="pub"><div class="pub-who" data-reveal>{who}</div><ol class="cards pub-list">{items}</ol></div>
</section>
'''
    s = head(pg, f"{d['nav'][3]} · {UI[l]['name']}", d['pubs_title'])
    s += '<body>\n' + page_hero(pg, d['pubs_title'], ' · '.join(p['name'] for p in d['pubs']), HEADIMG['pubs'])
    s += '<main id="main">\n' + blocks + '</main>\n' + footer(pg)
    return s


def page_contact(l):
    pg = Page(l, 'contact')
    d = D[l]
    heads, body = section_parts(d['contact'])
    intro = T(re.search(r'<p>(.*?)</p>', body, re.S).group(1))
    notes = re.findall(r'<p>\((.*?)\)</p>', body, re.S)
    note = T(notes[0]) if notes else ''
    offs = ''
    for name, lines_ in OFFICES[l]:
        q = '+'.join(lines_[1:]).replace(' ', '+')
        offs += f'<a class="acard" href="https://www.google.com/maps/search/?api=1&amp;query={e(q)}" rel="noopener" data-reveal><span class="ac-top"><h3>{e(name)}</h3><span class="circ">{ARR}</span></span><p>{"<br>".join(e(x) for x in lines_)}</p><span class="ac-meta">{e(X[l]["maps"])}</span></a>'
    s = head(pg, f"{d['nav'][4]} · {UI[l]['name']}", intro)
    s += '<body>\n' + page_hero(pg, heads[0] if heads else d['nav'][4], intro, HEADIMG['contact'])
    s += f'''<main id="main">
<section class="panel" aria-label="{e(d['nav'][4])}">
  <div class="biglines">
    <a href="tel:+41417663585" data-reveal><small>{e(UI[l]['phone_l'])}</small><span>+41 41 766 35 85</span><span class="circ">{ARR}</span></a>
    <a href="mailto:info@zanettilaw.ch" data-reveal><small>E-Mail</small><span>info@zanettilaw.ch</span><span class="circ">{ARR}</span></a>
  </div>
  <p class="muted" style="margin-top:18px" data-reveal>{e(UI[l]['fax_l'])} +41 41 766 35 80 · {e(note)}</p>
</section>
<section class="panel soft" aria-label="{e(X[l]['office'])}">
  <div class="split top">
    <div class="cards one">{offs}</div>
    <div class="map" data-reveal><iframe title="Google Maps – Zanetti Rechtsanwälte AG, Baar" src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d10840.119222836278!2d8.5708996!3d47.2159991!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xa08f4c2cdbca22ee!2sZanetti+Rechtsanw%C3%A4lte+AG!5e0!3m2!1sde!2sch!4v1552574030713" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</section>
'''
    s += contact_form(pg) + '</main>\n' + footer(pg)
    return s


def write(rel, s):
    p = os.path.join(OUT, rel, 'index.html')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


THEME = ''':root {
  --bg: #e9ecef; --panel: #fff; --soft: #f2f4f6; --ink: #0d1b28; --ink-2: #33414e; --muted: #64717d;
  --line: #e0e4e8; --line-strong: #c6ccd3; --dark: #071c2e; --on-dark: #f1f3f5; --on-dark-2: rgba(241,243,245,.66);
  --accent: #c9c1b1; --accent-strong: #7d96ab; --font: "Inter Tight", system-ui, sans-serif;
  --r-xl: 32px; --r-l: 22px; --ease: cubic-bezier(.22,1,.36,1);
}
'''
css = THEME + open(os.path.join(ROOT, '_src/law.css'), encoding='utf-8').read() + open(os.path.join(ROOT, '_src/zl.css'), encoding='utf-8').read()
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
