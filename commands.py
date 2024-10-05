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

    task = {
        '1': 'task',
        '2': 'task',
        '3': 'task'
    }

    #bot.send_message(message.chat.id, 'What difficulty will you choose?')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Easy', callback_data='easy')
    btn2 = types.InlineKeyboardButton('Middle', callback_data='middle')
    btn3 = types.InlineKeyboardButton('Hard', callback_data='hard')

    markup.row(btn1, btn2, btn3)

    bot.send_message(message.chat.id, 'What difficulty will you choose?', reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text.isdigit())  # Проверка, что сообщение содержит число
    def send_task(message):
        num = message.task  # Получаем число, введенное пользователем
    
        if num in task:
            
            with open(task[num], 'rb') as img:
                bot.send_photo(message.chat.id, img)
        else:
            # Если число не связано с картинкой, отправляем сообщение
            bot.send_message(message.chat.id, 'There is no puzzle under this number.')
    
    # @bot.message_handler(func=lambda message: True)
    # def info(message):
    #     text = message.text.lower()
    #     for key, response in tasks.items():
    #         if key in text:
    #             bot.reply_to(message, response)
    #             break

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'easy':
        bot.send_message(call.message.chat.id, 'Write a number from 1 to 10.')
    elif call.data == 'middle':
        bot.send_message(call.message.chat.id, 'Write a number from 11 to 20.')
    elif call.data == 'hard':
        bot.send_message(call.message.chat.id, 'Write a number from 21 to 30.')
    elif call.data == 'magnus':
        bot.send_message(call.message.chat.id, 'список ссылок и названия партий')
    elif call.data == 'bobby':
        bot.send_message(call.message.chat.id, 'список ссылок и названия партий')
    elif call.data == 'lasker':
        bot.send_message(call.message.chat.id, 'список ссылок и названия партий')

# sol = {
#     '1': 'solution',
#     '2': 'solution'
# }

# @bot.message_handler(commands=['solutions_to_puzzles'])
# def solutions(message):
#     bot.send_message(message.chat.id, 'Write the puzzle number')

@bot.message_handler(commands=['chess_books'])
def books(message):
    bot.send_message(message.chat.id, 'список лучших шахматных книг на 24 год и их описание')

@bot.message_handler(commands=['games'])
def games(message):
    
    markup = types.InlineKeyboardMarkup()
    
    btn1 = types.InlineKeyboardButton('Magnus Carlsen', callback_data='magnus')
    btn2 = types.InlineKeyboardButton('Bobby Fischer', callback_data='bobby')
    btn3 = types.InlineKeyboardButton('Emanuel Lasker', callback_data='lasker')

    markup.row(btn1)
    markup.row(btn2, btn3)

    bot.send_message(message.chat.id, "Which grandmaster's game will you choose?", reply_markup=markup)

bot.polling(non_stop=True)
