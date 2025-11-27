import os
import telebot
from telebot.types import ChatJoinRequest

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN non impostato!")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Messaggio di benvenuto
WELCOME_TEXT = """
<b>⚽️ BENVENUTO NEL CANALE PUBBLICO del CECCHINO 🎾🏆🔫</b>

Qui troverai tutte le promo più vantaggiose e consigli su come sfruttarle 👌

✅ Non aspettarti multiploni quota 100 che si vincono 2 volte all’anno: 
qui giochiamo precisi come cecchini per andare in profit tutti i giorni.

🏆 Inoltre, per te che sei appena entrato nel mio canale pubblico, 
posso farti prendere un BONUS SENZA DEPOSITO 💸 selezionando solo il bonus 
all’iscrizione tramite questo link 👇

➡️ <b>50 EURO GRATIS 💸💸💸</b>  
<a href="https://t.me/m/36n3dfU3MmNk">CLICCA QUI PER IL BONUS</a>

Se vuoi invece accedere a tutte le nostre giocate prima che le quote scendono 📉, 
alle nostre analisi, scalate periodiche, dati e statistiche, contatta la mia assistenza 👇

📩 <b>Contatta Assistenza:</b>  
<a href="https://t.me/m/36n3dfU3MmNk">https://t.me/m/36n3dfU3MmNk</a>
"""

# --- TEST /start ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🔫 Bot attivo! Ora prova a fare una richiesta di accesso al canale.")

# --- QUI SI ATTIVA IL MESSAGGIO AUTOMATICO ---
@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):

    # 1) INVIO DEL MESSAGGIO IN PRIVATO
    try:
        if getattr(join_request, "user_chat_id", None):
            bot.send_message(join_request.user_chat_id, WELCOME_TEXT)
    except Exception as e:
        print("Errore DM:", e)

    # 2) APPROVAZIONE DELLA RICHIESTA
    try:
        bot.approve_chat_join_request(
            join_request.chat.id,
            join_request.from_user.id
        )
    except Exception as e:
        print("Errore approvazione:", e)

print("Bot del Cecchino ONLINE…")
bot.infinity_polling(allowed_updates=["chat_join_request", "message"])
