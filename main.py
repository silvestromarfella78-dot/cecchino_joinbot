import os
import telebot
from telebot.types import ChatJoinRequest
from telebot.apihelper import ApiTelegramException

# Railway: a volte la variabile è BOT, altre BOT_TOKEN
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("BOT")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN/BOT non impostato! (Railway > Variables)")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# (consigliato) evita conflitti se in passato avevi webhook
try:
    bot.remove_webhook()
except Exception:
    pass

# ✅ 1) METTI QUI IL FILE_ID DELLA FOTO (dopo che lo estrai)
PHOTO_FILE_ID = ""  # es: "AgACAgQAAxkBAAIB...."

# -------------------------------
# MESSAGGIO DI BENVENUTO COMPLETO
# -------------------------------
WELCOME_TEXT = """
<b>⚽️BENVENUTO NEL CANALE PUBBLICO del CECCHINO ⚽️🏆🔫</b>

Qui troverai tutte le promo più vantaggiose e consigli su come sfruttarle 👌

Non aspettarti multiploni quota 100 che si vincono 1 volta ogni 2 anni, qui giochiamo in maniera chirurgica per andare in profit ogni santo giorno!

🏆 Inoltre, per te che sei appena entrato nel mio canale pubblico,
posso farti prendere un BONUS SENZA DEPOSITO 💸 selezionando solo il bonus
all’iscrizione tramite questi due link 👇

📌 <b><a href="https://bonus.sportbet.it/ilcecchino/">50,00€ GRATIS SPORTBET</a></b>

📌 <b><a href="https://sportium.it/offer/fun-convalida-50-cecchino/?father=spcecchino">50,00€ GRATIS SPORTIUM</a></b>

Se vuoi invece accedere a tutte le nostre giocate prima che le quote scendono 📉,
alle nostre analisi, scalate periodiche, dati e statistiche, contatta la mia assistenza
che la SNIPER ROOM (canale privato) è ancora aperta! 👇

⚠️ <b><a href="https://t.me/m/36n3dfU3MmNk">ASSISTENZA</a></b>
"""

# -------------------------------
# /start (solo per test)
# -------------------------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🔫 Bot del Cecchino attivo.\n\n"
        "Per ricevere il messaggio automatico, invia una richiesta di accesso al canale.\n\n"
        "Per ottenere il FILE_ID della foto: inviami una foto qui in chat e te lo rimando."
    )

# --------------------------------------------------------
# ✅ 2) QUESTO SERVE SOLO PER ESTRARRE IL FILE_ID DELLA FOTO
# Invia una foto al bot in privato e lui ti risponde con il FILE_ID.
# (Dopo che l'hai copiato in PHOTO_FILE_ID puoi anche cancellare questa funzione)
# --------------------------------------------------------
@bot.message_handler(content_types=['photo'])
def get_photo_id(message):
    file_id = message.photo[-1].file_id  # versione più grande
    bot.reply_to(message, f"FILE_ID:\n<code>{file_id}</code>")

# --------------------------------------------------------
# APPROVAZIONE AUTOMATICA + INVIO MESSAGGIO PRIVATO
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
            # ✅ Se hai messo PHOTO_FILE_ID, invia foto + messaggio
            if PHOTO_FILE_ID:
                bot.send_photo(target, PHOTO_FILE_ID)
                bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
            else:
                # Se non hai ancora il file_id, invia solo testo
                bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)

            print(f"✅ DM INVIATO A {target}")
            break
        except ApiTelegramException as e:
            print(f"❌ DM FALLITO A {target}: {e.error_code} - {e.description}")
        except Exception as e:
            print(f"❌ DM FALLITO A {target}: {repr(e)}")

print("Bot del Cecchino ONLINE con approvazione automatica…")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
