__author__ = 'massimone88'
class MessageSender:
    def __init__(self, bot, logging_user=None):
        self.bot = bot
        self.logging_user = logging_user

    def sendMessage(self, chat_id, text, **kwargs):
        self.bot.sendMessage(chat_id=chat_id, text=text, **kwargs)
        if self.logging_user and text:
            text_backup = "To %s\n" % str(chat_id)
            text_backup += text
            self.bot.sendMessage(chat_id=self.logging_user, text=text_backup)

    def send_authorized_user_message(self, sender_id):
        self.sendMessage(sender_id, 'I\'m sorry you\'re not authorized to user this bot')