'''
tokens = (
    #'FUNCTION', 'CALL', 'PARAMETERS', 'ARGUMENTS', 'STRING', 'ID', 'COLON', 'LBRACE', 'RBRACE', 'IF', 'ELIF', 'ELSE', 'QUOTE'
     'NUM_ENTERO','NUM_DECIMAL',
    'MAS','MENOS','POR','ENTRE','IGUAL',
    'IZQPAREN','DERPAREN')
'''
import re
import src.source.Parser as Parser
import src.source.Interprete as Interprete
from src.source.apuntador_errores import string_with_arrows
#############################################
# CONSTANTES
############################################

digits='0123456789'

#############################################
# ERRORES
############################################
class Error:
    def __init__(self,i_pos,f_pos,e_nombre,detalles):
        self.i_pos=i_pos
        self.f_pos=f_pos    
        self.e_nombre=e_nombre
        self.detalles=detalles
    def str_conv(self):
        
        resp=f'¡ERROR!\nArchivo <{self.f_pos.FileName}> en <Linea: {self.i_pos.lin + 1}, column: {self.i_pos.col + 1}>'
        resp+=f'\n---> Motivo: {self.e_nombre}, no se reconoce {self.detalles}'
        resp+='\n\n' + string_with_arrows(self.f_pos.FileTxt,self.i_pos,self.f_pos)
        return resp    

class ErrorElmIlegal(Error):
    def __init__(self, i_pos,f_pos,detalles):
        super().__init__(i_pos,f_pos,'Elemento Ilegal', detalles)        

class ErrorSintaxisInvalida(Error):
    def __init__(self, i_pos,f_pos,detalles):
        super().__init__(i_pos,f_pos,'Sintaxis Invalida', detalles)

class ErrorTiempoEjecucion(Error):
    def __init__(self, i_pos,f_pos,detalles):
        super().__init__(i_pos,f_pos,'Error de ejecución', detalles)        
        
    
         
#############################################
# LOCALIZADOR DE POSICIONES
############################################

class localizador:
    def __init__(self,ind,lin,col,FileName,FileTxt):
        self.ind=ind
        self.lin=lin
        self.col=col
        self.FileName=FileName
        self.FileTxt=FileTxt
    def mover(self,elem_actual=None):
        self.ind+=1
        self.col+=1
        if elem_actual=='\n':
            #print(self.lin)
            self.lin+=1
            self.col=0
        return self 
    def copiar(self):
        return localizador(self.ind,self.lin,self.col,self.FileName,self.FileTxt)   
            
    
#############################################
# TOKENS
############################################
t_ENTERO='ENTERO'
t_REAL='REAL'
t_TEXTO='TEXTO'
t_MAS ='MAS'
t_MENOS ='MENOS'
t_POR ='POR'
t_ENTRE ='ENTRE'
t_POT='POTENCIA'
t_REST='RESTO'
t_PARTICION='PARTICION'
t_FACTORIAL='FACTORIAL' 
t_IZQPAREN ='IZQPAREN'
t_DERPAREN ='DERPAREN'
t_IZQBLOQ ='IZQBLOQ'
t_DERBLOQ ='DERBLOQ'
t_ASIGNAR='ASIGNAR'
t_IGUAL='IGUAL'
t_DIFERENTE='DIFERENTE'
t_MENOR_QUE='MENOR_QUE'
t_MAYOR_QUE='MAYOR_QUE'
t_MAYOR_IGUAL='MAYOR_IGUAL'
t_MENOR_IGUAL='MENOR_IGUAL'
t_NAVEGAR='NAVEGAR'
t_COMMA='COMMA'
t_GUION='GUION'
t_PREGUNTAR='PREGUNTAR'
t_TRADUCIR='TRADUCIR'
t_GRADIENTE_COMB='GRADIENTE_COMB'
t_FLECHA_DER='FLECHA_DER'
t_VAR_IDEN='V_IDEN'
t_PALABRA_CLAVE='P_CLAVE'
t_FDA='FDA'
PALABRAS_CLAVE=['box',
                'and',
                'or',
                'not',
                'nand',
                'nor',
                'xor',
                'when',
                'other-case',
                'do',
                'other-when',
                'wheel',
                'limit',
                'freq',
                'wheel-while',
                'task',
                'exit']  
