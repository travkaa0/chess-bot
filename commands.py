import telebot
from telebot import types
import random

# token
bot = telebot.TeleBot('7821159484:AAHtVB82Ch2sL1HaUwmvb_7Nd5hyeDHWGbM')

@bot.message_handler(commands=['start'])
def hello(message):
    # find out the chat ID and send a message to it when the "start" command is run. output: Hello, {username}
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}, glad you decided to visit my bot.\nI hope you like it.')

tasks = {
    '1': {'image': 'puzzles/1.png', 'solution': 'Qa8#', 'topic': 'white to move. mate in 1.'},
    '2': {'image': 'puzzles/2.png', 'solution': 'Bc4#', 'topic': 'white to move. mate in 1.'},
    '3': {'image': 'puzzles/3.png', 'solution': 'Qe5#', 'topic': 'white to move. mate in 1.'},
    '4': {'image': 'puzzles/4.png', 'solution': 'e8N#', 'topic': 'white to move. mate in 1.'},
    '5': {'image': 'puzzles/5.png', 'solution': 'Rh7#', 'topic': 'white to move. mate in 1.'},
    '6': {'image': 'puzzles/6.png', 'solution': 'Nf7 R:f7\nQd8+ Rf8\nQ:f8#', 'topic': 'white to move. mate in 3.'},
    '7': {'image': 'puzzles/7.png', 'solution': '... Re4\nQ:e4 Bf5', 'topic': 'black to move. winning material.'},
    '8': {'image': 'puzzles/8.png', 'solution': 'B:f5\nf5 B:c3\nR:c3 Ne2', 'topic': 'black to move. fork.'},
    '9': {'image': 'puzzles/9.png', 'solution': 'Nd7', 'topic': 'white to move. fork.'},
    '10': {'image': 'puzzles/10.png', 'solution': 'B:f6 Q:c4\nRe4', 'topic': 'white to move. winning material.'},
    '11': {'image': 'puzzles/11.png', 'solution': '... R:a2\nK:a2 Ra3\nK:a3 Qa1#', 'topic': 'black to move. mate in 3.'} 
}

# function for escaping special characters in MarkdownV2
def escape_markdown_v2(text):
    # we only escape characters that must be escaped.
    escape_chars = r'\_*[]()~`>#+-=|{}!'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

@bot.message_handler(commands=['puzzles'])
def tasks_handler(message):
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Yes', callback_data='solve')
    btn_no = types.InlineKeyboardButton('No', callback_data='later')
    markup.add(btn_yes, btn_no)

    bot.send_message(message.chat.id, 'Do you want to solve the puzzle?', reply_markup=markup)

# processing clicks on the "Yes" and "No" buttons
@bot.callback_query_handler(func=lambda call: call.data in ['solve', 'later', 'no_info'])
def callback_handler(call):
    if call.data == 'solve':
        # we choose a random task
        task_id = random.choice(list(tasks.keys()))
        task = tasks[task_id]

        # escape special characters in solving the puzzle
        solution = escape_markdown_v2(task['solution'])
        topic = escape_markdown_v2(task['topic'])

        # we send a picture of the puzzle and the solution in a spoiler
        bot.send_message(call.message.chat.id, f"Topic of puzzle: {topic}")
        bot.send_photo(call.message.chat.id, open(task['image'], 'rb'))
        bot.send_message(call.message.chat.id, f"||{solution}||", parse_mode='MarkdownV2')
        
    elif call.data == 'later':
        bot.send_message(call.message.chat.id, 'OK, we will solve puzzles another time.')

    elif call.data == 'no_info':
        bot.send_message(call.message.chat.id, "You chose 'No'. If you change your mind, type /info again.")

@bot.callback_query_handler(func=lambda call: call.data in chess_history)
def callback_inline(call):
    # we get data about the century selected in the inline button
    century = call.data
    if century in chess_history:

        history_text = ""
        for topic, description in chess_history[century]:
            # we form the text by adding the topic (in bold text format) and its description
            history_text += f"*{topic}*\n{description}\n\n"

        bot.send_message(call.message.chat.id, history_text, parse_mode='Markdown')

