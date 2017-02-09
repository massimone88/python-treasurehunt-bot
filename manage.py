__author__ = 'massimone88'
import telegram
from telegram.ext import Updater, CommandHandler
from EventHandler import EventHandler
from MessageSender import MessageSender
from SenderFilterService import SenderFilterService
import sys
import time
import logging
import json
from telegram.ext import MessageHandler, Filters
from StateManager import *

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
    all_handler = MessageHandler(Filters.all, event_handler.handle_all)
    dispatcher.add_handler(all_handler)
    print 'waiting new messages...'
    updater.start_polling()

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)