class Token:
    def __init__(self,tipo_,valor,ln,pos_ini=None,pos_fin=None,ln_s=None):
        self.tipo=tipo_ 
        self.valor=valor
        self.ln=ln
        self.ln_s=ln_s
        if pos_ini:
            self.pos_ini=pos_ini.copiar()
            self.pos_fin=pos_ini.copiar()
            self.pos_fin.mover()
        if pos_fin:
            self.pos_fin=pos_fin.copiar()    
    
    
    def comprobar(self,tipo_,valor):
        return self.tipo==tipo_ and self.valor==valor    
           
    def __repr__(self) -> str:
        if self.ln_s!=None:
            return f'TOKEN({self.tipo}-->{self.valor},linea: {self.ln_s}, column: {self.pos_ini.col})'
        else:
            return f'TOKEN({self.tipo}-->{self.valor},linea: {self.ln}, column: {self.pos_ini.col})'
        
        
        #if self.valor:return f'TOKEN({self.tipo}-->{self.valor})'
        #return f'TOKEN({self.tipo})'

class AnalizadorLexico:
    def __init__(self,File,txt,linea=None) -> None:
        self.File=File
        self.txt=txt
        self.linea=linea
        self.pos=localizador(-1,0,-1,File,txt)
        self.elm_actual=None
        self.mover()
        
    def mover(self):
        
        self.pos.mover(self.elm_actual)
        self.elm_actual=self.txt[self.pos.ind] if self.pos.ind < len(self.txt) else None
        
            
    def constr_numero(self):
        num_str=''
        punto_cont=0
        pos_ini=self.pos.copiar()
        while self.elm_actual!=None and self.elm_actual in digits+'.':
            if self.elm_actual =='.':
                if punto_cont==1:break
                punto_cont+=1
                num_str+='.'   
            else:
                num_str+=self.elm_actual
            self.mover()
        if punto_cont==0:
            return Token(t_ENTERO,int(num_str),self.pos.lin+1,pos_ini,self.pos,self.linea)
        else:
            return Token(t_REAL,float(num_str),self.pos.lin+1,pos_ini,self.pos,self.linea)
            
        
    def constr_str(self):
        var_str=''
        pos_ini=self.pos.copiar()
        while self.elm_actual!=None and re.match(r'[a-zA-Z0-9_-]',self.elm_actual):
            var_str+=self.elm_actual
            self.mover()
                  
        tipo_tok=t_PALABRA_CLAVE if var_str in PALABRAS_CLAVE else t_VAR_IDEN
           
        
        if var_str=='mas': return Token(t_MAS,'mas',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='menos': return Token(t_MENOS,'menos',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='por': return Token(t_POR,'por',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='entre': return Token(t_ENTRE,'entre',self.pos.lin+1,pos_ini,self.pos,self.linea) 
        elif var_str=='elevado': return Token(t_POT,'elevado',self.pos.lin+1,pos_ini,self.pos,self.linea) 
        elif var_str=='resto': return Token(t_REST,'resto',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='factorial': return Token(t_FACTORIAL,'factorial',self.pos.lin+1,pos_ini,self.pos,self.linea)  
        elif var_str=='particion': return Token(t_PARTICION,'particion',self.pos.lin+1,pos_ini,self.pos,self.linea)  
        elif var_str=='mayor': return Token(t_MAYOR_QUE,'mayor',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='menor': return Token(t_MENOR_QUE,'menor',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='mayor-igual': return Token(t_MAYOR_IGUAL,'mayor-igual',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='menor-igual': return Token(t_MENOR_IGUAL,'menor-igual',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='igual': return Token(t_IGUAL,'igual',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='navegar': return Token(t_NAVEGAR,'navegar',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='traducir': return Token(t_TRADUCIR,'traducir',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='gradiente-comb': return Token(t_GRADIENTE_COMB,'gradiente-comb',self.pos.lin+1,pos_ini,self.pos,self.linea)
        elif var_str=='preguntar-ai-experta': return Token(t_PREGUNTAR,'preguntar-ai-experta',self.pos.lin+1,pos_ini,self.pos,self.linea)
      
        else:
            return Token(tipo_tok,var_str,self.pos.lin+1,pos_ini,self.pos,self.linea)  
    
    def constr_sp(self):
          tipo_tok=t_GUION
          pos_ini=self.pos.copiar()
          self.mover()
          sp_str='-'
          if self.elm_actual=='>':
              tipo_tok=t_FLECHA_DER
              sp_str='->'
              self.mover()
          return Token(tipo_tok,sp_str,self.pos.lin+1,pos_ini,self.pos,self.linea)     
    
    def constr_txt(self):
        text=''
        pos_ini=self.pos.copiar()
        esc_char=False 
        self.mover()
        esc_chars={'n':'\n','t':'\t'}
        while self.elm_actual !=None and (self.elm_actual!='"' or esc_char):
            if esc_char:
                text+=esc_chars.get(self.elm_actual,self.elm_actual)
            if self.elm_actual=='\\':
                esc_char=True
            else:
                text+=self.elm_actual 
            self.mover()
            esc_char=False
        self.mover()
        return Token(t_TEXTO,text,self.pos.lin+1,pos_ini,self.pos,self.linea)     
               
    def definir_tokens(self):
        
        tokens=[]
        #print(self.elm_actual)
        while self.elm_actual !=None:
            
            if self.elm_actual in '\n\t ':
                
                self.mover()
                
          
            
            elif re.match(r'[a-zA-Z]',self.elm_actual):
                
                tokens.append(self.constr_str())
                
            elif self.elm_actual in digits:
                tokens.append(self.constr_numero())
            elif self.elm_actual=='-':
                tokens.append(self.constr_sp())      
            elif self.elm_actual=='(':
                tokens.append(Token(t_IZQPAREN,'(',self.pos.lin+1,pos_ini=self.pos,ln_s=self.linea))
                self.mover()
            elif self.elm_actual==')':
                tokens.append(Token(t_DERPAREN,')',self.pos.lin+1,pos_ini=self.pos,ln_s=self.linea))
                self.mover()
            elif self.elm_actual=='>':
                tokens.append(Token(t_DERBLOQ,'>',self.pos.lin+1,pos_ini=self.pos,ln_s=self.linea))
                self.mover()
            elif self.elm_actual=='<':
                tokens.append(Token(t_IZQBLOQ,'<',self.pos.lin+1,pos_ini=self.pos,ln_s=self.linea))
                self.mover()
            elif self.elm_actual=='"':
                tokens.append(self.constr_txt())           
            elif self.elm_actual==':':
                tokens.append(Token(t_ASIGNAR,':',self.pos.lin+1,pos_ini=self.pos,ln_s=self.linea))
                self.mover()
            elif self.elm_actual==',':
                tokens.append(Token(t_COMMA,',',self.pos.lin+1,pos_ini=self.pos,ln_s=self.linea))
                self.mover()   
            elif self.elm_actual=='?':
                tokens.append(Token(t_DIFERENTE,'?',self.pos.lin+1,pos_ini=self.pos,ln_s=self.linea))
                self.mover()    
            else:
                init_pos=self.pos.copiar()
                elem=self.elm_actual
                self.mover()
                return [], ErrorElmIlegal(init_pos,self.pos,'"'+ elem +'"')           
        tokens.append(Token(t_FDA,'FDA',self.pos.lin+1,pos_ini=self.pos,ln_s=self.linea))                       
        return tokens, None

global_tabla_simbol=Interprete.TabSimbol()
global_tabla_simbol.set('NULL',Interprete.Numero(0))
global_tabla_simbol.set('VERDADERO',Interprete.Numero(1))
global_tabla_simbol.set('FALSO',Interprete.Numero(0))
global_tabla_simbol.set('PI',Interprete.Numero(3.141592))
global_tabla_simbol.set('EULER',Interprete.Numero(2.718281))

def run(FileName,instr,linea=None):
    # Generador de tokens
    lex=AnalizadorLexico(FileName,instr,linea)
    tokens,error=lex.definir_tokens()
    if error:return None, error
     # Parsear y generador de secuencias AST
    #print(tokens) 
    pars=Parser.parsear(tokens)
    ast=pars.parseo()
    if ast.error:return None, ast.error
    # EJECUTAR EL INTERPRETE
    inter=Interprete.Interprete(global_tabla_simbol)
   
    res=inter.visita(ast.nodo)
    #return ast.nodo,ast.error
    return res.valor,res.error
    
            