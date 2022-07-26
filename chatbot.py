def AI():
  #!/usr/bin/env python3 
  from flask import Flask

  app = Flask(__name__)

  from textgenrnn import textgenrnn

  @app.route("/AINoText")
  def AINoText():
    textgen = textgenrnn(weights_path='UnivaqBot_weights.hdf5',
                          vocab_path='UnivaqBot_vocab.json',
                          config_path='UnivaqBot_config.json')


    message = textgen.generate(1, temperature=1.0,return_as_list=True)        #decide il bot
    print(message)
    
    return (message[0])

