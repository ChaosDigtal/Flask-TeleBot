import telebot
from telebot import apihelper
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from flask import Flask, request
from datetime import datetime

TELEGRAM_TOKEN = '6045174097:AAHYV53yHblVs5_KXQGZNDq4JQE5ThB4vYI'

cryptos = ["Bitcoin", "BNB BSC", "Tether USDT (TRC20)", "BUSD BSC", "TRON TRX", "Bitcoin Cash", "Litecoin"]
wallet = ["bc1qs4fgmy5md8se2wdztdp7ekzh9mv0lclw4e6nqw", "0x629060ad93Eab915656797206429607FB64E0D88", "TMYPiJkBbVEg6Bhxa2Y4k6dMWmNjUKbVfj", "0x629060ad93Eab915656797206429607FB64E0D88", "TMYPiJkBbVEg6Bhxa2Y4k6dMWmNjUKbVfj", "qr5nfekx2ut54ht30ww43t54xt4736l22gp5q9wxgh", "LWJzcpuiYNkwVHw1xCu3cETGnXkiyCpQhd"]
kwallet = ["bc1q3vm0pgujlz5yhd45d6watfk3sqgpr2eqev9fw3", "0x9F6d7594F019BA8DcEE25d99b3b341a9AFc89E6C", "TFS9o9EhU4rmw2PBJWFAa84jrJgRjsDYiY", "0x9F6d7594F019BA8DcEE25d99b3b341a9AFc89E6C", "TFS9o9EhU4rmw2PBJWFAa84jrJgRjsDYiY", "qqqejg2ueu6j4uwwgztw8jvak5u5kes2tqgl447syf", "LNA9N5WreRjZjTSENcKQXF21EbWe7RRsCs"];
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

def gen_cbdata(flag, s):
    if flag == 0:
        return "None"
    return s

def gen_menu(rw = 2):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Deposit", callback_data=gen_cbdata(rw, "ic_Deposit")))
    markup.add(InlineKeyboardButton("Withdraw", callback_data=gen_cbdata(rw, "ic_Withdraw")))
    markup.add(InlineKeyboardButton("Check Earnings", callback_data=gen_cbdata(rw, "ic_ChkEarning")))
    markup.add(InlineKeyboardButton("Public Group", url=f"https://t.me/fly15investment", callback_data=gen_cbdata(rw, "ic_PbGroup")))
    markup.add(InlineKeyboardButton("Contact Support", url=f"https://t.me/fly15support", callback_data=gen_cbdata(rw, "ic_ContactSupport")))
    return markup

def gen_crypto(rw = 2):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(cryptos[0], callback_data=gen_cbdata(rw, cryptos[0])))
    markup.add(InlineKeyboardButton(cryptos[1], callback_data=gen_cbdata(rw, cryptos[1])))
    markup.add(InlineKeyboardButton(cryptos[2], callback_data=gen_cbdata(rw, cryptos[2])))
    markup.add(InlineKeyboardButton(cryptos[3], callback_data=gen_cbdata(rw, cryptos[3])))
    markup.add(InlineKeyboardButton(cryptos[4], callback_data=gen_cbdata(rw, cryptos[4])))
    markup.add(InlineKeyboardButton(cryptos[5], callback_data=gen_cbdata(rw, cryptos[5])))
    markup.add(InlineKeyboardButton(cryptos[6], callback_data=gen_cbdata(rw, cryptos[6])))
    return markup

def gen_withdraw(rw = 2):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(cryptos[0], callback_data=gen_cbdata(rw, "w"+cryptos[0])))
    markup.add(InlineKeyboardButton(cryptos[1], callback_data=gen_cbdata(rw, "w"+cryptos[1])))
    markup.add(InlineKeyboardButton(cryptos[2], callback_data=gen_cbdata(rw, "w"+cryptos[2])))
    markup.add(InlineKeyboardButton(cryptos[3], callback_data=gen_cbdata(rw, "w"+cryptos[3])))
    markup.add(InlineKeyboardButton(cryptos[4], callback_data=gen_cbdata(rw, "w"+cryptos[4])))
    markup.add(InlineKeyboardButton(cryptos[5], callback_data=gen_cbdata(rw, "w"+cryptos[5])))
    markup.add(InlineKeyboardButton(cryptos[6], callback_data=gen_cbdata(rw, "w"+cryptos[6])))
    return markup

def gen_earning(rw = 2):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(cryptos[0], callback_data=gen_cbdata(rw, "e"+cryptos[0])))
    markup.add(InlineKeyboardButton(cryptos[1], callback_data=gen_cbdata(rw, "e"+cryptos[1])))
    markup.add(InlineKeyboardButton(cryptos[2], callback_data=gen_cbdata(rw, "e"+cryptos[2])))
    markup.add(InlineKeyboardButton(cryptos[3], callback_data=gen_cbdata(rw, "e"+cryptos[3])))
    markup.add(InlineKeyboardButton(cryptos[4], callback_data=gen_cbdata(rw, "e"+cryptos[4])))
    markup.add(InlineKeyboardButton(cryptos[5], callback_data=gen_cbdata(rw, "e"+cryptos[5])))
    markup.add(InlineKeyboardButton(cryptos[6], callback_data=gen_cbdata(rw, "e"+cryptos[6])))
    return markup

