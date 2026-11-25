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


MADE_BY = {'de': 'Gestaltet von', 'fr': 'Conçu par', 'it': 'Realizzato da', 'en': 'Designed by'}
X = {
 'de': dict(brand='Fachanwälte SAV', spec='Fachanwälte', cant='Kantone', langs_n='Sprachen', profile='Profil', open='Profil ansehen', all='Alle anzeigen',
            certified='Zertifiziert durch den Schweizerischen Anwaltsverband SAV', why='Was eine Fachanwältin, einen Fachanwalt auszeichnet',
            team='Spezialistinnen und Spezialisten aus der ganzen Schweiz', pick='Kanton wählen', site='Seiten', search='Suche'),
 'fr': dict(brand='Spécialistes FSA', spec='Spécialistes', cant='Cantons', langs_n='Langues', profile='Profil', open='Voir le profil', all='Tout afficher',
            certified='Certifiés par la Fédération Suisse des Avocats FSA', why='Ce qui distingue une avocate ou un avocat spécialiste',
            team='Des spécialistes dans toute la Suisse', pick='Choisir un canton', site='Pages', search='Recherche'),
 'it': dict(brand='Specialisti FSA', spec='Specialisti', cant='Cantoni', langs_n='Lingue', profile='Profilo', open='Vedi il profilo', all='Mostra tutti',
            certified='Certificati dalla Federazione Svizzera degli Avvocati FSA', why='Che cosa contraddistingue un avvocato specialista',
            team='Specialisti in tutta la Svizzera', pick='Scegliere un cantone', site='Pagine', search='Ricerca'),
 'en': dict(brand='Specialists SBA', spec='Specialists', cant='Cantons', langs_n='Languages', profile='Profile', open='View profile', all='Show all',
            certified='Certified by the Swiss Bar Association SBA', why='What sets a certified specialist apart',
            team='Specialists across Switzerland', pick='Choose a canton', site='Pages', search='Search'),
}
ARR = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3 11L11 3M4.5 3H11v6.5"/></svg>'
SEARCH = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="7" cy="7" r="5"/><path d="M11 11l3.5 3.5"/></svg>'
LEFT = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M9 2L4 7l5 5"/></svg>'
RIGHT = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 2l5 5-5 5"/></svg>'
IMG.update(contract='contract.jpg', scales='scales1.jpg', lausanne='lausanne.jpg', plenar='plenar.jpg', books='books.jpg')
for _l, _d in {
 'de': dict(contract='Arbeitsvertrag mit Füllfederhalter', scales='Justitia mit Waage', lausanne='Gebäude des Bundesgerichts in Lausanne', plenar='Plenarsaal des Bundesgerichts', books='Juristische Fachbücher im Regal'),
 'fr': dict(contract='Contrat de travail et stylo-plume', scales='Statue de la Justice avec sa balance', lausanne='Bâtiment du Tribunal fédéral à Lausanne', plenar='Salle plénière du Tribunal fédéral', books='Ouvrages juridiques sur une étagère'),
 'it': dict(contract='Contratto di lavoro e penna stilografica', scales='Statua della Giustizia con la bilancia', lausanne='Sede del Tribunale federale a Losanna', plenar='Sala plenaria del Tribunale federale', books='Libri giuridici su uno scaffale'),
 'en': dict(contract='Employment contract and fountain pen', scales='Statue of Justice holding scales', lausanne='Swiss Federal Supreme Court building in Lausanne', plenar='Plenary hall of the Federal Supreme Court', books='Law books on a shelf'),
}.items():
    ALT[_l].update(_d)

PAGEIMG = dict(about='workers', areas='ribbon', lawyers='plenar', contact='lausanne', disclaimer='court')


def url(l, key, frm=None):
    return f"{P[l]['slugs'][key]}.html"


# salutations that crept into the name field ("Buchzik Bertram Herr")
for _x in L:
    _x['name'] = re.sub(r'\s+(Herr|Frau|Monsieur|Madame)$', '', _x['name']).strip()

