from AFD_Base import AutomatoFinitoD

class AFD_String(AutomatoFinitoD):
    def __init__(self):
        estados = ['q0', 'q1', 'q2']
        alfabeto = [chr(i) for i in range(32,127) if chr(i) != '"'] + ['"']
        transicoes = {'q0': {}, 'q1': {}, 'q2': {}}
        transicoes['q0']['"'] = 'q1'
        for c in alfabeto:
            if c != '"':
                transicoes['q1'][c] = 'q1'
        transicoes['q1']['"'] = 'q2'
        inic = 'q0'
        finais = ['q2']
        super().__init__(estados, alfabeto, transicoes, inic, finais)
        
        
