########################################
# INTERPRETE DEL LENGUAJE
####################################
import src.source.Lexador as lex
import re
class Interprete:
    def __init__(self,TabSim):
        self.TabSim=TabSim
     
    def get_tab(self):
        return self.TabSim 
          
    def visita(self,nodo):
        
        nombre_metod=f'{type(nodo).__name__}_visita'
        metod=getattr(self,nombre_metod,self.no_visita)
        #print(nombre_metod)
        return metod(nodo)
    def no_visita(self,nodo):
        raise Exception(f'No hay definido un metodo para peticiones o visitas, visit_{type(nodo).__name__}')
    def NodoNum_visita(self,nodo,):
        return TEResultado().exito(Numero(nodo.token.valor).dar_posicion(nodo.pos_ini,nodo.pos_fin))
    def NodoOp_visita(self,nodo):
        #print('Nodo de operaciones encontrado!')
        TERes=TEResultado()
        izq=TERes.registro(self.visita(nodo.NodoIzq))
        der=TERes.registro(self.visita(nodo.NodoDer))
        
        if nodo.TokOperador.tipo== lex.t_MAS:
            resul,error=izq.sumar_a(der)
        elif nodo.TokOperador.tipo== lex.t_MENOS:
            resul,error=izq.restar_a(der)
        elif nodo.TokOperador.tipo== lex.t_POR:
            resul,error=izq.multiplicar_por(der)  
        elif nodo.TokOperador.tipo== lex.t_ENTRE:
            resul,error=izq.dividir_entre(der)
        elif nodo.TokOperador.tipo== lex.t_POT:
            resul,error=izq.elevar_a(der)
        elif nodo.TokOperador.tipo== lex.t_REST:
            resul,error=izq.modulo(der)    
        elif nodo.TokOperador.tipo== lex.t_IGUAL:
            resul,error=izq.llamar_comparacion_igual(der)
        elif nodo.TokOperador.tipo== lex.t_DIFERENTE:
            resul,error=izq.llamar_comparacion_dif(der)     
        elif nodo.TokOperador.tipo== lex.t_MAYOR_QUE:
            resul,error=izq.llamar_comparacion_mayor(der) 
        elif nodo.TokOperador.tipo== lex.t_MAYOR_IGUAL:
            resul,error=izq.llamar_comparacion_mi(der) 
        elif nodo.TokOperador.tipo== lex.t_MENOR_QUE:
            resul,error=izq.llamar_comparacion_menor(der) 
        elif nodo.TokOperador.tipo== lex.t_MENOR_IGUAL:
            resul,error=izq.llamar_comparacion_meni(der)
        elif nodo.TokOperador.comprobar(lex.t_PALABRA_CLAVE,'or'):
            resul,error=izq.op_or(der)     
        elif nodo.TokOperador.comprobar(lex.t_PALABRA_CLAVE,'and'):
            resul,error=izq.op_and(der)
        elif nodo.TokOperador.comprobar(lex.t_PALABRA_CLAVE,'nor'):
            resul,error=izq.op_nor(der)
        elif nodo.TokOperador.comprobar(lex.t_PALABRA_CLAVE,'nand'):
            resul,error=izq.op_nand(der)   
        elif nodo.TokOperador.comprobar(lex.t_PALABRA_CLAVE,'xor'):
            resul,error=izq.op_xor(der)                                              
        if error: 
            return TERes.fracaso(error)
        else:
            return TERes.exito(resul.dar_posicion(nodo.pos_ini,nodo.pos_fin))
             
    def NodoOpUnit_visita(self,nodo):
        TERes=TEResultado()
        #print('Nodo de operaciones unitarias encontrado !') 
        num=TERes.registro(self.visita(nodo.Nodo))
        if TERes.error: return TERes
        error=None 
          
        if nodo.TokOperador.tipo== lex.t_MENOS:
            num,error=num.multiplicar_por(Numero(-1))
        elif nodo.TokOperador.comprobar(lex.t_PALABRA_CLAVE,'not'):
            num,error=num.negar()    
        if error:
            return TERes.fracaso(error)
        else:
            return TERes.exito(num.dar_posicion(nodo.pos_ini,nodo.pos_fin))    
    def NodoAccesoVar_visita(self,nodo):
        
        TERes=TEResultado()
        #print('nodo acceso')
        n_var=nodo.VarToken.valor
        valor=self.TabSim.get(n_var)
        
        if not valor:
            return TERes.fracaso(lex.ErrorTiempoEjecucion(nodo.pos_ini,nodo.pos_fin,f'Variable {n_var} no esta definida'))
        return TERes.exito(valor)
    
    def NodoAsigVar_visita(self,nodo):
        
        TERes=TEResultado()
        #print('nodo asignar')
        
        n_var=nodo.VarToken.valor
        valor=TERes.registro(self.visita(nodo.valor))
        #print(valor)
        if  TERes.error: return TERes
        self.TabSim.set(n_var,valor)
        return TERes.exito(None)
    
    def NodoIF_visita(self,nodo):
        TERes=TEResultado()
        for cond,expr in nodo.casos:
            val_cond=TERes.registro(self.visita(cond))
            if TERes.error: return TERes
            if val_cond.comprobar_verdad():
                val_expr=TERes.registro(self.visita(expr))
                if TERes.error: return TERes
                return TERes.exito(val_expr)
        
        if nodo.caso_no:
            val_expr_no=TERes.registro(self.visita(nodo.caso_no))
            if TERes.error: return TERes
            return TERes.exito(val_expr_no)    
        
        return TERes.exito(None)
    
    def NodoFOR_visita(self,nodo):
        TERes=TEResultado()
        val_ini=TERes.registro(self.visita(nodo.valor_var_ini))
        if TERes.error: return TERes
        val_limit=TERes.registro(self.visita(nodo.valor_var_fin))
        if TERes.error: return TERes
        if nodo.freq:
            val_freq=TERes.registro(self.visita(nodo.freq))
            if TERes.error: return TERes
        else:
            val_freq=Numero(1)
            
        i=val_ini.valor
        
        if val_freq.valor >=0:
            clausula=lambda : i< val_limit.valor
        else:
            clausula=lambda : i> val_limit.valor
        while clausula():
            self.TabSim.set(nodo.tok_var.valor,Numero(i))
            i+=val_freq.valor
            TERes.registro(self.visita(nodo.nodo_bloq))
            if TERes.error: return TERes
        return TERes.exito(None)                
            
    def NodoWHILE_visita(self,nodo):
        TERes=TEResultado()
        while True:
            clausula=TERes.registro(self.visita(nodo.nodo_cond))
            if TERes.error: return TERes
            if not clausula.comprobar_verdad():break
            TERes.registro(self.visita(nodo.nodo_bloq))
            if TERes.error: return TERes    
        return TERes.exito(None)
    
    def NodoDefFunc_visita(self,nodo):
        TERes=TEResultado()
        nom_fun = nodo.nom_tok_var.valor if nodo.nom_tok_var else None
       
        nodo_bloq = nodo.nodo_bloq
        nom_args = [arg_name.valor for arg_name in nodo.nom_toks_args]
        print(nodo_bloq)
        val_fun = Task_fun(nom_fun, nodo_bloq, nom_args).dar_posicion(nodo.pos_ini,nodo.pos_fin)
        
        if nodo.nom_tok_var:
            self.TabSim.set(nom_fun,val_fun)
            
        
        return TERes.exito(val_fun)
    
    def NodoLlamadas_visita(self,nodo):
        TERes=TEResultado()
        args=[]
        #print(nodo.nodo_para_llamar)
        valor_a_llamar = TERes.registro(self.visita(nodo.nodo_para_llamar)).dar_posicion(nodo.pos_ini,nodo.pos_fin)
        
        if TERes.error: return TERes
        

        for arg_node in nodo.nodos_args:
            args.append(TERes.registro(self.visita(arg_node)))
            if TERes.error: return TERes
        
        valor_ret = TERes.registro(valor_a_llamar.ejecutar(args, self.TabSim))
        if TERes.error: return TERes
        return TERes.exito(valor_ret)
        
             
