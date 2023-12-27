__author__ = 'massimone88'
import time
from State import *

class StateManager:

    def __init__(self, message_sender, chat_id, config):
        self.logger = logging.getLogger()
        self.logger.debug("init State Manager")
        self.chat_id = chat_id
        self.config = config
        self._states = []
        self._create_states(config["states"], config)
        self._current_state = None
        self._current_state_index = 0
        self.message_sender = message_sender

    def is_ready(self):
        return self.ready

    async def init_game(self):
        self.ready = False
        help_button = telegram.KeyboardButton(text=self.config['start_game_button'])
        custom_keyboard = [[help_button]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        await self.send_keyboard(text=self.config["start_game_msg"], reply_markup=reply_markup)

    def _create_states(self, state_dicts, global_config):
        for state_config in state_dicts:
            state = TreasureHuntState(self, state_config, global_config)
            self._states.append(state)

    async def text_handler(self, chat_id, msg):
        if msg == self.config['start_game_button'] and self._current_state is None:
            self.ready = True
            await self.send_keyboard(text="Ok", reply_markup=telegram.ReplyKeyboardRemove())
            await self.next_state()
        elif self.is_ready() and chat_id == self.chat_id and self._current_state.text_enabled:
            await self._current_state.text_handler(msg)

    async def help_handler(self, chat_id):
        if self.is_ready() and chat_id == self.chat_id:
            await self._current_state.help_handler()

    async def location_handler(self, chat_id, location):
        if self.is_ready() and chat_id == self.chat_id and self._current_state.position_enabled:
            await self._current_state.location_handler(location)

    async def qrcode_handler(self, chat_id):
        if self.is_ready() and chat_id == self.chat_id and self._current_state.qrcode_enabled:
            await self._current_state.qrcode_handler()

    async def send_text(self, text):
        await self.message_sender.sendMessage(chat_id=self.chat_id, text=text, parse_mode=telegram.constants.ParseMode.MARKDOWN)

    async def send_keyboard(self, text, reply_markup):
        await self.message_sender.sendMessage(chat_id=self.chat_id, text=text, reply_markup=reply_markup)

    async def next_state(self):
        if self._current_state:
            await self._current_state.on_exit()
            self._current_state_index += 1
        else:
            self._current_state_index = 0
        await self.message_sender.sendChatAction(chat_id=self.chat_id, action=telegram.constants.ChatAction.TYPING)
        time.sleep(0.5)
        if self._current_state_index < len(self._states):
            self._current_state = self._states[self._current_state_index]
            await self._current_state.on_enter()
        else:
            await self.send_text(self.config["finish_game_msg"])

    def get_current_state_index(self):
        return self._current_state_index