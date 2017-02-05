__author__ = 'massimone88'
class MessageSender:
    def __init__(self, bot):
        self.bot = bot

    def send_msg(self, to_id, text):
        self.bot.sendMessage(chat_id=to_id, text=text)

    def send_authorized_user_message(self, sender_id):
        self.send_msg(sender_id, 'I\'m sorry you\'re not authorized to user this bot')