__author__ = 'stefano'
class MessageSender:
    def __init__(self, bot):
        self.bot = bot

    def send_msg(self, to_id, text):
        self.bot.sendMessage(chat_id=to_id, text=text)

    def send_authorized_user_message(self, sender_id):
        self.send_msg(sender_id, 'Mi dispiace ma non sei abilitato a interagire con questo Bot!')