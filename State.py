__author__ = 'stefano'
class TreasureHuntState:
    def __init__(self, state_manager, config):
        self._state_manager = state_manager
        self.init_msg = config["init_msg"]
        self.help_msg = config["help_msg"]
        self.enabled_position = config["position_enabled"]
        if self.enabled_position:
            self.target_position = config["target_position"]
        self.enable_text = config["enable_text"]
        if self.enable_text:
            self.correct_answer = config["answer"]
            self.question = config["question"]
            self.wrong_answer_reply = config["wrong_answer_reply"]
            self.right_answer_reply = config["right_answer_reply"]

    def is_text_dispatcher_enabled(self):
        return self.enable_text

    def on_enter(self):
        self._state_manager.send_text(self.init_msg)

    def text_handler(self, bot, update):
        msg = update.message.text
        if msg == self.correct_answer:
            self._state_manager.next_state()
        else:
            self._state_manager.send_text(self.wrong_answer_reply)


    def on_exit(self):
        pass