def split_text(text, max_length=4096):
    # the split_text function splits a long text into chunks if its length exceeds a specified limit.
    # max_length - the maximum length of one chunk, default is 4096 (Telegram's message size limit).

    chunks = []
    while len(text) > max_length:
        # find the last newline character ('\n') before the max_length to avoid splitting in the middle of a word.
        split_index = text.rfind('\n', 0, max_length)
        if split_index == -1:
            split_index = max_length
        chunks.append(text[:split_index])

        # remove the chunk from the original text.
        text = text[split_index:]
    chunks.append(text)
    return chunks

@bot.message_handler(commands=['books'])
def books(message):
    chess_books_text = """
    1. Title: My System
    Author: Aron Nimzowitsch
    Description: This influential book introduces fundamental concepts of positional play, including pawn structures, prophylaxis, overprotection, and the blockading of passed pawns.
    Target Audience: Intermediate to advanced players

    2. Title: The Life and Games of Mikhail Tal
    Author: Mikhail Tal
    Description: A blend of autobiography and detailed analysis of games by the eighth World Chess Champion, known for his tactical brilliance and aggressive style.
    Target Audience: All levels, though intermediate and advanced players will benefit most

    3. Title: Chess Fundamentals
    Author: José Raúl Capablanca
    Description: A classic work focusing on essential chess principles such as simple tactics, endgames, and positional play, written by the third World Chess Champion.
    Target Audience: Beginners to intermediate players

    4. Title: Silman's Complete Endgame Course
    Author: Jeremy Silman
    Description: A comprehensive guide to endgames, organized by rating level to teach players the most essential endgame principles as they progress.
    Target Audience: Beginners to advanced players

    5. Title: Thinking, Fast and Slow
    Author: Daniel Kahneman
    Description: Not specifically a chess book, but highly recommended for understanding decision-making, mental biases, and managing risk, which are crucial skills in chess.
    Target Audience: Intermediate to advanced players

    6. Title: 100 Endgames You Must Know
    Author: Jesús de la Villa
    Description: Focuses on 100 essential endgames that every chess player must know, making it a highly relevant resource for practical improvement.
    Target Audience: Intermediate players, though advanced players will also benefit

    7. Title: How to Reassess Your Chess
    Author: Jeremy Silman
    Description: Teaches players how to recognize and capitalize on positional imbalances, helping them think like a master.
    Target Audience: Intermediate to advanced players

    8. Title: Zurich International Chess Tournament, 1953
    Author: David Bronstein
    Description: A detailed account of one of the most famous chess tournaments, with insights and annotated games from the world's top players, including future world champions.
    Target Audience: Advanced players and those aspiring to master-level play

    9. Title: Bobby Fischer Teaches Chess
    Author: Bobby Fischer
    Description: A beginner-friendly book structured as a series of puzzles, focusing on tactics and checkmate patterns.
    Target Audience: Beginners to intermediate players

    10. Title: Mastering Chess Strategy
    Author: Johan Hellsten
    Description: A comprehensive guide on strategy, covering piece coordination, weak squares, pawn structures, and other core strategic themes.
    Target Audience: Intermediate to advanced players

    11. Title: Attacking Chess: The King’s Indian
    Author: David Vigorito
    Description: A deep dive into the King’s Indian Defense, presenting modern ideas and analysis for players looking to master this aggressive opening.
    Target Audience: Advanced players or players interested in the King's Indian Defense

    12. Title: Secrets of Modern Chess Strategy: Advances Since Nimzowitsch
    Author: John Watson
    Description: Explores how modern chess strategy has evolved from Nimzowitsch's ideas, focusing on flexibility in principles such as center control and pawn structures.
    Target Audience: Advanced players and chess enthusiasts

    13. Title: Chess Structures: A Grandmaster Guide
    Author: Mauricio Flores Rios
    Description: A guide focused on pawn structures and their influence on chess strategy, providing practical advice for different formations.
    Target Audience: Intermediate to advanced players

    14. Title: The Art of Attack in Chess
    Author: Vladimir Vuković
    Description: A classic on attacking play, covering tactics, sacrifices, and strategic ideas that help players become more aggressive and dynamic.
    Target Audience: Intermediate to advanced players
    """

    chunks = split_text(chess_books_text)
    for chunk in chunks:
        bot.send_message(message.chat.id, chunk)

