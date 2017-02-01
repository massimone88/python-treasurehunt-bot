from EventHandler import EventHandler
from MessageSender import MessageSender
from SenderFilterService import SenderFilterService
import telegram
from telegram.ext import Updater, CommandHandler

__author__ = 'stefano'
import sys
import time
import logging
import json
from telegram.ext import MessageHandler, Filters
from StateManager import *

# funzione che viene eseguita ad ogni messaggio ricevuto
def handle(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    print content_type, chat_type, chat_id, message


def main_loop():
    json_data = open("config.json").read()
    config = json.loads(json_data)
    bot = telegram.Bot(token=config["TOKEN_BOT"])
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    sender_filter = SenderFilterService()
    message_sender = MessageSender(bot)
    event_handler = EventHandler(sender_filter, message_sender, config)
    echo_handler = MessageHandler(Filters.all, event_handler.handle_all)
    dispatcher.add_handler(echo_handler)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    print 'In attesa di nuovi messaggi...'
    updater.start_polling()

def start(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Ciao! sono un diagramma a stati! provami!")

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)