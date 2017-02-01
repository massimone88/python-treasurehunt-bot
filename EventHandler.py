__author__ = 'stefano'
from UserNotAuthorizedException import UserNotAuthorizedException
from StateManager import StateManager

class EventHandler:

    def __init__(self, SenderFilterService, MessageSender, config):
        self.sender_filter_service = SenderFilterService
        self.message_sender = MessageSender
        self.config = config
        self._users_id = {}

    def handle_all(self, bot, update):
        try:
            message = update.message.text
            user_id = self.sender_filter_service.filter_sender(update)
            if user_id not in self._users_id.keys() or message == "/start":
                state_manager = StateManager(bot, user_id, self.config)
                self._users_id[user_id] = state_manager
            else:
                state_manager = self._users_id[user_id]
                state_manager.text_handler(bot, update)
            #self.message_sender.send_msg(update.message.chat_id, 'Custom keyboard with various buttons')
        except UserNotAuthorizedException as e:
            sender_id = e.get_sender_id()
            self.message_sender.send_authorized_user_message(sender_id)