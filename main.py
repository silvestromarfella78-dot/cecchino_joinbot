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

# ✅ FOTO (file_id già pronto)
PHOTO_FILE_ID = "AgACAgQAAxkBAAIPzGlw2dJ7K7wSmgXReUSoSGFHHQtBAAKmC2sbRjiIU8APNBgRqWOnAQADAgADeQADOAQ"

# -------------------------------
# TESTO (NB: niente <br>, solo \n)
# - "SE VUOI..." sottolineato + grassetto + corsivo
# - tutto il resto in grassetto
# - ASSISTENZA con link
# -------------------------------
WELCOME_TEXT = """
<b>BENVENUTO NEL CANALE PUBBLICO del CECCHINO ⚽️🏆🔫</b>

<b>Guarda qui che cosa abbiamo COMBINATO</b>
<b><u><i>SE VUOI DISTRUGGERLI PURE TE CLICCA QUI SOTTO👌</i></u></b>

<b>contatta la mia assistenza</b>
<b>che la SNIPER ROOM (canale privato) è ancora aperta! 👇</b>

<b>⚠️ <a href="https://t.me/m/36n3dfU3MmNk">ASSISTENZA</a></b>
"""

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
