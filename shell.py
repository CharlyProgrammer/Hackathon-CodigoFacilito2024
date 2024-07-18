import src.source.Lexador as Lexador
import os 
comandos=[]



while True:
    instr=input('MICHI>>> ')
    
    if instr=='salir()':
        break
    
    elif instr.split()[0] =='ejecutar':
        result,error=Lexador.run(f'shell.py',instr.lstrip('ejecutar '))
        if error:
            print(error.str_conv())
        else:
            print(result)
    
    elif instr.split()[0]=='compilar':
        
        with open(instr.split()[1], instr.split()[2].lstrip('--')) as sourcecode:
            for c,i in enumerate(sourcecode.readlines()):
                result,error=Lexador.run(f'{os.path.basename(os.path.realpath(__file__))}',i.rstrip('\n'),c+1)
                print()
                if error:
                    print(error.str_conv())
                else:
                    print(result) 
                
             
        
      
              
    else:
        continue              
    
    
        
                    
                                
    
            
        