# role words in the title field are in the lawyer's own language; show them in the page language
TITLE_TR = {
    'fr': [('Fachanwalt SAV Arbeitsrecht', 'avocat spécialiste FSA droit du travail'), ('Mediatorin SAV', 'médiatrice FSA'),
           ('nicht praktizierend', 'non pratiquant'), ('öffentlicher Notar', 'notaire'), ('Rechtsanwältin', 'Avocate'),
           ('Rechtsanwalt', 'Avocat'), ('Fürsprecher', 'Avocat'), ('Advokat', 'Avocat'), ('Avvocata', 'Avocate'),
           ('Partnerin', 'associée'), ('Partner', 'associé'), ('Notar', 'notaire'), (' und ', ' et '), ('Senior Attorney', 'Avocat senior')],
    'it': [('Fachanwalt SAV Arbeitsrecht', 'avvocato specialista FSA diritto del lavoro'), ('Mediatorin SAV', 'mediatrice FSA'),
           ('nicht praktizierend', 'non praticante'), ('öffentlicher Notar', 'notaio'), ('Rechtsanwältin', 'Avvocata'),
           ('Rechtsanwalt', 'Avvocato'), ('Fürsprecher', 'Avvocato'), ('Advokat', 'Avvocato'), ('Avocate', 'Avvocata'),
           ('Avocat', 'Avvocato'), ('Partnerin', 'socia'), ('Partner', 'socio'), ('Notar', 'notaio'), (' und ', ' e '),
           ('Dr en droit', 'Dr. iur.'), ('Dr. en droit', 'Dr. iur.'), ('lic. en droit', 'lic. iur.'), ('lic.en droit', 'lic. iur.'), (' avec thèse', '')],
    'en': [('Fachanwalt SAV Arbeitsrecht', 'certified specialist SBA employment law'), ('Mediatorin SAV', 'mediator SBA'),
           ('nicht praktizierend', 'non-practising'), ('öffentlicher Notar', 'notary public'), ('Rechtsanwältin', 'Attorney'),
           ('Rechtsanwalt', 'Attorney'), ('Fürsprecher', 'Attorney'), ('Advokat', 'Attorney'), ('Avocate', 'Attorney'),
           ('Avocat', 'Attorney'), ('Avvocata', 'Attorney'), ('Partnerin', 'Partner'), ('Notar', 'notary'), (' und ', ' and '),
           ('Dr en droit', 'Dr. iur.'), ('Dr. en droit', 'Dr. iur.'), ('lic. en droit', 'lic. iur.'), ('lic.en droit', 'lic. iur.'), (' avec thèse', '')],
    'de': [('Avocate', 'Rechtsanwältin'), ('Avocat', 'Rechtsanwalt'), ('Avvocata', 'Rechtsanwältin'), ('Legale', 'Rechtsanwalt'),
           ('Dr en droit', 'Dr. iur.'), ('Dr. en droit', 'Dr. iur.'), ('lic. en droit', 'lic. iur.'), ('lic.en droit', 'lic. iur.'), (' avec thèse', '')],
}


SIT = {'de': ('Ihre Situation', 'Fachanwältinnen und Fachanwälte für Arbeitsrecht beraten Sie unter anderem bei:', 'Weitere Filter', ['Kündigung', 'Lohn nicht bezahlt', 'Überstunden', 'Arbeitszeugnis', 'Mobbing und Belästigung', 'Lohngleichheit', 'Arbeitsvertrag', 'Konkurrenzverbot']), 'fr': ('Votre situation', 'Les avocates et avocats spécialistes en droit du travail vous conseillent notamment en cas de :', 'Plus de filtres', ['Licenciement', 'Salaire impayé', 'Heures supplémentaires', 'Certificat de travail', 'Harcèlement au travail', 'Égalité salariale', 'Contrat de travail', 'Clause de non-concurrence']), 'it': ('La vostra situazione', 'Gli avvocati specialisti in diritto del lavoro vi consigliano tra l’altro in caso di:', 'Altri filtri', ['Licenziamento', 'Salario non pagato', 'Ore straordinarie', 'Certificato di lavoro', 'Mobbing e molestie', 'Parità salariale', 'Contratto di lavoro', 'Divieto di concorrenza']), 'en': ('Your situation', 'Certified employment law specialists advise you on matters such as:', 'More filters', ['Dismissal', 'Unpaid wages', 'Overtime', 'Reference letter', 'Harassment at work', 'Equal pay', 'Employment contract', 'Non-compete clause'])}


