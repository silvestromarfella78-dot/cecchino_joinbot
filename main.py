import os
import telebot
from telebot.types import ChatJoinRequest

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN non impostato!")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# -------------------------------
# MESSAGGIO DI BENVENUTO COMPLETO
# (corsivo + sottolineato dove serve)
# -------------------------------
WELCOME_TEXT = """
<b><u><i>BENVENUTO NEL NOSTRO CANALE<br>PUBBLICO 🏆</i></u></b>

<i>Qui troverai solo ed esclusivamente giocate studiate per pungere i bookmakers 🔫</i>

<i><b>In questo canale troverai :</b></i>

<b><i>- QUOTE MAGGIORATE OGNI GIORNO</i></b> 🔝<br>
<b><i>- BONUS SNIPER WEEK</i></b> <i>(che ci permette di giocare le multiple gratis ogni week end del mese per tutto l’anno)</i> 💰<br>
<b><i>- ANALISI SU MARCATORI E RISULTATI ESATTI</i></b> <i>(ci sono 2/3 studi settimanali)</i> 📈<br>
<b><i>- RICEVERAI 50,00€ GRATIS SOLO ALL’ISCRIZIONE E ALLA CONVALIDA DEI DOCUMENTI</i></b> <i>(selezionando il bonus all’iscrizione)</i> 🎁

<u><i>Per avere tutto ciò, ti basta un’iscrizione ad uno dei nostri book di riferimento, che ci permettono di avere questi bonus e noi li sfruttiamo al meglio. (Ricordati, è proprio con i bonus che abbiamo un vantaggio su tutto)</i></u>

<b>SPORTBET :</b> <a href="https://bonus.sportbet.it/ilcecchino/">https://bonus.sportbet.it/ilcecchino/</a><br>
<b>SPORTIUM :</b> <a href="https://sportium.it/fwlink/account-registration?father=spcecchino">https://sportium.it/fwlink/account-registration?father=spcecchino</a>

<i>Ora è arrivato il momento di fare sul serio, io ti do la mira, ma il grilletto lo devi premere tu! Benvenuto 👌</i>
"""

# -------------------------------
# /start (solo per test)
# -------------------------------
@bot.message_handler(commands=['start'])
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

    # 1) APPROVA LA RICHIESTA AUTOMATICAMENTE
    try:
        bot.approve_chat_join_request(
            join_request.chat.id,
            join_request.from_user.id
        )
        print(f"Approvata richiesta per user {join_request.from_user.id}")
    except Exception as e:
        print("Errore approvazione:", e)

    # 2) INVIA IL MESSAGGIO PRIVATO
    try:
        # Telegram fornisce user_chat_id solo se l'utente può ricevere DM
        if getattr(join_request, "user_chat_id", None):
            bot.send_message(join_request.user_chat_id, WELCOME_TEXT)
            print(f"Messaggio inviato a {join_request.user_chat_id}")
        else:
            print("⚠️ L'utente non può ricevere messaggi privati (privacy ON)")
    except Exception as e:
        print("Errore invio DM:", e)


print("Bot del Cecchino ONLINE con approvazione automatica…")
bot.infinity_polling(allowed_updates=["chat_join_request", "message"])
