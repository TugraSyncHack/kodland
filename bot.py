import telebot
import os
from logic import DatabaseManager, create_collage

TOKEN = 'BURAYA_BOT_TOKENINI_YAZ'
bot = telebot.TeleBot(TOKEN)
DATABASE = 'bot_database.db'

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Merhaba! Puanlarını görmek için /my_score yazabilirsin.")

@bot.message_handler(commands=['my_score'])
def get_my_score(message):
    m = DatabaseManager(DATABASE)
    user_id = message.from_user.id
    
    
    info = m.get_winners_img(user_id)
    prizes = [x[0] for x in info]
    
    
    if not os.path.exists('img'):
        bot.reply_to(message, "Hata: 'img' klasörü bulunamadı.")
        return

    paths = [f'img/{x}' if x in prizes else f'hidden_img/{x}' for x in os.listdir('img')]
    res = create_collage(paths)
    
    if res is not None:
        cv2.imwrite("c.png", res)
        with open("c.png", "rb") as f:
            bot.send_photo(message.chat.id, f)
        os.remove("c.png")
    else:
        bot.reply_to(message, "Henüz hiç ödül kazanmamışsın!")

bot.polling()
