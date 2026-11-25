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


