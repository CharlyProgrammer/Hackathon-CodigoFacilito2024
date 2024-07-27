import src.source.Lexador as Lexador
import os
import src.source.dar_bienvenida as welcome
comandos=[]


welcome.draw_welcome_AI_BITS()
while True:
    
    instr=input('[AI-BITS]>>> ')
    
    if instr=='salir()':
        break
    
    elif instr.split()[0].lower() =='ejecutar':
        instr=instr.replace(instr.split()[0],'')
        #print(instr.lstrip(' '))
        result,error=Lexador.run(f'shell.py',instr.lstrip(' '))
        if error:
            print(error.str_conv())
        elif result:
            print(f'[IA-BITS]>>> {result}')
    
    elif instr.split()[0].lower()=='compilar':
        
       with open(instr.split()[1], instr.split()[2].lstrip('--')) as sourcecode:
            for c,i in enumerate(sourcecode.readlines()):
                result,error=Lexador.run(f'{os.path.basename(os.path.realpath(__file__))}',i.rstrip('\n'),c+1)
                #print()
                if error:
                    print(error.str_conv())
                elif result:
                    print(f'[AI-BITS]>>> {result}') 

    else:
        try:
            raise SyntaxError
        
        except SyntaxError as e:
            print(f'{type(e)} : Se esperaba una instruccion de "ejecutar" o "compilar"')
        finally:
            continue              
    
    
        
                    
                                
    
            
        