import os
import telebot
from telebot.types import ChatJoinRequest

# Prende il token dall'env di Railway (BOT_TOKEN)
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN non impostato nelle variabili d'ambiente!")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Messaggio di benvenuto (NON lo cambiamo, solo il link finale)
WELCOME_TEXT = (
    "⚽️BENVENUTO NEL CANALE PUBBLICO del CECCHINO 🎾🏆🔫\n\n"
    "Qui troverai tutte le promo più vantaggiose e consigli su come sfruttarle 👌\n\n"
    "✅ Non aspettarti multiploni quota 100 che si vincono 2 volte all’anno, "
    "qui giochiamo precisi come cecchini per andare in profit tutti i giorni ✅\n\n"
    "🏆 Inoltre per te che sei appena entrato nel mio canale pubblico posso iniziare a farti prendere "
    "un bonus di 5️⃣ 🔤 💸 SENZA DEPOSITO (selezionando solo il bonus all’iscrizione) "
    "al nostro book di riferimento, tramite questo link 👇\n\n"
    "➡️ 50 EURO GRATIS 💸💸💸\n"
    "👉 <a href=\"https://t.me/m/36n3dfU3MmNk\">CLICCA QUI PER ATTIVARLI</a>\n\n"
    "Se vuoi invece accedere a tutte le nostre giocate prima che le quote scendono 📉, "
    "alle nostre analisi, alle nostre scalate periodiche e a tutti i dati e statistiche, "
    "contatta la mia assistenza che la SNIPER ROOM (canale privato) è ancora aperta! 👇"
)

# 👉 Comando /start per test veloce
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(
        message,
        "🔫 Bot del Cecchino attivo!\n"
        "Questo bot approva automaticamente le richieste di ingresso al canale "
        "e manda il messaggio di benvenuto in privato. "
        "Appena invii una richiesta di accesso dal tuo canale test, lui parte."
    )

# 👉 Handler per le richieste di join al canale
@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    try:
        # 1) Invia DM al nuovo utente
        if getattr(join_request, "user_chat_id", None):
            bot.send_message(join_request.user_chat_id, WELCOME_TEXT)
    except Exception as e:
        print("Errore nell'invio del DM:", e)

    try:
        # 2) Approva la richiesta al canale
        bot.approve_chat_join_request(
            join_request.chat.id,
            join_request.from_user.id
        )
    except Exception as e:
        print("Errore nell'approvazione della richiesta:", e)

print("Bot del Cecchino ONLINE (Railway)…")
bot.infinity_polling(allowed_updates=["chat_join_request", "message"])
