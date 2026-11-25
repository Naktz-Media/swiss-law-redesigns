"""Builds the avocat-droit-du-travail.ch / fachanwalt-arbeitsrecht.ch redesign.

Reads _data/fa_pages.json (page texts in de/fr/it/en) and _data/fa_lawyers.json
(the 202 lawyers of the SAV directory) and writes static pages into
avocat-droit-du-travail/<lang>/.
"""
import json, re, html, os, random

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'avocat-droit-du-travail')
P = json.load(open(os.path.join(ROOT, '_data/fa_pages.json'), encoding='utf-8'))
L = json.load(open(os.path.join(ROOT, '_data/fa_lawyers.json'), encoding='utf-8'))
LANGS = ['fr', 'de', 'it', 'en']
LANG_LABEL = {'de': 'Deutsch', 'fr': 'Français', 'it': 'Italiano', 'en': 'English'}
PROFILE = {'de': 'anwaeltinnen-anwaelte-profil', 'fr': 'avocates-avocats-profil',
           'it': 'elenco-degli-avvocati-profilo', 'en': 'lawyers-profile'}
BIG = {'de': 'Arbeitsrecht', 'fr': 'Droit du travail', 'it': 'Diritto del lavoro', 'en': 'Labour Law'}

UI = {
 'de': dict(find='Fachanwalt finden', menu='Menü', close='Schliessen', phone='Telefon', fax='Telefax', email='E-Mail',
            web='Website', back='Zur Liste', results='{n} Einträge', one='1 Eintrag', all='Alle Kantone', any='Alle',
            show='{n} Fachanwältinnen und Fachanwälte anzeigen', showc='{n} in {c} anzeigen', bycanton='Nach Kanton',
            none='Keine Einträge gefunden. Ändern Sie die Suche oder setzen Sie sie zurück.',
            cta='Die passende Fachanwältin, den passenden Fachanwalt finden', pics='Bilder', lang='Sprache',
            count='{n} Fachanwältinnen und Fachanwälte in {k} Kantonen', addr='Adresse', notfound='Dieses Profil wurde nicht gefunden.',
            canton_title='Kanton', law='Fachanwältinnen und Fachanwälte SAV Arbeitsrecht', skip='Zum Inhalt'),
 'fr': dict(find='Trouver un avocat', menu='Menu', close='Fermer', phone='Téléphone', fax='Téléfax', email='E-mail',
            web='Site web', back='Retour à la liste', results='{n} résultats', one='1 résultat', all='Tous les cantons', any='Tous',
            show='Afficher {n} avocates et avocats', showc='Afficher {n} dans le canton {c}', bycanton='Par canton',
            none='Aucun résultat. Modifiez la recherche ou réinitialisez-la.',
            cta='Trouver l’avocate ou l’avocat spécialiste qu’il vous faut', pics='Images', lang='Langue',
            count='{n} avocates et avocats spécialistes dans {k} cantons', addr='Adresse', notfound='Ce profil est introuvable.',
            canton_title='Canton', law='Avocates et avocats spécialistes FSA en droit du travail', skip='Aller au contenu'),
 'it': dict(find='Trovare un avvocato', menu='Menu', close='Chiudi', phone='Telefono', fax='Telefax', email='E-mail',
            web='Sito web', back='Torna all’elenco', results='{n} risultati', one='1 risultato', all='Tutti i cantoni', any='Tutti',
            show='Mostra {n} avvocati specialisti', showc='Mostra {n} nel cantone {c}', bycanton='Per cantone',
            none='Nessun risultato. Modificate la ricerca o reimpostatela.',
            cta='Trovare l’avvocato specialista adatto a voi', pics='Immagini', lang='Lingua',
            count='{n} avvocati specialisti in {k} cantoni', addr='Indirizzo', notfound='Questo profilo non è stato trovato.',
            canton_title='Cantone', law='Avvocati specialisti FSA in diritto del lavoro', skip='Vai al contenuto'),
 'en': dict(find='Find a specialist', menu='Menu', close='Close', phone='Phone', fax='Fax', email='E-mail',
            web='Website', back='Back to the list', results='{n} results', one='1 result', all='All cantons', any='All',
            show='Show {n} certified specialists', showc='Show {n} in {c}', bycanton='By canton',
            none='No results. Change the search or reset it.',
            cta='Find the certified specialist you need', pics='Pictures', lang='Language',
            count='{n} certified specialists in {k} cantons', addr='Address', notfound='This profile could not be found.',
            canton_title='Canton', law='Certified Specialists SBA in Labour Law', skip='Skip to content'),
}

