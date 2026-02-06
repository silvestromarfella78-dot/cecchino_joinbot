import os
import time
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

# ✅ TESTO
WELCOME_TEXT = """
<b>BENVENUTO NEL CANALE PUBBLICO del CECCHINO ⚽️🏆🔫</b>

<b>Guarda qui che cosa abbiamo COMBINATO</b>
<b><u><i>SE VUOI DISTRUGGERLI PURE TE CLICCA QUI SOTTO👌</i></u></b>

<b>contatta la mia assistenza</b>
<b>che la SNIPER ROOM (canale privato) è ancora aperta! 👇</b>

<b>⚠️ <a href="https://t.me/m/36n3dfU3MmNk">ASSISTENZA</a></b>
"""

# -------------------------------
# MEMORIA TEMPORANEA richieste in attesa
# user_id -> {"user_chat_id": ..., "chat_id": ..., "ts": ...}
# -------------------------------
PENDING = {}
PENDING_TTL_SECONDS = 6 * 60 * 60  # 6 ore

def cleanup_pending():
    now = time.time()
    to_del = [uid for uid, v in PENDING.items() if now - v["ts"] > PENDING_TTL_SECONDS]
    for uid in to_del:
        PENDING.pop(uid, None)

# -------------------------------
# /start (solo per test)
# -------------------------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🔫 Bot del Cecchino attivo.\n\n"
        "Il messaggio partirà quando approvate VOI la richiesta nel canale."
    )

# --------------------------------------------------------
# 1) ARRIVA LA RICHIESTA: NON APPROVIAMO, SALVIAMO SOLO
# --------------------------------------------------------
@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    cleanup_pending()

    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    PENDING[user_id] = {"user_chat_id": user_chat_id, "chat_id": chat_id, "ts": time.time()}
    print(f"🕒 Richiesta salvata in attesa: user_id={user_id} user_chat_id={user_chat_id} chat_id={chat_id}")

# --------------------------------------------------------
# 2) QUANDO LO APPROVATE VOI: ARRIVA CHAT_MEMBER -> INVIA DM
# --------------------------------------------------------
@bot.chat_member_handler()
def on_chat_member_update(update):
    cleanup_pending()

    try:
        chat_id = update.chat.id
        user_id = update.from_user.id if hasattr(update, "from_user") and update.from_user else None
        target_user_id = update.new_chat_member.user.id  # l’utente che cambia stato
        new_status = update.new_chat_member.status
        old_status = update.old_chat_member.status
    except Exception as e:
        print("❌ Errore lettura chat_member:", repr(e))
        return

    # Ci interessa: da "left/kicked" -> "member" (approvato)
    if new_status != "member":
        return
    if old_status not in ("left", "kicked", "restricted"):
        # comunque va bene, ma filtriamo i casi più comuni
        pass

    # Se quell’utente era in pending, inviamo
    pending = PENDING.get(target_user_id)
    if not pending:
        return

    if pending["chat_id"] != chat_id:
        return

    targets = []
    if pending.get("user_chat_id"):
        targets.append(pending["user_chat_id"])
    targets.append(target_user_id)

    print(f"✅ APPROVAZIONE RILEVATA: target_user={target_user_id} (old={old_status} -> new={new_status})")

    sent = False
    for target in targets:
        try:
            bot.send_photo(target, PHOTO_FILE_ID)
            bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
            print(f"✅ FOTO + DM INVIATI A {target}")
            sent = True
            break
        except ApiTelegramException as e:
            print(f"❌ INVIO FALLITO A {target}: {e.error_code} - {e.description}")
        except Exception as e:
            print(f"❌ INVIO FALLITO A {target}: {repr(e)}")

    # Se inviato (o anche se fallito), togliamo dalla pending per non duplicare
    PENDING.pop(target_user_id, None)
    if not sent:
        print("⚠️ Non sono riuscito a inviare il DM (privacy/limiti Telegram).")

print("Bot del Cecchino ONLINE (messaggio solo dopo approvazione manuale)…")
bot.infinity_polling(
    skip_pending=True,
    timeout=60,
    long_polling_timeout=60,
    allowed_updates=["chat_join_request", "chat_member", "message"]
)
