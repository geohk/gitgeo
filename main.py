import configparser
import logging
from pymongo import MongoClient

import telegram
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters

client = MongoClient('mongodb://fb-g:jtZKATQ7MbXuUKsK@cluster0.sudtx.mongodb.net/')
# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))
db=client.hongkong

fbid = db.fb.find({'mobile': 85295298869})
logger.info(fbid)
for doc in fbid:
    print(doc)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


def reply_handler(update, context):
    """Reply message."""
    context.bot.sendMessage(chat_id=update.message.chat_id,text=update.message.text)


# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)