CREDITS = json.load(open(os.path.join(OUT, 'assets/credits.json'), encoding='utf-8')) if os.path.exists(os.path.join(OUT, 'assets/credits.json')) else []
IMG = {
 'workers': 'winterthurer-bibliotheken-071824-sennhof-spinnerei-buehler-f.jpg',
 'ribbon': 'fotografie-bandfabrik-binderei.jpg',
 'court': 'schweizerisches-bundesgericht-roter-saal-ca-1990.jpg',
 'library': 'bibliothek-des-schweizerischen-bundesgerichts-ca-1990.jpg',
}
ALT = {
 'de': {'workers': 'Belegschaft der Spinnerei Bühler in Sennhof, historische Fotografie', 'ribbon': 'Arbeiterin in einer Bandfabrik, historische Fotografie',
        'court': 'Roter Saal des Schweizerischen Bundesgerichts in Lausanne', 'library': 'Bibliothek des Schweizerischen Bundesgerichts'},
 'fr': {'workers': 'Personnel de la filature Bühler à Sennhof, photographie historique', 'ribbon': 'Ouvrière dans une fabrique de rubans, photographie historique',
        'court': 'Salle rouge du Tribunal fédéral à Lausanne', 'library': 'Bibliothèque du Tribunal fédéral'},
 'it': {'workers': 'Personale della filanda Bühler a Sennhof, fotografia storica', 'ribbon': 'Operaia in una fabbrica di nastri, fotografia storica',
        'court': 'Sala rossa del Tribunale federale a Losanna', 'library': 'Biblioteca del Tribunale federale'},
 'en': {'workers': 'Workforce of the Bühler spinning mill in Sennhof, historical photograph', 'ribbon': 'Worker in a ribbon factory, historical photograph',
        'court': 'Red courtroom of the Swiss Federal Supreme Court in Lausanne', 'library': 'Library of the Swiss Federal Supreme Court'},
}

e = lambda s: html.escape(s or '', quote=True)
strip = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def paras(block):
    """Split an rte html block into a list of ('h'|'p', text) parts."""
    parts = []
    for tag, txt in re.findall(r'<(h1|p)>(.*?)</\1>', block, re.S):
        t = strip(txt)
        if t:
            parts.append(('h' if tag == 'h1' else 'p', t))
    return parts


def banner_small(l):
    b = P[l]['banner']
    b = re.sub(r'<b>.*?</b>', '', b, flags=re.S)
    return strip(b)


def credits_html(l):
    if not CREDITS:
        return ''
    items = []
    for c in CREDITS:
        t = c.get('title', '')
        who = (' · ' + e(c['creator'])) if c.get('creator') else ''
        items.append(f'<a href="{e(c.get("page") or c.get("source",""))}">{e(t)}</a>{who}, {e(c.get("licence") or c.get("license",""))}')
    return f'<p class="credits">{UI[l]["pics"]}: ' + '; '.join(items) + '</p>'


def url(l, key, frm=None):
    s = P[l]['slugs'][key]
    return f'{s}.html'


def head(l, title, desc, extra=''):
    alts = ''.join(f'<link rel="alternate" hreflang="{x}" href="../{x}/">' for x in LANGS)
    return f'''<!doctype html>
<html lang="{l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{alts}
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders:wght@800&family=Public+Sans:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
<script>document.documentElement.classList.add('js')</script>
{extra}
</head>
'''


