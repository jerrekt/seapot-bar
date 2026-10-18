# Seapot Bar Guide

Staff-facing drink recipes for Seapot Korean BBQ & Hot Pot.
Live at **https://seapot-bar.adsuaracloud.com** · customer menu: https://menu.adsuaracloud.com

## Layout
- `site/index.html` — the guide (recipes live in the `D` array; `chk:1` shows a "Confirm recipe" badge)
- `deploy/` — nginx config, systemd units, setup + auto-deploy scripts

## Deploy
Hosted on the `menu-server` LXC (CT 202, Adsuara), behind the `seapot-menu-sj` Cloudflare Tunnel.
A systemd timer pulls `main` every minute and applies changes — push to deploy.

First-time server setup: `deploy/setup.sh`.
