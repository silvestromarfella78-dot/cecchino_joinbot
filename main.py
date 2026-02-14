import os
import telebot
from telebot.types import ChatJoinRequest
from telebot.apihelper import ApiTelegramException

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("BOT")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN/BOT non impostato! (Railway > Variables)")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# (consigliato) evita conflitti se in passato avevi webhook
try:
    bot.remove_webhook()
except Exception:
    pass

# -------------------------------
# /start (solo per test)
# -------------------------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "✅ Bot approvazione attivo.\n\n"
        "Appena qualcuno richiede accesso, viene approvato automaticamente."
    )

# --------------------------------------------------------
# APPROVAZIONE AUTOMATICA (SENZA MESSAGGIO)
# --------------------------------------------------------
@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    try:
        bot.approve_chat_join_request(
            join_request.chat.id,
            join_request.from_user.id
        )
        print(f"✅ Approvata richiesta: user={join_request.from_user.id} chat={join_request.chat.id}")
    except ApiTelegramException as e:
        print(f"❌ Errore approvazione: {e.error_code} - {e.description}")
    except Exception as e:
        print("❌ Errore approvazione:", repr(e))

print("Bot ONLINE: approvazione automatica attiva (nessun DM)…")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
