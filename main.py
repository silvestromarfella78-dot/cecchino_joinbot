# -*- coding: utf-8 -*-
import os
import telebot
from telebot.types import ChatJoinRequest

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("BOT")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN/BOT non impostato!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "✅ ONLINE")

@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    bot.approve_chat_join_request(join_request.chat.id, join_request.from_user.id)

print("ONLINE")
bot.infinity_polling(skip_pending=True)    "⚠️ <b><a href=\"https://t.me/m/7IaxhPVCYjlk\">ASSISTENZA</a></b>\n"
)

# ========= /start =========
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "✅ Bot attivo.\n\n"
        "📸 Per ottenere il FILE_ID della foto:\n"
        "1) inviami una foto qui in privato\n"
        "2) ti rispondo con il FILE_ID\n\n"
        "Poi incollalo in PHOTO_FILE_ID e redeploy."
    )

# ========= ESTRAI FILE_ID FOTO =========
@bot.message_handler(content_types=["photo"])
def get_photo_id(message):
    try:
        file_id = message.photo[-1].file_id
        bot.reply_to(message, f"FILE_ID:\n<code>{file_id}</code>")
        print("📸 FILE_ID:", file_id)
    except Exception as e:
        print("❌ get_photo_id error:", repr(e))

# ========= JOIN REQUEST: APPROVA + INVIA =========
@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    print(f"📩 JOIN REQUEST: chat_id={chat_id} user_id={user_id} user_chat_id={user_chat_id}")

    # 1) Approva richiesta
    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"✅ APPROVATA: user={user_id}")
    except ApiTelegramException as e:
        print(f"❌ APPROVAZIONE: {e.error_code} - {e.description}")
        return
    except Exception as e:
        print("❌ APPROVAZIONE error:", repr(e))
        return

    # 2) Invia DM (prima user_chat_id se c’è, poi user_id)
    targets = []
    if user_chat_id:
        targets.append(user_chat_id)
    targets.append(user_id)

    for target in targets:
        try:
            if PHOTO_FILE_ID:
                bot.send_photo(target, PHOTO_FILE_ID)
            bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
            print(f"✅ DM INVIATO A {target}")
            break
        except ApiTelegramException as e:
            print(f"❌ DM FAIL a {target}: {e.error_code} - {e.description}")
        except Exception as e:
            print(f"❌ DM FAIL a {target}: {repr(e)}")

print("Bot ONLINE…")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
# -------------------------------
# /start (test + guida file_id)
# -------------------------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "✅ Bot attivo.\n\n"
        "📸 Per ottenere il FILE_ID della foto:\n"
        "1) inviami una foto qui in privato\n"
        "2) ti rispondo con il FILE_ID\n\n"
        "Poi incollalo in PHOTO_FILE_ID e redeploy."
    )

# -------------------------------
# Estrai file_id foto
# -------------------------------
@bot.message_handler(content_types=["photo"])
def get_photo_id(message):
    try:
        file_id = message.photo[-1].file_id
        bot.reply_to(message, f"FILE_ID:\n<code>{file_id}</code>")
        print("📸 FILE_ID:", file_id)
    except Exception as e:
        print("❌ get_photo_id error:", repr(e))

# -------------------------------
# Join request: approva + invia
# -------------------------------
@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    print(f"📩 JOIN REQUEST: chat_id={chat_id} user_id={user_id} user_chat_id={user_chat_id}")

    # 1) Approva
    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"✅ APPROVATA: user={user_id}")
    except ApiTelegramException as e:
        print(f"❌ APPROVAZIONE: {e.error_code} - {e.description}")
        return
    except Exception as e:
        print("❌ APPROVAZIONE error:", repr(e))
        return

    # 2) Invia DM (prima user_chat_id se c’è, poi fallback su user_id)
    targets = []
    if user_chat_id:
        targets.append(user_chat_id)
    targets.append(user_id)

    for target in targets:
        try:
            if PHOTO_FILE_ID:
                bot.send_photo(target, PHOTO_FILE_ID)
            bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
            print(f"✅ DM INVIATO A {target}")
            break
        except ApiTelegramException as e:
            print(f"❌ DM FAIL a {target}: {e.error_code} - {e.description}")
        except Exception as e:
            print(f"❌ DM FAIL a {target}: {repr(e)}")

