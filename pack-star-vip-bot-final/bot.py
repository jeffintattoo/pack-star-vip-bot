import telebot
import os
import threading
import time
from dotenv import load_dotenv
from telebot import types

# === Carrega variáveis de ambiente ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
IMG_REBECA = os.getenv("IMG_REBECA")
QR_CODE = os.getenv("QR_CODE")
GRUPO_ID = int(os.getenv("GRUPO_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

# === Comando /start ===
@bot.message_handler(commands=["start"])
def start(message):
    try:
        with open(IMG_REBECA, "rb") as img:
            bot.send_photo(message.chat.id, img, caption="""
<b>🔥 Bem-vindo(a) ao VIP 🔥</b>

✅ Packs exclusivos de cornos, hotwives, esposas infiéis e exibicionismo!

🎥 Veja as prévias abaixo, depois clique para assinar 👇
            """, parse_mode="HTML")

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("🔞 Ver Prévias", callback_data="ver_previas")
        btn2 = types.InlineKeyboardButton("💳 Assinar - R$20", callback_data="pix")
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(message.chat.id, "Escolha abaixo:", reply_markup=markup)

    except Exception as e:
        print(f"Erro no /start: {e}")

# === Callback de prévias ===
@bot.callback_query_handler(func=lambda call: call.data == "ver_previas")
def enviar_previas(call):
    try:
        videos = [
            "video_2025-04-16_22-55-24.mp4",
            "video_2025-04-16_22-55-40.mp4",
            "video_2025-04-16_22-56-02.mp4"
        ]
        for video in videos:
            with open(video, "rb") as v:
                bot.send_video(call.message.chat.id, v)
    except Exception as e:
        print(f"Erro ao enviar vídeos de prévias: {e}")

# === Callback Pix ===
@bot.callback_query_handler(func=lambda call: call.data == "pix")
def ver_pix(call):
    try:
        with open(QR_CODE, "rb") as qr:
            bot.send_photo(call.message.chat.id, qr, caption="""
<b>💳 PAGAMENTO - R$20</b>

✅ Faça o Pix para liberar o acesso VIP.

🔻 Copie a chave abaixo ou escaneie o QR code:

<code>chavepix@seudominio.com</code>
            """, parse_mode="HTML")
    except Exception as e:
        print(f"Erro ao enviar QR: {e}")

# === Apaga links de membros comuns ===
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
        print(f"Erro ao deletar link: {e}")

# === Excluir mensagens de serviço ===
@bot.message_handler(content_types=['new_chat_members', 'left_chat_member', 'pinned_message'])
def deletar_servico(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Erro ao excluir serviço: {e}")

# === Envia regras automaticamente a cada 1h ===
def enviar_regras_periodicamente():
    while True:
        try:
            markup = types.InlineKeyboardMarkup()
            botao = types.InlineKeyboardButton("🔥 Assinar", url="https://t.me/packStarVipBot?start=start")
            markup.add(botao)

            msg = bot.send_message(GRUPO_ID, """
🚨 <b>REGRAS DO GRUPO</b> 🚨

• Proibido divulgar links de outros grupos
• Sem spam e sem links
• Proibido invadir o privado (PV) sem permissão
• Proibido fotos de pau (só aceitas se tiver mulher na imagem)

🚫 <b>Quem descumprir será banido!</b>

Clique no botão abaixo para ver prévias e assinar o VIP:
            """, parse_mode="HTML", reply_markup=markup)

            time.sleep(3600)

        except Exception as e:
            print(f"Erro ao enviar regras: {e}")
            time.sleep(10)

# === Comando /teste ===
@bot.message_handler(commands=["teste"])
def teste(message):
    bot.reply_to(message, "✅ Bot funcionando perfeitamente!")

# === Inicialização ===
print("🤖 Bot rodando com envio automático de regras e segurança ativa...")
threading.Thread(target=enviar_regras_periodicamente, daemon=True).start()
bot.infinity_polling()
