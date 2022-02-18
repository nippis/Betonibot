from env import tg_token

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from random import randint
from telegram.ext import MessageFilter
from time import sleep

class FilterHashtag(MessageFilter):
    def filter(self, message):
        return message.text.startswith("#protip")
    
def protip(update: Update, context:CallbackContext):
    file = open("protips.txt", "r")
    protips = []
    for line in file:
        protips.append(line)
    if len(protips) > 0:
        message = protips[randint(0,len(protips)-1)]
        message = message.replace("\n", "")
        print("Message size is:", len(message.encode('utf-8')))
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        print("Message sent:", message)
    file.close()
    sleep(4)
    
def protipAdd(update: Update, context: CallbackContext):
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
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Protip "{text}" lisätty listalle.')
    sleep(4)
        
def main():
    print("Main function started")
    # Remember to initialize the class.
    filter_hashtag = FilterHashtag()
    
    updater = Updater(tg_token)

    protipHandler = CommandHandler('protip', protip)
    updater.dispatcher.add_handler(protipHandler)
    
    protipAddHandler = MessageHandler(Filters.text & filter_hashtag, protipAdd)
    updater.dispatcher.add_handler(protipAddHandler)
    
    updater.start_polling(drop_pending_updates=True, bootstrap_retries=0)

main()
