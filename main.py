import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Messaggio di benvenuto
welcome_message = """
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

# /start handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, welcome_message)

# Avvio bot
print("Bot del Cecchino ONLINE...")
bot.polling(skip_pending=True, none_stop=True)
