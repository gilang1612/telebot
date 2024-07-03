import requests
import json
import os
import time
# from datetime import datetime
# from itertools import cycle
from colorama import init, Fore, Style
# from tqdm import tqdm
import telebot
from telebot import types
from Config import token, debug
# from main import create_inline_keyboard


def create_inline_keyboard():
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    markup.add('HAMSTER', 'PIXELVERSE')

    return markup


init(autoreset=True)
# MAIN CODE
auto_claim_daily_combo = None
combo_list = None
cek_task_dict = {}
claimed_ciphers = set()
combo_upgraded = {}
token_dict = {}

fungsi_terpilih = []

# NANYA AJA
ask_tap = None
ask_daily = None
ask_task_list = None
ask_cipher = None
cipher_text = None
ask_daily_combo = None

message = None


def load_tokens(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]


def get_headers(token):
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'

    }


def get_token(init_data_raw):
    url = 'https://api.hamsterkombat.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'authorization': 'authToken is empty, store token null',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    try:
        response = requests.post(url, headers=headers, data=data)
        # print(response.status_code)
        if response.status_code == 200:
            return response.json()['authToken']
            # return response.json()['authToken']
        elif response.status_code == 403:
            print(Fore.RED + Style.BRIGHT +
                  "\rAkses Ditolak. Status 403", flush=True)
        elif response.status_code == 500:
            print(response.json())
            print(Fore.RED + Style.BRIGHT +
                  "\rInternal Server Error", flush=True)
        else:
            error_data = response.json()
            if "invalid" in error_data.get("error_code", "").lower():
                print(Fore.RED + Style.BRIGHT +
                      "\rGagal Mendapatkan Token. Data init tidak valid", flush=True)
            else:
                print(Fore.RED + Style.BRIGHT +
                      f"\rGagal Mendapatkan Token. {error_data}", flush=True)
    except requests.exceptions.Timeout:
        print(Fore.RED + Style.BRIGHT +
              "\rGagal Mendapatkan Token. Request Timeout", flush=True)
    except requests.exceptions.ConnectionError:
        print(Fore.RED + Style.BRIGHT +
              "\rGagal Mendapatkan Token. Kesalahan Koneksi", flush=True)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT +
              f"\rGagal Mendapatkan Token. Error: {str(e)}", flush=True)
    return None


def authenticate(token):
    url = 'https://api.hamsterkombat.io/auth/me-telegram'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

# ===== FOR TAP TAP ========


def tap(token, max_taps, available_taps, bot, chat_id):
    global message
    # print('jalan tap tap')
    # return
    url = 'https://api.hamsterkombat.io/clicker/tap'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps(
        {"count": max_taps, "availableTaps": available_taps, "timestamp": int(time.time())})
    # response = requests.post(url, headers=headers, data=data)
    # return response
    print(max_taps, available_taps)
    if available_taps == max_taps:
        print(Fore.GREEN +
              f"\r[ Status Klik ] : Mulai Klik ...", end="", flush=True)
        message = bot.send_message(chat_id, "Mulai Klik ...")
        response = requests.post(url, headers=headers, data=data)
        time.sleep(3)
        if response.status_code == 200:
            print(Fore.GREEN + Style.BRIGHT +
                  "\r[ Status Klik ] : Berhasil Mengklik", flush=True)
            bot.send_message(
                chat_id=chat_id,  text="Berhasil Mengklik ...")
            time.sleep(3)
        else:
            print(Fore.RED + Style.BRIGHT +
                  "\r[ Status Klik ] : Gagal Mengklik", flush=True)
            bot.send_message(
                chat_id=chat_id,  text="Gagal Mengklik ...")
            time.sleep(3)
    else:
        print(Fore.RED + Style.BRIGHT +
              f"\r[ Status Klik ] : Energi Klik Tidak Cukup | {available_taps}/{max_taps}", flush=True)
        bot.send_message(
            chat_id, f"Energi Klik Tidak Cukup | {available_taps}/{max_taps}", parse_mode='markdown')
        time.sleep(3)
        # print(Fore.YELLOW + Style.BRIGHT +
        #       f"\r[ Status Klik ] : Loading hingga energi penuh", flush=True)