def topbar(l, active, page_key, profile=False):
    nav = P[l]['nav']
    keys = ['about', 'areas', 'lawyers', 'contact', 'disclaimer']
    links = ''.join(
        f'<a href="{url(l,k)}"{" aria-current=\"page\"" if k == active else ""}>{e(n)}</a>'
        for k, n in zip(keys, nav))
    langs = []
    for x in LANGS:
        target = (PROFILE[x] + '.html') if profile else url(x, page_key)
        cur = ' aria-current="true"' if x == l else ''
        langs.append(f'<a href="../{x}/{target}" hreflang="{x}" lang="{x}" data-keepquery title="{LANG_LABEL[x]}"{cur}>{x.upper()}</a>')
    return f'''<a class="skip" href="#main">{UI[l]["skip"]}</a>
<header class="top">
  <a class="mark" href="{url(l,'about')}"><span>{e(banner_small(l))}</span> <b>{e(BIG[l])}</b></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{UI[l]["menu"]}</button>
  <div class="menu" id="menu">
    <nav class="nav" aria-label="{e(UI[l]['law'])}">{links}</nav>
    <nav class="langs" aria-label="{UI[l]['lang']}">{''.join(langs)}</nav>
  </div>
</header>
'''


def footer(l, page_key, profile=False):
    nav = P[l]['nav']
    keys = ['about', 'areas', 'lawyers', 'contact', 'disclaimer']
    links = ''.join(f'<a href="{url(l,k)}">{e(n)}</a>' for k, n in zip(keys, nav))
    langs = ''.join(f'<a href="../{x}/{(PROFILE[x] + ".html") if profile else url(x, page_key)}" lang="{x}" data-keepquery>{LANG_LABEL[x]}</a>' for x in LANGS)
    cantons = len({x['canton'] for x in L})
    return f'''<footer class="foot">
  <div class="foot-top">
    <div class="foot-cta">
      <h2 class="foot-h" data-reveal>{e(UI[l]['find'])}</h2>
      <p class="foot-sub" data-reveal>{e(UI[l]['cta'])}</p>
      <a class="btn btn-accent" href="{url(l,'lawyers')}" data-reveal>{e(P[l]['nav'][2])}</a>
    </div>
    <div class="foot-links" data-reveal>{links}</div>
    <div class="foot-links" data-reveal>{langs}</div>
  </div>
  <div class="foot-legal">
    <p>{e(UI[l]['count'].format(n=len(L), k=cantons))} · © {e(UI[l]['law'])}</p>
    {credits_html(l)}
  </div>
  <p class="foot-word" aria-hidden="true">{e(BIG[l])}</p>
</footer>
<script src="../assets/site.js" defer></script>
</body>
</html>
'''


def img(l, key, cls='', w=1600, h=1000, lazy=True, sizes='100vw'):
    return (f'<img class="{cls}" src="../assets/{IMG[key]}" alt="{e(ALT[l][key])}" width="{w}" height="{h}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')


def canton_counts(l):
    names = P[l]['form']['cantons']
    c = {}
    for x in L:
        c[x['canton']] = c.get(x['canton'], 0) + 1
    order = list(names.keys())
    return [(k, names[k], c.get(k, 0)) for k in order if c.get(k)]


def canton_select(l, sid, with_counts=False):
    names = P[l]['form']['cantons']
    counts = {k: n for k, _, n in canton_counts(l)}
    opts = [f'<option value="">{e(UI[l]["all"])}</option>']
    for k, n in names.items():
        lab = f'{n} ({counts.get(k,0)})' if with_counts else n
        opts.append(f'<option value="{k}">{e(lab)}</option>')
    return f'<select id="{sid}" name="canton">{"".join(opts)}</select>'


def stairs(sentence, n=5):
    w = sentence.split()
    per = max(1, round(len(w) / n))
    lines = [' '.join(w[i:i + per]) for i in range(0, len(w), per)]
    if len(lines) > n:
        lines[n - 1] = ' '.join(lines[n - 1:])
        lines = lines[:n]
    return ''.join(f'<span class="stair s{i}">{e(t)}</span>' for i, t in enumerate(lines))


# ---------------------------------------------------------------- pages

