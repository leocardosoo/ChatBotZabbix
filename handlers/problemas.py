# handlers/problemas.py
from telegram import Update
from telegram.ext import ContextTypes
from zabbix_api import get_problemas

async def problemas_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    severity = None
    if context.args:
        try:
            severity = int(context.args[0])
        except:
            severity = None

    triggers = get_problemas(severity_min=severity)
    if not triggers:
        await update.message.reply_text("✅ Nenhum problema ativo (ou filtro sem resultados).")
        return

    lines = []
    for t in triggers[:50]:
        host = (t.get("hosts") or [{"host":"N/A"}])[0].get("host")
        prio = t.get("priority", "0")
        desc = t.get("description", "Sem descrição")
        lines.append(f"[{prio}] {host} — {desc}")

    await update.message.reply_text("\n".join(lines))
