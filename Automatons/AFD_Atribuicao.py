from AFD_Base import AutomatoFinitoD

class AFD_Atribuicao(AutomatoFinitoD):
    def __init__(self):
        estados = ['q0', 'q1']
        alfabeto = ['=']
        transicoes = {'q0': {}, 'q1': {}}
        transicoes['q0']['='] = 'q1'
        inic = 'q0'
        finais = ['q1']
        super().__init__(estados, alfabeto, transicoes, inic, finais)
        

