import os
import telebot
from telebot.types import ChatJoinRequest
from telebot.apihelper import ApiTelegramException

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN non impostato! (Railway > Variables > BOT_TOKEN)")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

WELCOME_TEXT = """
<b><u><i>BENVENUTO NEL NOSTRO CANALE<br>PUBBLICO 🏆</i></u></b>

<i>Qui troverai solo ed esclusivamente giocate studiate per pungere i bookmakers 🔫</i>

<i><b>In questo canale troverai :</b></i>

<b><i>- QUOTE MAGGIORATE OGNI GIORNO</i></b> 🔝<br>
<b><i>- BONUS SNIPER WEEK</i></b> <i>(che ci permette di giocare le multiple gratis ogni week end del mese per tutto l’anno)</i> 💰<br>
<b><i>- ANALISI SU MARCATORI E RISULTATI ESATTI</i></b> <i>(ci sono 2/3 studi settimanali)</i> 📈<br>
<b><i>- RICEVERAI 50,00€ GRATIS SOLO ALL’ISCRIZIONE E ALLA CONVALIDA DEI DOCUMENTI</i></b> <i>(selezionando il bonus all’iscrizione)</i> 🎁

<u><i>Per avere tutto ciò, ti basta un iscrizione ad uno dei nostri book di riferimento, che ci permettono di avere questi bonus e noi li sfruttiamo a meglio. (Ricordati, è proprio con i bonus che abbiamo un vantaggio su tutto)</i></u>

<b>SPORTBET :</b> <a href="https://bonus.sportbet.it/ilcecchino/">https://bonus.sportbet.it/ilcecchino/</a><br>
<b>SPORTIUM :</b> <a href="https://sportium.it/fwlink/account-registration?father=spcecchino">https://sportium.it/fwlink/account-registration?father=spcecchino</a>

<i>Ora è arrivato il momento di fare sul serio, io ti do la mira, ma il grilletto lo devi premere tu! Benvenuto 👌</i>
"""

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🔫 Bot del Cecchino attivo.\n\n"
        "Per ricevere il messaggio automatico, invia una richiesta di accesso al canale."
    )

@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    print(f"📩 Join request ricevuta: chat_id={chat_id} user_id={user_id} user_chat_id={user_chat_id}")

    # 1) Approva richiesta
    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"✅ Approvata richiesta per user {user_id}")
    except ApiTelegramException as e:
        print(f"❌ Errore approvazione: {e.error_code} - {e.description}")
        return
    except Exception as e:
        print("❌ Errore approvazione:", repr(e))
        return

    # 2) Invia DM (prima user_chat_id, poi fallback su user_id)
    try:
        target = user_chat_id if user_chat_id else user_id
        bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
        print(f"✅ Messaggio inviato in privato a {target}")
    except ApiTelegramException as e:
        print(f"❌ Errore invio DM: {e.error_code} - {e.description}")
    except Exception as e:
        print("❌ Errore invio DM:", repr(e))

print("Bot del Cecchino ONLINE con approvazione automatica…")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