def tr_title(l, t):
    for a, b in TITLE_TR.get(l, []):
        t = t.replace(a, b)
    t = re.sub(r'(?<=\w) ?\| ?', ', ', t)
    return t


def localised(l, x):
    return dict(x, title=tr_title(l, x['title']))


def city(x):
    a = x['addr'][-1] if x['addr'] else ''
    return re.sub(r'^\d{4}\s*', '', a)


def initials(n):
    return ''.join(w[0] for w in n.split()[:2])


WITH_PHOTO = [x for x in L if x.get('img')]
_r = random.Random(7)
FEATURED = _r.sample(WITH_PHOTO, 10)


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
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
<script>document.documentElement.classList.add('js')</script>
{extra}
</head>
'''


def bar(l, active, page_key, profile=False):
    nav = P[l]['nav']
    keys = ['about', 'areas', 'lawyers', 'contact']
    links = ''.join(f'<a href="{url(l,k)}"{" aria-current=\"page\"" if k == active else ""}>{e(n)}</a>' for k, n in zip(keys, nav))
    langs = ''.join(
        f'<a href="../{x}/{(PROFILE[x] + ".html") if profile else url(x, page_key)}" hreflang="{x}" lang="{x}" data-keepquery title="{LANG_LABEL[x]}"{" aria-current=\"true\"" if x == l else ""}>{x.upper()}</a>'
        for x in LANGS)
    return f'''<div class="bar">
    <a class="brand" href="{url(l,'about')}"><img src="../assets/logo.svg" alt="" width="40" height="40"><span>{e(BIG[l])}<small>{e(X[l]["brand"])}</small></span></a>
    <nav class="pills" id="menu" aria-label="{e(UI[l]['law'])}">{links}</nav>
    <div class="bar-right">
      <nav class="langs" aria-label="{UI[l]['lang']}">{langs}</nav>
      <a class="btn small light" href="{url(l,'lawyers')}">{e(UI[l]['find'])}<span class="arr">{ARR}</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{UI[l]['menu']}</button>
    </div>
  </div>'''


def lines(t):
    """Split a headline into reveal lines of roughly equal length."""
    w = t.split()
    n = 1 if len(t) < 22 else 2 if len(t) < 48 else 3
    per = -(-len(w) // n)
    out = [' '.join(w[i:i + per]) for i in range(0, len(w), per)]
    return ''.join(f'<span class="l"><span style="--i:{i}">{e(x)}</span></span>' for i, x in enumerate(out))


def page_hero(l, key, title, sub='', profile=False, right=''):
    return f'''<header class="hero sub">
  <div class="hero-bg">{img(l, PAGEIMG[key], '', 1920, 1280, False)}</div>
  {bar(l, key, key, profile)}
  <div class="hero-main"><h1 id="h1" class="hero-h h-xl">{lines(title)}</h1></div>
  <div class="hero-foot">
    <p class="hero-sub" data-load>{e(sub)}</p>
    {right}
  </div>
