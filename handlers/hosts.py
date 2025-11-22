# handlers/hosts.py
from telegram import Update
from telegram.ext import ContextTypes
from zabbix_api import get_hosts, get_host_by_name

async def hosts_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filtro = context.args[0] if context.args else None
    hosts = get_hosts(search=filtro)
    if not hosts:
        await update.message.reply_text("Nenhum host encontrado.")
        return
    lines = [f"{h['hostid']} • {h['host']}" for h in hosts[:100]]
    await update.message.reply_text("\n".join(lines))

async def host_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /host <hostname>")
        return
    h = get_host_by_name(context.args[0])
    if not h:
        await update.message.reply_text("Host não encontrado.")
        return
    ip = h.get("interfaces", [{}])[0].get("ip", "N/A")
    await update.message.reply_text(f"Host: {h.get('host')}\nID: {h.get('hostid')}\nIP: {ip}")
