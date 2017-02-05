import logging

__author__ = 'massimone88'
from UserNotAuthorizedException import UserNotAuthorizedException
from StateManager import StateManager

class EventHandler:

    def __init__(self, SenderFilterService, MessageSender, config):
        self.sender_filter_service = SenderFilterService
        self.message_sender = MessageSender
        self.config = config
        self._users_id = {}
        self.logger = logging.getLogger()

    def handle_all(self, bot, update):
        self.logger.debug("received something!")
        try:
            message = update.message.text
            location = update.message.location
            self.logger.debug("check if sender is authorized...")
            user_id = self.sender_filter_service.filter_sender(update)
            self.logger.debug("authorized!")
            if user_id not in self._users_id.keys():
                state_manager = self._init_state_manager(bot, user_id)
            else:
                state_manager = self._users_id[user_id]
            if message:
                self.logger.debug("it's a text message!")
                if message == "/start":
                    self.logger.debug("it's a start command! ")
                    state_manager = self._init_state_manager(bot, user_id)
                elif message == "Aiuto!":
                    state_manager.help_handler(user_id)
                else:
                    state_manager.text_handler(user_id, message)
            elif location:
                self.logger.debug("it's a location!")
                state_manager.location_handler(user_id, location)
        except UserNotAuthorizedException as e:
            sender_id = e.get_sender_id()
            self.message_sender.send_authorized_user_message(sender_id)
        finally:
            self.init = False

    def _init_state_manager(self, bot, user_id):
        self.logger.debug("create state Manager for user %d" % user_id)
        state_manager = StateManager(bot, user_id, self.config)
        self._users_id[user_id] = state_manager
        return state_manager
