__author__ = 'massimone88'
import logging
from UserNotAuthorizedException import UserNotAuthorizedException
from StateManager import StateManager

class EventHandler:

    def __init__(self, SenderFilterService, MessageSender, config, logging_user=None):
        self.sender_filter_service = SenderFilterService
        self.message_sender = MessageSender
        self.config = config
        self._users_id = {}
        self.logger = logging.getLogger()
        self.logging_user = logging_user

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
                text_backup = "From %s\n" % str(user_id)
                text_backup += message
                if self.logging_user:
                    self.message_sender.sendMessage(chat_id=self.logging_user, text=text_backup)
                if message == "/start":
                    self.logger.debug("it's a start command! ")
                    state_manager = self._init_state_manager(bot, user_id)
                elif message == "Help me!":
                    state_manager.help_handler(user_id)
                else:
                    state_manager.text_handler(user_id, message)
            elif location:
                self.logger.debug("it's a location!")
                state_manager.location_handler(user_id, location)
        except UserNotAuthorizedException as e:
            sender_id = e.get_sender_id()
            if sender_id != self.logging_user:
                self.message_sender.send_authorized_user_message(sender_id)
            else:
                for user_id in self._users_id.keys():
                    self.message_sender.send_msg(user_id, update.message.text)
        finally:
            self.init = False

    def _init_state_manager(self, bot, user_id):
        self.logger.debug("create state Manager for user %d" % user_id)
        state_manager = StateManager(self.message_sender, user_id, self.config)
        self._users_id[user_id] = state_manager
        return state_manager