def page_about(l):
    p = P[l]
    lead = paras(p['about'][0])[0][1]
    body = paras(p['about'][1])
    adv = paras(p['about2'][1])
    fields = []
    i = 0
    while i < len(adv) - 1:
        if adv[i][0] == 'h':
            fields.append((adv[i][1], adv[i + 1][1])); i += 2
        else:
            i += 1
    areas_lead = paras(p['areas'][0])[0][1]
    fields.append((p['nav'][1], areas_lead, url(l, 'areas')))
    form_intro = p['form']['intro'] or strip(p['lawyers'][0])
    cantons = canton_counts(l)
    title = f'{banner_small(l)} {BIG[l]}'
    s = head(l, title, lead)
    s += '<body class="home">\n' + topbar(l, 'about', 'about')
    s += f'''<main id="main">
<section class="hero" aria-labelledby="h1">
  <h1 id="h1" class="hero-h"><span class="hero-small mask"><span>{e(banner_small(l))}</span></span><span class="hero-big mask"><span>{e(BIG[l])}</span></span></h1>
  <div class="hero-foot">
    <p class="hero-sub" data-load>{e(form_intro)}</p>
    <form class="quick" action="{url(l,'lawyers')}" method="get" data-load>
      <label for="q-canton" class="vh">{e(p['form']['canton'] if 'canton' in p['form'] else 'Kanton')}</label>
      {canton_select(l, 'q-canton', True)}
      <button class="btn btn-ink" type="submit" data-label-all="{e(UI[l]['show'])}" data-label-c="{e(UI[l]['showc'])}" data-total="{len(L)}">{e(UI[l]['show'].format(n=len(L)))}</button>
    </form>
  </div>
</section>

<section class="stairs-sec" aria-label="{e(p['title']['about'])}">
  <p class="stairs-text" data-reveal>{stairs(lead)}</p>
  <figure class="stairs-pics" data-reveal>
    {img(l,'workers','pic', 1920, 1299)}
    {img(l,'ribbon','pic', 1938, 1280)}
  </figure>
</section>

<section class="sav" aria-labelledby="sav-h">
  <h2 id="sav-h" class="h2" data-reveal>{e(p['title']['about'])}</h2>
  <div class="sav-cols">
    {''.join(f'<p data-reveal>{e(t)}</p>' for _, t in body)}
  </div>
</section>

<div class="fields">
'''
    tones = ['f-dark', 'f-accent', 'f-surface']
    for k, f in enumerate(fields):
        link = f'<a class="field-link" href="{f[2]}">{e(f[0])} →</a>' if len(f) > 2 else ''
        s += f'''  <section class="field {tones[k % 3]} {'mirror' if k % 2 else ''}" aria-labelledby="f{k}">
    <p class="field-text" data-reveal>{e(f[1])}{(' ' + link) if link else ''}</p>
    <h2 id="f{k}" class="field-h" data-reveal>{e(f[0])}</h2>
  </section>
'''
    s += f'''</div>
<figure class="band" data-reveal>{img(l,'library','pic band-img', 1920, 1253)}</figure>

<section class="cantons" aria-labelledby="ct-h">
  <div class="cantons-col">
    <h2 id="ct-h" class="h3" data-reveal>{e(UI[l]['bycanton'])}</h2>
    <ul class="rows">
      {''.join(f'<li data-reveal><a href="{url(l,"lawyers")}?canton={k}"><span class="code">{k}</span><span class="name">{e(n)}</span><span class="val">{c}</span></a></li>' for k, n, c in cantons)}
    </ul>
  </div>
  <figure class="cantons-pic" data-reveal>{img(l,'court','pic', 1920, 1276)}</figure>
</section>
</main>
'''
    s += footer(l, 'about')
    return s


def page_areas(l):
    p = P[l]
    lead = paras(p['areas'][0])[0][1]
    items = [strip(x) for x in re.findall(r'<li>(.*?)</li>', p['areas'][1], re.S)]
    s = head(l, f"{p['nav'][1]} · {UI[l]['law']}", lead)
    s += '<body>\n' + topbar(l, 'areas', 'areas')
    s += f'''<main id="main">
<section class="phead" aria-labelledby="h1">
  <h1 id="h1" class="phead-h mask"><span>{e(p['nav'][1])}</span></h1>
  <p class="phead-lead" data-load>{e(lead)}</p>
</section>
<section class="areas" aria-label="{e(p['nav'][1])}">
  <div class="areas-wrap">
  <ul class="area-list">
    {''.join(f'<li data-reveal>{e(t)}</li>' for t in items)}
  </ul>
  <figure class="areas-pic" data-reveal>{img(l,'workers','pic', 1920, 1299)}</figure>
  </div>
</section>
<figure class="band" data-reveal>{img(l,'library','pic band-img', 1920, 1253)}</figure>
</main>
'''
    s += footer(l, 'areas')
    return s


