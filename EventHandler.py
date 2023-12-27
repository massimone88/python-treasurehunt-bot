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

    async def handle_all(self, update, context):
        self.logger.debug("received something!")
        try:
            message = update.message.text
            location = update.message.location
            photo = None
            if len(update.message.photo) > 0:
                photo = update.message.photo[-1]
            self.logger.debug("check if sender is authorized...")
            user_id = self.sender_filter_service.filter_sender(update)
            self.logger.debug("authorized!")
            if message and self.logging_user and self.logging_user != user_id:
                    text_backup = "From %s\n" % str(user_id)
                    text_backup += message
                    self.message_sender.sendMessage(chat_id=self.logging_user, text=text_backup)
            if location and self.logging_user and self.logging_user != user_id:
                    text_backup = "From %s" % str(user_id)
                    self.message_sender.sendMessage(chat_id=self.logging_user, text=text_backup)
                    self.message_sender.sendLocation(chat_id=self.logging_user, latitude=location['latitude'],
                                                     longitude=location['longitude'])
            if user_id not in self._users_id.keys():
                state_manager = await self._init_state_manager(context, user_id)
            else:
                state_manager = self._users_id[user_id]
            if message:
                self.logger.debug("it's a text message!")
                text_backup = "From %s\n" % str(user_id)
                text_backup += message
                if self.logging_user and self.logging_user != user_id:
                    self.message_sender.sendMessage(chat_id=self.logging_user, text=text_backup)
                if message == "/start" and state_manager.get_current_state_index() != 0:
                    self.logger.debug("it's a start command! ")
                    state_manager = await self._init_state_manager(context, user_id)
                elif message == "Help me!":
                    await state_manager.help_handler(user_id)
                else:
                    await state_manager.text_handler(user_id, message)
            elif location:
                self.logger.debug("it's a location!")
                await  state_manager.location_handler(user_id, location)
            elif photo:
                self.logger.debug("photo")
                id_img = photo.file_id
                foto = await context.bot.getFile(id_img)
                new_file = await context.bot.get_file(foto.file_id)
                await new_file.download_to_drive('qrcode.png')
                await state_manager.qrcode_handler(user_id)


        except UserNotAuthorizedException as e:
            sender_id = e.get_sender_id()
            if sender_id != self.logging_user:
                await self.message_sender.send_unauthorized_user_message(sender_id)
            else:
                for user_id in self._users_id.keys():
                    await self.message_sender.sendMessage(user_id, update.message.text)
        finally:
            self.init = False

    async def _init_state_manager(self, bot, user_id):
        self.logger.debug("create state Manager for user %d" % user_id)
        state_manager = StateManager(self.message_sender, user_id, self.config)
        await state_manager.init_game()
        self._users_id[user_id] = state_manager
        return state_manager