@bot.message_handler(commands=['games'])
def games(message):
    
    markup = types.InlineKeyboardMarkup()
    
    btn1 = types.InlineKeyboardButton('Magnus Carlsen', url='https://www.chess.com/games/magnus-carlsen')
    btn2 = types.InlineKeyboardButton('Bobby Fischer', url='https://www.chess.com/games/bobby-fischer')
    btn3 = types.InlineKeyboardButton('Emanuel Lasker', url='https://www.chess.com/games/emanuel-lasker')
    btn4 = types.InlineKeyboardButton('Garry Kasparov', url='https://www.chess.com/games/garry-kasparov')
    btn5 = types.InlineKeyboardButton('José Raúl Capablanca', url='https://www.chess.com/games/jose-raul-capablanca')
    btn6 = types.InlineKeyboardButton('Mikhail Tal', url='https://www.chess.com/games/mikhail-tal')
    btn7 = types.InlineKeyboardButton('Hikaru Nakamura', url='https://www.chess.com/games/hikaru-nakamura')
    btn8 = types.InlineKeyboardButton('Paul Morphy', url='https://www.chess.com/games/paul-morphy')
    btn9 = types.InlineKeyboardButton('Mikhail Botvinnik', url='https://www.chess.com/games/mikhail-botvinnik')

    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4)
    markup.row(btn5, btn6)
    markup.row(btn7)
    markup.row(btn8, btn9)

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

@bot.message_handler(commands=['recommendations'])
def rec(message):
    recs = """
    Getting started with chess can be both exciting and a bit daunting! Here are some recommendations to help you ease into the game:

    1. Learn the Basics
       - Chessboard Setup: Familiarize yourself with the board layout, the names of the pieces, and how each piece moves.
       - Basic Rules: Understand the rules of chess, including how to check, checkmate, and stalemate.
       - Special Moves: Learn about castling, en passant, and pawn promotion.

    2. Opening Principles
       - Control the Center: Focus on controlling the center squares (e4, e5, d4, d5) as they offer better mobility for your pieces.
       - Develop Your Pieces: Aim to get your knights and bishops out early, preferably to squares where they control the center.
       - King Safety: Don’t forget to castle early to protect your king and connect your rooks.

    3. Practice Tactics
       - Tactics Training: Use online resources or apps that offer tactical puzzles. This helps improve your pattern recognition.
       - Common Tactics: Familiarize yourself with basic tactics like forks, pins, skewers, and discovered attacks.

    4. Play Regularly
       - Online Platforms: Sign up on websites like Chess.com, Lichess.org, or PlayMagnus.com to play against others or against the computer.
       - Join a Club: Look for local chess clubs or online communities to find opponents and gain experience.

    5. Study Simple Endgames
       - Basic Endgames: Learn key endgame principles and simple checkmating patterns (like King and Queen vs. King, King and Rook vs. King).
       - King and Pawn Endgames: Understand how to convert a pawn advantage into a win.

    6. Watch and Learn
       - Videos and Streams: Follow chess channels on YouTube or Twitch where you can watch games, tutorials, and analysis.
       - Famous Games: Study classic games played by grandmasters to learn strategies and tactics in action.

    7. Analyze Your Games
       - Post-Game Review: After playing, review your games to understand what went well and where you could improve.
       - Use Analysis Tools: Online platforms often provide analysis tools that can highlight mistakes and suggest better moves.

    8. Read Chess Books
       - Beginner Books: Consider starting with books like:
         - "Bobby Fischer Teaches Chess" by Bobby Fischer
         - "The Steps Method" by Roberta and Peter Schaeffer
         - "Chess for Kids" by Michael Basman

    9. Set Goals
       - Short-Term Goals: Set achievable goals, like improving your rating by a certain number of points or learning a specific opening.
       - Long-Term Goals: Consider aiming to participate in a local tournament when you feel ready.

    10. Have Fun!
       - Remember to enjoy the game! Chess is as much about enjoying the process of learning and playing as it is about winning.

    By following these recommendations, you'll build a solid foundation in chess. Happy playing!
    """
    
    bot.send_message(message.chat.id, recs)