def sync_clicker(token):
    url = 'https://api.hamsterkombat.io/clicker/sync'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response
# ======== END TAP TAP =======

# ======== GET INFO USER ========


def get_info_user(token, bot, chat_id):
    response = sync_clicker(token)
    if response.status_code == 200:
        clicker_data = response.json()['clickerUser']
        info_user = f'''\r
{Fore.CYAN + Style.BRIGHT}===========================================
{Fore.GREEN + Style.BRIGHT}     Level            : {Fore.CYAN + Style.BRIGHT}{clicker_data['level']}
{Fore.GREEN + Style.BRIGHT}     Total Earned     : {Fore.CYAN + Style.BRIGHT}{int(clicker_data['totalCoins'])}
{Fore.GREEN + Style.BRIGHT}     Passive Earn / H : {Fore.CYAN + Style.BRIGHT}{int(clicker_data['earnPassivePerHour'])}
{Fore.GREEN + Style.BRIGHT}     Coin             : {Fore.CYAN + Style.BRIGHT}{int(clicker_data['balanceCoins'])}
{Fore.GREEN + Style.BRIGHT}     Energy           : {Fore.CYAN + Style.BRIGHT}{clicker_data['availableTaps']}
{Fore.GREEN + Style.BRIGHT}     Exchange         : {Fore.CYAN + Style.BRIGHT}{clicker_data['exchangeId']}
{Fore.CYAN + Style.BRIGHT}============================================
'''
        info_user_to_bot = f'''
*==================================*
*Level                         : {clicker_data['level']}*
*Total Earned          : {int(clicker_data['totalCoins'])}*
*Passive Earn / H   : {int(clicker_data['earnPassivePerHour'])}*
*Coin                          : {int(clicker_data['balanceCoins'])}*
*Energy                     : {clicker_data['availableTaps']}*
*Exchange                : {clicker_data['exchangeId']}*
*===================================*
'''

        return clicker_data, info_user, info_user_to_bot

    else:
        print(Fore.RED + Style.BRIGHT +
              f"\r Gagal mendapatkan info user {response.status_code}", flush=True)
        bot.send_message(
            chat_id, f"Gagal mendapatkan info user {response.status_code}", parse_mode='markdown'
        )

# ======= END GET INFO USER =======

# ======= CLAIM DAILY ========


def claim_daily(token, bot, chat_id):
    global message
    # print('jalan claim daily')
    # return
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    response = requests.post(url, headers=headers, data=data)
    # return response

    if response.status_code == 200:
        daily_response = response.json()['task']
        print(Fore.GREEN +
              f"\r[ Checkin Daily ] : Checking...", end="", flush=True)
        message = bot.send_message(
            chat_id, "Checking daily...", parse_mode='markdown'
        )
        time.sleep(3)
        if daily_response['isCompleted']:
            print(Fore.GREEN + Style.BRIGHT +
                  f"\r[ Checkin Daily ] Days {daily_response['days']} | Berhasil di claim", flush=True)
            bot.send_message(
                chat_id=chat_id,  text=f"Berhasil di claim | Days {daily_response['days']}", parse_mode='markdown'
            )
            time.sleep(3)
        else:
            print(Fore.RED + Style.BRIGHT +
                  f"\r[ Checkin Daily ] Days {daily_response['days']} | Belum saat nya claim daily", flush=True)
            bot.send_message(
                chat_id=chat_id,  text=f"Belum saat nya claim daily | Days {daily_response['days']}", parse_mode='markdown'
            )
            time.sleep(3)
    else:
        print(Fore.RED + Style.BRIGHT +
              f"\r[ Checkin Daily ] Gagal cek daily {response.status_code}", flush=True)
        bot.send_message(
            chat_id=chat_id,  text=f"Gagal cek daily {response.status_code}", parse_mode='markdown'
        )
        time.sleep(3)
