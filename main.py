from env import tg_token

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from random import randint
from telegram.ext import MessageFilter

class FilterHashtag(MessageFilter):
    def filter(self, message):
        return message.text.startswith("#protip")

def hello(update: Update, context: CallbackContext):
    update.message.reply_text(f"Hello {update.effective_user.first_name}")
    
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    
def protip(update: Update, context:CallbackContext):
    file = open("protips.txt", "r")
    protips = []
    for line in file:
        protips.append(line)
    if len(protips) > 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=protips[randint(0,len(protips)-1)])
    file.close()
    
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
    
def printMessage(update: Update, context: CallbackContext):
    text = update.message.text
    print(text)
    
def main():
    print("Main function started")
    # Remember to initialize the class.
    filter_hashtag = FilterHashtag()
    
    updater = Updater(tg_token)
    updater.dispatcher.add_handler(CommandHandler("hello", hello))
    
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)
    
    protip_handler = CommandHandler('protip', protip)
    updater.dispatcher.add_handler(protip_handler)
    
    protipAddHandler = MessageHandler(Filters.text & filter_hashtag, protipAdd)
    updater.dispatcher.add_handler(protipAddHandler)
    
    genMessageHandler = MessageHandler(Filters.text, printMessage)
    updater.dispatcher.add_handler(genMessageHandler)

    updater.start_polling()
    updater.idle()

main()