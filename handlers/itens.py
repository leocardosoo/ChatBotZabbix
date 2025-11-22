# handlers/itens.py
from telegram import Update
from telegram.ext import ContextTypes
from zabbix_api import get_host_by_name, get_items_by_hostid

async def itens_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /itens <hostname>")
        return
    h = get_host_by_name(context.args[0])
    if not h:
        await update.message.reply_text("Host não encontrado.")
        return
    items = get_items_by_hostid(h["hostid"])
    lines = [f"{it['itemid']} • {it.get('name') or it.get('key_')} • last: {it.get('lastvalue')}" for it in items[:50]]
    await update.message.reply_text("\n".join(lines))
