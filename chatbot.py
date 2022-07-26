#!/usr/bin/env python

# venv\Scripts\activate to activate the virtual environment

from datetime import datetime
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from textgenrnn import textgenrnn

import markovify
import json

import random
import time

global dateNow 
dateNow = datetime.utcnow()
dateNow = time.mktime(dateNow.timetuple())  # set dell'ora che ha il pc
mute = 0

# insert textgenrnn code into the directory

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  #idk ci deve stare
                    level=logging.INFO)   

logger = logging.getLogger(__name__) #molto probabilmente avvia il bot con il codice a riga 135


def Attiva(update, context):
  global mute
  mute=0
  update.message.reply_text("************* ADESSO POSSO PARLARE *************")
  print("************* ADESSO POSSO PARLARE ************* "+str(mute))

def Disattiva(update,context):
  global mute
  mute=1
  update.message.reply_text("************* ADESSO NON POSSO PARLARE *************")
  print("************* ADESSO NON POSSO PARLARE ************* "+str(mute))
  

def error(update, context):   #funzione che risponde agli errori
  """Log Errors caused by Updates."""
  logger.warning('Update "%s" caused error "%s"', update, context.error)

def print_out(out,update,context):    #funzione che stampa il messaggio su telegram e shell
    print(out[0])
    update.message.reply_text(out[0]) #stampa il messaggio su telegram, out è un array sempre composto da un elemento









def AINoText(update, context):    #funzione che risponde a tutti i messaggi

  global mute
  if(mute==0):
    dateMs = update.message.date
    dateMs = time.mktime(dateMs.timetuple())  # prendo l'ora del messaggio

    print("************* TEMPO DEL MESSAGGIO *************")
    print(dateMs)

    # if date > dateNow continue
    if (dateMs > dateNow):

      up = update   # riga 45 e 46 mi serviranno quando chiamo il print_out
      cont = context

      messaggio = update.message.text.lower() # prendo il messaggio e lo metto in minuscolo
      rand = random.randint(0, 20)            # genero un numero random da 0 a 20 
                                              # serve per decidere se può parlare autonomamento o no

      print("________________")
      print(messaggio)                # debug in shell
      print(rand)
      print("lunghezza: "+str(len(messaggio)))
      print("________________")

      textgen = textgenrnn( weights_path='UnivaqBot_weights.hdf5',      # carico il modello dell'AI
                            vocab_path='UnivaqBot_vocab.json',          # possono essere sostituiti se l'ai viene allenata con altri dati
                            config_path='UnivaqBot_config.json')

      f = open('mydata.json')
      model_json = json.load(f)
      text_model= markovify.Text.from_json(model_json)    # carico il modello markov
      
      
      if(messaggio.count("banal") > 0):           # se il messaggio contiene la parola banal
        print("****** banale detected ******")
        if(random.randint(0, 1)==1):                  # decido se rispondere o no
          out = textgen.generate(1, prefix=messaggio,temperature=0.7,return_as_list=True) # genera il testo tramite AI
          if(out!=messaggio): print_out(out,up,cont)  # se il messaggio non è uguale a quello ricevuto allora lo stampa
      elif(messaggio.count("trivial") > 0):         # se il messaggio contiene la parola trivial
        print("****** triviale detected ******")
        if(random.randint(0, 1)==1):          # decido se rispondere o no 
           update.message.reply_text(text_model.make_sentence_with_start("triviale",strict=False))
      elif(messaggio.count("palese") > 0):          # se il messaggio contiene la parola palese
        print("****** palese detected ******")
        if(random.randint(0, 1)==1):      # decido se rispondere o no
          update.message.reply_text(text_model.make_sentence_with_start("palese",strict=False))
      elif(messaggio.count("@aiunivaqbot")>0):            # il bot viene taggato
          print("****** SONO STATO CHIAMATO??? ******")
          temp = messaggio
          temp = temp.replace("@aiunivaqbot","")        # rimuovo il tag
          temp=temp.lstrip()
          print(temp)
          if(temp==""):                            # se il messaggio dopo il tag è vuoto
            update.message.reply_text(text_model.make_short_sentence(1000))        #decide il bot
          else:                                # se il messaggio dopo il tag non è vuoto   
            try:
              print("****** TRY ******")
              update.message.reply_text(text_model.make_sentence_with_start(temp,strict=False))
            except:
              print("****** EXCEPT ******")             
              out = textgen.generate(1, prefix=temp, temperature=0.7,return_as_list=True,)    #decide il bot prendendo il messaggio dopo il tag
              print_out(out,up,cont)
      elif (rand == 20):               # se nessuna delle condizioni precedenti è vera decido se parlare autonomaneamente o no
        print("****** vado di numero random ******")
        if(len(messaggio)<7):           # se il messaggio è più corto di 7 caratteri allora lo prendo per generare il testo
          try:
            print("****** TRY ******")
            update.message.reply_text(text_model.make_sentence_with_start(messaggio,strict=False))
          except:
            print("****** EXCEPT ******")
            out = textgen.generate(1, prefix=messaggio, temperature=0.7,return_as_list=True, max_gen_length=300)       # genera il testo tramite AI
            print_out(out,up,cont)
        else:         # genero il testo senza nessun vincolo
          update.message.reply_text(text_model.make_short_sentence(1000))        #decide il bot
  






def start(update, context):     #funzione che risponde al comando /start
  update.message.reply_text("Ciao, esisto")

def main():

  print("************* TEMPO DI AVVIO *************")
  print(dateNow)

  """Start the bot."""
  # prendo e inserisco la chiave del bot
  f = open("chiave.txt","r")
  chiave = f.read()
  updater = Updater(chiave, use_context=True)
  dp = updater.dispatcher

  #chiamata delle diverse funzioni

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("attiva", Attiva))
  dp.add_handler(CommandHandler("disattiva", Disattiva))
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
  main()                    # DA QUI INIZIA TUTTO
