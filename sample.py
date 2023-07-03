import telebot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from flask import Flask, request
from datetime import datetime

TELEGRAM_TOKEN = '6354853592:AAG5_pH0dnAm_d4eoENsWXEQIQ64tLz5Frk'

cryptos = ["Bitcoin", "BNB BSC", "Tether USDT (TRC20)", "BUSD BSC", "TRON TRX", "Bitcoin Cash", "Litecoin"]
wallet = ["bc1qs4fgmy5md8se2wdztdp7ekzh9mv0lclw4e6nqw", "0x629060ad93Eab915656797206429607FB64E0D88", "TMYPiJkBbVEg6Bhxa2Y4k6dMWmNjUKbVfj", "0x629060ad93Eab915656797206429607FB64E0D88", "TMYPiJkBbVEg6Bhxa2Y4k6dMWmNjUKbVfj", "qr5nfekx2ut54ht30ww43t54xt4736l22gp5q9wxgh", "LWJzcpuiYNkwVHw1xCu3cETGnXkiyCpQhd"]

c23 = {
    "Bitcoin": "btc",
    "BNB BSC": "bnb",
    "Tether USDT (TRC20)": "trc",
    "BUSD BSC": "bsc",
    "TRON TRX": "trx",
    "Bitcoin Cash": "bcs",
    "Litecoin": "ltc",
}

bot = telebot.TeleBot(TELEGRAM_TOKEN)
#bot.delete_webhook()

client = MongoClient('mongodb://localhost:27017/telebot')
db = client['telebot']
pending_contract = db['pending_contract']
pending_withdraw = db['pending_withdraw']
User = db['user']

app = Flask(__name__)


def gen_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Deposit", callback_data="ic_Deposit"))
    markup.add(InlineKeyboardButton("Withdraw", callback_data="ic_Withdraw"))
    markup.add(InlineKeyboardButton("Check Earnings", callback_data="ic_ChkEarning"))
    markup.add(InlineKeyboardButton("Public Group", url=f"https://t.me/fly15investment", callback_data="ic_PbGroup"))
    markup.add(InlineKeyboardButton("Contact Support", url=f"https://t.me/fly15support", callback_data="ic_ContactSupport"))
    return markup

def gen_crypto():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(cryptos[0], callback_data=cryptos[0]))
    markup.add(InlineKeyboardButton(cryptos[1], callback_data=cryptos[1]))
    markup.add(InlineKeyboardButton(cryptos[2], callback_data=cryptos[2]))
    markup.add(InlineKeyboardButton(cryptos[3], callback_data=cryptos[3]))
    markup.add(InlineKeyboardButton(cryptos[4], callback_data=cryptos[4]))
    markup.add(InlineKeyboardButton(cryptos[5], callback_data=cryptos[5]))
    markup.add(InlineKeyboardButton(cryptos[6], callback_data=cryptos[6]))
    return markup

def gen_withdraw():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(cryptos[0], callback_data="w"+cryptos[0]))
    markup.add(InlineKeyboardButton(cryptos[1], callback_data="w"+cryptos[1]))
    markup.add(InlineKeyboardButton(cryptos[2], callback_data="w"+cryptos[2]))
    markup.add(InlineKeyboardButton(cryptos[3], callback_data="w"+cryptos[3]))
    markup.add(InlineKeyboardButton(cryptos[4], callback_data="w"+cryptos[4]))
    markup.add(InlineKeyboardButton(cryptos[5], callback_data="w"+cryptos[5]))
    markup.add(InlineKeyboardButton(cryptos[6], callback_data="w"+cryptos[6]))
    return markup

