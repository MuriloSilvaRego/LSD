from AFD_Base import AutomatoFinitoD

class AFD_Operadores(AutomatoFinitoD):
    def __init__(self):
        estados = ['q0', 'q1', 'q2']
        alfabeto = ['=', '!', '>', '<', '+', '-', '*', '/']
        transicoes = {'q0': {}, 'q1': {}, 'q2': {}}
        for c in ['=', '!', '>', '<', '+', '-', '*', '/']:
            transicoes['q0'][c] = 'q1'
        transicoes['q1']['='] = 'q2'
        inic = 'q0'
        finais = ['q1', 'q2'] # Final q2 para "==","!=",">=","<=", q1 para ">", "<"
        super().__init__(estados, alfabeto, transicoes, inic, finais)
        