@bot.message_handler(commands=['quotes'])
def quotes(message):

    quote = [
        "Garry Kasparov:\n\nChess is a game of mistakes. The one who makes the least mistakes is the winner.",
        "Garry Kasparov:\n\nIt is not enough to be a good player; you must also have the mental strength to win.",
        "Anatoly Karpov:\n\nChess is everything: art, science, and sport.",
        "Anatoly Karpov:\n\nThe main thing is to have a good day. If you play your best, the result will take care of itself.",
        "Bobby Fischer:\n\nChess is life.",
        "Bobby Fischer:\n\nAll that matters on the chessboard is good moves.",
        "Magnus Carlsen:\n\nI think chess players are the most unappreciated athletes in the world.",
        "Magnus Carlsen:\n\nI always believe that when you’re playing against someone, it’s more about your own game than about your opponent.",
        "Vladimir Kramnik:\n\nThe most important thing is to keep your head cool.",
        "Vladimir Kramnik:\n\nIn chess, as in life, the best way to win is to avoid losing.",
        "Mikhail Tal:\n\nI have always believed that the best way to improve is to play as many games as possible.",
        "Mikhail Tal:\n\nThe most beautiful thing about chess is that it can be played in the mind.",
        "José Raúl Capablanca:\n\nIn chess, as in life, opportunity strikes but once.",
        "José Raúl Capablanca:\n\nThe most important thing is to be able to think independently.",
        "Hikaru Nakamura:\n\nYou have to take risks in order to win. That's the nature of chess.",
        "Hikaru Nakamura:\n\nChess is like a war on a chessboard. The goal is to destroy your opponent's king.",
        "Judit Polgar:\n\nThere is no such thing as an easy opponent. Every opponent is strong.",
        "Judit Polgar:\n\nYou have to believe in yourself when you play chess."
    ]

    # send a random quote
    rand_quote = random.choice(quote)
    bot.send_message(message.chat.id, rand_quote)

