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

    century = call.data
    if century in chess_history:
        
        history_text = ""
        for topic, description in chess_history[century]:
            history_text += f"*{topic}*\n{description}\n\n"

        bot.send_message(call.message.chat.id, history_text, parse_mode='Markdown')

# sol = {
#     '1': 'solution',
#     '2': 'solution'
# }

# @bot.message_handler(commands=['solutions_to_puzzles'])
# def solutions(message):
#     bot.send_message(message.chat.id, 'Write the puzzle number')

@bot.message_handler(commands=['books'])
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

chess_history = {
    "6th Century": [
        ("Topic: Indian Roots (Chaturanga)", 
         "Chess is believed to have originated in India around the 6th century. The game was called Chaturanga, meaning 'four divisions of the military' (infantry, cavalry, elephants, and chariots), which later evolved into the modern pieces: pawns, knights, bishops, and rooks."),
        ("Topic: Early Spread to Persia (Shatranj)", 
         "Chaturanga spread to Persia, where it became known as Shatranj. Here, some key rules changes occurred, but it still resembled its Indian predecessor.")
    ],
    "7th-10th Century": [
        ("Topic: Islamic Golden Age and Chess Literature", 
        "Chess spread throughout the Islamic world, reaching regions such as North Africa, the Middle East, and Spain. During this period, chess began to gain cultural and intellectual significance, especially in the courts of caliphs."),
        ("Notable Text: 'Kitab ash-shatranj'", 
        "The earliest known book on chess, written by al-Adli around the 9th century, discussed strategies and annotated games, helping to formalize the rules and tactics.")
    ],
    "11th-13th Century": [
        ("Topic: Europe’s Adoption of Chess", 
         "Chess reached Europe through the Islamic territories in Spain and Sicily. The game's presence in the courts of nobility was particularly prominent during the Middle Ages, becoming a symbol of education and courtly virtues."),
        ("Changes to the Game", 
         "The game continued evolving in Europe, though slowly. Pieces were still moving similarly to Shatranj, and major pieces like the queen and bishop were limited in movement.")
    ],
    "15th Century": [
        ("Topic: Rule Changes in Europe", 
         "Around the late 1400s, significant changes were introduced, especially in Spain and Italy, transforming chess into its modern form. The queen became the most powerful piece, moving any number of squares diagonally, vertically, or horizontally. The bishop was also given the ability to move across any number of squares diagonally."),
        ("Topic: First Chess Books", 
         "The first printed book on chess was published by Luis Ramírez de Lucena in 1497, titled 'Repetición de Amores y Arte de Ajedrez,' marking the start of formalized chess theory.")
    ],
    "16th-18th Century": [
        ("Topic: Standardization and Competitive Play", 
         "Chess gained popularity among the European aristocracy and intellectuals during the Renaissance. Players like Gioachino Greco in Italy wrote extensively about tactics and combinations. Chess became a common subject for problem-solving and intellectual discussion."),
        ("Topic: Establishment of Chess Clubs", 
         "The first organized chess clubs began to appear in cities like London and Paris. Chess evolved from a leisurely pastime for the elite to a more structured game with established rules."),
        ("First International Matches", 
         "Chess began to move toward competitive play between different nations, though there were no formalized international tournaments yet.")
    ],
    "19th Century": [
        ("Topic: The Romantic Era of Chess", 
         "This period saw the rise of spectacular, tactical sacrifices and attacking play. Paul Morphy, an American chess prodigy, became the unofficial world champion after defeating Europe's best players in the mid-1800s."),
        ("Topic: First Chess Tournaments and the First World Champion", 
         "The first modern chess tournament was held in London in 1851, won by Adolf Anderssen. In 1886, the first official World Chess Championship match took place between Wilhelm Steinitz and Johannes Zukertort, with Steinitz becoming the first recognized World Champion."),
        ("Topic: The Evolution of Chess Theory", 
         "Wilhelm Steinitz revolutionized chess by introducing a more systematic approach to the game, focusing on positional play rather than purely tactical brilliance. His work laid the foundation for modern chess strategy.")
    ],
    "20th Century": [
        ("Topic: Chess as a Global Phenomenon", 
         "Chess became a truly global sport in the 20th century, with players from countries all over the world competing at the highest levels."),
        ("Topic: Soviet Dominance", 
         "Following the Russian Revolution, chess became an integral part of Soviet culture, with state support for training programs and competitions. The Soviet Union produced a number of World Champions, including Mikhail Botvinnik, Anatoly Karpov, and Garry Kasparov."),
        ("Topic: Chess Opens to the World", 
         "The World Chess Federation (FIDE) was founded in 1924, which began organizing and regulating international competitions. The Candidates Tournament and Interzonal tournaments became pathways to challenge the World Champion."),
        ("Cold War Rivalry", 
         "Chess became a symbol of Cold War rivalry, culminating in the famous 1972 World Championship match between American Bobby Fischer and Soviet Boris Spassky."),
        ("Topic: Chess Computers", 
         "The development of computer chess programs began in the mid-20th century, culminating in 1997 when IBM's Deep Blue defeated Garry Kasparov, marking the dawn of a new era of artificial intelligence in chess.")
    ],
    "21st Century": [
        ("Topic: Online Chess and Global Accessibility", 
         "The internet revolutionized chess, making it more accessible than ever. Chess platforms like Chess.com and Lichess offer millions of players from around the world the opportunity to play and learn. This has led to a democratization of chess, where players from any background can compete and learn."),
        ("Topic: The Magnus Carlsen Era", 
         "Norwegian Magnus Carlsen became World Champion in 2013 and has been dominating the chess world since. He is known for his universal playing style and profound understanding of endgames."),
        ("Topic: Artificial Intelligence and Engines", 
         "Chess engines like Stockfish and AlphaZero have transformed how top-level players prepare for games. AlphaZero, using machine learning, introduced new, creative strategies to the game, while Stockfish remains a powerful tool for analysis.")
    ]
}

@bot.message_handler(commands=['history'])
def history(message):

    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton('6th Century', callback_data='6th Century')
    btn2 = types.InlineKeyboardButton('7th-10th Century', callback_data='7th-10th Century')
    btn3 = types.InlineKeyboardButton('11th-13th Century', callback_data='11th-13th Century')
    btn4 = types.InlineKeyboardButton('15th Century', callback_data='15th Century')
    btn5 = types.InlineKeyboardButton('16th-18th Century', callback_data='16th-18th Century')
    btn6 = types.InlineKeyboardButton('19th Century', callback_data='19th Century')
    btn7 = types.InlineKeyboardButton('20th Century', callback_data='20th Century')
    btn8 = types.InlineKeyboardButton('21st Century', callback_data='21st Century')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

    bot.send_message(message.chat.id, "Select a century to learn about the history of chess:", reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: True)
# def handle_callback(call):
#     century = call.data
#     if century in chess_history:
#         # Combine topics into a single message
#         history_text = ""
#         for topic, description in chess_history[century]:
#             history_text += f"*{topic}*\n{description}\n\n"

#         # Send the history of the selected century
#         bot.send_message(call.message.chat.id, history_text, parse_mode='Markdown')

bot.polling(non_stop=True)
