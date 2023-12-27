__author__ = 'massimone88'
import logging
import telegram
from Util import ThreasureHuntUtil
from pyzbar.pyzbar import decode

# System libraries
import os
from os import listdir
from os.path import isfile, join

from io import BytesIO
from PIL import Image

class TreasureHuntState:
    def __init__(self, state_manager, config, global_config):
        self.logger = logging.getLogger()
        self._state_manager = state_manager
        self.init_msg = config["init_msg"]
        self.help_msg = config["help_msg"]
        self.position_enabled = config["type"] == "position"
        self.qrcode_enabled = config["type"] == "qrcode"
        self.repeat_question_button = global_config["repeat_question_button"]
        if self.position_enabled:
            self.target_position = config["target_position"]
            self.wrong_position_reply = config["wrong_position_reply"]
            self.max_distance = config["max_distance"]
        self.text_enabled = config["type"] == "text" or config["type"] == "qrcode"
        if self.text_enabled or self.qrcode_enabled:
            self.init_msg = config["init_msg"]
            self.correct_answer = config["answer"]
            self.question = config["question"]
            self.wrong_answer_reply = config["wrong_answer_reply"]
        if "on_exit_reply" in config.keys():
            self.on_exit_reply = config["on_exit_reply"]
        else:
            self.on_exit_reply = None

    def is_text_dispatcher_enabled(self):
        return self.text_enabled

    async def on_enter(self):
        if self.position_enabled:
            await self._state_manager.send_text(self.init_msg)
            location_button = telegram.KeyboardButton(text="Send the position", request_location=True)
            help_button = telegram.KeyboardButton(text="Help me!")
            custom_keyboard = [[location_button, help_button]]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            await self._state_manager.send_keyboard(text="Can you send me the position when you're arrived?",
                     reply_markup=reply_markup)
        elif self.text_enabled:
            if self.init_msg:
                await self._state_manager.send_text(self.init_msg)
            repeat_question = telegram.KeyboardButton(text=self.repeat_question_button)
            help_button = telegram.KeyboardButton(text="Help me!")
            custom_keyboard = [[repeat_question]]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            await self._state_manager.send_keyboard(self.question, reply_markup=reply_markup)

    async def text_handler(self, msg):
        self.logger.debug("check if answer is correct..")
        if msg == self.repeat_question_button:
            await self._state_manager.send_text(self.question)
            return
        if msg.lower() == self.correct_answer.lower():
            self.logger.debug("Yes! go to next state!")
            await self._state_manager.next_state()
        else:
            self.logger.debug("Yes! no send wrong_answer_reply!")
            help_button = telegram.KeyboardButton(text="Help me!")
            repeat_question = telegram.KeyboardButton(text=self.repeat_question_button)
            custom_keyboard = [[help_button, repeat_question]]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            await  self._state_manager.send_keyboard(self.wrong_answer_reply, reply_markup=reply_markup)

    async def help_handler(self):
        self.logger.debug("user ask help")
        if self.help_msg:
            await self._state_manager.send_text(self.help_msg)
        else:
            await self._state_manager.send_text("No help!")

    async def location_handler(self, location):
        loc = (location['latitude'], location['longitude'])
        distance = self.calculate_distance_from_target_position(loc)
        self.logger.debug("distance from target position in meters %d" % distance)
        if distance > self.max_distance:
            self.logger.debug("Too far from target position!")
            await self._state_manager.send_text(self.wrong_position_reply % distance)
        else:
            self.logger.debug("The user is at target position!")
            await self._state_manager.next_state()

    def calculate_distance_from_target_position(self, location):
        distance_km = ThreasureHuntUtil.haversine(location[0], location[1], self.target_position[0],
                                                  self.target_position[1])
        return distance_km * 1000

    async def qrcode_handler(self):
        try:
            result = decode(Image.open('qrcode.png'))
            answer = result[0].data.decode("utf-8")
            await self.text_handler(answer)
            os.remove("qrcode.png")
        except Exception as e:
            await self.text_handler(str(e))


    async def on_exit(self):
        if self.on_exit_reply:
            await self._state_manager.send_keyboard(text=self.on_exit_reply, reply_markup=telegram.ReplyKeyboardRemove())
