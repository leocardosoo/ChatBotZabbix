# handlers/grupos.py
from telegram import Update
from telegram.ext import ContextTypes
from zabbix_api import get_groups

async def grupos_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    groups = get_groups()
    lines = [f"{g['groupid']} • {g['name']}" for g in groups[:200]]
    await update.message.reply_text("\n".join(lines))
