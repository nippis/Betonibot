from env import tg_token

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from random import randint
from time import sleep

from filters import FilterHashtag, FilterCalculation
from calculator import calculator

messageQueue = []
    
def protip(update: Update, context:CallbackContext):
    try:
        file = open("protips.txt", "r")
        protips = []
        for line in file:
            protips.append(line)
        if len(protips) > 0:
            message = protips[randint(0,len(protips)-1)]
            message = message.replace("\n", "")
            print("Message size is:", len(message.encode('utf-8')))
            messageQueue.append((context, update.effective_chat.id, message))
            print("Message sent:", message)
        file.close()
    except:
        pass
    
def protipAdd(update: Update, context: CallbackContext):
    try:
        print("Adding protip")
        file = open("protips.txt", "a")
        text = update.message.text
        text = text.replace("#protip", "")
        text = text.replace("\n", "")
        text = text.strip()
        if not text.endswith("."):
            text = text + "."
        if not text[0].isupper():
            text = text.capitalize()
        text = text+"\n"
        if len(text) < 3:
            return
        file.write(text)
        file.close()
        print("Protip added")
        text = text.replace("\n", "")
        messageQueue.append((context, update.effective_chat.id, f'Protip "{text}" lisätty listalle.'))
    except:
        pass

def calculate(update: Update, context: CallbackContext):
    try:
        calcInput = update.message.text
        result = str(calculator(calcInput))
        print(result)
        print("Pituus:", len(str(result)))
        if len(str(result)) > 0:
            messageQueue.append((context, update.effective_chat.id, result))
    except:
        pass
        
def main():
    print("Main function started")
    # Remember to initialize the class.
    filter_hashtag = FilterHashtag()
    filter_calc = FilterCalculation()

    updater = Updater(tg_token)

    protipHandler = CommandHandler('protip', protip)
    updater.dispatcher.add_handler(protipHandler)
    
    protipAddHandler = MessageHandler(Filters.text & filter_hashtag, protipAdd)
    updater.dispatcher.add_handler(protipAddHandler)

    plus = r'^=\s*[0-9]+\s*\+\s*[0-9]+'
    minus = r'^=\s*[0-9]+\s*-\s*[0-9]+'
    mult = r'^=\s*[0-9]+\s*\*\s*[0-9]+'
    div = r'^=\s*[0-9]+\s*/\s*[0-9]+'
    calcHandler = MessageHandler(Filters.text & (Filters.regex(plus) | Filters.regex(minus) | Filters.regex(mult) | Filters.regex(div)), calculate)
    updater.dispatcher.add_handler(calcHandler)
    
    updater.start_polling(drop_pending_updates=True, bootstrap_retries=0)

    while True:
        if len(messageQueue) > 0:
            message = messageQueue.pop(0)
            message[0].bot.send_message(message[1], message[2])
            sleep(9)
        sleep(1)

main()