@bot.message_handler(commands=['dictionary'])
def dic(message):
    terms = {
        'A': [
            "**Algebraic Notation**: A method of recording and describing moves in chess using letters and numbers to indicate pieces and squares.",
            "",
            "**Ambush**: A tactic where a piece appears to be inactive but can suddenly attack when the opportunity arises.",
            "",
            "**Analyze**: To study a position or a game to understand strengths, weaknesses, and possible improvements.",
            "",
            "**Annotation**: Notes made on a game or position explaining the ideas behind certain moves."
        ],
        'B': [
            "**Back Rank**: The row of squares on the player's first rank, often referring to the danger of checkmate on that rank.",
            "",
            "**Bishop**: A piece that moves diagonally any number of squares.",
            "",
            "**Blunder**: A significant mistake that can lead to a loss of material or position.",
            "",
            "**Book Move**: A move that is part of established opening theory."
        ],
        'C': [
            "**Check**: A situation where a king is under direct attack and must be moved out of attack on the next turn.",
            "",
            "**Checkmate**: A position in which the king is in check and has no legal moves to escape, resulting in the end of the game.",
            "",
            "**Challenger**: A player who contests the title or position of another player.",
            "",
            "**Counterattack**: An immediate response to an opponent's threat or attack."
        ],
        'D': [
            "**Defense**: A strategy to prevent an opponent from gaining an advantage.",
            "",
            "**Draw**: A result of the game where neither player wins. This can happen through stalemate, insufficient material, or mutual agreement.",
            "",
            "**D4**: The pawn move to the d4 square, often seen in openings like the Queen's Pawn Game."
        ],
        'E': [
            "**Endgame**: The final phase of the game where few pieces remain on the board, and the focus is on promoting pawns and checkmating the opponent.",
            "",
            "**En Passant**: A special pawn capture that can occur immediately after a pawn moves two squares forward from its starting position, allowing an adjacent opponent's pawn to capture it as if it had only moved one square.",
            "",
            "**Equal**: A term used to describe a position that is balanced, with neither side having a significant advantage."
        ],
        'F': [
            "**Fianchetto**: A pawn structure where a bishop is developed to the second rank of the adjacent pawn (e.g., g2 or b2).",
            "",
            "**Fork**: A tactic where a single piece attacks two or more of the opponent's pieces simultaneously."
        ],
        'G': [
            "**Gambit**: A chess opening in which a player sacrifices material, usually a pawn, for an advantage in position or development.",
            "",
            "**Grandmaster (GM)**: A title awarded by FIDE, representing one of the highest levels of chess expertise."
        ],
        'H': [
            "**Half-Open File**: A file with one player’s pawns and the opponent’s pawns missing, allowing for potential attacks along that file.",
            "",
            "**Hanging Piece**: A piece that is unprotected and can be captured without consequence."
        ],
        'I': [
            "**Initiative**: The ability to make threats and dictate the pace of the game, often leading to an advantage.",
            "",
            "**Isolated Pawn**: A pawn that has no friendly pawns on adjacent files, making it a potential weakness."
        ],
        'J': [
            "**Judgment**: The ability to evaluate positions and make decisions based on strategic understanding."
        ],
        'K': [
            "**King**: The most crucial piece in chess; the game ends if a king is checkmated.",
            "",
            "**Kf3**: Notation for moving the king to the f3 square.",
            "",
            "**King's Pawn Opening**: A common opening move for white (1.e4) that controls the center."
        ],
        'L': [
            "**Lateral Move**: A movement where a piece moves horizontally or vertically, typically referring to the rook or queen.",
            "",
            "**Ligature**: A tactical move that leads to a series of forced moves."
        ],
        'M': [
            "**Mate**: Short for checkmate, indicating the end of the game.",
            "",
            "**Middle Game**: The phase of the game between the opening and endgame, where players develop their pieces and formulate plans.",
            "",
            "**Minor Pieces**: Refers to bishops and knights, as opposed to major pieces (rooks and queens)."
        ],
        'N': [
            "**Notation**: The method of recording moves in a game, often in algebraic or descriptive format.",
            "",
            "**Knight**: A piece that moves in an L-shape: two squares in one direction and one square perpendicular."
        ],
        'O': [
            "**Opening**: The initial phase of the game, characterized by specific moves aimed at developing pieces and controlling the center.",
            "",
            "**Outpost**: A square that is controlled by a piece, particularly a knight, that cannot be attacked by pawns."
        ],
        'P': [
            "**Pawn**: The most numerous piece on the board, moving forward one square (or two from its starting position) and capturing diagonally.",
            "",
            "**Promotion**: The process of upgrading a pawn to a more powerful piece (usually a queen) when it reaches the opposite side of the board.",
            "",
            "**Pincered Piece**: A piece that is attacked by two enemy pieces at the same time, making it difficult for the opponent to defend it."
        ],
        'Q': [
            "**Queen**: The most powerful piece, capable of moving any number of squares in any direction.",
            "",
            "**Queen's Gambit**: A popular opening that begins with 1.d4 d5 2.c4."
        ],
        'R': [
            "**Rook**: A piece that moves horizontally or vertically any number of squares.",
            "",
            "**Rotating**: The act of changing the position of pieces or altering the pawn structure."
        ],
        'S': [
            "**Stalemate**: A situation in which one player has no legal moves and their king is not in check, resulting in a draw.",
            "",
            "**Sacrifice**: The act of giving up material (usually a piece) for a strategic advantage.",
            "",
            "**Skewer**: A tactical move where a more valuable piece is attacked, forcing it to move and exposing a less valuable piece behind it."
        ],
        'T': [
            "**Tactic**: A short-term sequence of moves that leads to a gain of material or a better position.",
            "",
            "**Tempo**: A term used to describe a turn or move; losing tempo means giving the opponent an advantage in time."
        ],
        'U': [
            "**Undermine**: A tactic aimed at attacking the pawn structure of an opponent, weakening their position.",
            "",
            "**Underpromotion**: Promoting a pawn to a piece other than a queen, usually a knight or rook, for tactical reasons."
        ],
        'V': [
            "**Vincent's Defense**: A specific defensive strategy against a particular opening or attack.",
            "",
            "**Visualization**: The ability to mentally picture moves and positions without looking at the board."
        ],
        'W': [
            "**Weak Square**: A square that cannot be defended by pawns, making it vulnerable to attack.",
            "",
            "**Winning Plan**: A strategic sequence of moves that aims to convert an advantage into a victory."
        ],
        'X': [
            "**X-ray**: A tactic where a piece attacks an opponent’s piece through another piece, often used with rooks or queens."
        ],
        'Y': [
            "**Yardstick**: A term used informally to measure progress or evaluate a player's performance."
        ],
        'Z': [
            "**Zugzwang**: A situation where a player is forced to make a move that puts them at a disadvantage, typically occurring in endgames."
        ]
    }

    # ask user for the letter
    bot.send_message(message.chat.id, "Please enter a letter (A-Z) to get the chess terms:")

    # register the next step
    bot.register_next_step_handler(message, get_terms, terms)