def page_lawyers(l):
    p = P[l]
    f = p['form']
    intro = f['intro'] or strip(p['lawyers'][0])
    genders = ''.join(f'<option value="{k}">{e(v)}</option>' for k, v in f['genders'].items())
    data = [dict(id=x['id'], n=x['name'], f=x['firm'], t=x['title'], c=x['canton'], g=x['gender'],
                 a=x['addr'][-1] if x['addr'] else '', i=x.get('img', '')) for x in L]
    s = head(l, f"{p['nav'][2]} · {UI[l]['law']}", intro)
    s += '<body class="dir">\n' + topbar(l, 'lawyers', 'lawyers')
    s += f'''<main id="main">
<section class="phead" aria-labelledby="h1">
  <h1 id="h1" class="phead-h mask"><span>{e(p['nav'][2])}</span></h1>
  <p class="phead-lead" data-load>{e(intro)}</p>
</section>
<section class="finder" aria-label="{e(p['nav'][2])}">
  <form class="filters" id="filters" role="search">
    <div class="fld"><label for="f-last">{e(f['lastname'])}</label><input id="f-last" name="lastname" type="search" autocomplete="off"></div>
    <div class="fld"><label for="f-first">{e(f['firstname'])}</label><input id="f-first" name="firstname" type="search" autocomplete="off"></div>
    <div class="fld"><label for="f-canton">{e(f['canton'])}</label>{canton_select(l,'f-canton')}</div>
    <div class="fld"><label for="f-gender">{e(f['gender'])}</label><select id="f-gender" name="gender"><option value="">{e(UI[l]['any'])}</option>{genders}</select></div>
    <fieldset class="mode">
      <legend class="vh">{e(f['radios'][1])}</legend>
      <label><input type="radio" name="result_type" value="all" checked> {e(f['radios'][1])}</label>
      <label><input type="radio" name="result_type" value="rand"> {e(f['radios'][0])}</label>
    </fieldset>
    <div class="actions">
      <button class="btn btn-ghost" type="reset">{e(f['buttons'][0])}</button>
      <button class="btn btn-ink" type="submit">{e(f['buttons'][1])}</button>
    </div>
  </form>
  <div class="results">
    <p class="count" id="count" aria-live="polite" data-one="{e(UI[l]['one'])}" data-many="{e(UI[l]['results'])}"></p>
    <ol class="lawyers" id="list"></ol>
    <p class="empty" id="empty" hidden>{e(UI[l]['none'])}</p>
    <noscript><ol class="lawyers">{''.join(f'<li><a href="{PROFILE[l]}.html?id={x["id"]}"><span class="who"><b>{e(x["name"])}</b><span>{e(x["firm"])}</span></span><span class="where">{e(x["addr"][-1] if x["addr"] else "")}</span></a></li>' for x in L)}</ol></noscript>
  </div>
</section>
</main>
<script>window.LAWYERS={json.dumps(data, ensure_ascii=False)};window.PROFILE="{PROFILE[l]}.html";window.CANTONS={json.dumps(f['cantons'], ensure_ascii=False)};</script>
'''
    s += footer(l, 'lawyers')
    return s


def page_profile(l):
    p = P[l]
    full = {str(x['id']): x for x in L}
    s = head(l, f"{p['nav'][2]} · {UI[l]['law']}", UI[l]['law'])
    s += '<body class="profile-page">\n' + topbar(l, 'lawyers', 'lawyers', profile=True)
    s += f'''<main id="main">
<article class="profile" id="profile" data-labels='{e(json.dumps({k: UI[l][k] for k in ("phone","fax","email","web","back","notfound","addr","canton_title")}, ensure_ascii=False))}'>
  <h1 class="phead-h" id="p-name">{e(p['nav'][2])}</h1>
  <p><a class="btn btn-ink" href="{url(l,'lawyers')}">{e(UI[l]['back'])}</a></p>
</article>
</main>
<script>window.PEOPLE={json.dumps(full, ensure_ascii=False)};window.CANTONS={json.dumps(p['form']['cantons'], ensure_ascii=False)};window.LIST="{url(l,'lawyers')}";</script>
'''
    s += footer(l, 'lawyers', profile=True)
    return s


