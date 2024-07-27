import openai 
import os 
from dotenv import load_dotenv 
import webbrowser


webs={'youtube':'https://www.youtube.com','curiosidades':'https://es.wikihow.com/','traducir':'https://context.reverso.net/traduccion/'}
while True:
    comando=input("digite la opcion: ")
    if comando=='salir':
        break
    if comando=='youtube':
         webbrowser.open(webs[comando])
    elif comando=='traducir':
            webbrowser.open(webs[comando])
    elif comando=='curiosidades':
            webbrowser.open(webs[comando])    
        
    else:
        print('Su comando no existe en nuestra base de datos')
        continue            
