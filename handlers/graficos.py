# handlers/graficos.py
from telegram import Update
from telegram.ext import ContextTypes
from zabbix_api import get_host_by_name, get_item_by_key, get_history
from utils.images import plot_values
from config import GRAPH_POINTS

async def grafico_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Use: /grafico <host> <item_key>")
        return
    hostname = context.args[0]
    item_key = " ".join(context.args[1:])
    h = get_host_by_name(hostname)
    if not h:
        await update.message.reply_text("Host não encontrado.")
        return
    item = get_item_by_key(h["hostid"], item_key)
    if not item:
        await update.message.reply_text("Item não encontrado.")
        return
    history = get_history(item["itemid"], limit=GRAPH_POINTS)
    if not history:
        await update.message.reply_text(f"Sem histórico. Último valor: {item.get('lastvalue')}")
        return
    ys = [float(x['value']) for x in history]
    title = item.get("name") or item.get("key_")
    buf = plot_values(ys, title=title)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buf)
    buf.close()
