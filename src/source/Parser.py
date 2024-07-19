#############################
#         No NODOS
##################################
import src.source.Lexador as Lexador
class NodoNum:
    def __init__(self,token):
        self.token=token
    
    def __repr__(self) -> str:
        return f'{self.token}'
    
class NodoOp:
    def __init__(self,NodoIzq,TokOperador,NodoDer):
        self.NodoIzq=NodoIzq
        self.TokOperador=TokOperador
        self.NodoDer=NodoDer
    def __repr__(self) -> str:
        return f'({self.NodoIzq},{self.TokOperador},{self.NodoDer})' 

class NodoOpUnit:
    def __init__(self,TokOperador,Nodo):
        self.TokOperador=TokOperador
        self.Nodo=Nodo
    
    def __repr__(self) -> str:
        return f'({self.TokOperador},{self.Nodo})'    
             
    
#############################
#         RES PARSEADOR
################################## 

class resParse():
    def __init__(self) -> None:
        self.error=None
        self.nodo=None    
    def registro(self,res):
        if isinstance(res,resParse):
            if res.error:
                self.error=res.error
            return res.nodo    
        return res
        
    def exito(self,nodo):
        self.nodo=nodo
        return self
    
    def fracaso(self,error):
        self.error=error
        return self
        
    
#############################
#         PARSEADOR
################################## 

class parsear:
    def __init__(self,tokens):
        self.tokens=tokens
        self.id=-1
        self.recorrer() 
    def recorrer(self):
        self.id+=1
        if self.id < len(self.tokens):
            self.token_actual=self.tokens[self.id]
        return self.token_actual
    
    def parseo(self):
        res=self.expresion()
        if not res.error and self.token_actual.tipo !=Lexador.t_FDA:
            
            res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.loc,self.token_actual.loc,", se esperaba un elemento '&', '~', '@', '%' o '(' "))
        return res
    
    
    def expresion(self):
        return self.op_binar(self.termino,(Lexador.t_MAS,Lexador.t_MENOS)) 
    def termino(self):
        
        return self.op_binar(self.factor,(Lexador.t_POR,Lexador.t_ENTRE))    
    def op_binar(self,func,ops):
        res=resParse()
        izq=res.registro(func())
        if res.error:return res.error
        while self.token_actual.tipo in ops:
            tok_op=self.token_actual
            res.registro(self.recorrer())  
            der=res.registro(func())
            if res.error:return res.error
            izq=NodoOp(izq,tok_op,der)
          
        return res.exito(izq) 
        
                
    
    def factor(self):
        res=resParse()
        tok=self.token_actual
        
        if tok.tipo in (Lexador.t_MAS,Lexador.t_MENOS):
            res.registro(self.recorrer())
            factor=res.registro(self.factor())
            if res.error: return res
            return res.exito(NodoOpUnit(tok,factor))
        
        elif tok.tipo in (Lexador.t_ENTERO,Lexador.t_REAL,Lexador.t_VARIABLE):
             res.registro(self.recorrer())
             return res.exito(NodoNum(tok))
        elif tok.tipo in(Lexador.t_IZQPAREN):
            res.registro(self.recorrer())
            expr=res.registro(self.expresion())
            if res.error: return res
            if self.token_actual.tipo in (Lexador.t_DERPAREN):
                res.registro(self.recorrer())
                return res.exito(expr)
            else:
                
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos,self.token_actual.loc,', se esperaba un elemento DERPAREN --> ")" '))
                
             
        
        return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos,self.token_actual.loc,', se esperaba un elemento ENTERO o REAL')) 
    
                 