# ======= END CLAIM DAILY =======

# ======= TASK ========


def check_task(token, task_id):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": task_id})
    response = requests.post(url, headers=headers, data=data)
    # return response
    if response.status_code == 200 and response.json()['task']['isCompleted']:
        print(
            Fore.GREEN + Style.BRIGHT + f"\r[ List Task ] : Claimed {task_id}\n", flush=True)
        time.sleep(3)
    else:
        print(Fore.RED + Style.BRIGHT +
              f"\r[ List Task ] : Gagal Claim {task_id}\n", flush=True)
        time.sleep(3)


def list_tasks(token, bot, chat_id):
    global message

    url = 'https://api.hamsterkombat.io/clicker/list-tasks'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    # return response
    print(Fore.GREEN + f"\r[ List Task ] : Checking...", end="", flush=True)
    message = bot.send_message(
        chat_id, "Checking Task...", parse_mode='markdown'
    )
    time.sleep(3)
    if token not in cek_task_dict:
        cek_task_dict[token] = False

    if not cek_task_dict[token]:
        cek_task_dict[token] = True

    if response.status_code == 200:
        tasks = response.json()['tasks']
        all_completed = all(task['isCompleted'] or task['id']
                            == 'invite_friends' for task in tasks)

        if all_completed:
            print(Fore.GREEN + Style.BRIGHT +
                  "\r[ List Task ] : Semua task sudah diclaim\n", flush=True)
            bot.send_message(
                chat_id=chat_id,  text="Semua task sudah diclaim", parse_mode='markdown'
            )
            time.sleep(3)
            print(Fore.GREEN + Style.BRIGHT +
                  "\r[ List Task ] : Lanjut Mang...\n", flush=True)
            time.sleep(3)
        else:
            for task in tasks:
                if not task['isCompleted']:
                    print(Fore.YELLOW + Style.BRIGHT +
                          f"\r[ List Task ] : Claiming {task['id']}...", end="", flush=True)
                    bot.send_message(
                        chat_id, f"Claiming Task {task['id']} ...", parse_mode='markdown'
                    )
                    time.sleep(3)
                    check_task(token, task['id'])
                else:
                    print(Fore.GREEN + Style.BRIGHT +
                          f"\r[ List Task ] : {task['id']} sudah diclaim\n", flush=True)
                    try:
                        bot.send_message(
                            chat_id, f"Task {str(task['id'])} sudah diclaim", parse_mode='markdown'
                        )
                    except:
                        pass
                    time.sleep(3)

            print(Fore.GREEN + Style.BRIGHT +
                  "\r[ List Task ] : Semua task sudah diclaim\n", flush=True)
            bot.send_message(
                chat_id, "Semua task sudah diclaim", parse_mode='markdown'
            )
            time.sleep(3)
            print(Fore.GREEN + Style.BRIGHT +
                  "\r[ List Task ] : Lanjut Mang...\n", flush=True)
            time.sleep(3)
    else:
        print(Fore.RED + Style.BRIGHT +
              f"\r[ List Task ] : Gagal mendapatkan list task {response.status_code}", flush=True)
        bot.send_message(
            chat_id, f"Gagal mendapatkan list task {response.status_code}", parse_mode='markdown'
        )
        time.sleep(3)

# ======= END TASK =======

# ======= CLAIM CIPHER ========