########################################
# TABLA DE SIMBOLOS
####################################

class TabSimbol:
    def __init__(self,padre=None):
        self.simbolos={}
        self.padre=padre
    
    def get(self,n_var):
        valor=self.simbolos.get(n_var,None)
        if valor==None and self.padre:
            return self.padre.get(n_var)
        return valor
    def set(self,n_var,valor):
        self.simbolos[n_var]=valor
    
    def quitar(self,n_var):
        del self.simbolos[n_var]    
        
#######################################
# EJECUCIÓN DE RESULTADOS
####################################

class TEResultado:
    def __init__(self,valor=None,error=None):
        self.valor=valor
        self.error=error
    def registro(self,res):
        if res.error: self.error=res.error
        return res.valor
    def exito(self,valor):
        self.valor=valor
        return self
    def fracaso(self,error):
        self.error=error
        return self
        
            

            
########################################
# VALORES/ELEMENTOS DEL LENGUAJE
####################################

class ValorNumerico:
    def __init__(self):
        
        self.dar_posicion()
        
    
    def dar_posicion(self,i_pos=None,f_pos=None):
        self.i_pos=i_pos
        self.f_pos=f_pos
        return self
    
    
    
    def sumar_a(self,other):
        return None, self.Operacion_ilegal(other) 
    
    def restar_a(self,other):
        return None, self.Operacion_ilegal(other)
    
    def multiplicar_por(self,other):
        return None, self.Operacion_ilegal(other)
    
    def dividir_entre(self,other):
        return None, self.Operacion_ilegal(other)
        
    def elevar_a(self,other):
        return None, self.Operacion_ilegal(other)   
    
    def modulo(self,other):
        return None, self.Operacion_ilegal(other)
    
    def llamar_comparacion_igual(self,other):
        return None, self.Operacion_ilegal(other) 
    def llamar_comparacion_dif(self,other):
        return None, self.Operacion_ilegal(other)  
    def llamar_comparacion_mayor(self,other):
        return None, self.Operacion_ilegal(other) 
    def llamar_comparacion_mi(self,other):
        return None, self.Operacion_ilegal(other)
    def llamar_comparacion_menor(self,other):
        return None, self.Operacion_ilegal(other)     
    def llamar_comparacion_meni(self,other):
        return None, self.Operacion_ilegal(other)      
    def op_or(self,other):
        return None, self.Operacion_ilegal(other)   
    def op_and(self,other):
        return None, self.Operacion_ilegal(other)  
    def negar(self):
        return None, self.Operacion_ilegal(other)
              
    def op_nand(self,other):
        return None, self.Operacion_ilegal(other)    
    def op_nor(self,other):
        return None, self.Operacion_ilegal(other)   
    def op_xor(self,other):
        return None, self.Operacion_ilegal(other)  
    
    def ejecutar(self,args):
        return TEResultado().fracaso(self.Operacion_ilegal())
            
    def comprobar_verdad(self):
        return False
    
    def Operacion_ilegal(self, other=None):
        if not other: other = self
        return lex.ErrorTiempoEjecucion(other.i_pos,other.f_pos,'Operación Ilegal')

