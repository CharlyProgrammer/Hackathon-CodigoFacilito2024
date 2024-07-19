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
t_MAS ='MAS'
t_MENOS ='MENOS'
t_POR ='POR'
t_ENTRE ='ENTRE'
t_IZQPAREN ='IZQPAREN'
t_DERPAREN ='DERPAREN'
t_VARIABLE='BOX'
t_FDA='FDA'   
class Token:
    def __init__(self,tipo_,valor,ln,pos,loc,ln_s=None):
        self.tipo=tipo_ 
        self.valor=valor
        self.pos=pos
        self.ln=ln
        self.loc=loc
        self.ln_s=ln_s
        
           
    def __repr__(self) -> str:
        if self.ln_s!=None:
            return f'TOKEN({self.tipo}-->{self.valor},linea: {self.ln_s}, column: {self.pos})'
        else:
            return f'TOKEN({self.tipo}-->{self.valor},linea: {self.ln}, column: {self.pos})'
        
        
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
        while self.elm_actual!=None and self.elm_actual in digits+'.':
            if self.elm_actual =='.':
                if punto_cont==1:break
                punto_cont+=1
                num_str+='.'   
            else:
                num_str+=self.elm_actual
            self.mover()
        if punto_cont==0:
            return Token(t_ENTERO,int(num_str),self.pos.lin+1,self.pos.col,self.pos,self.linea)
        else:
            return Token(t_REAL,float(num_str),self.pos.lin+1,self.pos.col+1-len(num_str),self.pos,self.linea)
            
        
    def constr_str(self):
        var_str=''
        count_nn=0
        while self.elm_actual!=None and re.match(r'[a-zA-Z0-9_]',self.elm_actual):
            if re.match(r'[a-zA-Z_]',self.elm_actual):
                count_nn+=1
                var_str+=self.elm_actual
            else:
                var_str+=self.elm_actual   
            self.mover()
            if var_str.upper() in ('MAS','MENOS','POR','ENTRE'):
                  break
        
            
        if count_nn >0:
            if var_str.upper()=='MAS': return Token(t_MAS,'MAS',self.pos.lin+1,self.pos.col+1,self.pos,self.linea)
            elif var_str.upper()=='MENOS': return Token(t_MENOS,'MENOS',self.pos.lin+1,self.pos.col+1,self.pos,self.linea)
            elif var_str.upper()=='POR': return Token(t_POR,'POR',self.pos.lin+1,self.pos.col+1,self.pos,self.linea)
            elif var_str.upper()=='ENTRE': return Token(t_ENTRE,'ENTRE',self.pos.lin+1,self.pos.col+1,self.pos,self.linea)    
            else:Token(t_VARIABLE,var_str,self.pos.lin+1,self.pos.col+1-len(var_str),self.pos,self.linea)  
              
                
        
       
    def constr_var(self):
        var_str=''
        count_nn=0
        while self.elm_actual!=None and re.match(r'[a-zA-Z0-9_]',self.elm_actual):
            if re.match(r'[a-zA-Z_]',self.elm_actual):
                count_nn+=1
                var_str+=self.elm_actual
            else:
                var_str+=self.elm_actual   
            self.mover()
        if count_nn >0:
            if var_str.upper()=='MAS': return Token(t_MAS,'MAS',self.pos.lin+1,self.pos.col+1,self.pos,self.linea)
            return Token(t_VARIABLE,var_str,self.pos.lin+1,self.pos.col+1-len(var_str),self.pos,self.linea)        
        
                                          
    def definir_tokens(self):
        
        tokens=[]
        while self.elm_actual !=None:
            
            if self.elm_actual in '\n\t ':
                
                self.mover()
            elif re.match(r'[a-zA-Z]',self.elm_actual):
                tokens.append(self.constr_str())
                
            elif self.elm_actual in digits:
                tokens.append(self.constr_numero())
                  
            elif self.elm_actual=='(':
                tokens.append(Token(t_IZQPAREN,'(',self.pos.lin+1,self.pos.col+1,self.pos,self.linea))
                self.mover()
            elif self.elm_actual==')':
                tokens.append(Token(t_DERPAREN,')',self.pos.lin+1,self.pos.col+1,self.pos,self.linea))
                self.mover()
            else:
                init_pos=self.pos.copiar()
                elem=self.elm_actual
                self.mover()
                return [], ErrorElmIlegal(init_pos,self.pos,'"'+ elem +'"')           
        tokens.append(Token(t_FDA,'FDA',self.pos.lin+1,self.pos.col+1,self.pos,self.linea))                       
        return tokens, None




def run(FileName,instr,linea=None):
    # Generador de tokens
    lex=AnalizadorLexico(FileName,instr,linea)
    tokens,error=lex.definir_tokens()
    if error:return None, error
     # Parsear y generador de secuencias AST
    pars=Parser.parsear(tokens)
    ast=pars.parseo()
    if ast.error:return None, ast.error
    # EJECUTAR EL INTERPRETE
    inter=Interprete.Interprete()
    res=inter.visita(ast.nodo)
    #return ast.nodo,ast.error
    return res.valor,res.error
    
            