print("Bot ONLINE…")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)    bot.send_message(
        message.chat.id,
        "✅ Bot attivo.\n\n"
        "📸 Per ottenere il FILE_ID:\n"
        "1) inviami una foto qui in privato\n"
        "2) ti rispondo con il FILE_ID da copiare\n\n"
        "Poi incollalo in PHOTO_FILE_ID e redeploy."
    )

@bot.message_handler(content_types=["photo"])
def get_photo_id(message):
    try:
        file_id = message.photo[-1].file_id
        bot.reply_to(message, f"FILE_ID:\n<code>{file_id}</code>")
        print(f"📸 FILE_ID inviato: {file_id}")
    except Exception as e:
        print("❌ Errore get_photo_id:", repr(e))

@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    print(f"📩 JOIN REQUEST: chat_id={chat_id} user_id={user_id} user_chat_id={user_chat_id}")

    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"✅ APPROVATA: user={user_id}")
    except ApiTelegramException as e:
        print(f"❌ ERRORE APPROVAZIONE: {e.error_code} - {e.description}")
        return
    except Exception as e:
        print("❌ ERRORE APPROVAZIONE:", repr(e))
        return

    targets = []
    if user_chat_id:
        targets.append(user_chat_id)
    targets.append(user_id)

    for target in targets:
        try:
            if PHOTO_FILE_ID:
                bot.send_photo(target, PHOTO_FILE_ID)
            bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
            print(f"✅ DM INVIATO A {target}")
            break
        except ApiTelegramException as e:
            print(f"❌ DM FALLITO A {target}: {e.error_code} - {e.description}")
        except Exception as e:
            print(f"❌ DM FALLITO A {target}: {repr(e)}")

print("Bot del Cecchino ONLINE…")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)Se vuoi invece accedere a tutte le nostre giocate prima che le quote scendono 📉,
alle nostre analisi, scalate periodiche, dati e statistiche, contatta la mia assistenza
che la SNIPER ROOM (canale privato) è ancora aperta! 👇

⚠️ <b><a href="https://t.me/m/7IaxhPVCYjlk">ASSISTENZA</a></b>
"""

# -------------------------------
# /start
# -------------------------------
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

# --------------------------------------------------------
# ✅ ESTRAI FILE_ID FOTO (invia foto al bot in privato)
# --------------------------------------------------------
@bot.message_handler(content_types=["photo"])
def get_photo_id(message):
    try:
        file_id = message.photo[-1].file_id  # versione più grande
        bot.reply_to(message, f"FILE_ID:\n<code>{file_id}</code>")
        print(f"📸 FILE_ID inviato: {file_id}")
    except Exception as e:
        print("❌ Errore get_photo_id:", repr(e))

# --------------------------------------------------------
# APPROVAZIONE AUTOMATICA + INVIO (foto se presente) + testo
# --------------------------------------------------------
@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    print(f"📩 JOIN REQUEST: chat_id={chat_id} user_id={user_id} user_chat_id={user_chat_id}")

    # 1) APPROVA LA RICHIESTA
    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"✅ APPROVATA: user={user_id}")
    except ApiTelegramException as e:
        print(f"❌ ERRORE APPROVAZIONE: {e.error_code} - {e.description}")
        return
    except Exception as e:
        print("❌ ERRORE APPROVAZIONE:", repr(e))
        return

    # 2) INVIA DM (prima user_chat_id, poi fallback su user_id)
    targets = []
    if user_chat_id:
        targets.append(user_chat_id)
    targets.append(user_id)

    for target in targets:
        try:
            if PHOTO_FILE_ID:
                bot.send_photo(target, PHOTO_FILE_ID)
            bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
            print(f"✅ DM INVIATO A {target}")
            break
        except ApiTelegramException as e:
            print(f"❌ DM FALLITO A {target}: {e.error_code} - {e.description}")
        except Exception as e:
            print(f"❌ DM FALLITO A {target}: {repr(e)}")

print("Bot del Cecchino ONLINE…")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)Se vuoi invece accedere a tutte le nostre giocate prima che le quote scendono 📉,
alle nostre analisi, scalate periodiche, dati e statistiche, contatta la mia assistenza
che la SNIPER ROOM (canale privato) è ancora aperta! 👇

⚠️ <b><a href="https://t.me/m/7IaxhPVCYjlk">ASSISTENZA</a></b>
"""

