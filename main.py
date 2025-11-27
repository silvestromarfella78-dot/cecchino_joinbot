import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Messaggio di benvenuto
welcome_message = """
⚽️ <b>BENVENUTO NEL CANALE PUBBLICO DEL CECCHINO</b> 🎾🏆🔫

Dopo l’ennesima scia di vittorie degli ultimi giorni, continuiamo a spingere forte senza fermarci nemmeno per respirare.

Qui dentro trovi solo:
• Letture chirurgiche  
• Schedine senza rischio inutile  
• Giocate selezionate al millimetro  
• Nessuna perdita di tempo

Se vuoi entrare PRIMA che le quote si muovono, entra qui 👇
👉 <a href="https://t.me/m/36n3dfU3MmNk">ACCEDI AL PRIVATO</a>

Preparati: oggi si vola pesante.  
"""

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:
        bot.send_message(message.chat.id, welcome_message)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(message.chat.id, welcome_message)

print("Bot del Cecchino ONLINE...")
bot.polling(none_stop=True)
