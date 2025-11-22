# Zabbix Telegram Bot 🤖

Um bot do Telegram que envia alertas do Zabbix diretamente para os administradores. Permite monitorar triggers, hosts, gráficos e itens de forma prática e em tempo real.

---

## ⚡ Funcionalidades

- Enviar alertas automáticos de novos problemas do Zabbix para usuários no Telegram.
- Consultar problemas existentes e filtrá-los por severidade.
- Listar hosts, itens e grupos do Zabbix.
- Gerar gráficos simples de métricas do Zabbix.
- Comandos interativos via Telegram:
  - `/start` – Inicia o bot.
  - `/ajuda` – Mostra todos os comandos disponíveis.
  - `/problemas [severidade]` – Lista problemas filtrados.
  - `/hosts [filtro]` – Lista hosts.
  - `/host <nome>` – Informações detalhadas de um host.
  - `/itens <host>` – Lista de itens de um host.
  - `/grupos` – Lista de grupos.
  - `/grafico <host> <item_key>` – Gera gráfico simples de um item.

---

## ⚙️ Configuração

1. **Criar um bot no Telegram**
   - Abra o Telegram e converse com o [BotFather](https://t.me/BotFather).
   - Use `/newbot` e siga as instruções.
   - Copie o **token** fornecido pelo BotFather.

2. **Obter IDs dos administradores**
   - Use [@userinfobot](https://t.me/userinfobot) e envie qualquer mensagem.
   - Ele vai te retornar seu **user ID**.
   - Esse ID deve ser adicionado na lista `ADMIN_CHAT_IDS` no arquivo `config.py`.

3. **Configurar o `config.py`**
```python
TELEGRAM_TOKEN = "SEU_TOKEN_TELEGRAM"
ADMIN_CHAT_IDS = [SEU_ID_REAL, OUTRO_ID]  # IDs dos admins que receberão alertas
POLL_INTERVAL_SECONDS = 30  # Intervalo entre checagens automáticas
GRAPH_POINTS = 60           # Pontos para gráficos
ZABBIX_URL = "http://IP/zabbix/api_jsonrpc.php"
ZABBIX_TOKEN = "SEU_TOKEN_API_ZABBIX"
