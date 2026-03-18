# -*- coding: utf-8 -*-
import os
import telebot
from telebot.types import ChatJoinRequest
from telebot.apihelper import ApiTelegramException

# --- TOKEN: Railway variable "BOT" (o "BOT_TOKEN") ---
TOKEN = os.getenv("BOT") or os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT (o BOT_TOKEN) non impostato in Railway > Variables")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# (consigliato) pulizia webhook residuo
try:
    bot.remove_webhook()
except Exception:
    pass

# --- FOTO: incolla qui il file_id quando lo ottieni ---
PHOTO_FILE_ID = "AgACAgQAAxkBAAMDabqhCnYOi6UvF_8DMHcLPCbWFLcAAncNaxvveKFRSHbuAnPXCQ8BAAMCAAN5AAM6BA"  # es: "AgACAgQAAxkBAA..."

# --- TESTI ---
START_TEXT = (
    "✅ Bot attivo.\n\n"
    "📸 Per ottenere il FILE_ID della foto:\n"
    "1) inviami una foto qui in privato\n"
    "2) ti rispondo con il FILE_ID\n\n"
    "Poi incollalo in PHOTO_FILE_ID e redeploy."
)

WELCOME_TEXT = (
    "<b>BENVENUTO NEL CANALE PUBBLICO del</b>\n"
    "<b>CECCHINO ⚽️🏆🔫</b>\n\n"
    "<b>Guarda qui che cosa abbiamo COMBINATO</b>\n"
    "<b><u><i>SE VUOI DISTRUGGERLI PURE TE CLICCA QUI SOTTO👌</i></u></b>\n\n"
    "<b>contatta la mia assistenza</b>\n"
    "<b>che la SNIPER ROOM (canale privato) è ancora aperta! 👇</b>\n\n"
    "⚠️ <b><a href=\"https://t.me/m/7IaxhPVCYjlk\">ASSISTENZA</a></b>"
)

# --- /start ---
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, START_TEXT)

# --- Ottieni FILE_ID foto: manda una foto al bot in privato ---
@bot.message_handler(content_types=["photo"])
def get_photo_id(message):
    file_id = message.photo[-1].file_id
    bot.reply_to(message, f"FILE_ID:\n<code>{file_id}</code>")
    print("FILE_ID:", file_id)

# --- Join request: approva + invia DM (foto opzionale) ---
@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    print(f"JOIN REQUEST: chat_id={chat_id} user_id={user_id} user_chat_id={user_chat_id}")

    # 1) Approva richiesta
    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"APPROVATA: user={user_id}")
    except ApiTelegramException as e:
        print(f"ERRORE APPROVAZIONE: {e.error_code} - {e.description}")
        return
    except Exception as e:
        print("ERRORE APPROVAZIONE:", repr(e))
        return

    # 2) Invia DM
    target = user_chat_id or user_id
    try:
        if PHOTO_FILE_ID:
            bot.send_photo(target, PHOTO_FILE_ID)
        bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
        print(f"DM INVIATO A {target}")
    except ApiTelegramException as e:
        print(f"ERRORE DM: {e.error_code} - {e.description}")
    except Exception as e:
        print("ERRORE DM:", repr(e))

print("ONLINE")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