def page_contact(l):
    p = P[l]
    txt = ' '.join(t for _, t in paras(''.join(p['contact'])))
    s = head(l, f"{p['nav'][3]} · {UI[l]['law']}", txt)
    s += '<body>\n' + topbar(l, 'contact', 'contact')
    s += f'''<main id="main">
<section class="phead" aria-labelledby="h1">
  <h1 id="h1" class="phead-h mask"><span>{e(p['nav'][3])}</span></h1>
  <p class="phead-sub" data-load>{e(UI[l]['law'])}</p>
</section>
<section class="contact" aria-label="{e(p['nav'][3])}">
  <div class="contact-text">
    <p class="statement" data-reveal>{e(txt)}</p>
    <a class="btn btn-ink" href="{url(l,'lawyers')}" data-reveal>{e(p['nav'][2])}</a>
  </div>
  <figure class="contact-pic" data-reveal>{img(l,'library','pic', 1920, 1253)}</figure>
</section>
<section class="cantons-rows" aria-labelledby="ctr-h">
  <h2 id="ctr-h" class="h3" data-reveal>{e(UI[l]['bycanton'])}</h2>
  <ul class="display-rows">
    {''.join(f'<li data-reveal><a href="{url(l,"lawyers")}?canton={k}"><span>{e(n)}</span><span class="n">{c}</span></a></li>' for k, n, c in canton_counts(l)[:6])}
  </ul>
</section>
<figure class="band" data-reveal>{img(l,'court','pic band-img', 1920, 1276)}</figure>
</main>
'''
    s += footer(l, 'contact')
    return s


def page_disclaimer(l):
    p = P[l]
    parts = paras(''.join(p['disclaimer']))
    body = ''
    for _, t in parts:
        if len(t) < 40:
            body += f'<h2 class="h3" data-reveal>{e(t)}</h2>'
        else:
            body += f'<p data-reveal>{e(t)}</p>'
    s = head(l, f"{p['nav'][4]} · {UI[l]['law']}", parts[0][1][:150] if parts else '')
    s += '<body>\n' + topbar(l, 'disclaimer', 'disclaimer')
    s += f'''<main id="main">
<section class="phead" aria-labelledby="h1">
  <h1 id="h1" class="phead-h mask"><span>{e(p['nav'][4])}</span></h1>
  <p class="phead-sub" data-load>{e(UI[l]['law'])}</p>
</section>
<section class="legal">
  <div class="legal-text">{body}</div>
  <figure class="legal-pic" data-reveal>{img(l,'court','pic', 1920, 1276)}</figure>
</section>
</main>
'''
    s += footer(l, 'disclaimer')
    return s


def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8', newline='\n').write(s)


for l in LANGS:
    d = os.path.join(OUT, l)
    about = page_about(l)
    write(os.path.join(d, 'index.html'), about)
    write(os.path.join(d, url(l, 'about')), about)
    write(os.path.join(d, url(l, 'areas')), page_areas(l))
    write(os.path.join(d, url(l, 'lawyers')), page_lawyers(l))
    write(os.path.join(d, PROFILE[l] + '.html'), page_profile(l))
    write(os.path.join(d, url(l, 'contact')), page_contact(l))
    write(os.path.join(d, url(l, 'disclaimer')), page_disclaimer(l))

write(os.path.join(OUT, 'index.html'), '''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Avocates et avocats spécialistes FSA en droit du travail</title>
<meta http-equiv="refresh" content="0; url=fr/">
<link rel="canonical" href="fr/">
<script>var l=(navigator.language||'fr').slice(0,2);location.replace((['de','fr','it','en'].indexOf(l)>-1?l:'fr')+'/');</script>
</head><body><p><a href="fr/">Français</a> · <a href="de/">Deutsch</a> · <a href="it/">Italiano</a> · <a href="en/">English</a></p></body></html>
''')
print('built fa:', len(LANGS), 'languages,', len(L), 'lawyers')