def gen_earning():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(cryptos[0], callback_data="e"+cryptos[0]))
    markup.add(InlineKeyboardButton(cryptos[1], callback_data="e"+cryptos[1]))
    markup.add(InlineKeyboardButton(cryptos[2], callback_data="e"+cryptos[2]))
    markup.add(InlineKeyboardButton(cryptos[3], callback_data="e"+cryptos[3]))
    markup.add(InlineKeyboardButton(cryptos[4], callback_data="e"+cryptos[4]))
    markup.add(InlineKeyboardButton(cryptos[5], callback_data="e"+cryptos[5]))
    markup.add(InlineKeyboardButton(cryptos[6], callback_data="e"+cryptos[6]))
    return markup

def gen_wallet(budget, crypto):
    yes_button = InlineKeyboardButton("Yes", callback_data='ic_yes:{}:{}'.format(budget, crypto))
    no_button = InlineKeyboardButton("No", callback_data="ic_no")

    markup = InlineKeyboardMarkup(
        [
            [
                yes_button,
                no_button  
            ]   
        ]
    )
    return markup

def gen_withdraw_confirm(username, crypto, withdraw, address):
    yes_button = InlineKeyboardButton("Yes", callback_data='wc_yes:{}:{}:{}:{}'.format(username, crypto, withdraw, address))
    no_button = InlineKeyboardButton("No", callback_data="wc_no")

    markup = InlineKeyboardMarkup(
        [
            [
                yes_button,
                no_button  
            ]   
        ]
    )
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "ic_Deposit":
        bot.answer_callback_query(call.id, "Deposit")
        bot.send_message(call.message.chat.id, "Please choose a crypto to deposit", reply_markup=gen_crypto())
    elif call.data == "ic_Withdraw":
        bot.answer_callback_query(call.id, "Withdraw")
        bot.send_message(call.message.chat.id, "Please choose a crypto to withdraw", reply_markup=gen_withdraw())
    elif call.data == "ic_ChkEarning":
        bot.answer_callback_query(call.id, "ChkGroup")
        bot.send_message(call.message.chat.id, "Please choose a crypto.", reply_markup=gen_earning())
    elif call.data == "ic_PbGroup":
        bot.answer_callback_query(call.id, "PbGroup")
    elif call.data == "ic_ContactSupport":
        bot.answer_callback_query(call.id, "ContactSupport")
    elif call.data == cryptos[0]:
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 0)
    elif call.data == cryptos[1]:
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 1)
    elif call.data == cryptos[2]:
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 2)
    elif call.data == cryptos[3]:
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 3)
    elif call.data == cryptos[4]:
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 4)
    elif call.data == cryptos[5]:
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 5)
    elif call.data == cryptos[6]:
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 6)
    elif call.data == ("w"+cryptos[0]):
        crypto = c23[cryptos[0]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 0, user[crypto])
    elif call.data == ("w"+cryptos[1]):
        crypto = c23[cryptos[1]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 1, user[crypto])
    elif call.data == ("w"+cryptos[2]):
        crypto = c23[cryptos[2]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 2, user[crypto])
    elif call.data == ("w"+cryptos[3]):
        crypto = c23[cryptos[3]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 3, user[crypto])
    elif call.data == ("w"+cryptos[4]):
        crypto = c23[cryptos[4]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 4, user[crypto])
    elif call.data == ("w"+cryptos[5]):
        crypto = c23[cryptos[5]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 5, user[crypto])
    elif call.data == ("w"+cryptos[6]):
        crypto = c23[cryptos[6]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 6, user[crypto])
    elif call.data == ("e"+cryptos[0]):
        crypto = c23[cryptos[0]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[0]}')
    elif call.data == ("e"+cryptos[1]):
        crypto = c23[cryptos[1]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[1]}')    
    elif call.data == ("e"+cryptos[2]):
        crypto = c23[cryptos[2]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[2]}')
    elif call.data == ("e"+cryptos[3]):
        crypto = c23[cryptos[3]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[3]}')
    elif call.data == ("e"+cryptos[4]):
        crypto = c23[cryptos[4]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[4]}')
    elif call.data == ("e"+cryptos[5]):
        crypto = c23[cryptos[5]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[5]}')
    elif call.data == ("e"+cryptos[6]):
        crypto = c23[cryptos[6]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[6]}')
    elif call.data == "ic_no":
        bot.send_message(call.message.chat.id, text="Investment Canceled!\n\n/start command for menu!")
    elif call.data.split(':')[0] == "ic_yes":
        bot.send_message(call.message.chat.id, text=f'Please deposit to the following address:\n\n{wallet[int(call.data.split(":")[2])]}\n\nOnce you deposit, input your transaction hash to finish your investment')
        bot.register_next_step_handler(call.message, finishTransaction, call.data.split(':')[1], call.data.split(':')[2])
    elif call.data == "wc_no":
        bot.send_message(call.message.chat.id, "Withdraw canceled\n\n/start command for menu.")
    elif call.data.split(':')[0] == "wc_yes":
        array = call.data.split(':')
        pending_withdraw.insert_one({
            "username": array[1],
            "chat_id": call.message.chat.id,
            "crypto": cryptos[int(array[2])],
            "amount": array[3],
            "address": array[4],
            "time": datetime.now(),
        })
        bot.send_message(call.message.chat.id, "Your request has been sent successfully!\n\nPlease wait for acception!")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    if message.chat.id in bot.active_chats:
        return
    elif message.text == "/start":
        bot.send_message(message.chat.id, "What would you like to do?", reply_markup=gen_menu())
    else:
        bot.send_message(message.chat.id, text="/start command for menu!")

