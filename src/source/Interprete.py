########################################
# INTERPRETE DEL LENGUAJE
####################################

class Interprete:
    
        
    def visita(self,nodo):
        nombre_metod=f'visit_{type(nodo).__name__}'
        metod=getattr(self,nombre_metod,self.no_visita)
        return metod(nodo)
    def no_visita(self,nodo):
        raise Exception(f'No hay definido un metodo para peticiones o visitas, visit_{type(nodo).__name__}')
    def NumNode_visita(self,nodo):
        print('Nodo encontrado!')
    def Nodo_OpBin_visita(self,nodo):
        print('Nodo de operaciones encontrado!')   
    def UnitOpNodo_visita(self,nodo):
        print('Nodo de operaciones unitarias encontrado !')     