__author__ = 'massimone88'
from UserNotAuthorizedException import *

class SenderFilterService:

    def __init__(self, config):
        self.authorized_users = config["authorized_users"]

    def filter_sender(self, update):
        sender_id = update.message.chat_id
        print 'sender %d' % sender_id
        found = False
        if sender_id in self.authorized_users:
            found = True
        if not found:
            raise UserNotAuthorizedException(sender_id)
        return sender_id
