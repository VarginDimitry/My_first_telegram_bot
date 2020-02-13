import telebot
import config
import random
from telebot import types

ALL_WORDS_FILE = open('WORDS_DICT.txt', 'r')
WORDS_DICT = []
for line in ALL_WORDS_FILE:
    line = line[:len(line) - 1]
    WORDS_DICT.append(line.upper())
ALL_WORDS_FILE.close()
print(WORDS_DICT)

bot = telebot.TeleBot(config.TOKEN)
DATA_BASE = {}  # 'user_id': [0'word', 1'new_word', 2'used characters', 3'misses']
aplph = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')


@bot.message_handler(commands=['start'])
def Hello(message):
    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("NEW GAME🎮")
    markup.add(item)

    bot.send_message(message.chat.id, '❤️❤️❤️Hello, ' + message.from_user.first_name + '❤️❤️❤️\nPress to start!️',
                     reply_markup=markup)
    sti = open('hello_sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    sti.close()


@bot.message_handler(content_types=['text'])
def Write(message):
    if message.text == "NEW GAME🎮":
        # Keyboard of chars
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item = types.KeyboardButton("NEW GAME🎮")
        markup.add(item)
        markup.add('A', 'B', 'C', 'D', 'E', 'F')
        markup.add('G', 'H', 'I', 'J', 'K', 'L')
        markup.add('M', 'N', 'O', 'P', 'Q', 'R')
        markup.add('S', 'T', 'U', 'V', 'W', 'X')
        markup.add('Y', 'Z')

        word = random.choice(WORDS_DICT)
        DATA_BASE[message.chat.id] = [word, '_' * len(word), '', 0]

        bot.send_message(message.chat.id, "Great!")
        bot.send_message(message.chat.id, "You got a {} character word".format(len(word)))
        bot.send_message(message.chat.id, DATA_BASE[message.chat.id][1], reply_markup=markup)
        sti = open('pict_of_misses\\0miss.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        sti.close()

    elif message.text in aplph:
        pass
        if message.text in DATA_BASE[message.chat.id][0] and message.text not in DATA_BASE[message.chat.id][2]:
            char = DATA_BASE[message.chat.id][0].find(message.text)
            while char != -1:
                if char != len(DATA_BASE[message.chat.id][1]) - 1:
                    DATA_BASE[message.chat.id][1] = DATA_BASE[message.chat.id][1][:char] + message.text + \
                                                    DATA_BASE[message.chat.id][1][char + 1:]
                    DATA_BASE[message.chat.id][0] = DATA_BASE[message.chat.id][0][:char] + '_' + \
                                                    DATA_BASE[message.chat.id][0][char + 1:]
                else:
                    DATA_BASE[message.chat.id][1] = DATA_BASE[message.chat.id][1][:char] + message.text
                    DATA_BASE[message.chat.id][0] = DATA_BASE[message.chat.id][0][:char] + '_'
                char = DATA_BASE[message.chat.id][0].find(message.text)

            if DATA_BASE[message.chat.id][1].find('_') == -1:
                # Keyboard
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item = types.KeyboardButton("NEW GAME🎮")
                markup.add(item)

                bot.send_message(message.chat.id, 'Yes, it was "{}"'.format(DATA_BASE[message.chat.id][1]))

                bot.send_message(message.chat.id, 'You win!', reply_markup=markup)

            else:
                sure_mes = ('Sure!', 'Of course!', 'Naturally!')
                bot.send_message(message.chat.id, random.choice(sure_mes))
                bot.send_message(message.chat.id, DATA_BASE[message.chat.id][1])
                DATA_BASE[message.chat.id][2] += message.text

        elif message.text not in DATA_BASE[message.chat.id][2]:
            DATA_BASE[message.chat.id][3] += 1
            if DATA_BASE[message.chat.id][3] >= 7:
                # Keyboard
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item = types.KeyboardButton("NEW GAME🎮")
                markup.add(item)

                word = ''
                for i in range(len(DATA_BASE[message.chat.id][0])):
                    if DATA_BASE[message.chat.id][0][i] != '_':
                        word += DATA_BASE[message.chat.id][0][i]
                    else:
                        word += DATA_BASE[message.chat.id][1][i]
                bot.send_message(message.chat.id, "GAME OVER⚰️\nIt was " + word, reply_markup=markup)
                sti = open('pict_of_misses\\7miss.webp', 'rb')
                bot.send_sticker(message.chat.id, sti)
                sti.close()

            else:
                DATA_BASE[message.chat.id][2] += message.text
                bot.send_message(message.chat.id, "There aren't {}\nTry again🤕\nYou have {} miss{}".format(message.text,
                                DATA_BASE[message.chat.id][3], "es" if DATA_BASE[message.chat.id][3] > 1 else ""))
                sti = open('pict_of_misses\\{}miss.webp'.format(DATA_BASE[message.chat.id][3]), 'rb')
                bot.send_sticker(message.chat.id, sti)
                sti.close()

        else:
            bot.send_message(message.chat.id, "You already used this!")


# RUN
bot.polling(none_stop=True)