def getBudget(message, crypto):
    if message.text == "/start":
        bot.send_message(message.chat.id, "What would you like to do?", reply_markup=gen_menu())
        return
    try:
        budget = float(message.text)
        bot.send_message(message.chat.id, f'Do you agree to invest {budget}$ {cryptos[crypto]} to this platform?', reply_markup=gen_wallet(budget, crypto))
    except ValueError:
        bot.send_message(message.chat.id, "Input valid number!")
        bot.register_next_step_handler(message, getBudget, crypto)

def finishTransaction(message, budget, crypto):
    print(message.text)
    if message.text == "/start":
        bot.send_message(message.chat.id, "What would you like to do?", reply_markup=gen_menu())
        return
    bot.send_message(message.chat.id, text="Thanks for your investment!!!\n\nYour submission is pending and will be confirmed and accepted soon!\n\n/start command for menu!")
    return
    pending_contract.insert_one({
        "username": message.from_user.username,
        "chat_id": int(message.chat.id),
        "budget": float(budget),
        "crypto": cryptos[int(crypto)],
        "time": datetime.now(),
        "hash": message.text,
    })

def withdrawBudget(message, crypto, limit):
    withdraw = float(message.text)
    if message.text == "/start":
        bot.send_message(message.chat.id, "What would you like to do?", reply_markup=gen_menu())
    elif withdraw > limit:
        bot.send_message(message.chat.id, f'You can withdraw at most {limit}$.\n\nPlease input valid price!')
        bot.register_next_step_handler(message, withdrawBudget, 0, limit)
    else:
        bot.send_message(message.chat.id, f'Please input your {cryptos[crypto]} address to withdraw')
        bot.register_next_step_handler(message, confirmWithdraw, crypto, withdraw)

def confirmWithdraw(message, crypto, withdraw):
    if message.text == "/start":
        bot.send_message(message.chat.id, "What would you like to do?", reply_markup=gen_menu())
    else:
        bot.send_message(message.chat.id, f'Are you sure to withdraw {withdraw}$ to follwing address?\n\n{message.text}', reply_markup=gen_withdraw_confirm(message.from_user.username, crypto, withdraw, message.text))
bot.infinity_polling()
# def run_bot():
#     time.sleep(5)  # Wait for 5 seconds
#     bot.infinity_polling()

# bot_thread = threading.Thread(target=run_bot)
# bot_thread.start()

# app.run(host='127.0.0.1', port=5000, debug=True)
    