def claim_cipher(token, cipher_text, bot, chat_id):
    global message

    cipher_text = cipher_text.upper()
    # print('jalan claim cipher ', cipher_text)
    # return
    url = 'https://api.hamsterkombat.io/clicker/claim-daily-cipher'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"cipher": cipher_text})
    # response = requests.post(url, headers=headers, data=data)

    if token not in claimed_ciphers:
        print(Fore.GREEN + Style.BRIGHT +
              f"\r[ Claim Cipher ] : Claiming cipher...", end="", flush=True)
        message = bot.send_message(
            chat_id, "Claiming cipher...", parse_mode='markdown'
        )
        response = requests.post(url, headers=headers, data=data)
        try:
            if response.status_code == 200:
                bonuscoins = response.json(
                )['dailyCipher']['bonusCoins']
                print(
                    Fore.GREEN + Style.BRIGHT + f"\r[ Claim Cipher ] : Berhasil claim cipher | {bonuscoins} bonus coin", flush=True)
                bot.send_message(
                    chat_id=chat_id,  text=f"Berhasil claim cipher | {bonuscoins} bonus coin", parse_mode='markdown'
                )
                claimed_ciphers.add(token)
                time.sleep(3)
            else:
                error_info = response.json()
                if error_info.get('error_code') == 'DAILY_CIPHER_DOUBLE_CLAIMED':
                    print(
                        Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : Cipher already claimed", flush=True)
                    bot.send_message(
                        chat_id=chat_id,  text="Cipher already claimed", parse_mode='markdown'
                    )
                    time.sleep(3)
                else:
                    print(
                        Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : Gagal claim cipher dengan error: {error_info.get('error_message', 'No error message')}", flush=True)
                    bot.send_message(
                        chat_id=chat_id,  text=f"Gagal claim cipher dengan error: {error_info.get('error_message', 'No error message')}", parse_mode='markdown'
                    )
                    time.sleep(3)
        except json.JSONDecodeError:
            print(
                Fore.RED + Style.BRIGHT + "\r[ Claim Cipher ] : Gagal mengurai JSON dari respons.", flush=True)
            bot.send_message(
                chat_id=chat_id,  text="Gagal mengurai JSON dari respons.", parse_mode='markdown'
            )
            time.sleep(3)
        except Exception as e:
            print(
                Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : Terjadi error: {str(e)}", flush=True)
            bot.send_message(
                chat_id=chat_id,  text=f"Terjadi error: {str(e)}", parse_mode='markdown'
            )
            time.sleep(3)
    else:
        print(Fore.RED + Style.BRIGHT +
              f"\r[ Claim Cipher ] : Cipher sudah pernah di-claim sebelumnya.", flush=True)
        bot.send_message(
            chat_id=chat_id, text="Cipher sudah pernah di-claim sebelumnya.", parse_mode='markdown'
        )
        time.sleep(3)

# ======= END CLAIM CIPHER =======

# ======= CLAIM DAILY COMBO ========


def get_available_upgrades_combo(token):
    url = 'https://api.hamsterkombat.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            print(Fore.GREEN + Style.BRIGHT +
                  f"\r[ Daily Combo ] : Berhasil mendapatkan list upgrade.", flush=True)
            time.sleep(3)
            return upgrades
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT +
                  "\r[ Daily Combo ] : Gagal mendapatkan response JSON.", flush=True)
            time.sleep(3)
            return []
    else:
        print(Fore.RED + Style.BRIGHT +
              f"\r[ Daily Combo ] : Gagal mendapatkan daftar upgrade: Status {response.status_code}", flush=True)
        time.sleep(3)
        return []


def check_and_upgrade(token, upgrade_id, required_level, bot, chat_id):
    upgrades = get_available_upgrades_combo(token)
    if upgrades:
        for upgrade in upgrades:

            if upgrade['id'] == upgrade_id and upgrade['level'] < required_level + 1:
                print(Fore.CYAN + Style.BRIGHT +
                      f"[ Daily Combo ] : Upgrading {upgrade_id}", flush=True)
                time.sleep(3)
                req_level_total = required_level + 1
                for _ in range(req_level_total - upgrade['level']):
                    result = buy_upgrade_combo(token, upgrade_id)
                    # print("buying..")
                    if isinstance(result, dict) and 'error_code' in result and result['error_code'] == 'UPGRADE_NOT_AVAILABLE':
                        # print("ada error")
                        needed_upgrade = result['error_message'].split(
                            ':')[-1].strip().split()
                        needed_upgrade_id = needed_upgrade[1]
                        needed_upgrade_level = int(needed_upgrade[-1])
                        print(Fore.YELLOW + Style.BRIGHT +
                              f"\r[ Daily Combo ] : Mencoba membeli {needed_upgrade_id} level {needed_upgrade_level}", flush=True)
                        time.sleep(3)
                        if check_and_upgrade(token, needed_upgrade_id, needed_upgrade_level):
                            print(Fore.GREEN + Style.BRIGHT +
                                  f"\r[ Daily Combo ] : Berhasil upgrade {needed_upgrade_id} ke level {needed_upgrade_level}. Mencoba kembali upgrade {upgrade_id}.", flush=True)
                            time.sleep(3)
                            # continue  # Setelah berhasil, coba lagi upgrade asli
                        else:
                            print(
                                Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal upgrade {needed_upgrade_id} ke level {needed_upgrade_level}", flush=True)
                            time.sleep(3)
                            return False
                    elif result == 'insufficient_funds':
                        print("coin")
                        print(Fore.RED + Style.BRIGHT +
                              f"\r[ Daily Combo ] : Coin tidak cukup untuk upgrade {upgrade_id}", flush=True)
                        time.sleep(3)
                        return False
                    elif result.status_code != 200:
                        print(f"error response : {result}")
                        print(Fore.RED + Style.BRIGHT +
                              f"\r[ Daily Combo ] : Gagal upgrade {upgrade_id} dengan error: {result}", flush=True)
                        time.sleep(3)
                        return False
                print(Fore.GREEN + Style.BRIGHT +
                      f"\r[ Daily Combo ] : Upgrade {upgrade_id} berhasil dilakukan ke level {required_level}", flush=True)
                time.sleep(3)
                return True
    # print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : Upgrade {upgrade_id} berhasil dilakukan ke level {required_level}", flush=True)
    return False


def buy_upgrade_combo(token, upgrade_id, bot, chat_id):
    url = 'https://api.hamsterkombat.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + Style.BRIGHT +
                  f"\r[ Daily Combo ] : Combo {upgrade_id} berhasil dibeli.", flush=True)
            bot.send_message(chat_id, f"Combo {upgrade_id} berhasil dibeli.")
            time.sleep(3)
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT +
                  "\r[ Daily Combo ] : Gagal mengurai JSON saat upgrade.", flush=True)
            bot.send_message(chat_id, "Gagal mengurai JSON saat upgrade.")
            time.sleep(3)
        return response
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.RED + Style.BRIGHT +
                      f"\r[ Daily Combo ] : Coin tidak cukup.", flush=True)
                bot.send_message(chat_id, "Coin tidak cukup.")
                time.sleep(3)
                return 'insufficient_funds'
            else:
                # print(f"error saat beli combo: {error_response}")
                # print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Error: {error_response.get('error_message', 'No error message provided')}", flush=True)
                return error_response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT +
                  f"\r[ Daily Combo ] : Gagal mendapatkan respons JSON. Status: {response.status_code}", flush=True)
            bot.send_message(
                chat_id, f"Gagal mendapatkan respons JSON. Status: {response.status_code}")
            time.sleep(3)
            return None