def gen_wallet(budget, crypto, username, rw = 2):
    yes_button = InlineKeyboardButton("Yes", callback_data=gen_cbdata(rw, 'ic_yes:{}:{}:{}'.format(budget, crypto, username)))
    no_button = InlineKeyboardButton("No", callback_data=gen_cbdata(rw, 'ic_no:{}:{}'.format(budget, crypto)))

    markup = InlineKeyboardMarkup(
        [
            [
                yes_button,
                no_button  
            ]   
        ]
    )
    return markup

def gen_withdraw_confirm(username, crypto, withdraw, address, rw = 2):
    yes_button = InlineKeyboardButton("Yes", callback_data=gen_cbdata(rw, 'wc_yes:{}:{}:{}:{}'.format(username, crypto, withdraw, address)))
    no_button = InlineKeyboardButton("No", callback_data=gen_cbdata(rw, 'wc_no:{}:{}:{}:{}'.format(username, crypto, withdraw, address)))

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
        print("Deposit")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="What would you like to do?", reply_markup=gen_menu(0))
        bot.send_message(call.message.chat.id, "Please choose a crypto to deposit", reply_markup=gen_crypto())
    elif call.data == "ic_Withdraw":
        print("Withdraw")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="What would you like to do?", reply_markup=gen_menu(0))
        bot.send_message(call.message.chat.id, "Please choose a crypto to withdraw", reply_markup=gen_withdraw())
    elif call.data == "ic_ChkEarning":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="What would you like to do?", reply_markup=gen_menu(0))
        bot.send_message(call.message.chat.id, "Please choose a crypto.", reply_markup=gen_earning())
    elif call.data == "ic_PbGroup":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="What would you like to do?", reply_markup=gen_menu(0))
    elif call.data == "ic_ContactSupport":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="What would you like to do?", reply_markup=gen_menu(0))
    elif call.data == cryptos[0]:
        print(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to deposit", reply_markup=gen_crypto(0))
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 0)
    elif call.data == cryptos[1]:
        print(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to deposit", reply_markup=gen_crypto(0))
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 1)
    elif call.data == cryptos[2]:
        print(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to deposit", reply_markup=gen_crypto(0))
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 2)
    elif call.data == cryptos[3]:
        print(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to deposit", reply_markup=gen_crypto(0))
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 3)
    elif call.data == cryptos[4]:
        print(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to deposit", reply_markup=gen_crypto(0))
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 4)
    elif call.data == cryptos[5]:
        print(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to deposit", reply_markup=gen_crypto(0))
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 5)
    elif call.data == cryptos[6]:
        print(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to deposit", reply_markup=gen_crypto(0))
        bot.send_message(call.message.chat.id, "How much would you like to invest?")
        bot.register_next_step_handler(call.message, getBudget, 6)
    elif call.data == ("w"+cryptos[0]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to withdraw", reply_markup=gen_withdraw(0))
        crypto = c23[cryptos[0]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 0, user[crypto])
    elif call.data == ("w"+cryptos[1]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to withdraw", reply_markup=gen_withdraw(0))
        crypto = c23[cryptos[1]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 1, user[crypto])
    elif call.data == ("w"+cryptos[2]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to withdraw", reply_markup=gen_withdraw(0))
        crypto = c23[cryptos[2]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 2, user[crypto])
    elif call.data == ("w"+cryptos[3]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to withdraw", reply_markup=gen_withdraw(0))
        crypto = c23[cryptos[3]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 3, user[crypto])
    elif call.data == ("w"+cryptos[4]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to withdraw", reply_markup=gen_withdraw(0))
        crypto = c23[cryptos[4]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 4, user[crypto])
    elif call.data == ("w"+cryptos[5]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to withdraw", reply_markup=gen_withdraw(0))
        crypto = c23[cryptos[5]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 5, user[crypto])
    elif call.data == ("w"+cryptos[6]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto to withdraw", reply_markup=gen_withdraw(0))
        crypto = c23[cryptos[6]]
        user = User.find_one({"chat_id": call.message.chat.id})
        if user == None or user[crypto] == 0:
            bot.send_message(call.message.chat.id, "You can withdraw nothing!")
            return
        bot.send_message(call.message.chat.id, f'You can withdraw at most {user[crypto]}$.\n\n How much would you like to withdraw?')
        bot.register_next_step_handler(call.message, withdrawBudget, 6, user[crypto])
    elif call.data == ("e"+cryptos[0]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto.", reply_markup=gen_earning(0))
        crypto = c23[cryptos[0]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[0]}')
    elif call.data == ("e"+cryptos[1]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto.", reply_markup=gen_earning(0))
        crypto = c23[cryptos[1]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[1]}')    
    elif call.data == ("e"+cryptos[2]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto.", reply_markup=gen_earning(0))
        crypto = c23[cryptos[2]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[2]}')
    elif call.data == ("e"+cryptos[3]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto.", reply_markup=gen_earning(0))
        crypto = c23[cryptos[3]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[3]}')
    elif call.data == ("e"+cryptos[4]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto.", reply_markup=gen_earning(0))
        crypto = c23[cryptos[4]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[4]}')
    elif call.data == ("e"+cryptos[5]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto.", reply_markup=gen_earning(0))
        crypto = c23[cryptos[5]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[5]}')
    elif call.data == ("e"+cryptos[6]):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Please choose a crypto.", reply_markup=gen_earning(0))
        crypto = c23[cryptos[6]]
        user = User.find_one({"chat_id": call.message.chat.id})
        earned = 0
        if user != None:
            earned = user[crypto]
        bot.send_message(call.message.chat.id, f'You earned {earned}$ over {cryptos[6]}')
    elif call.data.split(':')[0] == "ic_no":
        print("No")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Do you agree to invest {call.data.split(":")[1]}$ {cryptos[int(call.data.split(":")[2])]} to this platform?', reply_markup=gen_wallet(call.data.split(':')[1], call.data.split(':')[2], "", 0))
        bot.send_message(call.message.chat.id, text="Investment Canceled!\n\n/start command for menu!")
    elif call.data.split(':')[0] == "ic_yes":
        print("Yes")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Do you agree to invest {call.data.split(":")[1]}$ {cryptos[int(call.data.split(":")[2])]} to this platform?', reply_markup=gen_wallet(call.data.split(':')[1], call.data.split(':')[2], "", 0))
        sent_message = None
        if call.data.split(":")[3] == 'aless000000' or call.data.split(":")[3] == 'fly15support' :
            sent_message = bot.send_message(call.message.chat.id, text=f'Please deposit to the following address:\n\n{wallet[int(call.data.split(":")[2])]}\n\nOnce you deposit, input your transaction hash to finish your investment')
        else:
            sent_message = bot.send_message(call.message.chat.id, text=f'Please deposit to the following address:\n\n{kwallet[int(call.data.split(":")[2])]}\n\nOnce you deposit, input your transaction hash to finish your investment')
        bot.register_next_step_handler(call.message, finishTransaction, call.data.split(':')[1], call.data.split(':')[2], sent_message.message_id)
    elif call.data.split(':')[0] == "wc_no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Are you sure to withdraw {call.data.split(":")[3]}$ to follwing address?\n\n{call.data.split(":")[4]}', reply_markup=gen_withdraw_confirm("1", 2, 3, "4", 0))
        bot.send_message(call.message.chat.id, "Withdraw canceled\n\n/start command for menu.")
    elif call.data.split(':')[0] == "wc_yes":
        print(array[1], cryptos[int(array[2])], array[3], array[4])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Are you sure to withdraw {call.data.split(":")[3]}$ to follwing address?\n\n{call.data.split(":")[4]}', reply_markup=gen_withdraw_confirm("1", 2, 3, "4", 0))
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
#5939115860


@bot.message_handler(commands=['start'])
def message_handler(message):
    print(message.chat.id, message.from_user.username, message.from_user.id)
    bot.send_message(message.chat.id, "What would you like to do?", reply_markup=gen_menu())

def getBudget(message, crypto):
    if message.text == "/start":
        bot.send_message(message.chat.id, "What would you like to do?", reply_markup=gen_menu())
        return
    try:
        budget = float(message.text)
        print(message.text + "$")
        bot.send_message(message.chat.id, f'Do you agree to invest {budget}$ {cryptos[crypto]} to this platform?', reply_markup=gen_wallet(budget, crypto, message.from_user.username))
    except ValueError:
        bot.send_message(message.chat.id, "Input valid number!")
        bot.register_next_step_handler(message, getBudget, crypto)

def finishTransaction(message, budget, crypto, message_id):
    print(message.text)
    if message.text == "/start":
        bot.send_message(message.chat.id, "What would you like to do?", reply_markup=gen_menu())
        return
    bot.send_message(message.chat.id, text="Thanks for your investment!!!\n\nYour submission is pending and will be confirmed and accepted soon!\n\n/start command for menu!")
    if message.from_user.username != 'aless000000' and message.from_user.username != 'fly15support':
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text=f'Please deposit to the following address:\n\n{wallet[int(crypto)]}\n\nOnce you deposit, input your transaction hash to finish your investment')
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
    if message.text == "/start":
        bot.send_message(message.chat.id, "What would you like to do?", reply_markup=gen_menu())
        return
    try:
        withdraw = float(message.text)
        if withdraw > limit:
            bot.send_message(message.chat.id, f'You can withdraw at most {limit}$.\n\nPlease input valid price!')
            bot.register_next_step_handler(message, withdrawBudget, crypto, limit)
        else:
            bot.send_message(message.chat.id, f'Please input your {cryptos[crypto]} address to withdraw')
            bot.register_next_step_handler(message, confirmWithdraw, crypto, withdraw)
    except ValueError:
        bot.send_message(message.chat.id, "Input only number")
        bot.register_next_step_handler(message, withdrawBudget, crypto, limit)

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
    

