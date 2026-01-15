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
# MESSAGGIO DI BENVENUTO COMPLETO
# NB: NIENTE <br> -> usa solo \n
# -------------------------------
WELCOME_TEXT = """
<b>BENVENUTO NEL NOSTRO CANALE PUBBLICO 🏆</b>

Qui troverai solo ed esclusivamente giocate studiate per pungere i bookmakers 🔫

<b>In questo canale troverai :</b>

- <b>QUOTE MAGGIORATE OGNI GIORNO</b> 🔝

- <b>BONUS SNIPER WEEK</b> (che ci permette di giocare le multiple gratis ogni week end del mese per tutto l’anno) 💰

- <b>ANALISI SU MARCATORI E RISULTATI ESATTI</b> (ci sono 2/3 studi settimanali) 📈

- <b>RICEVERAI 50,00€ GRATIS</b> SOLO ALL’ISCRIZIONE E ALLA CONVALIDA DEI DOCUMENTI (selezionando il bonus all’iscrizione) 🎁

Per avere tutto ciò, ti basta un iscrizione ad uno dei nostri book di riferimento, che ci permettono di avere questi bonus e noi li sfruttiamo a meglio.
(Ricordati, è proprio con i bonus che abbiamo un vantaggio su tutto)

<b>SPORTBET :</b> <a href="https://bonus.sportbet.it/ilcecchino/">https://bonus.sportbet.it/ilcecchino/</a>

<b>SPORTIUM :</b> <a href="https://sportium.it/fwlink/account-registration?father=spcecchino">https://sportium.it/fwlink/account-registration?father=spcecchino</a>

<b>Ora è arrivato il momento di fare sul serio, io ti do la mira, ma il grilletto lo devi premere tu! Benvenuto 👌</b>

Se invece vuoi accedere <b>A TUTTE LE ANALISI ESCLUSIVE</b> contatta l’assistenza che ti spiega come accedere al canale privato 👇

👉 <b><a href="https://t.me/m/36n3dfU3MmNk">ASSISTENZA</a></b> 👈
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
            bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
            print(f"✅ DM INVIATO A {target}")
            break
        except ApiTelegramException as e:
            print(f"❌ DM FALLITO A {target}: {e.error_code} - {e.description}")
        except Exception as e:
            print(f"❌ DM FALLITO A {target}: {repr(e)}")

print("Bot del Cecchino ONLINE con approvazione automatica…")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
