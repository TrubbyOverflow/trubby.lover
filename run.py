import os
import random
import logging
import yaml
import jellyfish

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Enable logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Get text data
with open('data.yml', 'r') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


# Prepare the available bot commands on Telegram:
### random - let me surprise you a bit
### good_day - have a good day, sir
### good_afternoon - oh, my, good afternoon
### good_night - nite-nite
### goodbye - don't come back
### failure - you suck
### help_out - such generosity
### success - you don't deserve it
### date_help - let's move out!
def random_cmd(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(data['random'])['text'])

def good_day_cmd(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(data['good_day'])['text'])

def good_afternoon_cmd(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(data['good_afternoon'])['text'])

def good_night_cmd(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(data['good_night'])['text'])

def goodbye_cmd(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(data['goodbye'])['text'])

def failure_cmd(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(data['failure'])['text'])

def help_out_cmd(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(data['help_out'])['text'])

def success_cmd(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(data['success'])['text'])

def date_help_cmd(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(data['date_help'])['text'])


def smart_response(update, context):
    def get_closest_string(message):
        closest_string = {
            'text': data['random'][0]['text'],
            'distance': 999999,
        }
        for response in data['random']:
            distance = jellyfish.damerau_levenshtein_distance(response['text'], message)
            if distance < closest_string['distance']:
                closest_string['text'] = response['text']
                closest_string['distance'] = distance
        return closest_string['text']

    context.bot.send_message(chat_id=update.effective_chat.id, text=get_closest_string(update.message.text))


# Connect to Telegram and start all handlers
updater = Updater(token=os.environ.get('TELEGRAM_ACCESS_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

random_handler = CommandHandler('random', random_cmd)
dispatcher.add_handler(random_handler)

good_day_handler = CommandHandler('good_day', good_day_cmd)
dispatcher.add_handler(good_day_handler)

good_afternoon_handler = CommandHandler('good_afternoon', good_afternoon_cmd)
dispatcher.add_handler(good_afternoon_handler)

good_night_handler = CommandHandler('good_night', good_night_cmd)
dispatcher.add_handler(good_night_handler)

goodbye_handler = CommandHandler('goodbye', goodbye_cmd)
dispatcher.add_handler(goodbye_handler)

failure_handler = CommandHandler('failure', failure_cmd)
dispatcher.add_handler(failure_handler)

help_out_handler = CommandHandler('help_out', help_out_cmd)
dispatcher.add_handler(help_out_handler)

success_handler = CommandHandler('success', success_cmd)
dispatcher.add_handler(success_handler)

date_help_handler = CommandHandler('date_help', date_help_cmd)
dispatcher.add_handler(date_help_handler)

smart_response_handler = MessageHandler(Filters.text & (~Filters.command), smart_response)
dispatcher.add_handler(smart_response_handler)

updater.start_polling()