def check_combo_purchased(token, bot, chat_id):
    url = 'https://api.hamsterkombat.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        purchased_combos = data.get('dailyCombo', {}).get('upgradeIds', [])
        return purchased_combos
    else:
        print(Fore.RED + Style.BRIGHT +
              f"Gagal mendapatkan status combo. Status: {response.status_code}", flush=True)
        bot.send_message(
            chat_id, f"Gagal mendapatkan status combo. Status: {response.status_code}")
        time.sleep(3)
        return None


def claim_daily_combo(token, bot, chat_id):
    global message

    url = 'https://api.hamsterkombat.io/clicker/claim-daily-combo'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    # if auto_claim_daily_combo == 'y' and not combo_upgraded.get(init_data_raw):
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        print(
            Fore.GREEN + Style.BRIGHT + "\r[ Daily Combo ] : Berhasil mengklaim daily combo.", flush=True)
        bot.send_message(chat_id, 'Berhasil mengklaim daily combo.',
                         reply_markup=types.ReplyKeyboardRemove())
        time.sleep(3)
        return response.json()
    else:
        error_response = response.json()
        if error_response.get('error_code') == 'DAILY_COMBO_DOUBLE_CLAIMED':
            print(Fore.YELLOW + Style.BRIGHT +
                  "\r[ Daily Combo ] : Sudah Claimed          ", flush=True)
            bot.send_message(chat_id, 'Combo Sudah Di Claim. Tidak dapat claim kembali.',
                             reply_markup=types.ReplyKeyboardRemove())
            time.sleep(3)
        else:
            print(Fore.RED + Style.BRIGHT +
                  f"\r[ Daily Combo ] : Belum Di Claim. {response}", flush=True)
            bot.send_message(chat_id, 'Combo Belum Di Claim.',
                             reply_markup=types.ReplyKeyboardRemove())
            time.sleep(3)
        return error_response

    # if response.status_code == 200:
    #     print(Fore.GREEN + Style.BRIGHT +
    #           "\r[ Daily Combo ] : Berhasil mengklaim daily combo.                                          ", flush=True)
    #     return response.json()
    # else:
    #     error_response = response.json()
    #     if error_response.get('error_code') == 'DAILY_COMBO_DOUBLE_CLAIMED':
    #         print(Fore.YELLOW + Style.BRIGHT +
    #               "\r[ Daily Combo ] : Claimed          ", flush=True)
    #     else:
    #         print(Fore.RED + Style.BRIGHT +
    #               f"\r[ Daily Combo ] : Faile. {response}", flush=True)
    #     return error_response


