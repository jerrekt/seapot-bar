# seapot-bar — notes for Claude

Staff-only bar guide for Seapot → https://seapot-bar.adsuaracloud.com (noindex)
Owner: BJ (GitHub `jerrekt`). Sister sites: `jerrekt/seapot-menu` (customer menu), `jerrekt/jerrekts-bar` (home bar — this guide's UI was ported from its `site/guide/`).

## Rules
- **Only `git push` when BJ says "push".** Commit locally, show a preview/screenshot, then wait.
- Keep chat replies short; keep the page condensed (collapsed one-line cards, tap to expand).
- Drinks/ingredients follow the customer menu (`seapot-menu`). Pour amounts not confirmed by BJ get `chk:1` → "CONFIRM" tag.
- Guide shows prices; they must match the customer menu (`seapot-menu`). Any new drink or price change goes in **both** repos.

## Layout
- `site/index.html` — single file. Recipes are the `D` array: `{cat,name,note?,chk?,glass,garnish,ing:[[amt,name,note?]],steps:[]}`.
- Look matches the menu: Cinzel gold "SEAPOT", gold dividers, `#0a0a0a` / `#151515` / `#c9a84c`.
- Glass badge opens a pop-up with a gold line drawing (`GW` map, matched by `glassKey()`); set `photo:"img/x.jpg"` to use a real photo.
- Footer: "Not sure? lol gl" + small "hi from jerrekt".

## Hosting
Same as seapot-menu: CT 202 `menu-server`, nginx root `/opt/seapot-bar/site`, `seapot-bar-autodeploy.timer` (1 min), Cloudflare Tunnel `seapot-menu-sj` (locally managed, `/etc/cloudflared/config.yml`). nginx block must include `listen [::]:80;` (cloudflared uses `::1`).

## Gotchas
- nginx sends `Cache-Control: no-cache, must-revalidate` so pushes show up right away. Still stale → Cloudflare Purge Everything.

## Open items
- Recipes now follow the Seapot recipe book (photos, Oct 23). Cocktail/mocktail glasses and garnishes not in the book are unconfirmed.
- Still CONFIRM: Sunrise (Virgin) grenadine amount, Fresh Lemonade, Mimosa, Shirley Temple.
- Book drinks NOT on the customer menu (not added, need BJ's call + prices in both repos): Man-Gogo mocktail, Margarita, Mojito, Martini, Vodka Sun, Strawberry Lemon Drop, Soju Bomb.
- Allergens need BJ's input on what's in the premixes before `ALLERGENS` is filled in the menu.
