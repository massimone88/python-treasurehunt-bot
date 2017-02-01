__author__ = 'stefano'
from UserNotAuthorizedException import *


class SenderFilterService:

    def __init__(self):
        self.authorized_users = []
        for line in open("known_users.txt"):
            li = line.strip()
            if not li.startswith("#"):
                user_id = int(line.rstrip())
                self.authorized_users.append(user_id)

    def filter_sender(self, update):
        sender_id = update.message.chat_id
        print 'sender %d' % sender_id
        found = False
        if sender_id in self.authorized_users:
            found = True
        if not found:
            raise UserNotAuthorizedException(sender_id)
        return sender_id
