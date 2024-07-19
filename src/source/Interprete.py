########################################
# INTERPRETE DEL LENGUAJE
####################################
import src.source.Lexador as lex
import re
class Interprete:
    
        
    def visita(self,nodo):
        
        nombre_metod=f'{type(nodo).__name__}_visita'
        metod=getattr(self,nombre_metod,self.no_visita)
        return metod(nodo)
    def no_visita(self,nodo):
        raise Exception(f'No hay definido un metodo para peticiones o visitas, visit_{type(nodo).__name__}')
    def NodoNum_visita(self,nodo):
        return TEResultado().exito(Numero(nodo.token.valor).dar_posicion(nodo.token.loc,nodo.token.loc))
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
        if error: 
            return TERes.fracaso(error)
        else:
            return TERes.exito(resul.dar_posicion(nodo.TokOperador.pos,nodo.TokOperador.pos+1))
             
    def NodoOpUnit_visita(self,nodo):
        TERes=TEResultado()
        #print('Nodo de operaciones unitarias encontrado !') 
        num=TERes.registro(self.visita(nodo.Nodo))
        if TERes.error: return TERes
        error=None 
          
        if nodo.TokOperador.tipo== lex.t_MENOS:
            num,error=num.multiplicar_por(Numero(-1))
        if error:
            return TERes.fracaso(error)
        else:
            return TERes.exito(num.dar_posicion(nodo.TokOperador.pos,nodo.TokOperador.pos+1))    
       
########################################
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

class Numero:
    def __init__(self,valor):
        self.valor=valor
        self.dar_posicion()
    
    def dar_posicion(self,i_pos=None,f_pos=None):
        self.i_pos=i_pos
        self.f_pos=f_pos
        return self
    def sumar_a(self,other):
        if isinstance(other,Numero):
            return Numero(self.valor + other.valor),None 
    
    def restar_a(self,other):
        if isinstance(other,Numero):
            return Numero(self.valor - other.valor),None
    
    def multiplicar_por(self,other):
        if isinstance(other,Numero):
            return Numero(self.valor * other.valor),None
    
    def dividir_entre(self,other):
        if isinstance(other,Numero):
            
            if other.valor==0:
                
                return None,lex.ErrorTiempoEjecucion(other.i_pos,other.f_pos,'División por zero')
            return Numero(self.valor / other.valor),None
    
    def __repr__(self) -> str:
        
        if re.match(r'-',str(self.valor) ):return 'MENOS '+str(self.valor*-1)
        
        return str(self.valor)                                          