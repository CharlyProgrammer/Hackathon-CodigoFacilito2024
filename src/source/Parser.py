#############################
#         No NODOS
##################################
import src.source.Lexador as Lexador
class NodoNum:
    def __init__(self,token):
        self.token=token
        self.pos_ini=self.token.pos_ini
        self.pos_fin=self.token.pos_fin
    def __repr__(self) -> str:
        return f'{self.token}'
    
class NodoOp:
    def __init__(self,NodoIzq,TokOperador,NodoDer):
        self.NodoIzq=NodoIzq
        self.TokOperador=TokOperador
        self.NodoDer=NodoDer
        self.pos_ini=self.NodoIzq.pos_ini
        self.pos_fin=self.NodoDer.pos_fin
    def __repr__(self) -> str:
        return f'({self.NodoIzq},{self.TokOperador},{self.NodoDer})' 

class NodoOpUnit:
    def __init__(self,TokOperador,Nodo):
        self.TokOperador=TokOperador
        self.Nodo=Nodo
        self.pos_ini=self.TokOperador.pos_ini
        self.pos_fin=Nodo.pos_fin
    
    def __repr__(self) -> str:
        return f'({self.TokOperador},{self.Nodo})'    

class NodoAccesoVar:
    def __init__(self,VarToken):
        self.VarToken=VarToken
        self.pos_ini=self.VarToken.pos_ini
        self.pos_fin=self.VarToken.pos_fin
        
        
class NodoAsigVar:
    def __init__(self,VarToken,valor):
        self.VarToken=VarToken
        self.valor=valor
        self.pos_ini=self.VarToken.pos_ini
        self.pos_fin=self.valor.pos_fin             
    
#############################
#         RES PARSEADOR
################################## 

class resParse():
    def __init__(self) -> None:
        self.error=None
        self.nodo=None
        
    def registro_recorrer(self):
        pass
            
    def registro(self,res):
        if res.error:
            self.error=res.error
        return res.nodo    
      
        
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
           
           res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,", se esperaba un elemento 'MAS', 'MENOS', 'POR', 'ENTRE' o 'ELEVADO' "))
        return res
    
    
    def expresion(self):
        res=resParse()
        
        if self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'BOX'):
            res.registro_recorrer()
            self.recorrer()
            if self.token_actual.tipo !=Lexador.t_VAR_IDEN:
                res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba una variable VAR_IDEN '))
            nom_var=self.token_actual
            res.registro_recorrer()
            self.recorrer()
            if self.token_actual.tipo !=Lexador.t_ASIGNAR:
                res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un signo de asignacion ":" ')) 
            res.registro_recorrer()
            self.recorrer()
            expr=res.registro(self.expresion())
            if res.error: return res
            return res.exito(NodoAsigVar(nom_var,expr))
              
        nodo= res.registro(self.op_binar(self.termino,(Lexador.t_MAS,Lexador.t_MENOS)))
        if res.error:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un elemento ENTERO, REAL, "BOX",operadores MAS, MENOS o IZQPAREN --> "("'))
        return res.exito(nodo)
            
    def termino(self):
        
        return self.op_binar(self.factor,(Lexador.t_POR,Lexador.t_ENTRE))    
    def op_binar(self,func_A,ops,func_B=None):
        if func_B==None:
            func_B=func_A
        res=resParse()
        izq=res.registro(func_A())
        if res.error:return res
        while self.token_actual.tipo in ops:
            tok_op=self.token_actual
            res.registro_recorrer()
            self.recorrer()  
            der=res.registro(func_B())
            if res.error:return res
            izq=NodoOp(izq,tok_op,der)
          
        return res.exito(izq) 
        
    def potencia(self):
        return self.op_binar(self.atomico,(Lexador.t_POT, ),self.factor)
            
        
    def atomico(self):
        res=resParse()
        tok=self.token_actual
        if tok.tipo in (Lexador.t_ENTERO,Lexador.t_REAL):
             res.registro_recorrer()
             self.recorrer()
             return res.exito(NodoNum(tok))
        elif tok.tipo in (Lexador.t_VAR_IDEN):
            res.registro_recorrer()
            self.recorrer()
            return res.exito(NodoAccesoVar(tok)) 
        elif tok.tipo in(Lexador.t_IZQPAREN):
            res.registro_recorrer()
            self.recorrer()
            expr=res.registro(self.expresion())
            if res.error: return res
            if self.token_actual.tipo in (Lexador.t_DERPAREN):
                res.registro_recorrer()
                self.recorrer()
                return res.exito(expr)
            else:
                
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un elemento DERPAREN --> ")" '))
        return res.fracaso(Lexador.ErrorSintaxisInvalida(tok.pos_ini,tok.pos_fin,', se esperaba un elemento ENTERO, REAL, VAR_IDEN, operadores MAS,MENOS o IZQPAREN --> "("'))        
                    
    
    def factor(self):
        res=resParse()
        tok=self.token_actual
        
        if tok.tipo in (Lexador.t_MAS,Lexador.t_MENOS):
            res.registro_recorrer()
            self.recorrer()
            factor=res.registro(self.factor())
            if res.error: return res
            return res.exito(NodoOpUnit(tok,factor))
        
        return self.potencia()
    
                 