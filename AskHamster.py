import telebot
import os
from telebot import types
from Config import token, debug
from time import sleep
# from Hamster import Hamster
import Hamster


class AskHamster:

    def __init__(self, bot):
        self.bot = bot

        self.ask_tap = None
        self.ask_claim_daily = None
        self.ask_claim_task = None

        self.ask_claim_chiper = None
        self.chiper_text = None

        self.ask_claim_daily_combo = None
        self.id_combo = None

    def makrup_keyboard(self, nama_1, nama_2):
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True)
        markup.add(nama_1, nama_2)

        return markup

    def ubah_query_id_hamster(self, message):
        if debug:
            print('[Debug] Ubah Query ID')

        if message.text.lower() == 'ya':
            self.bot.send_message(message.chat.id, 'Masukkan Query ID: ',
                                  reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(
                message, self.save_query_id_hamster)
        else:
            self.bot.send_message(message.chat.id, 'Query ID tidak diubah',
                                  reply_markup=types.ReplyKeyboardRemove())
            sleep(3)
            # self.bot.delete_message(
            #     chat_id=message.chat.id, message_id=message.message_id)
            self.bot.send_message(
                message.chat.id, 'BOT HAMSTER DI JALANKAN...',)
            # jalanin bot hamster
            sleep(1)
            print('[Debug] Ask Tap Hamster')
            self.bot.send_message(message.chat.id, 'Apakah anda ingin menggunakan auto tap?',
                                  reply_markup=self.makrup_keyboard('YA', 'TIDAK'))
            self.bot.register_next_step_handler(message, self.ask_tap_hamster)

    def save_query_id_hamster(self, message):
        path = './data_hamster'
        with open(f'{path}/{message.chat.id}.txt', 'w') as file:
            file.write(f'{message.text}\n')

            if os.path.exists(f'{path}/{message.chat.id}.txt'):
                self.bot.send_message(message.chat.id, 'Query ID tersimpan')

                sleep(1)
                print('[Debug] Ask Tap Hamster')
                self.bot.send_message(message.chat.id, 'Apakah anda ingin menggunakan auto tap?',
                                      reply_markup=self.makrup_keyboard('YA', 'TIDAK'))
                self.bot.register_next_step_handler(
                    message, self.ask_tap_hamster)

    def ask_tap_hamster(self, message):
        # global ask_tap
        if debug:
            print('[Debug] Ask Claim Daily')

        self.ask_tap = message.text

        self.bot.send_message(message.chat.id, 'Apakah anda ingin claim daily?',
                              reply_markup=self.makrup_keyboard('YA', 'TIDAK'))
        self.bot.register_next_step_handler(
            message, self.ask_claim_daily_hamster)

    def ask_claim_daily_hamster(self, message):
        # global ask_claim_daily
        if debug:
            print('[Debug] Ask Claim Task')

        self.ask_claim_daily = message.text
        self.bot.send_message(message.chat.id, 'Apakah anda ingin claim task?',
                              reply_markup=self.makrup_keyboard('YA', 'TIDAK'))
        self.bot.register_next_step_handler(
            message, self.ask_claim_task_hamster)

    def ask_claim_task_hamster(self, message):
        if debug:
            print('[Debug] Ask Claim Chiper')

        self.ask_claim_task = message.text

        self.bot.send_message(message.chat.id, 'Apakah anda ingin claim chiper?',
                              reply_markup=self.makrup_keyboard('YA', 'TIDAK'))
        self.bot.register_next_step_handler(
            message, self.ask_claim_chiper_hamster)

    def ask_claim_chiper_hamster(self, message):

        self.ask_claim_chiper = message.text

        if self.ask_claim_chiper.lower() == 'ya':
            if debug:
                print('[Debug] Input Chiper text')
            self.bot.send_message(
                chat_id=message.chat.id, text='Masukkan Chiper: ', reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(
                message, self.save_chiper_text_hamster)
        else:
            if debug:
                print('[Debug] Ask Claim Daily Combo')

            self.bot.send_message(message.chat.id, 'Apakah anda ingin claim daily combo?', reply_markup=self.makrup_keyboard(
                'YA', 'TIDAK'))
            self.bot.register_next_step_handler(
                message, self.ask_claim_daily_combo_hamster)

    def save_chiper_text_hamster(self, message):
        if debug:
            print('[Debug] Save Chiper Text')

        self.chiper_text = message.text
        self.bot.send_message(message.chat.id, 'Chiper tersimpan')

        if debug:
            print('[Debug] Ask Claim Daily Combo')

        sleep(1)
        self.bot.send_message(message.chat.id, 'Apakah anda ingin claim daily combo?', reply_markup=self.makrup_keyboard(
            'YA', 'TIDAK'))
        self.bot.register_next_step_handler(
            message, self.ask_claim_daily_combo_hamster)

    def ask_claim_daily_combo_hamster(self, message):
        self.ask_claim_daily_combo = message.text

        if self.ask_claim_daily_combo.lower() == 'ya':
            if debug:
                print('[Debug] Input ID Combo')
            self.bot.send_message(
                chat_id=message.chat.id, text='Masukkan ID combo, contoh: (id_1, id_2, id_3) : ', reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(
                message, self.save_id_combo_hamster)
        else:
            pesan = f'''
===== INFORMATION =====
*Auto Tap           : {self.ask_tap}*
*Auto Claim Daily   : {self.ask_claim_daily}*
*Auto Claim Task    : {self.ask_claim_task}*
*Auto Claim Chiper  : {self.ask_claim_chiper}*
*Chiper Text        : {self.chiper_text}*
*Auto Claim Combo   : {self.ask_claim_daily_combo}*
*ID Combo           : {self.id_combo}*
        '''
            self.bot.send_message(message.chat.id, pesan, parse_mode='markdown',
                                  reply_markup=types.ReplyKeyboardRemove())

            Hamster.main(message.chat.id, self.ask_tap,
                         self.ask_claim_daily, self.ask_claim_task, self.ask_claim_chiper, self.chiper_text, self.ask_claim_daily_combo, self.id_combo, self.bot)

    def save_id_combo_hamster(self, message):
        if debug:
            print('[Debug] Save id combo')

        self.id_combo = message.text.replace(' ', '').split(',')

        pesan = f'''
===== INFORMATION =====
*Auto Tap           : {self.ask_tap}*
*Auto Claim Daily   : {self.ask_claim_daily}*
*Auto Claim Task    : {self.ask_claim_task}*
*Auto Claim Chiper  : {self.ask_claim_chiper}*
*Chiper Text        : {self.chiper_text}*
*Auto Claim Combo   : {self.ask_claim_daily_combo}*
*ID Combo           : {self.id_combo}*
        '''
        self.bot.send_message(message.chat.id, pesan, parse_mode='markdown',
                              reply_markup=types.ReplyKeyboardRemove())

        Hamster.main(message.chat.id, self.ask_tap,
                     self.ask_claim_daily, self.ask_claim_task, self.ask_claim_chiper, self.chiper_text, self.ask_claim_daily_combo, self.id_combo, self.bot)
