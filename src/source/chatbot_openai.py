import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import speech_recognition as sr 
import pyttsx3

load_dotenv() 
class ChatGPT:
  def __init__(self,end_point,modelo,version,key):
    self.end_point=end_point
    self.modelo=modelo
    self.version=version
    self.key=key
  def inicio(self):
    
    self.ClienteOA = AzureOpenAI(api_key =os.getenv(self.key),
                            api_version = self.version,
                            azure_endpoint = os.getenv(self.end_point)
                           )
    
    return self.ClienteOA
    
  def consulta(self,cliente,rol=None,trad=False):
       
    
    
    if rol ==None:
      rol=''
      tema=input('Ingrese el tema que le gustaria ver: ')
      rol+="Eres un experto en "+tema+"que ayudas a las personas a responder preguntas de forma amable y gentil"
       
    else:
      rol+="Eres un experto en "+rol+"que ayudas a las personas a responder preguntas de forma amable y gentil"
    
    
    prompt=input('Digame, cual es su pregunta?: ')  
    respuesta = cliente.chat.completions.create(
    model=self.modelo, 
    messages=[
        {"role": "system", "content": rol},
        {"role": "user", "content": prompt}
    ])
    respuesta=respuesta.choices[0].message.content
    print()
    if trad:
      print(f"Tu respuesta es : {respuesta}")
    else:
      
      print(f"Tu respuesta es : {respuesta}")
      self.talk(respuesta)

  def talk(self,message):
    id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
    #Ignite the engine of pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id2)

    # Read the message
    engine.say(message)
    engine.runAndWait()
    
    """
    To know the available voices:

    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
      print(voice)
    """