</header>
'''


def footer(l, page_key, profile=False):
    nav = P[l]['nav']
    keys = ['about', 'areas', 'lawyers', 'contact', 'disclaimer']
    links = ''.join(f'<a href="{url(l,k)}">{e(n)}</a>' for k, n in zip(keys, nav))
    langs = ''.join(f'<a href="../{x}/{(PROFILE[x] + ".html") if profile else url(x, page_key)}" lang="{x}" data-keepquery>{LANG_LABEL[x]}</a>' for x in LANGS)
    cc = canton_counts(l)
    top = sorted(cc, key=lambda t: -t[2])[:6]
    cl = ''.join(f'<a href="{url(l,"lawyers")}?canton={k}">{e(n)} <span style="opacity:.5">{c}</span></a>' for k, n, c in top)
    return f'''<footer class="foot">
  <div class="foot-cta">
    <h2 class="h-l" data-reveal>{e(UI[l]['cta'])}</h2>
    <a class="btn light" href="{url(l,'lawyers')}" data-reveal>{e(UI[l]['find'])}<span class="arr">{ARR}</span></a>
  </div>
  <div class="foot-grid">
    <div><img class="foot-logo" src="../assets/logo.svg" alt="" width="48" height="48"><h3>{e(UI[l]['law'])}</h3><p>{e(UI[l]['count'].format(n=len(L), k=len(cc)))}. {e(X[l]['certified'])}.</p></div>
    <nav aria-label="{e(X[l]['site'])}"><h3>{e(X[l]['site'])}</h3>{links}</nav>
    <nav aria-label="{e(UI[l]['bycanton'])}"><h3>{e(UI[l]['bycanton'])}</h3>{cl}</nav>
    <nav aria-label="{UI[l]['lang']}"><h3>{UI[l]['lang']}</h3>{langs}</nav>
  </div>
  <div class="foot-legal"><p>© 2026 {e(UI[l]['law'])}</p><p><a href="{url(l,'disclaimer')}">{e(nav[4])}</a> · <a href="{url(l,'contact')}">{e(nav[3])}</a></p><a class="made" href="https://naktz.com/" rel="noopener"><span>{MADE_BY[l]}</span><img src="../assets/naktz-logo.png" alt="Naktz Media" width="105" height="30"></a></div>
  {credits_html(l)}
</footer>
<script src="../assets/site.js" defer></script>
</body>
</html>
'''


def img(l, key, cls='', w=1600, h=1000, lazy=True, sizes='100vw'):
    return (f'<img{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} src="../assets/{IMG[key]}" alt="{e(ALT[l][key])}" width="{w}" height="{h}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')


def canton_counts(l):
    names = P[l]['form']['cantons']
    c = {}
    for x in L:
        c[x['canton']] = c.get(x['canton'], 0) + 1
    return [(k, names[k], c.get(k, 0)) for k in names if c.get(k)]


def canton_select(l, sid, with_counts=False, cls=''):
    names = P[l]['form']['cantons']
    counts = {k: n for k, _, n in canton_counts(l)}
    opts = [f'<option value="">{e(UI[l]["all"])}</option>']
    for k, n in names.items():
        lab = f'{n} ({counts.get(k,0)})' if with_counts else n
        opts.append(f'<option value="{k}">{e(lab)}</option>')
    return f'<select id="{sid}" name="canton"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>{"".join(opts)}</select>'


def person_mini(l, x):
    return (f'<a class="pcard" href="{PROFILE[l]}.html?id={x["id"]}"><span class="pc-top"><img src="../img/lawyers/{x["img"]}" alt="" width="96" height="120" loading="lazy"><span class="circ">{ARR}</span></span>'
            f'<span class="pc-name">{e(x["name"])}</span><span class="pc-role">{e(x["firm"])}</span><span class="pc-city">{e(city(x))} · {e(x["canton"])}</span></a>')


def person_card(l, x, tag=True):
    return (f'<a class="photo" href="{PROFILE[l]}.html?id={x["id"]}"><img src="../img/lawyers/{x["img"]}" alt="" width="440" height="550" loading="lazy">'
            + (f'<span class="tag">{e(X[l]["profile"])}<i>{ARR}</i></span>' if tag else '')
            + f'<span class="ph-in"><span class="ph-name">{e(x["name"])}</span><span class="ph-role">{e(x["firm"])} · {e(city(x))}</span></span></a>')


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
    areas = [strip(x) for x in re.findall(r'<li>(.*?)</li>', p['areas'][1], re.S)]
    form_intro = p['form']['intro'] or strip(p['lawyers'][0])
    cc = canton_counts(l)
    faces = ''.join(f'<img src="../img/lawyers/{x["img"]}" alt="" width="38" height="38">' for x in FEATURED[:4])
    title = f'{banner_small(l)} {BIG[l]}'
    feat = FEATURED[0]
    s = head(l, title, lead)
    s += '<body class="home">\n' + f'<a class="skip" href="#main">{UI[l]["skip"]}</a>\n'
    s += f'''<header class="hero">
  <div class="hero-bg">{img(l,'workers','', 1920, 1440, False)}</div>
  {bar(l, 'about', 'about')}
  <div class="hero-main"><h1 id="h1" class="hero-h h-xl home-h"><span class="l"><span style="--i:0">{e(banner_small(l))}</span></span> <span class="l"><span style="--i:1" class="hl">{e(BIG[l])}</span></span></h1></div>
  <div class="hero-foot">
    <p class="hero-sub" data-load>{e(lead)}</p>
    <div class="widget-wrap" data-load>
      <form class="widget glass quick" action="{url(l,'lawyers')}" method="get">
        <p class="w-label">{e(form_intro)}</p>
        <label for="q-canton" class="vh">{e(p['form']['canton'])}</label>
        {canton_select(l, 'q-canton', True)}
        <button class="w-row w-main" type="submit" data-label-all="{e(UI[l]['show'])}" data-label-c="{e(UI[l]['showc'])}" data-total="{len(L)}"><span class="ic">{SEARCH}</span><span class="t">{e(UI[l]['show'].format(n=len(L)))}</span>{ARR}</button>
      </form>
    </div>
    <div class="hero-right" data-load>
      <div class="avatars glass chip"><span class="faces">{faces}</span><span>{len(L)} · {len(cc)} {e(X[l]['cant'])}</span></div>
      <p>{e(X[l]['certified'])}.</p>
    </div>
  </div>
