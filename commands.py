import telebot
from telebot import types

# token
bot = telebot.TeleBot('8025279344:AAEr6dt_MU8rKCbrjAWs610rrZ_AM9Cy5Os')

@bot.message_handler(commands=['start'])
def hello(message):
    #выяснение айди чата и отправка на него сообщения при запуске команды "старт". вывод: Привет, {имя пользователя}
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}, glad you decided to visit my bot.\nI hope you like it.')

@bot.message_handler(commands=['puzzles'])
def tasks(message):
    task = []
    bot.send_message(message.chat.id, 'What difficulty will you choose?')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Easy', )
    btn2 = types.InlineKeyboardButton('Middle', )
    btn3 = types.InlineKeyboardButton('Hard', )


sol = {
    '1': 'solution',
    '2': 'solution'
}

@bot.message_handler(commands=['solutions_to_puzzles'])
def solutions(message):
    bot.send_message(message.chat.id, 'Write the puzzle number')

    @bot.message_handler(func=lambda message: True)
    def info(message):
        text = message.text.lower()
        for key, response in sol.items():
            if key in text:
                bot.reply_to(message, response)
                break
    
        bot.send_message(message, 'There is no puzzle under this number')



bot.polling(non_stop=True)
