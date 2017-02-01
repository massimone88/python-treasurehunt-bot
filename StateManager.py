import logging
from State import *
__author__ = 'stefano'

class StateManager:

    def __init__(self, bot, chat_id, config):
        self.logger = logging.getLogger()
        self.logger.debug("init State Manager")
        self.chat_id = chat_id
        self.config = config
        self._states = []
        self._create_states(config["states"])
        self._current_state = None
        self._current_state_index = 0
        self.bot = bot
        self.send_text(config["start_game_msg"])
        self.next_state()

    def _create_states(self, state_dicts):
        for state_config in state_dicts:
            state = TreasureHuntState(self, state_config)
            self._states.append(state)

    def text_handler(self, bot, update):
        chat_id = update.message.chat_id
        if chat_id == self.chat_id and self._current_state.enable_text:
            self._current_state.text_handler(bot, update)

    def send_text(self, text):
        self.bot.sendMessage(chat_id=self.chat_id, text=text)

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
