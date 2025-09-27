from AFD_Base import AutomatoFinitoD

class AFD_Comentario(AutomatoFinitoD):
    def __init__(self):
        estados = ['q0', 'q1', 'q2', 'q3']
        alfabeto = [chr(i) for i in range(32, 127)] + ['\n', '/']
        transicoes = {'q0': {}, 'q1': {}, 'q2': {}}
        transicoes['q0']['/'] = 'q1'
        transicoes['q1']['/'] = 'q2'
        for c in alfabeto:
            if c != '\n':
                transicoes['q2'][c] = 'q2'
        transicoes['q2']['\n'] = 'q3'  # Fica em q2 até o fim da linha
        inic = 'q0'
        finais = ['q3']
        super().__init__(estados, alfabeto, transicoes, inic, finais)
        
        
        
