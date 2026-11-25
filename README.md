# Swiss law redesigns

Design refreshes of two Swiss law websites. Each keeps the original page structure, page names and content.

| Site | Original | Preview |
|---|---|---|
| Fachanwälte SAV Arbeitsrecht | http://avocat-droit-du-travail.ch/ | `avocat-droit-du-travail/` |
| Zanetti Rechtsanwälte | http://www.zanettilaw.ch/ | `zanettilaw/` |

Both are static HTML/CSS/JS, served by GitHub Pages from the repository root.

## Rebuilding

The pages are generated from the content in `_data/`. The shared stylesheet is `_src/law.css`; each site adds its own theme and `_src/fa.css` or `_src/zl.css`. The build scripts are assembled from `_src/*_top.py` and `_src/*_rest.py`.

```
python build_fa.py   # avocat-droit-du-travail/{fr,de,it,en}/
python build_zl.py   # zanettilaw/ (DE) and zanettilaw/en/
```

Picture credits for the open-licence images are listed in `avocat-droit-du-travail/assets/credits.json` and in the site footer.
