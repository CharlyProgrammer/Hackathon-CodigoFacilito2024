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
        
# Nodos para estructuras WHEN - WHEEL        

class NodoIF:
    def __init__(self,casos,casos_no):
        self.casos=casos
        self.caso_no=casos_no
        self.pos_ini=self.casos[0][0].pos_ini
        self.pos_fin=(self.caso_no or self.casos[len(self.casos)-1][0]).pos_fin
        
class NodoFOR:
    def __init__(self,tok_var,valor_var_ini,valor_var_fin, freq,nodo_bloq):
        self.tok_var=tok_var
        self.valor_var_ini= valor_var_ini
        self.valor_var_fin= valor_var_fin
        self.freq= freq
        self.nodo_bloq= nodo_bloq                    
        
        self.pos_ini=self.tok_var.pos_ini
        self.pos_fin=self.nodo_bloq.pos_fin 
        
class NodoWHILE:
    def __init__(self,nodo_cond,nodo_bloq):
        self.nodo_cond= nodo_cond
        self.nodo_bloq= nodo_bloq
        
        self.pos_ini=self.nodo_cond.pos_ini
        self.pos_fin=self.nodo_bloq.pos_fin 
    
#############################
#         RES PARSEADOR
################################## 

class resParse():
    def __init__(self) -> None:
        self.error=None
        self.nodo=None
        self.cont_avance = 0
    def registro_recorrer(self):
        self.cont_avance+=1
            
    def registro(self,res):
        self.cont_avance += res.cont_avance
        if res.error:
            self.error=res.error
        return res.nodo    
      
        
    def exito(self,nodo):
        self.nodo=nodo
        return self
    
    def fracaso(self,error):
        if not self.error or self.cont_avance==0:
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
           
           res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,", se esperaba un OPERADOR ARITMETICO, DE COMPARACIÓN o LÓGICO VALIDO '"))
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
        #nodo= res.registro(self.op_binar(self.termino,(Lexador.t_MAS,Lexador.t_MENOS)))      
        nodo= res.registro(self.op_binar(self.exp_comp,((Lexador.t_PALABRA_CLAVE,'AND'),(Lexador.t_PALABRA_CLAVE,'OR'),(Lexador.t_PALABRA_CLAVE,'NAND'),(Lexador.t_PALABRA_CLAVE,'NOR'),(Lexador.t_PALABRA_CLAVE,'XOR'))))
        if res.error:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un ENTERO, REAL, DECLARACION CON "BOX",operadores ARITMETICOS, LOGICOS,(),WHEN o WHEEL'))
        return res.exito(nodo)
    
    def exp_comp(self):
        res=resParse()
        if self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'NOT'):
            tok_op=self.token_actual
            res.registro_recorrer()
            self.recorrer()
            nodo=res.registro(self.exp_comp())
            if res.error: return res
            return res.exito(NodoOpUnit(tok_op,nodo))
        nodo=res.registro(self.op_binar(self.exp_aritm,(Lexador.t_DOBLE_ASIGN,Lexador.t_DIFERENTE,Lexador.t_MAYOR_QUE,Lexador.t_MENOR_QUE,Lexador.t_MAYOR_IGUAL,Lexador.t_MENOR_IGUAL)))
        if res.error:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un un elemento ENTERO, REAL, VAR_IDEN,operadores MAS, MENOS, "(" o NOT' ))
        return res.exito(nodo)
    
    
    def exp_aritm(self):
        return self.op_binar(self.termino,(Lexador.t_MAS,Lexador.t_MENOS))
        
    
    def termino(self):
        
        return self.op_binar(self.factor,(Lexador.t_POR,Lexador.t_ENTRE,Lexador.t_REST))    
    def op_binar(self,func_A,ops,func_B=None):
        if func_B==None:
            func_B=func_A
        res=resParse()
        izq=res.registro(func_A())
        if res.error:return res
        while self.token_actual.tipo in ops or (self.token_actual.tipo, self.token_actual.valor) in ops:
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
        
        elif tok.comprobar(Lexador.t_PALABRA_CLAVE,'WHEN'):
            if_expr=res.registro(self.if_expr())
            if res.error: return res
            return res.exito(if_expr)
        
        elif tok.comprobar(Lexador.t_PALABRA_CLAVE,'WHEEL'):
            for_expr=res.registro(self.for_expr())
            if res.error: return res
            return res.exito(for_expr) 
        
        elif tok.comprobar(Lexador.t_PALABRA_CLAVE,'WHEEL-WHILE'):
            while_expr=res.registro(self.while_expr())
            if res.error: return res
            return res.exito(while_expr) 
        
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
    
    def if_expr(self):
        res=resParse()
        casos=[]
        casos_no= None
        
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'WHEN'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un WHEN')) 
        res.registro_recorrer()
        self.recorrer()
        clausula=res.registro(self.expresion())    
        if res.error: return res
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'DO'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un DO')) 
        res.registro_recorrer()
        self.recorrer()
        if self.token_actual.tipo !=Lexador.t_IZQBLOQ:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un <')) 
        res.registro_recorrer()
        self.recorrer()
        expr_if=res.registro(self.expresion()) 
        if res.error: return res
        casos.append((clausula,expr_if)) 
        if self.token_actual.tipo !=Lexador.t_DERBLOQ:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un >')) 
        res.registro_recorrer()
        self.recorrer()
        while self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'OTHER-WHEN'):
            res.registro_recorrer()
            self.recorrer()
            clausula=res.registro(self.expresion())
            if res.error: return res
            if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'DO'):
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un DO')) 
            res.registro_recorrer()
            self.recorrer()
            if self.token_actual.tipo !=Lexador.t_IZQBLOQ:
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un <')) 
            res.registro_recorrer()
            self.recorrer()
            expr_if=res.registro(self.expresion()) 
            if res.error: return res
            casos.append((clausula,expr_if)) 
            if self.token_actual.tipo !=Lexador.t_DERBLOQ:
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un >')) 
            res.registro_recorrer()
            self.recorrer()
        if self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'OTHER-CASE'):
            res.registro_recorrer()
            self.recorrer()
            if self.token_actual.tipo !=Lexador.t_IZQBLOQ:
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un <')) 
      
            res.registro_recorrer()
            self.recorrer()
            casos_no=res.registro(self.expresion()) 
            if res.error: return res
        
        if self.token_actual.tipo !=Lexador.t_DERBLOQ:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un >')) 
        res.registro_recorrer()
        self.recorrer()    
            
        return res.exito(NodoIF(casos,casos_no))
    def for_expr(self):
        res=resParse()
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'WHEEL'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un WHEEL')) 
        res.registro_recorrer()
        self.recorrer()
        if self.token_actual.tipo !=Lexador.t_VAR_IDEN:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba una variable, VAR_IDEN')) 
        nom_var=self.token_actual
        res.registro_recorrer()
        self.recorrer()
        if self.token_actual.tipo !=Lexador.t_ASIGNAR:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba signo de asignacion, ":"')) 
        res.registro_recorrer()
        self.recorrer()
        
        val_ini=res.registro(self.expresion())
        if res.error: return res
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'LIMIT'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un LIMIT')) 
        res.registro_recorrer()
        self.recorrer()
        val_lim=res.registro(self.expresion())
        if res.error: return res 
        if self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'FREQ'):
            res.registro_recorrer()
            self.recorrer()
            val_freq=res.registro(self.expresion())
            if res.error: return res
        else:
            val_freq=None
        
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'DO'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un DO')) 
        res.registro_recorrer()
        self.recorrer()
        
        if self.token_actual.tipo !=Lexador.t_IZQBLOQ:
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un <')) 
        res.registro_recorrer()
        self.recorrer() 
        expr_bloq= res.registro(self.expresion())     
        if res.error: return res
        if self.token_actual.tipo !=Lexador.t_DERBLOQ:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un >')) 
        res.registro_recorrer()
        self.recorrer()
        return res.exito(NodoFOR(nom_var,val_ini,val_lim,val_freq,expr_bloq)) 
    
    def while_expr(self):
        res=resParse()
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'WHEEL-WHILE'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un WHEEL-WHILE')) 
        res.registro_recorrer()
        self.recorrer()
        cond_expr=res.registro(self.expresion())
        if res.error: return res
                
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'DO'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un DO')) 
        res.registro_recorrer()
        self.recorrer()
        
        if self.token_actual.tipo !=Lexador.t_IZQBLOQ:
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un <')) 
        res.registro_recorrer()
        self.recorrer() 
        expr_bloq= res.registro(self.expresion())     
        if res.error: return res
        if self.token_actual.tipo !=Lexador.t_DERBLOQ:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un >')) 
        res.registro_recorrer()
        self.recorrer()
        return res.exito(NodoWHILE(cond_expr,expr_bloq)) 
         