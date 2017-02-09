__author__ = 'massimone88'

import telegram

class MessageSender:
    def __init__(self, bot, config, logging_user=None):
        self.bot = bot
        self.logging_user = logging_user
        self.config = config

    def sendMessage(self, chat_id, text, **kwargs):
        self.bot.sendMessage(chat_id=chat_id, text=text, **kwargs)
        if self.logging_user and text and chat_id != self.logging_user:
            text_backup = "To %s\n" % str(chat_id)
            text_backup += text
            self.bot.sendMessage(chat_id=self.logging_user, text=text_backup)

    def sendChatAction(self, chat_id, action):
        self.bot.sendChatAction(chat_id,action)

    def sendLocation(self, chat_id, latitude, longitude, **kwargs):
        self.bot.sendLocation(chat_id=chat_id, latitude=latitude, longitude=longitude, **kwargs)

    def send_unauthorized_user_message(self, sender_id):
        if 'unauthorized_user_msg' in self.config.keys():
            self.sendMessage(sender_id, self.config['unauthorized_user_msg'])