# function to process the entered letter
def get_terms(message, terms):
    letter = message.text.upper()

    if letter in terms:
        # we form and send a response with terms
        response = f"**Terms for '{letter}':**\n\n" + "\n".join(terms[letter])
        bot.send_message(message.chat.id, response, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Invalid letter. Please enter a letter (A-Z).")
        bot.register_next_step_handler(message, get_terms, terms)

    # use a state to capture the user's response
    # @bot.message_handler(func=lambda m: True)
    # def info(message):
    #     letter = message.text.upper()  # convert to uppercase for consistency
    #     if letter in terms:
    #         # Format response
    #         response = f"**Terms for '{letter}':**\n\n\n" + "\n".join(terms[letter])
    #         bot.send_message(message.chat.id, response, parse_mode='Markdown')
    #     else:
    #         bot.send_message(message.chat.id, "Invalid letter. Please enter a letter (A-Z).")

    #     # optionally, you can remove this handler after the first valid response
    #     bot.remove_message_handler(info)

@bot.message_handler(commands=['learning'])
def learn(message):
    markup = types.InlineKeyboardMarkup()
    
    btn1 = types.InlineKeyboardButton('Opening Principles', url='https://www.youtube.com/watch?v=8IlJ3v8I4Z8&list=PLEU2htGGqTT_dNgPztXTf6Ze7crT_PUxk')
    btn2 = types.InlineKeyboardButton('Practice Tactics', url='https://www.youtube.com/watch?v=D3uEIk9_RYg&list=PLEU2htGGqTT-9aaVFXTYzAfyKM15zyyme')
    btn3 = types.InlineKeyboardButton('Simple Endgames', url='https://www.youtube.com/watch?v=mCsc24k-Q8M&list=PLEU2htGGqTT_nX4Bfz-a9NdCybfh1Q8AD')
    btn4 = types.InlineKeyboardButton('Game Analysis', url='https://www.youtube.com/watch?v=ylpAHvPlafc&list=PLEU2htGGqTT8sunIJuMRODQ62i3YQtQwa')

    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4)

    bot.send_message(message.chat.id, "What do you want to learn first?", reply_markup=markup)

basic = {
    "Start": "You can choose one of 11 topics to study. For greater compactness, the topics will be indicated when you click on the buttons",

    "Topic 1": """
    **Chess Pieces & Setup\n\nPieces**: 
    - King (♔): Moves one square in any direction.
    - Queen (♕): Moves any number of squares in any direction.
    - Rook (♖): Moves horizontally or vertically.
    - Bishop (♗): Moves diagonally.
    - Knight (♘): Moves in an "L" shape.
    - Pawn (♙): Moves forward but captures diagonally.

    **Setup**: 
    - Place the rooks in the corners, knights next to them, then bishops, queen on her color, and the king beside her.
    - Pawns on the second row for each side.
    """,
    
    "Topic 2": """
    **How the Pieces Move\n\nKing**: \nMoves one square in any direction.
    **Queen**: \nMoves any number of squares vertically, horizontally, or diagonally.
    **Rook**: \nMoves any number of squares horizontally or vertically.
    **Bishop**: \nMoves diagonally any number of squares.
    **Knight**: \nMoves in an L-shape and can jump over pieces.
    **Pawn**: \nMoves forward one square, captures diagonally.
    """,

    "Topic 3": """
    **Basic Rules\n\nObjective**: \nCheckmate the opponent's king.
    **Check**: \nWhen a king is under threat and must be protected.
    **Checkmate**: \nWhen the king is in check and cannot escape.
    **Stalemate**: \nA draw occurs when a player cannot make a legal move but is not in check.
    """,

    "Topic 4": """
    **Special Moves\n\nCastling**: \nMove the king two squares towards a rook, then move the rook next to the king. Conditions apply.
    **En Passant**: \nSpecial pawn capture when a pawn moves two squares forward.
    **Pawn Promotion**: \nWhen a pawn reaches the 8th rank, it can become a queen, rook, bishop, or knight.
    """,

    "Topic 5": """
    **Winning Conditions\n\nCheckmate**: \nThe most common way to win.
    **Resignation**: \nA player can concede at any time.
    **Stalemate**: \nA draw if no legal moves are available and the player isn't in check.
    **Threefold Repetition**: \nA draw if the same position occurs three times.
    **50-Move Rule**: \nA draw if no pawn has moved and no piece has been captured in 50 moves.
    """,

    "Topic 6": """
    **Opening Principles\n\nControl the Center**: \nMove pawns and pieces to control the center.
    **Develop Your Pieces**: \nMove knights and bishops early.
    **King Safety**: \nCastle early to protect your king.
    """,

    "Topic 7": """
    **Tactics\n\nFork**: \nOne piece attacks two enemy pieces.
    **Pin**: \nA piece is immobilized to protect a more valuable piece behind it.
    **Skewer**: \nA more valuable piece is attacked, forcing it to move, exposing a weaker piece behind it.
    **Discovered Attack**: \nMoving one piece reveals an attack from another.
    """,

    "Topic 8": """
    **Endgame Principles\n\nActivate the King**: \nIn the endgame, the king becomes powerful.
    **Push Passed Pawns**: \nPromote pawns to win.
    **Opposition**: \nIn king and pawn endgames, opposition is key.
    """,

    "Topic 9": """
    Common Mistakes to Avoid\n\n- Moving the same piece multiple times in the opening.
    - Neglecting King Safety.
    - Not controlling the center.
    """,

    "Topic 10": """
    **Practice Puzzles\n\nPuzzle 1**: \nFind the checkmate in one move.
    """,

    "Topic 11": """
    **Chess Notation\n\nAlgebraic Notation**:\n 
    - Files: a-h (columns).
    - Ranks: 1-8 (rows).
    **Example Move**: e4 means moving the pawn to the e4 square.
    """
}

