__author__ = 'massimone88'

import asyncio

import telegram
from telegram.ext import Updater, CommandHandler, ApplicationBuilder
from EventHandler import EventHandler
from MessageSender import MessageSender
from SenderFilterService import SenderFilterService
import sys
import time
import logging
import json
from telegram.ext import MessageHandler, filters
from StateManager import *

def main_loop():
    json_data = open("config.json").read()
    config = json.loads(json_data)
    application = ApplicationBuilder().token(config["TOKEN_BOT"]).build()
    logging_user = config['logging_user'] if 'logging_user' in config.keys() else None
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    sender_filter = SenderFilterService(config)
    message_sender = MessageSender(application.bot, config, logging_user=logging_user)
    event_handler = EventHandler(sender_filter, message_sender, config, logging_user=logging_user)
    all_handler = MessageHandler(None, event_handler.handle_all)
    application.add_handler(all_handler)
    print('waiting new messages...');
    application.run_polling();


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
