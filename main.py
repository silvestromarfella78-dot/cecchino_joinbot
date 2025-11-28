import os
import telebot
from telebot.types import ChatJoinRequest

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN non impostato!")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# -------------------------------
# MESSAGGIO DI BENVENUTO COMPLETO
# -------------------------------
WELCOME_TEXT = """
<b>⚽️BENVENUTO NEL CANALE PUBBLICO del CECCHINO 🎾🏆🔫</b>

Qui troverai tutte le promo più vantaggiose e consigli su come sfruttarle 👌

✅ Non aspettarti multiploni quota 100 che si vincono 2 volte all’anno, 
qui giochiamo precisi come cecchini per andare in profit tutti i giorni.

🏆 Inoltre, per te che sei appena entrato nel mio canale pubblico, 
posso farti prendere un BONUS SENZA DEPOSITO 💸 selezionando solo il bonus 
all’iscrizione tramite questo link 👇

➡️ <b><a href="https://bonus.sportbet.it/ilcecchino/">50 EURO GRATIS 💸💸💸</a></b>

Se vuoi invece accedere a tutte le nostre giocate prima che le quote scendono 📉, 
alle nostre analisi, scalate periodiche, dati e statistiche, contatta la mia assistenza 
che la SNIPER ROOM (canale privato) è ancora aperta! 👇

⚠️ <b><a href="https://t.me/m/36n3dfU3MmNk">ASSISTENZA</a></b>
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