@bot.message_handler(commands=['chess_basics'])
def basics(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_start = types.KeyboardButton('Start')
    
    markup.add(btn_start)
    
    bot.send_message(message.chat.id, "Welcome! Press 'Start' to begin.", reply_markup=markup)

# function to hide the keyboard
def hide_keyboard():
    # create a blank keyboard to hide the previous one
    return types.ReplyKeyboardRemove()

# Message handler for chess topics
@bot.message_handler(func=lambda message: message.text in ['Start'] + [f"Topic {i}" for i in range(1, 12)])
def send_topic(message):
    if message.text == "Start":
        bot.send_message(message.chat.id, basic["Start"], reply_markup=hide_keyboard())
        show_next_topic(message, 1)  # Show the first topic
    else:
        # Determine the current topic from the message
        topic_num = None
        for topic in basic:
            if message.text == topic:
                topic_num = int(topic.split(" ")[1])  # Extract the topic number
                
        if topic_num:
            bot.send_message(message.chat.id, basic[f"Topic {topic_num}"], parse_mode="Markdown", reply_markup=hide_keyboard())

            # If this is not the last topic, show the next topic button
            if topic_num < 11:
                show_next_topic(message, topic_num + 1)
        else:
            bot.send_message(message.chat.id, "Please select a valid topic.", reply_markup=hide_keyboard())

# text message handler
# @bot.message_handler(func=lambda message: True)
# def send_topic(message):
#     if message.text == "Start":
#         bot.send_message(message.chat.id, basic["Start"], reply_markup=hide_keyboard())
#         show_next_topic(message, 1)  # show first topic
#     else:
#         # determine the current topic from a message
#         topic_num = None
#         for topic in basic:
#             if message.text == topic:
#                 topic_num = int(topic.split(" ")[1])  # extracting the topic number
                
#         if topic_num:
#             bot.send_message(message.chat.id, basic[f"Topic {topic_num}"], parse_mode="Markdown", reply_markup=hide_keyboard())

#             # if not the last topic, show the next button
#             if topic_num < 11:
#                 show_next_topic(message, topic_num + 1)
#         else:
#             bot.send_message(message.chat.id, "Please select a valid topic.", reply_markup=hide_keyboard())

# function to show next topic button
def show_next_topic(message, next_topic_num):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    next_topic_btn = types.KeyboardButton(f"Topic {next_topic_num}")
    
    markup.add(next_topic_btn)
    
    bot.send_message(message.chat.id, f"Press the button for Topic {next_topic_num}.", reply_markup=markup)

@bot.message_handler(commands=['info'])
def info(message):
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton(text='Yes', url='https://travkaa0.github.io/chess-bot-info.github.io/')
    btn_no = types.InlineKeyboardButton(text='No', callback_data='no_info')

    markup.add(btn_yes, btn_no)
    bot.send_message(message.chat.id, "Do you want to get information about the use of my bot?", reply_markup=markup)

bot.polling(non_stop=True)