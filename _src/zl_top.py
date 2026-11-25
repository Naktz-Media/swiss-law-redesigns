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


