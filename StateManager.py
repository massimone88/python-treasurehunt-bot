__author__ = 'massimone88'
import logging
import time
from State import *

class StateManager:

    def __init__(self, message_sender, chat_id, config):
        self.logger = logging.getLogger()
        self.logger.debug("init State Manager")
        self.chat_id = chat_id
        self.config = config
        self._states = []
        self._create_states(config["states"])
        self._current_state = None
        self._current_state_index = 0
        self.message_sender = message_sender
        self._init_game()

    def is_ready(self):
        return self.ready

    def _init_game(self):
        self.ready = False
        help_button = telegram.KeyboardButton(text="Start the game")
        custom_keyboard = [[help_button]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        self.send_keyboard(text=self.config["start_game_msg"], reply_markup=reply_markup)

    def _create_states(self, state_dicts):
        for state_config in state_dicts:
            state = TreasureHuntState(self, state_config)
            self._states.append(state)

    def text_handler(self, chat_id, msg):
        if msg == "Start the game":
            self.ready = True
            self.send_keyboard(text="Ok", reply_markup=telegram.ReplyKeyboardRemove())
            self.next_state()
        if self.is_ready() and chat_id == self.chat_id and self._current_state.text_enabled:
            self._current_state.text_handler(msg)

    def help_handler(self, chat_id):
        if self.is_ready() and chat_id == self.chat_id:
            self._current_state.help_handler()

    def location_handler(self, chat_id, location):
        if self.is_ready() and chat_id == self.chat_id and self._current_state.position_enabled:
            self._current_state.location_handler(location)

    def send_text(self, text):
        self.message_sender.sendMessage(chat_id=self.chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

    def send_keyboard(self, text, reply_markup):
        self.message_sender.sendMessage(chat_id=self.chat_id, text=text, reply_markup=reply_markup)

    def next_state(self):
        if self._current_state:
            self._current_state.on_exit()
            self._current_state_index += 1
        else:
            self._current_state_index = 0
        if self._current_state_index < len(self._states):
            self._current_state = self._states[self._current_state_index]
            self._current_state.on_enter()
        else:
            self.send_text(self.config["finish_game_msg"])
