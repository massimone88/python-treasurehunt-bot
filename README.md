# Instructions

## 1. know_users files
Create `known_users.txt` file and put in every line the id of users who can communicate with your bot. Lines starting
with `#` will be ignored.

## 2. Config file
Create config files with the following schema
```
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "TOKEN_BOT": {
      "type": "string"
    },
    "start_game_msg": {
      "type": "string"
    },
    "finish_game_msg": {
      "type": "string"
    },
    "states": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "init_msg": {
            "type": "string"
          },
          "help_msg": {
            "type": "string"
          },
          "position_enabled": {
            "type": "boolean"
          },
          "text_enabled": {
            "type": "boolean"
          },
          "question": {
            "type": "string"
          },
          "answer": {
            "type": "string"
          },
          "right_answer_reply": {
            "type": "string"
          },
          "wrong_answer_reply": {
            "type": "string"
          }
        },
        "required": [
          "init_msg",
          "help_msg",
          "position_enabled",
          "text_enabled",
          "question",
          "answer",
          "right_answer_reply",
          "wrong_answer_reply"
        ]
      }
    }
  },
  "required": [
    "TOKEN_BOT",
    "start_game_msg",
    "finish_game_msg",
    "states"
  ]
}
```