</header>
<main id="main">
<section class="panel sit" aria-labelledby="si-h">
  <div class="sit-in">
    <div><h2 id="si-h" class="h-l" data-reveal>{e(SIT[l][0])}</h2><p class="lead" data-reveal>{e(SIT[l][1])}</p></div>
    <ul class="sits" data-reveal>{''.join(f'<li><a href="{url(l,"lawyers")}">{e(t)}<span class="arr">{ARR}</span></a></li>' for t in SIT[l][3])}</ul>
  </div>
</section>
<section class="panel" aria-labelledby="ab-h">
  <div class="sec-head">
    <h2 id="ab-h" class="h-l" data-reveal>{e(X[l]['why'])}</h2>
    <p class="lead center" data-reveal>{e(body[0][1])}</p>
  </div>
  <div class="bento">
    <figure class="photo" data-reveal>{img(l,'plenar','', 1920, 1269)}
      <div class="stats">
        <div class="stat glass"><b>{len(L)}</b><span>{e(X[l]['spec'])}</span></div>
        <div class="stat glass"><b>{len(cc)}</b><span>{e(X[l]['cant'])}</span></div>
        <div class="stat glass"><b>4</b><span>{e(X[l]['langs_n'])}</span></div>
      </div>
    </figure>
    <div class="quote-card" data-reveal>
      <blockquote class="long"><p>{e(body[1][1] if len(body) > 1 else lead)}</p></blockquote>
      <div class="who"><span class="mono">SAV</span><span><b>{e(UI[l]['law'])}</b><span>{e(p['title']['about'])}</span></span></div>
    </div>
    <a class="photo" href="{url(l,'lawyers')}" data-reveal>{img(l,'court','', 1920, 1276)}<span class="tag">{e(p['nav'][2])}<i>{ARR}</i></span><span class="ph-in"><span class="ph-name">{e(UI[l]['find'])}</span><span class="ph-role">{e(UI[l]['count'].format(n=len(L), k=len(cc)))}</span></span></a>
  </div>
</section>

<section class="panel" aria-labelledby="st-h">
  <div class="steps">
    <figure class="photo" data-reveal>{img(l,'scales','', 1920, 1440)}</figure>
    <div class="steps-mid">
      <div class="sec-head left" style="margin:0">
        <h2 id="st-h" class="h-m" data-reveal>{e(p['title']['about2'] if p['title']['about2'] != p['title']['about'] else UI[l]['law'])}</h2>
        {''.join(f'<p class="muted" data-reveal>{e(t)}</p>' for _, t in body[2:4])}
      </div>
      <div class="bignum" data-reveal><b>{len(L)}</b><span>{e(UI[l]['count'].format(n=len(L), k=len(cc)))}</span></div>
    </div>
    <div class="acc" data-reveal>
      {''.join(f'<details{" open" if k == 0 else ""}><summary>{e(h)}<span class="pm" aria-hidden="true"></span></summary><div class="acc-body"><p>{e(t)}</p></div></details>' for k, (h, t) in enumerate(fields))}
    </div>
  </div>
