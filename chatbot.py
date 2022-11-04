#!/usr/bin/env python

# venv\Scripts\activate to activate the virtual environment

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# from textgenrnn import textgenrnn 

# insert textgenrnn code into the directory

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(update, context):
  """Log Errors caused by Updates."""
  logger.warning('Update "%s" caused error "%s"', update, context.error)

def AINoText(update, context):
  textgen = textgenrnn( weights_path='UnivaqBot_weights.hdf5',
                        vocab_path='UnivaqBot_vocab.json',
                        config_path='UnivaqBot_config.json')


  message = textgen.generate(1, temperature=1.0,return_as_list=True)        #decide il bot
  print(message)


  update.message.reply_text(message[0])

def start(update, context):
  update.message.reply_text("Ciao, esisto")

def main():

  """Start the bot."""
  f = open("chiave.txt","r")
  chiave = f.read()
  updater = Updater(chiave, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(MessageHandler(None,AINoText))



  # log all errors
  dp.add_error_handler(error)

  # Start the Bot
  updater.start_polling()
  # Run the bot until you press Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT. This should be used most of the time, since
  # start_polling() is non-blocking and will stop the bot gracefully.
  updater.idle()


if __name__ == '__main__':
  main()
