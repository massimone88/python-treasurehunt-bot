# Python Threasure Hung Bot

A treasure hunt telegram bot written in python

![Image of Yaktocat](https://github.com/massimone88/python-treasurehunt-bot/blob/master/image.png)


# Instructions

## 1. Install dependencies.
Install python requirements using **pip**: `pip install -r requirements.txt`.

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
    "authorized_users": {
      "type": "array",
      "items": {
        "type": "integer"
      }
    },
    "logging_user": {
      "type": "integer"
    },
    "unauthorized_user_msg": {
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
          "type": {
            "type": "string",
            "oneOf": [
                "position",
                "text"
            ]
          },
          "init_msg": {
            "type": "string"
          },
          "help_msg": {
            "type": "string"
          },
          "target_position": {
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "max_distance": {
            "type": "integer"
          },
          "wrong_position_reply": {
            "type": "string"
          },
          "question": {
            "type": "string"
          },
          "answer": {
            "type": "string"
          },
          "wrong_answer_reply: {
            "type": "string"
          },
          "on_exit_reply": {
            "type": "string"
          }
        },
        "required": [
          "type",
          "init_msg",
          "help_msg",
          "target_position", "max_distance", "wrong_position_reply", (for states with type "position")
          "question, "answer, "wrong_answer_reply (for state with type "text")
          "on_exit_reply"
        ]
      }
    }
  },
  "required": [
    "TOKEN_BOT",
    "authorized_users",
    "logging_user",
    "unauthorized_user_msg",
    "start_game_msg",
    "finish_game_msg",
    "states"
  ]
}
```

Here an example:
```
{
  "TOKEN_BOT": "token",
  "authorized_users": [12345678, 87654321],
  "logging_user":12345679,
  "unauthorized_user_msg": "Im'sorry but you can't use this bot!",
  "start_game_msg": "Hi! Welcome to treasure hunt bot. Start the game!",
  "finish_game_msg": "Great! you finish the game!",
  "states": [
    {
      "type": "position",
      "init_msg": "Go to Time Square to continue the game",
      "help_msg": "Go to New York first and you're near enough to go to Time Square :)",
      "target_position": [40.758895,-73.98513100000002],
      "max_distance": 100,
      "wrong_position_reply": "You are %d meters to the target position",
      "on_exit_reply": "Great go to the next step"
    },
    {
      "type":"text",
      "init_msg": "Here your question",
      "help_msg": "If you ask an help you're not so smart :)",
      "question": "What color was Napoleon's white horse?",
      "answer": "white",
      "on_exit_reply": "",
      "wrong_answer_reply": "Come on! Who doesn't known Napoleon's white horse?"
    },
    ...
  ]
}
```

## Deploy to Heroku
This repo has all requested files to deploy the application on Heroku!
