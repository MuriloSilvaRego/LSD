from AFD_Base import AutomatoFinitoD

class AFD_Separador(AutomatoFinitoD):
    def __init__(self):
        estados = ['q0', 'q1']
        alfabeto = ['(', ')', '[', ']', ',', '.', ' ', '\n']
        transicoes = {'q0': {}, 'q1': {}}
        for s in alfabeto:
            transicoes['q0'][s] = 'q1'
        inic = 'q0'
        finais = ['q1']
        super().__init__(estados, alfabeto, transicoes, inic, finais)
        