</section>

<section class="panel dark" aria-labelledby="tm-h">
  <div class="row-head">
    <div class="sec-head left" style="margin:0"><h2 id="tm-h" class="h-l" data-reveal>{e(X[l]['team'])}</h2></div>
    <div class="rail-ctl"><button type="button" data-rail="-1" aria-label="‹">{LEFT}</button><button type="button" data-rail="1" aria-label="›">{RIGHT}</button></div>
  </div>
  <div class="rail" id="rail">{''.join(person_mini(l, x) for x in FEATURED)}</div>
  <p style="margin-top:28px"><a class="btn light" href="{url(l,'lawyers')}">{e(UI[l]['show'].format(n=len(L)))}<span class="arr">{ARR}</span></a></p>
</section>

<section class="panel" aria-labelledby="ar-h">
  <div class="split top">
    <div class="sec-head left" style="margin:0">
      <h2 id="ar-h" class="h-l" data-reveal>{e(p['nav'][1])}</h2>
      <p class="lead" data-reveal>{e(areas_lead)}</p>
      <a class="btn" href="{url(l,'areas')}" data-reveal>{e(p['nav'][1])}<span class="arr">{ARR}</span></a>
    </div>
    <ul class="alist">
      {''.join(f'<li data-reveal><a href="{url(l,"areas")}#a{k}">{e(t)}<span class="arr">{ARR}</span></a></li>' for k, t in enumerate(areas[:6]))}
    </ul>
  </div>
</section>

<section class="panel soft" aria-labelledby="ct-h">
  <div class="split">
    <figure class="photo" data-reveal>{img(l,'lausanne','', 1920, 1280)}<span class="ph-in"><span class="ph-name">{e(ALT[l]['lausanne'])}</span></span></figure>
    <div class="sec-head left" style="margin:0">
      <h2 id="ct-h" class="h-l" data-reveal>{e(UI[l]['bycanton'])}</h2>
      <p class="lead" data-reveal>{e(UI[l]['count'].format(n=len(L), k=len(cc)))}</p>
      <div class="chips" data-reveal>{''.join(f'<a href="{url(l,"lawyers")}?canton={k}">{e(n)}<b>{c}</b></a>' for k, n, c in cc)}</div>
    </div>
  </div>
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
    s += '<body>\n' + f'<a class="skip" href="#main">{UI[l]["skip"]}</a>\n'
    s += page_hero(l, 'areas', p['nav'][1], lead, right=f'<a class="btn light" href="{url(l,"lawyers")}" data-load>{e(UI[l]["find"])}<span class="arr">{ARR}</span></a>')
    s += f'''<main id="main">
<section class="panel" aria-label="{e(p['nav'][1])}">
  <div class="row-head"><h2 class="h-l" data-reveal>{e(UI[l]['law'])}</h2><p class="muted" data-reveal>{len(items)} {e(p['nav'][1])}</p></div>
  <ol class="cards">
    {''.join(f'<li class="acard" id="a{k}" data-reveal><h3>{e(t)}</h3></li>' for k, t in enumerate(items))}
  </ol>
</section>
<section class="panel soft" aria-label="{e(UI[l]['find'])}">
  <div class="split">
    <figure class="photo" data-reveal>{img(l,'ribbon','', 1938, 1280)}<span class="ph-in"><span class="ph-role">{e(ALT[l]['ribbon'])}</span></span></figure>
    <div class="sec-head left" style="margin:0">
      <h2 class="h-l" data-reveal>{e(UI[l]['cta'])}</h2>
      <p class="lead" data-reveal>{e(UI[l]['count'].format(n=len(L), k=len(canton_counts(l))))}</p>
      <a class="btn" href="{url(l,'lawyers')}" data-reveal>{e(UI[l]['find'])}<span class="arr">{ARR}</span></a>
    </div>
  </div>
</section>
</main>
'''
    s += footer(l, 'areas')
    return s


