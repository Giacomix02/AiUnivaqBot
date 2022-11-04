#!/usr/bin/env python

# venv\Scripts\activate to activate the virtual environment

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from textgenrnn import textgenrnn 
import random

# insert textgenrnn code into the directory

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(update, context):
  """Log Errors caused by Updates."""
  logger.warning('Update "%s" caused error "%s"', update, context.error)

def print_out(out,update,context):
    print(out)
    update.message.reply_text(out[0])


def AINoText(update, context):

  up = update 
  cont = context

  messaggio = update.message.text.lower()
  rand = random.randint(0, 12)

  print("________________")
  print(messaggio)
  print(rand)
  print("________________")


  textgen = textgenrnn( weights_path='UnivaqBot_weights.hdf5',
                        vocab_path='UnivaqBot_vocab.json',
                        config_path='UnivaqBot_config.json')




  if(messaggio.count("banal") > 0):
    print("****** banale detected ******")
    if(random.randint(0, 1)==1):
      out = textgen.generate(1, prefix=messaggio,temperature=0.1,return_as_list=True)
      if(out!=messaggio): print_out(out,up,cont)
  elif(messaggio.count("trivial") > 0):
    print("****** triviale detected ******")
    if(random.randint(0, 1)==1):
      out = textgen.generate(1, prefix=messaggio,temperature=0.1,return_as_list=True)
      if(out!=messaggio): print_out(out,up,cont)
  elif(messaggio.count("palese") > 0):
    print("****** palese detected ******")
    if(random.randint(0, 1)==1):
      out = textgen.generate(1, prefix=messaggio,temperature=0.1,return_as_list=True)
      if(out!=messaggio): print_out(out,up,cont)
  elif (rand > 9):
    print("****** vado di numero random ******")
    if(len(messaggio)<20):
      out = textgen.generate(1, prefix=messaggio, temperature=0.5,return_as_list=True)        #decide il bot
      print_out(out,up,cont)
    else:
      out = textgen.generate(1, temperature=1.0,return_as_list=True)        #decide il bot
      print_out(out,up,cont)
  elif(messaggio.count("@AiUnivaqBot")):
      print("****** SONO STATO CHIAMOATO??? ******")
      temp = messaggio
      temp.replace('@AiUnivaqBot','')
      if(temp==''):
        out = textgen.generate(1, temperature=1.0,return_as_list=True)        #decide il bot
        print_out(out,up,cont)
      else:
        out = textgen.generate(1, prefix=temp, temperature=1.0,return_as_list=True)        #decide il bot
        print_out(out,up,cont)



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
