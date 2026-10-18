#!/usr/bin/env bash
# One-time setup on the menu-server LXC (CT 202). Run as root.
# Afterwards, every push to main is live within ~1 minute.
set -euo pipefail
REPO=git@github.com:jerrekt/seapot-bar.git
DIR=/opt/seapot-bar
KEY=/root/.ssh/seapot_bar_deploy
HOST=seapot-bar.adsuaracloud.com

if [[ "$(hostname)" != "menu-server" ]]; then
  read -rp "Hostname is $(hostname), not menu-server. Continue anyway? [y/N] " a; [[ $a == y ]] || exit 1
fi

echo "==> Packages"
apt-get update -qq
apt-get install -y -qq git openssh-client nginx curl >/dev/null

echo "==> Deploy key (separate from jerrekts-bar — GitHub deploy keys are per-repo)"
mkdir -p /root/.ssh && chmod 700 /root/.ssh
[[ -f $KEY ]] || ssh-keygen -q -t ed25519 -N "" -C "menu-server seapot-bar deploy" -f "$KEY"
ssh-keyscan github.com >> /root/.ssh/known_hosts 2>/dev/null || true
sort -u /root/.ssh/known_hosts -o /root/.ssh/known_hosts
echo
echo "Add this as a READ-ONLY deploy key:"
echo "  github.com/jerrekt/seapot-bar -> Settings -> Deploy keys -> Add deploy key"
echo
cat "$KEY.pub"
echo
read -rp "Press Enter once the key is added... "

echo "==> Clone"
export GIT_SSH_COMMAND="ssh -i $KEY -o IdentitiesOnly=yes"
if [[ -d $DIR/.git ]]; then git -C "$DIR" pull -q; else git clone -q "$REPO" "$DIR"; fi
git -C "$DIR" config core.sshCommand "ssh -i $KEY -o IdentitiesOnly=yes"
chmod -R a+rX "$DIR"

echo "==> Auto-deploy timer"
cp "$DIR"/deploy/*.service "$DIR"/deploy/*.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable -q --now seapot-bar-autodeploy.timer

echo "==> nginx"
cp "$DIR"/deploy/nginx-seapot-bar.conf /etc/nginx/sites-available/seapot-bar
ln -sf /etc/nginx/sites-available/seapot-bar /etc/nginx/sites-enabled/seapot-bar
nginx -t -q && systemctl reload nginx

echo "==> Smoke test"
sleep 1
echo "    guide $(curl -s -o /dev/null -w '%{http_code}' -H "Host: $HOST" http://127.0.0.1/)"
echo "==> Auto-deploy is on. Logs: journalctl -u seapot-bar-autodeploy -n 20"
echo
echo "Last step (once): Cloudflare Zero Trust -> Tunnels -> seapot-menu-sj -> Public Hostname"
echo "  add  $HOST  ->  http://localhost:80"
