# bot.py (central)
from telegram.ext import ApplicationBuilder, CommandHandler
from config import TELEGRAM_TOKEN, ADMIN_CHAT_IDS, POLL_INTERVAL_SECONDS
from handlers.problemas import problemas_cmd
from handlers.hosts import hosts_cmd, host_cmd
from handlers.itens import itens_cmd
from handlers.graficos import grafico_cmd
from handlers.grupos import grupos_cmd
from handlers.problemas import problemas_cmd
from utils import images  # opcional
from zabbix_api import get_problemas

SEEN_TRIGGER_IDS = set()

async def start_cmd(update, context):
    await update.message.reply_text("🤖 ZabbixBot top! Digite /ajuda")

async def ajuda_cmd(update, context):
    text = (
        "/problemas [severidade]\n/hosts [filtro]\n/host <nome>\n/itens <host>\n"
        "/grupos\n/grafico <host> <item_key>\n/cpu <host>\n/status <host>\n/ajuda\n"
    )
    await update.message.reply_text(text)

async def poll_job(context):
    global SEEN_TRIGGER_IDS
    try:
        triggers = get_problemas()
        new = []
        for t in triggers:
            tid = t.get("triggerid")
            if tid and tid not in SEEN_TRIGGER_IDS:
                SEEN_TRIGGER_IDS.add(tid)
                new.append(t)
        for t in new:
            host = (t.get("hosts") or [{"host":"N/A"}])[0].get("host")
            prio = t.get("priority", "0")
            desc = t.get("description", "Sem descrição")
            text = f"🚨 NOVO PROBLEMA\n[{prio}] {host}\n{desc}"
            for chat in ADMIN_CHAT_IDS:
                try:
                    await context.bot.send_message(chat_id=chat, text=text)
                except Exception as e:
                    print(f"Erro ao enviar para {chat}: {e}")
    except Exception as e:
        print("Erro no poll_job:", e)

def build_and_run():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("ajuda", ajuda_cmd))
    app.add_handler(CommandHandler("problemas", problemas_cmd))
    app.add_handler(CommandHandler("hosts", hosts_cmd))
    app.add_handler(CommandHandler("host", host_cmd))
    app.add_handler(CommandHandler("itens", itens_cmd))
    app.add_handler(CommandHandler("grupos", grupos_cmd))
    app.add_handler(CommandHandler("grafico", grafico_cmd))
    app.job_queue.run_repeating(poll_job, interval=POLL_INTERVAL_SECONDS, first=10)
    print("🤖 Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    build_and_run()
