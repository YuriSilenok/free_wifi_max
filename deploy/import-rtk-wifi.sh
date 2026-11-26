#!/usr/bin/env bash
set -euo pipefail
umask 077
/opt/max-bots/venv/bin/python - <<'PY'
import sqlite3,time
with sqlite3.connect('/var/lib/max-bots/wifi/bot.sqlite3') as source, sqlite3.connect('/opt/max-bots/backups/wifi-before-rtk-'+str(int(time.time()))+'.sqlite3') as target:
    source.backup(target)
PY
/opt/max-bots/venv/bin/python /opt/max-bots/current/manage.py wifi import-wifi --file /opt/max-bots/rtk-wifi-import.json
/opt/max-bots/venv/bin/python /opt/max-bots/current/manage.py wifi status
systemctl show max-bot-wifi -p ActiveState -p SubState
