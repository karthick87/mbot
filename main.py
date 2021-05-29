#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os
from time import time
from src.entry import entry
import json

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

try:
    BOT_TOKEN = os.environ["BOT_TOKEN"]
except KeyError:
    logging.error("Bot credentials not found in environment")

# How long the container exist
LIFESPAN = 7200


def main():
    """Run the bot."""

    try:
        update_id = int(os.environ["UPDATE_ID"])
    except:
        update_id = 0

    start_time = int(time())

    bot = telegram.Bot(BOT_TOKEN)

    while True:
        try:
            for update in bot.get_updates(offset=update_id, timeout=10):
                update_id = update.update_id + 1
                logging.info(f"Update ID:{update_id}")
                entry(bot, update)
        except NetworkError as e:
            print("Network Error")
            print(e)
            sleep(1)
        except Unauthorized:
            print("Unauthorized")
            # The user has removed or blocked the bot.
            update_id += 1
        # except Exception as e:
        #     logging.error("Generic Error")
        #     logging.error(e)
        #     sleep(5)
        if int(time()) - start_time > LIFESPAN:
            logging.info("Enough for the day! Passing on to next Meeseek")
            with open("/tmp/update_id", "w") as the_file:
                the_file.write(str(update_id))
            break


if __name__ == "__main__":
    main()