def page_lawyers(l):
    p = P[l]
    f = p['form']
    intro = f['intro'] or strip(p['lawyers'][0])
    genders = ''.join(f'<option value="{k}">{e(v)}</option>' for k, v in f['genders'].items())
    data = [dict(id=x['id'], n=x['name'], f=x['firm'], t=tr_title(l, x['title']), c=x['canton'], g=x['gender'],
                 a=x['addr'][-1] if x['addr'] else '', i=x.get('img', '')) for x in L]
    s = head(l, f"{p['nav'][2]} · {UI[l]['law']}", intro)
    s += '<body class="dir">\n' + f'<a class="skip" href="#main">{UI[l]["skip"]}</a>\n'
    s += page_hero(l, 'lawyers', p['nav'][2], intro)
    s += f'''<main id="main">
<section class="panel finder" aria-label="{e(p['nav'][2])}">
  <form class="filters" id="filters" role="search">
    <h2 class="h-s">{e(X[l]['search'])}</h2>
    <label class="lab" for="f-canton">{e(f['canton'])}{canton_select(l,'f-canton', cls='inp')}</label>
    <details class="more" id="more"><summary>{e(SIT[l][2])}</summary><div class="more-in">
    <label class="lab" for="f-last">{e(f['lastname'])}<input class="inp" id="f-last" name="lastname" type="search" autocomplete="off"></label>
    <label class="lab" for="f-first">{e(f['firstname'])}<input class="inp" id="f-first" name="firstname" type="search" autocomplete="off"></label>
    <label class="lab" for="f-gender">{e(f['gender'])}<select class="inp" id="f-gender" name="gender"><option value="">{e(UI[l]['any'])}</option>{genders}</select></label>
    <fieldset class="mode">
      <legend class="vh">{e(f['radios'][1])}</legend>
      <label><input type="radio" name="result_type" value="all" checked><span>{e(f['radios'][1])}</span></label>
      <label><input type="radio" name="result_type" value="rand"><span>{e(f['radios'][0])}</span></label>
    </fieldset>
    </div></details>
    <div class="actions">
      <button class="btn line" type="reset">{e(f['buttons'][0])}</button>
      <button class="btn" type="submit">{e(f['buttons'][1])}<span class="arr">{SEARCH}</span></button>
    </div>
  </form>
  <div class="results">
    <p class="count h-m" id="count" aria-live="polite" data-one="{e(UI[l]['one'])}" data-many="{e(UI[l]['results'])}"></p>
    <ol class="lawyers" id="list"></ol>
    <p class="empty" id="empty" hidden>{e(UI[l]['none'])}</p>
    <noscript><ol class="lawyers">{''.join(f'<li><a class="lrow" href="{PROFILE[l]}.html?id={x["id"]}"><span class="who"><b>{e(x["name"])}</b><span>{e(x["firm"])}</span></span><span class="where">{e(x["addr"][-1] if x["addr"] else "")}</span></a></li>' for x in L)}</ol></noscript>
  </div>
</section>
</main>
<script>window.LAWYERS={json.dumps(data, ensure_ascii=False)};window.PROFILE="{PROFILE[l]}.html";window.CANTONS={json.dumps(f['cantons'], ensure_ascii=False)};window.ARR='{ARR}';</script>
'''
    s += footer(l, 'lawyers')
    return s


def page_profile(l):
    p = P[l]
    full = {str(x['id']): localised(l, x) for x in L}
    s = head(l, f"{p['nav'][2]} · {UI[l]['law']}", UI[l]['law'])
    s += '<body class="profile-page">\n' + f'<a class="skip" href="#main">{UI[l]["skip"]}</a>\n'
    s += f'''<header class="hero sub slim">
  <div class="hero-bg">{img(l,'library','', 1920, 1253, False)}</div>
  {bar(l, 'lawyers', 'lawyers', True)}
  <div class="hero-main"><p class="hero-sub">{e(UI[l]['law'])}</p></div>
  <div class="hero-foot"></div>
</header>
<main id="main">
<article class="panel profile" id="profile" data-labels='{e(json.dumps({k: UI[l][k] for k in ("phone","fax","email","web","back","notfound","addr","canton_title")}, ensure_ascii=False))}'>
  <h1 class="h-l" id="p-name">{e(p['nav'][2])}</h1>
  <p><a class="back" href="{url(l,'lawyers')}">{LEFT}{e(UI[l]['back'])}</a></p>
</article>
</main>
<script>window.PEOPLE={json.dumps(full, ensure_ascii=False)};window.CANTONS={json.dumps(p['form']['cantons'], ensure_ascii=False)};window.LIST="{url(l,'lawyers')}";window.ARR='{ARR}';window.LEFT='{LEFT}';</script>
'''
    s += footer(l, 'lawyers', profile=True)
    return s