# -------------------------------
# /start
# -------------------------------
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

# --------------------------------------------------------
# ✅ ESTRAI FILE_ID FOTO (invia foto al bot in privato)
# --------------------------------------------------------
@bot.message_handler(content_types=["photo"])
def get_photo_id(message):
    try:
        file_id = message.photo[-1].file_id  # versione più grande
        bot.reply_to(message, f"FILE_ID:\n<code>{file_id}</code>")
        print(f"📸 FILE_ID inviato: {file_id}")
    except Exception as e:
        print("❌ Errore get_photo_id:", repr(e))

# --------------------------------------------------------
# APPROVAZIONE AUTOMATICA + INVIO (foto se presente) + testo
# --------------------------------------------------------
@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    print(f"📩 JOIN REQUEST: chat_id={chat_id} user_id={user_id} user_chat_id={user_chat_id}")

    # 1) APPROVA LA RICHIESTA
    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"✅ APPROVATA: user={user_id}")
    except ApiTelegramException as e:
        print(f"❌ ERRORE APPROVAZIONE: {e.error_code} - {e.description}")
        return
    except Exception as e:
        print("❌ ERRORE APPROVAZIONE:", repr(e))
        return

    # 2) INVIA DM (prima user_chat_id, poi fallback su user_id)
    targets = []
    if user_chat_id:
        targets.append(user_chat_id)
    targets.append(user_id)

    for target in targets:
        try:
            if PHOTO_FILE_ID:
                bot.send_photo(target, PHOTO_FILE_ID)
            bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
            print(f"✅ DM INVIATO A {target}")
            break
        except ApiTelegramException as e:
            print(f"❌ DM FALLITO A {target}: {e.error_code} - {e.description}")
        except Exception as e:
            print(f"❌ DM FALLITO A {target}: {repr(e)}")

print("Bot del Cecchino ONLINE…")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)"""

# -------------------------------
# /start (solo per test)
# -------------------------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🔫 Bot del Cecchino attivo.\n\n"
        "Per ricevere il messaggio automatico, invia una richiesta di accesso al canale."
    )

# --------------------------------------------------------
# APPROVAZIONE AUTOMATICA + INVIO FOTO + MESSAGGIO PRIVATO
# --------------------------------------------------------
@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    print(f"📩 JOIN REQUEST: chat_id={chat_id} user_id={user_id} user_chat_id={user_chat_id}")

    # 1) APPROVA LA RICHIESTA
    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"✅ APPROVATA: user={user_id}")
    except ApiTelegramException as e:
        print(f"❌ ERRORE APPROVAZIONE: {e.error_code} - {e.description}")
        return
    except Exception as e:
        print("❌ ERRORE APPROVAZIONE:", repr(e))
        return

    # 2) INVIA DM (prima user_chat_id, poi fallback su user_id)
    targets = []
    if user_chat_id:
        targets.append(user_chat_id)
    targets.append(user_id)

    for target in targets:
        try:
            # Foto + testo separato (più sicuro per limiti caption)
            bot.send_photo(target, PHOTO_FILE_ID)
            bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
            print(f"✅ FOTO + DM INVIATI A {target}")
            break
        except ApiTelegramException as e:
            print(f"❌ INVIO FALLITO A {target}: {e.error_code} - {e.description}")
        except Exception as e:
            print(f"❌ INVIO FALLITO A {target}: {repr(e)}")

print("Bot del Cecchino ONLINE con approvazione automatica…")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
