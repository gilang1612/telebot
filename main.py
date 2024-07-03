import telebot
import os
from telebot import types
from Config import token, debug, nama_bot
from time import sleep
from AskHamster import AskHamster

os.system('cls' if os.name == 'nt' else 'clear')
bot = telebot.TeleBot(token)


# ASK HAMSTER
ask_tap = None
ask_claim_daily = None

askhamster = AskHamster(bot)


def create_inline_keyboard():
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    markup.add('HAMSTER', 'PIXELVERSE')

    return markup


def makrup_keyboard(nama_1, nama_2):
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    markup.add(nama_1, nama_2)

    return markup


@bot.message_handler(commands=['start'])
def welcome(message):

    if debug:
        print('[Debug] Start')

    bot.send_message(message.chat.id, f'Selamat datang di {nama_bot.upper()}, silahkan pilih bot mana yang mau digunakan',
                     reply_markup=create_inline_keyboard())


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text.lower() == 'hamster':
        if debug:
            print('[Debug] Hamster')
        bot.send_message(message.chat.id, 'BOT HAMSTER STARTED...',
                         reply_markup=types.ReplyKeyboardRemove())

        path = './data_hamster'

        print('[Debug] Checking Query ID...')

        if os.path.exists(f'{path}/{message.chat.id}.txt'):
            print('[Debug] Query ID found')
            bot.send_message(
                message.chat.id, 'Query ID sudah ada')

            sleep(3)
            # bot.delete_message(chat_id=message.chat.id,
            #                    message_id=message.message_id+2)
            # sleep(1)
            markup = types.ReplyKeyboardMarkup(
                one_time_keyboard=True, resize_keyboard=True)
            markup.add('Ya', 'Tidak')
            bot.send_message(
                message.chat.id, 'Mau ubah query ID?', reply_markup=markup)

            bot.register_next_step_handler(
                message, askhamster.ubah_query_id_hamster)

        else:
            markup = types.ReplyKeyboardMarkup(
                one_time_keyboard=True, resize_keyboard=True)
            markup.add('Add Query ID')

            bot.send_message(
                message.chat.id, 'Query ID tidak ada', reply_markup=markup)

    elif message.text.lower() == 'pixelverse':
        bot.send_message(message.chat.id, 'BOT PIXEL MASIH TAHAP DEVELOPE...')

    elif message.text == 'Add Query ID':
        if debug:
            print('[Debug] Add Query ID')
        bot.send_message(
            message.chat.id, 'Masukan Query ID:', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(
            message, askhamster.save_query_id_hamster)


print('Bot is running...')

bot.polling()