def cek_daily_combo(token, init_data_raw, bot, chat_id):
    global message

    response = claim_daily_combo(token, bot, chat_id)

    if response.get('error_code') != 'DAILY_COMBO_DOUBLE_CLAIMED':

        purchased_combos = check_combo_purchased(token, bot, chat_id)

        if purchased_combos is None:
            print(Fore.RED + Style.BRIGHT +
                  "\r[ Daily Combo ] : Gagal mendapatkan status combo.", flush=True)
            bot.send_message(chat_id, 'Gagal mendapatkan status combo.',
                             reply_markup=types.ReplyKeyboardRemove())
            time.sleep(3)
        else:
            for combo in combo_list:
                if combo in purchased_combos:
                    print(Fore.GREEN + Style.BRIGHT +
                          f"\r[ Daily Combo ] : {combo} sudah dibeli.", flush=True)
                    bot.send_message(
                        chat_id, f'{combo} sudah dibeli.', reply_markup=types.ReplyKeyboardRemove())
                else:
                    print(Fore.YELLOW + Style.BRIGHT +
                          f"\r[ Daily Combo ] : Membeli {combo}", flush=True)
                    bot.send_message(
                        chat_id, f'Membeli {combo}', reply_markup=types.ReplyKeyboardRemove())

                    result = buy_upgrade_combo(token, combo, bot, chat_id)

                    if result == 'insufficient_funds':
                        print(
                            Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal membeli {combo} coin tidak cukup", flush=True)
                        bot.send_message(
                            chat_id, f'Gagal membeli {combo} coin tidak cukup.', reply_markup=types.ReplyKeyboardRemove())
                    elif 'error_code' in result and result['error_code'] == 'UPGRADE_NOT_AVAILABLE':
                        upgrade_details = result['error_message'].split(
                            ':')[-1].strip().split()
                        upgrade_key = upgrade_details[1]
                        upgrade_level = int(
                            upgrade_details[-1])
                        print(
                            Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal beli {combo} membutuhkan {upgrade_key} level {upgrade_level}", flush=True)
                        bot.send_message(
                            chat_id, f'Gagal beli {combo} membutuhkan {upgrade_key} level {upgrade_level}.', reply_markup=types.ReplyKeyboardRemove())
                        time.sleep(3)
                        print(
                            Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Mencoba membeli {upgrade_key} level {upgrade_level}", flush=True)
                        bot.send_message(
                            chat_id, f'Mencoba membeli {upgrade_key} level {upgrade_level}.', reply_markup=types.ReplyKeyboardRemove())
                        time.sleep(3)

                        result = check_and_upgrade(
                            token, upgrade_key, upgrade_level, bot, chat_id)

            combo_upgraded[init_data_raw] = True
            required_combos = set(combo_list)

            purchased_combos = set(check_combo_purchased(token, bot, chat_id))

            if purchased_combos == required_combos:
                print(
                    Fore.GREEN + Style.BRIGHT + "\r[ Daily Combo ] : Semua combo telah dibeli.", end="", flush=True)
                bot.send_message(chat_id, 'Semua combo telah dibeli.',
                                 reply_markup=types.ReplyKeyboardRemove())
                time.sleep(3)
                print(
                    Fore.GREEN + Style.BRIGHT + "\r[ Daily Combo ] : mengklaim daily combo.", end="", flush=True)
                bot.send_message(chat_id, 'mengklaim daily combo.',
                                 reply_markup=types.ReplyKeyboardRemove())
                time.sleep(3)
                claim_daily_combo(token, bot, chat_id)
            else:
                print(
                    Fore.YELLOW + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal. Combo yang belum dibeli: {required_combos - purchased_combos}               ", flush=True)
                bot.send_message(
                    chat_id, f'Gagal. Combo yang belum dibeli: {required_combos - purchased_combos}               ', reply_markup=types.ReplyKeyboardRemove())
                combo_upgraded[init_data_raw] = False
                time.sleep(3)
# ======== END CLAIM DAILY COMBO =======

# ========== OTENTISASI TOKEN DAN CEK TOKEN ==========


def otentisasi_token(token, init_data_raw, bot, chat_id):
    response_auth = authenticate(token)

    if response_auth.status_code == 200:
        user_data = response_auth.json()
        firstName = user_data.get(
            'telegramUser', {}).get('firstName', '')
        lastName = user_data.get('telegramUser', {}).get('lastName', '')

        # INFO USER
        # clicker_data, info_user = get_info_user(ambil_token)
        # kamu_nanya(token, firstName, lastName, init_data_raw)
        return firstName, lastName

    elif response_auth.status_code == 401:
        err_data = response_auth.json()
        if err_data.get("error_code") == "NotFound_Session":
            print(Fore.RED + Style.BRIGHT +
                  f"=== [ Token Invalid {token} ] ===")
            bot.send_message(
                chat_id, f"=== [ Token Invalid {token} ] ===", parse_mode='markdown'
            )
            time.sleep(3)
            token_dict.pop(init_data_raw, None)
        else:
            print(Fore.RED + Style.BRIGHT +
                  "Authentication failed with unknown error")
            bot.send_message(
                chat_id, "Authentication failed with unknown error", parse_mode='markdown'
            )
            time.sleep(3)
    else:
        print(Fore.RED + Style.BRIGHT +
              f"Error with status code: {response_auth.status_code}")
        bot.send_message(
            chat_id, f"Error with status code: {response_auth.status_code}", parse_mode='markdown'
        )
        time.sleep(3)
# ========= END OTENTISASI TOKEN DAN CEK TOKEN ==========


def main(chat_id, ask_tap, ask_claim_daily, ask_claim_task, ask_claim_chiper, chiper_text, ask_claim_daily_combo, id_combo, bot):
    global cek_task_dict, claimed_ciphers, auto_claim_daily_combo, combo_list, combo_upgraded, message

    if debug:
        print('[Debug] Main')
        print('')
        print(chat_id)
        print(ask_tap)
        print(ask_claim_daily)
        print(ask_claim_task)
        print(ask_claim_chiper)
        print(chiper_text)
        print(ask_claim_daily_combo)
        print(id_combo)
        print('')

    path = './data_hamster'
    with open(f'{path}/{chat_id}.txt', 'r') as file:
        init_data = file.readlines()

    for init_data_raw in init_data:
        init_data_raw = init_data_raw.strip()
        token = token_dict.get(init_data_raw)

        if token:
            time.sleep(3)
            print(Fore.GREEN + Style.BRIGHT +
                  f"\n\rMenggunakan token yang sudah ada...", end="", flush=True)
            bot.send_message(
                chat_id, f"Menggunakan token yang sudah ada...", parse_mode='markdown'
            )
        else:
            print(Fore.RED + Style.BRIGHT +
                  f"\n\rToken kosong...", end="", flush=True)
            time.sleep(3)
            print(Fore.YELLOW + Style.BRIGHT +
                  f"\rMengambil token...", end="", flush=True)
            message = bot.send_message(
                chat_id, f"Mengambil token...", parse_mode='markdown'
            )
            time.sleep(3)

            token = get_token(init_data_raw)

            if token:
                token_dict[init_data_raw] = token
                print(Fore.GREEN + Style.BRIGHT +
                      "\rSukses ambil token!", flush=True)
                bot.send_message(
                    chat_id=chat_id,  text=f"Sukses ambil token!", parse_mode='markdown'
                )
                # bot.send_message(
                #     chat_id, f"Sukses ambil token!", parse_mode='markdown'
                # )
            else:
                print(Fore.RED + Style.BRIGHT +
                      "\rGagal ambil token!", flush=True)
                bot.send_message(
                    chat_id=chat_id,  text=f"Gagal ambil token!", parse_mode='markdown'
                )
                time.sleep(3)

        firstName, lastName = otentisasi_token(
            token, init_data_raw, bot, chat_id)
        clicker_data, info_user, info_user_to_bot = get_info_user(
            token, bot, chat_id)

        print(Fore.GREEN + Style.BRIGHT + "\rBOT Mulai...")
        bot.send_message(
            chat_id, f'*{firstName} {lastName}*\n{info_user_to_bot}', parse_mode='markdown')
        time.sleep(5)

        if ask_tap == 'YA':
            tap(token, clicker_data['maxTaps'],
                clicker_data['availableTaps'], bot, chat_id)
        else:
            pass

        if ask_claim_daily == 'YA':
            claim_daily(token, bot, chat_id)
        else:
            pass

        if ask_claim_task == 'YA':
            list_tasks(token, bot, chat_id)
        else:
            pass

        if ask_claim_chiper == 'YA':
            claim_cipher(token, chiper_text, bot, chat_id)
        else:
            pass

        if ask_claim_daily_combo == 'YA':
            combo_list = id_combo
            cek_daily_combo(token, init_data_raw, bot, chat_id)
        else:
            pass

    _, _, info_user_to_bot_ = get_info_user(token, bot, chat_id)
    bot.send_message(
        chat_id, f'*{firstName} {lastName}*\n{info_user_to_bot_}', parse_mode='markdown')
    time.sleep(3)

    bot.send_message(
        chat_id, f'Bot Hamster Selesai Dijalankan', parse_mode='markdown', reply_markup=create_inline_keyboard())
