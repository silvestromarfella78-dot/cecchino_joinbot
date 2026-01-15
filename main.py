import os
import telebot
from telebot.types import ChatJoinRequest
from telebot.apihelper import ApiTelegramException

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("BOT")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN/BOT non impostato! (Railway > Variables)")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ✅ METTI QUI IL TUO @username del bot (senza @)
# Esempio: BOT_USERNAME = "IlCecchinoJoinBot"
BOT_USERNAME = os.getenv("BOT_USERNAME", "").replace("@", "").strip()

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
        "Se hai inviato una richiesta di accesso, riceverai il messaggio automatico appena approvato."
    )

@bot.chat_join_request_handler()
def handle_join_request(join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    user_id = join_request.from_user.id
    user_chat_id = getattr(join_request, "user_chat_id", None)

    print(f"📩 JOIN REQUEST: chat_id={chat_id} user_id={user_id} user_chat_id={user_chat_id} chat_type={getattr(join_request.chat, 'type', None)}")

    # 1) Approva
    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"✅ APPROVATA: user={user_id}")
    except ApiTelegramException as e:
        print(f"❌ APPROVAZIONE FALLITA: {e.error_code} - {e.description}")
        return
    except Exception as e:
        print(f"❌ APPROVAZIONE FALLITA: {repr(e)}")
        return

    # 2) Prova DM (prima user_chat_id, poi user_id)
    dm_sent = False
    targets = []
    if user_chat_id:
        targets.append(user_chat_id)
    targets.append(user_id)

    for target in targets:
        try:
            bot.send_message(target, WELCOME_TEXT, disable_web_page_preview=True)
            print(f"✅ DM INVIATO A: {target}")
            dm_sent = True
            break
        except ApiTelegramException as e:
            print(f"❌ DM FALLITO A {target}: {e.error_code} - {e.description}")
        except Exception as e:
            print(f"❌ DM FALLITO A {target}: {repr(e)}")

    # 3) Fallback: se DM non possibile, avvisa in chat (solo se è gruppo/supergroup)
    # (Su un canale spesso non serve, ma almeno capisci che è un limite DM)
    if not dm_sent:
        try:
            start_link = f"https://t.me/{BOT_USERNAME}?start=1" if BOT_USERNAME else ""
            mention = f'<a href="tg://user?id={user_id}">clicca qui</a>'
            msg = (
                f"⚠️ Non riesco a scriverti in privato ({mention}).\n"
                f"Apri la chat col bot e premi START"
            )
            if start_link:
                msg += f": <a href=\"{start_link}\">START BOT</a>"
            bot.send_message(chat_id, msg, disable_web_page_preview=True)
            print("✅ Fallback in chat inviato (DM non disponibile).")
        except Exception as e:
            print("❌ Fallback in chat fallito:", repr(e))


print("Bot del Cecchino ONLINE con approvazione automatica…")
# 👇 lascia così per evitare filtri che tagliano update
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
