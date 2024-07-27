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

class NodoText:
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


class NodoDefFunc:
    def __init__(self,nom_tok_var,nom_toks_args,nodo_bloq):
        self.nom_tok_var= nom_tok_var
        self.nom_toks_args = nom_toks_args
        self.nodo_bloq =nodo_bloq 

        if self.nom_tok_var:
           self.pos_ini= self.nom_tok_var.pos_ini
        elif len(self.nom_toks_args)>0:
            self.pos_ini= self.nom_toks_args[0].pos_ini
        else:
            self.pos_ini=self.nodo_bloq.pos_ini
        self.pos_fin=self.nodo_bloq.pos_fin
        
class NodoLlamadas:
    def __init__(self,nodo_para_llamar,nodos_args):
        self.nodo_para_llamar= nodo_para_llamar
        self.nodos_args = nodos_args
        
        self.pos_ini=self.nodo_para_llamar.pos_ini
        if len(self.nodos_args)>0:
            self.pos_fin=self.nodos_args[len(self.nodos_args)-1].pos_fin
        else:
            self.pos_fin=self.nodo_para_llamar.pos_fin
                          
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
           #print(self.token_actual.tipo)
           res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,", se esperaba un OPERADOR ARITMETICO, DE COMPARACIÓN o LÓGICO VALIDO '"))
        return res
    
   
    def expresion(self):
        res=resParse()
        
        if self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'box'):
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
        nodo= res.registro(self.op_binar(self.exp_comp,((Lexador.t_PALABRA_CLAVE,'and'),(Lexador.t_PALABRA_CLAVE,'or'),(Lexador.t_PALABRA_CLAVE,'nand'),(Lexador.t_PALABRA_CLAVE,'nor'),(Lexador.t_PALABRA_CLAVE,'xor'))))
        if res.error:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un ENTERO, REAL, DECLARACION CON "BOX",operadores ARITMETICOS, LOGICOS,(),WHEN o WHEEL'))
        return res.exito(nodo)
    
    def exp_comp(self):
        res=resParse()
        if self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'not'):
            tok_op=self.token_actual
            res.registro_recorrer()
            self.recorrer()
            nodo=res.registro(self.exp_comp())
            if res.error: return res
            return res.exito(NodoOpUnit(tok_op,nodo))
        elif self.token_actual.tipo==Lexador.t_FACTORIAL:
            tok_op=self.token_actual
            res.registro_recorrer()
            self.recorrer()
            nodo=res.registro(self.exp_comp())
            if res.error: return res
            return res.exito(NodoOpUnit(tok_op,nodo))
        elif self.token_actual.tipo==Lexador.t_GRADIENTE_COMB:
            tok_op=self.token_actual
            res.registro_recorrer()
            self.recorrer()
            nodo=res.registro(self.exp_comp())
            if res.error: return res
            return res.exito(NodoOpUnit(tok_op,nodo))
        nodo=res.registro(self.op_binar(self.exp_aritm,(Lexador.t_IGUAL,Lexador.t_DIFERENTE,Lexador.t_MAYOR_QUE,Lexador.t_MENOR_QUE,Lexador.t_MAYOR_IGUAL,Lexador.t_MENOR_IGUAL)))
        if res.error:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un un elemento ENTERO, REAL, VAR_IDEN,operadores MAS, MENOS, "(" o NOT' ))
        return res.exito(nodo)
    
    
    def exp_aritm(self):
        return self.op_binar(self.termino,(Lexador.t_MAS,Lexador.t_MENOS))
        
    
    def termino(self):
        
        return self.op_binar(self.factor,(Lexador.t_POR,Lexador.t_ENTRE,Lexador.t_REST,Lexador.t_PARTICION, Lexador.t_NAVEGAR,Lexador.t_TRADUCIR))    
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
        return self.op_binar(self.llamada,(Lexador.t_POT, ),self.factor)
    
    def llamada(self):
        res=resParse()
        atm=res.registro(self.atomico())        
        if res.error:return res
        if self.token_actual.tipo ==Lexador.t_IZQPAREN:
            res.registro_recorrer()
            self.recorrer()
            nodos_arg=[]
            if self.token_actual.tipo ==Lexador.t_DERPAREN:
                res.registro_recorrer()
                self.recorrer()
            else:
                nodos_arg.append(res.registro(self.expresion()))
                if res.error:
                    return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba "VAR_IDEN", when, wheel, wheel-while, task, ENTERO, REAL, "box", mas, menos, "(", "<" o "not"')) 
                while self.token_actual.tipo ==Lexador.t_COMMA:
                     res.registro_recorrer()
                     self.recorrer()
                     nodos_arg.append(res.registro(self.expresion()))
                     if res.error:return res
                if self.token_actual.tipo !=Lexador.t_DERPAREN:
                    return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba una COMMA "," o ")"')) 
                
                res.registro_recorrer()
                self.recorrer()     
            return res.exito(NodoLlamadas(atm,nodos_arg))
        
        return res.exito(atm)  
          
    def atomico(self):
        res=resParse()
        tok=self.token_actual
        if tok.tipo in (Lexador.t_ENTERO,Lexador.t_REAL):
             res.registro_recorrer()
             self.recorrer()
             return res.exito(NodoNum(tok))
        elif tok.tipo in (Lexador.t_TEXTO):
            res.registro_recorrer()
            self.recorrer()
            return res.exito(NodoText(tok))  
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
        
        elif tok.comprobar(Lexador.t_PALABRA_CLAVE,'when'):
            if_expr=res.registro(self.if_expr())
            if res.error: return res
            return res.exito(if_expr)
        
        elif tok.comprobar(Lexador.t_PALABRA_CLAVE,'wheel'):
            for_expr=res.registro(self.for_expr())
            if res.error: return res
            return res.exito(for_expr) 
        
        elif tok.comprobar(Lexador.t_PALABRA_CLAVE,'wheel-while'):
            while_expr=res.registro(self.while_expr())
            if res.error: return res
            return res.exito(while_expr)
        
        elif tok.comprobar(Lexador.t_PALABRA_CLAVE,'task'):
            def_func_expr=res.registro(self.def_func_expr())
            
            if res.error: return res
            return res.exito(def_func_expr)  
        
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
        
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'when'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un WHEN')) 
        res.registro_recorrer()
        self.recorrer()
        clausula=res.registro(self.expresion())    
        if res.error: return res
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'do'):
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
        while self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'other-when'):
            res.registro_recorrer()
            self.recorrer()
            clausula=res.registro(self.expresion())
            if res.error: return res
            if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'do'):
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
        if self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'other-case'):
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
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'wheel'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un "wheel"')) 
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
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'limit'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un LIMIT')) 
        res.registro_recorrer()
        self.recorrer()
        val_lim=res.registro(self.expresion())
        if res.error: return res 
        if self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'freq'):
            res.registro_recorrer()
            self.recorrer()
            val_freq=res.registro(self.expresion())
            if res.error: return res
        else:
            val_freq=None
        
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'do'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un "do"')) 
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
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'wheel-while'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un "wheel-while"')) 
        res.registro_recorrer()
        self.recorrer()
        cond_expr=res.registro(self.expresion())
        if res.error: return res
                
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'do'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un "do"')) 
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
    
    def def_func_expr(self):
        res=resParse()
        
        if not self.token_actual.comprobar(Lexador.t_PALABRA_CLAVE,'task'):
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un "task"')) 
        res.registro_recorrer()
        self.recorrer()
        
        if self.token_actual.tipo ==Lexador.t_VAR_IDEN:
            nom_tok_iden=self.token_actual
            res.registro_recorrer()
            self.recorrer()
            if self.token_actual.tipo != Lexador.t_IZQPAREN:
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un "("')) 
        else:
            nom_tok_iden=None
            if self.token_actual.tipo != Lexador.t_IZQPAREN:
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un identificador VAR_IDEN o "("')) 
        
        res.registro_recorrer()
        self.recorrer() 
        nom_tok_args=[]
        if self.token_actual.tipo ==Lexador.t_VAR_IDEN:
            nom_tok_args.append(self.token_actual)
            res.registro_recorrer()
            self.recorrer()
            while self.token_actual.tipo ==Lexador.t_COMMA:
                res.registro_recorrer()
                self.recorrer()
                if self.token_actual.tipo !=Lexador.t_VAR_IDEN:
                    return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba un identificador VAR_IDEN ')) 
                nom_tok_args.append(self.token_actual)
                res.registro_recorrer()
                self.recorrer()
            
            if self.token_actual.tipo != Lexador.t_DERPAREN:
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba una COMMA "," o ")"')) 
            
        else:
            if self.token_actual.tipo != Lexador.t_DERPAREN:
                return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba UN identificador VAR_IDEN o ")"')) 
            
        res.registro_recorrer()
        self.recorrer()
            
        if self.token_actual.tipo != Lexador.t_FLECHA_DER:
            return res.fracaso(Lexador.ErrorSintaxisInvalida(self.token_actual.pos_ini,self.token_actual.pos_fin,', se esperaba "->"')) 
        res.registro_recorrer()
        self.recorrer()
        nodo_bloq=res.registro(self.expresion())
        
        if res.error: return res
        return res.exito(NodoDefFunc(nom_tok_iden, nom_tok_args,nodo_bloq))
                
            
       