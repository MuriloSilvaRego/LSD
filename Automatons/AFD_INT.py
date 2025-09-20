from AFD_Base import AutomatoFinitoD

class AFD_INT(AutomatoFinitoD):
    def __init__(self):
        estados = ['q0', 'q1']
        alfabeto = [str(i) for i in range(10)]
        transicoes = {'q0': {}, 'q1': {}}
        for d in alfabeto:
            if d != "0":
                transicoes['q0'][d] = 'q1'
            transicoes['q1'][d] = 'q1'
        inic = 'q0'
        finais = ['q1']
        super().__init__(estados, alfabeto, transicoes, inic, finais)
        
