# -*- coding: utf-8 -*-
import os
import telebot
from telebot.types import ChatJoinRequest
from telebot.apihelper import ApiTelegramException

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("BOT")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN/BOT non impostato! (Railway > Variables)")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

try:
    bot.remove_webhook()
except Exception:
    pass

# ✅ quando hai il file_id, incollalo qui
PHOTO_FILE_ID = ""  # es: "AgACAgQAAxkBAA...."

WELCOME_TEXT = (
    "<b>BENVENUTO NEL CANALE PUBBLICO del</b>\n"
    "<b>CECCHINO ⚽️🏆🔫</b>\n\n"
    "<b>Guarda qui che cosa abbiamo COMBINATO</b>\n"
    "<b><u><i>SE VUOI DISTRUGGERLI PURE TE CLICCA QUI SOTTO👌</i></u></b>\n\n"
    "<b>contatta la mia assistenza</b>\n"
    "<b>che la SNIPER ROOM (canale privato) è ancora aperta! 👇</b>\n\n"
    "⚠️ <b><a href=\"https://t.me/m/7IaxhPVCYjlk\">ASSISTENZA</a></b>\n"
)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "✅ Bot attivo.\n\n"
        "📸 Per ottenere il FILE_ID:\n"
        "1) inviami una foto qui in privato\n"
        "2) ti rispondo con il FILE_ID da copiare\n\n"
        "Poi incollalo in PHOTO_FILE_ID e redeploy."
    )

# ✅ Handler per ottenere il file_id della foto
@bot.message_handler(content_types=["photo"])
def get_photo_id(message):
    try:
        file_id = message.photo[-1].file_id  # la più grande
        bot.reply_to(message, f"FILE_ID:\n<code>{file_id}</code>")
        print("📸 FILE_ID:", file_id)
    except Exception as e:
        print("❌ get_photo_id error:", repr(e))

@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"✅ APPROVATA: user={user_id}")
    except ApiTelegramException as e:
        print(f"❌ APPROVAZIONE: {e.error_code} - {e.description}")
        return

    target = user_chat_id or user_id

    try:
        if PHOTO_FILE_ID:
            bot.send_photo(target, PHOTO_FILE_ID)
        bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
        print(f"✅ DM INVIATO A {target}")
    except ApiTelegramException as e:
        print(f"❌ DM FAIL: {e.error_code} - {e.description}")

print("ONLINE")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"✅ APPROVATA: user={user_id}")
    except ApiTelegramException as e:
        print(f"❌ APPROVAZIONE: {e.error_code} - {e.description}")
        return

    target = user_chat_id or user_id

    try:
        if PHOTO_FILE_ID:
            bot.send_photo(target, PHOTO_FILE_ID)
        bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
        print(f"✅ DM INVIATO A {target}")
    except ApiTelegramException as e:
        print(f"❌ DM FAIL: {e.error_code} - {e.description}")

print("ONLINE")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
