__author__ = 'massimone88'

class UserNotAuthorizedException:
    def __init__(self, sender_id):
        self.sender_id = sender_id

    def get_sender_id(self):
        return self.sender_id