def page_contact(l):
    p = P[l]
    txt = ' '.join(t for _, t in paras(''.join(p['contact'])))
    cc = canton_counts(l)
    s = head(l, f"{p['nav'][3]} · {UI[l]['law']}", txt)
    s += '<body>\n' + f'<a class="skip" href="#main">{UI[l]["skip"]}</a>\n'
    s += page_hero(l, 'contact', p['nav'][3], UI[l]['law'])
    s += f'''<main id="main">
<section class="panel" aria-label="{e(p['nav'][3])}">
  <div class="split">
    <div class="sec-head left" style="margin:0">
      <p class="h-m" data-reveal>{e(txt)}</p>
      <a class="btn" href="{url(l,'lawyers')}" data-reveal>{e(UI[l]['find'])}<span class="arr">{ARR}</span></a>
    </div>
    <figure class="photo" data-reveal>{img(l,'court','', 1920, 1276)}<span class="ph-in"><span class="ph-role">{e(ALT[l]['court'])}</span></span></figure>
  </div>
</section>
<section class="panel soft" aria-labelledby="ct-h">
  <div class="row-head"><h2 id="ct-h" class="h-l" data-reveal>{e(UI[l]['bycanton'])}</h2><p class="muted" data-reveal>{e(UI[l]['count'].format(n=len(L), k=len(cc)))}</p></div>
  <div class="chips" data-reveal>{''.join(f'<a href="{url(l,"lawyers")}?canton={k}">{e(n)}<b>{c}</b></a>' for k, n, c in cc)}</div>
</section>
</main>
'''
    s += footer(l, 'contact')
    return s


def page_disclaimer(l):
    p = P[l]
    parts = paras(''.join(p['disclaimer']))
    body = ''
    for _, t in parts:
        body += f'<h2>{e(t)}</h2>' if len(t) < 40 else f'<p>{e(t)}</p>'
    s = head(l, f"{p['nav'][4]} · {UI[l]['law']}", parts[0][1][:150] if parts else '')
    s += '<body>\n' + f'<a class="skip" href="#main">{UI[l]["skip"]}</a>\n'
    s += page_hero(l, 'disclaimer', p['nav'][4], UI[l]['law'])
    s += f'''<main id="main">
<section class="panel">
  <div class="textgrid">
    <div class="rich" data-reveal>{body}</div>
    <aside class="aside" data-reveal>
      <figure class="photo">{img(l,'library','', 1920, 1253)}</figure>
      <div class="infocard"><h2 class="h-s">{e(UI[l]['find'])}</h2><p>{e(UI[l]['count'].format(n=len(L), k=len(canton_counts(l))))}</p><a class="btn small light" href="{url(l,'lawyers')}">{e(p['nav'][2])}<span class="arr">{ARR}</span></a></div>
    </aside>
  </div>
</section>
</main>
'''
    s += footer(l, 'disclaimer')
    return s


def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8', newline='\n').write(s)


THEME = ''':root {
  --bg: #ebeae6; --panel: #fff; --soft: #f4f3f0; --ink: #121211; --ink-2: #3b3a37; --muted: #6b6a66;
  --line: #e3e1dc; --line-strong: #cbc9c3; --dark: #111110; --on-dark: #f3f2ee; --on-dark-2: rgba(243,242,238,.64);
  --accent: #dcc897; --accent-strong: #a8893f; --font: "Inter Tight", system-ui, sans-serif;
  --r-xl: 32px; --r-l: 22px; --ease: cubic-bezier(.22,1,.36,1);
}
'''
css = THEME + open(os.path.join(ROOT, '_src/law.css'), encoding='utf-8').read() + open(os.path.join(ROOT, '_src/fa.css'), encoding='utf-8').read()
write(os.path.join(OUT, 'assets/site.css'), css)

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
