import telebot
import os
import threading
import time
from dotenv import load_dotenv
from telebot import types

# === Carrega variáveis do .env ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
IMG_REBECA = os.getenv("IMG_REBECA")
QR_CODE = os.getenv("QR_CODE")
GRUPO_ID = int(os.getenv("GRUPO_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

# === /start ===
@bot.message_handler(commands=["start"])
def start(message):
    try:
        print(f"[LOG] /start chamado por {message.from_user.id}")

        # Envia a imagem da Rebeca
        with open(IMG_REBECA, "rb") as img:
            bot.send_photo(message.chat.id, img, caption="""
<b>🔥 Bem-vindo(a) ao VIP 🔥</b>

✅ Packs exclusivos de cornos, hotwives, esposas infiéis e exibicionismo!

🎥 Veja as prévias abaixo, depois clique para assinar 👇
            """, parse_mode="HTML")

        # Envia os vídeos de prévia
        videos = ["video_2025-04-16_22-55-24.mp4", "video_2025-04-16_22-55-40.mp4", "video_2025-04-16_22-56-02.mp4"]
        for video in videos:
            with open(video, "rb") as v:
                bot.send_video(message.chat.id, v)

        # Botões
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔞 Ver Canal Público", url="https://t.me/ClubeDaStakeAlta"))
        markup.add(types.InlineKeyboardButton("💳 Assinar - R$20", callback_data="pix"))
        bot.send_message(message.chat.id, "👇 Escolha uma opção abaixo:", reply_markup=markup)

    except Exception as e:
        print(f"[ERRO /start] {e}")

# === Callback do botão de Pix ===
@bot.callback_query_handler(func=lambda call: call.data == "pix")
def ver_pix(call):
    try:
        with open(QR_CODE, "rb") as qr:
            bot.send_photo(call.message.chat.id, qr, caption="""
<b>💳 PAGAMENTO - R$20</b>

✅ Faça o Pix para liberar o acesso VIP.

🔻 Copie a chave abaixo ou escaneie o QR code:

<code>vipgrupos2025@pix.com</code>

📸 Após o pagamento, envie o comprovante aqui no bot.
            """, parse_mode="HTML")
    except Exception as e:
        print(f"[ERRO PIX] {e}")

# === Exclui links de membros comuns ===
@bot.message_handler(func=lambda m: True, content_types=["text"])
def deletar_links(m):
    try:
        if m.chat.type in ["group", "supergroup"]:
            if "http" in m.text.lower() or "t.me" in m.text.lower():
                membro = bot.get_chat_member(m.chat.id, m.from_user.id)
                if membro.status not in ["administrator", "creator"]:
                    bot.delete_message(m.chat.id, m.message_id)
                    bot.send_message(m.chat.id, "🚫 *Proibido divulgar links!*", parse_mode="Markdown")
    except Exception as e:
        print(f"[ERRO LINK] {e}")

# === Exclui mensagens de serviço ===
@bot.message_handler(content_types=["new_chat_members", "left_chat_member", "pinned_message"])
def deletar_mensagens_de_servico(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"[ERRO SERVIÇO] {e}")

# === Regras automáticas a cada 1 hora com botão que leva ao bot ===
def enviar_regras_periodicamente():
    while True:
        try:
            markup = types.InlineKeyboardMarkup()
            botao = types.InlineKeyboardButton("💳 Assinar", url="https://t.me/packStarVipBot")
            markup.add(botao)

            msg = bot.send_message(GRUPO_ID, """
🚨 <b>REGRAS DO GRUPO - Packs VIP 2025</b> 🚨

❌ Proibido divulgar links de outros grupos
❌ Proibido invadir o PV de outros membros
⚠️ Fotos de pau só serão aceitas se houver mulher na mesma imagem
🚫 Quem descumprir será banido!

📌 Seja educado(a) e respeite a comunidade.

👇 Toque abaixo para ver as prévias e assinar o VIP:
            """, parse_mode="HTML", reply_markup=markup)

            threading.Timer(600, lambda: bot.delete_message(GRUPO_ID, msg.message_id)).start()
            time.sleep(3600)

        except Exception as e:
            print(f"[ERRO REGRAS] {e}")
            time.sleep(10)

# === /teste ===
@bot.message_handler(commands=["teste"])
def teste(message):
    bot.reply_to(message, "✅ Bot funcionando perfeitamente!")

# === Inicia o bot ===
print("🤖 Bot rodando com segurança ativa e mensagens automáticas...")
threading.Thread(target=enviar_regras_periodicamente, daemon=True).start()
bot.infinity_polling()