class Numero(ValorNumerico):
    def __init__(self,valor):
        super().__init__()
        self.valor=valor
       
    
    def sumar_a(self,other):
        if isinstance(other,Numero):
            return Numero(self.valor + other.valor),None 
        else:
            return None, self.Operacion_ilegal(other)
    def restar_a(self,other):
        if isinstance(other,Numero):
            return Numero(self.valor - other.valor),None
        else:
            return None, self.Operacion_ilegal(other)
    def multiplicar_por(self,other):
        if isinstance(other,Numero):
            return Numero(self.valor * other.valor),None
        else:
            return None, self.Operacion_ilegal(other)
    def dividir_entre(self,other):
        if isinstance(other,Numero):
            
            if other.valor==0:
                
                return None,lex.ErrorTiempoEjecucion(other.i_pos,other.f_pos,'División por zero')
            return Numero(self.valor / other.valor),None
        else:
            return None, self.Operacion_ilegal(other)
    def elevar_a(self,other):
        if isinstance(other,Numero):
            return Numero(self.valor ** other.valor),None    
        else:
            return None, self.Operacion_ilegal(other)
    def modulo(self,other):
        if isinstance(other,Numero):
            return Numero(self.valor % other.valor),None 
        else:
            return None, self.Operacion_ilegal(other)
    
    def llamar_comparacion_igual(self,other):
        if isinstance(other,Numero):
            return Numero(int(self.valor==other.valor)),None 
        else:
            return None, self.Operacion_ilegal(other)
    def llamar_comparacion_dif(self,other):
        if isinstance(other,Numero):
            return Numero(int(self.valor!=other.valor)),None
        else:
            return None, self.Operacion_ilegal(other)    
    def llamar_comparacion_mayor(self,other):
        if isinstance(other,Numero):
            return Numero(int(self.valor>other.valor)),None 
        else:
            return None, self.Operacion_ilegal(other)
    def llamar_comparacion_mi(self,other):
        if isinstance(other,Numero):
            return Numero(int(self.valor>=other.valor)),None
        else:
            return None, self.Operacion_ilegal(other) 
    def llamar_comparacion_menor(self,other):
        if isinstance(other,Numero):
            return Numero(int(self.valor<other.valor)),None
        else:
            return None, self.Operacion_ilegal(other)     
    def llamar_comparacion_meni(self,other):
        if isinstance(other,Numero):
            return Numero(int(self.valor<=other.valor)),None 
        else:
            return None, self.Operacion_ilegal(other)     
    def op_or(self,other):
        if isinstance(other,Numero):
            return Numero(int(self.valor or other.valor)),None
        else:
            return None, self.Operacion_ilegal(other)    
    def op_and(self,other):
        if isinstance(other,Numero):
            return Numero(int(self.valor and other.valor)),None
        else:
            return None, self.Operacion_ilegal(other)  
    def negar(self):
        return Numero(1 if self.valor==0 else 0), None
        
              
    def op_nand(self,other):
        if isinstance(other,Numero):
            return Numero(int(not(self.valor and other.valor))),None
        else:
            return None, self.Operacion_ilegal(other)    
    def op_nor(self,other):
        if isinstance(other,Numero):
            return Numero(int(not(self.valor or other.valor))),None    
        else:
            return None, self.Operacion_ilegal(other)
    def op_xor(self,other):
        if isinstance(other,Numero):
            A=self.valor
            B=other.valor
            return Numero(int((A and not(B))or(not(A) and B))),None  
        else:
            return None, self.Operacion_ilegal(other)
        
    def comprobar_verdad(self):
        return self.valor !=0
              
    def __repr__(self) -> str:
        
        if re.match(r'-',str(self.valor) ):return 'menos '+str(self.valor*-1)
        
        return str(self.valor)     

class Task_fun(ValorNumerico):
    
    def __init__(self,nom,nodo_bloq,nom_args):
        super().__init__()
        self.nom=nom or "<la_sin_nombre>"
        self.nodo_bloq=nodo_bloq
        self.nom_args=nom_args
        
    def ejecutar(self,args,table):
        res= TEResultado()
        
        print(self.nodo_bloq)
        if len(args) > len(self.nom_args):
            return res.fracaso(lex.ErrorTiempoEjecucion(self.pos_ini,self.pos_fin,f'{len(args)-len(self.nom_args)} demasiados parametros pasados a {self.nom}'))
        if len(args) < len(self.nom_args):
            return res.fracaso(lex.ErrorTiempoEjecucion(self.pos_ini,self.pos_fin,f'{len(self.nom_args) - len(args)} pocos parametros pasados a {self.nom}'))
        
        for i in range(len(args)):
            nom_arg=self.nom_args[i]
            val_arg=args[i]
            table.set(nom_arg,val_arg)  
        
        valor=res.registro(Interprete.visita(self.nodo_bloq))
        if res.error:return res
        return res.exito(valor)  
    
    def __repr__(self) -> str:
        return f'<Task {self.nom}>'                                           