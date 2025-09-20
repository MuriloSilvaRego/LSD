from AFD_Base import AutomatoFinitoD

class AFD_Identificador(AutomatoFinitoD):
    def __init__(self):
        estados = ['q0', 'q1']
        alfabeto = [chr(c) for c in range(65, 91)] + \
                   [chr(c) for c in range(97, 123)] + \
                   [str(i) for i in range(10)] + ['_']
        transicoes = {
            'q0': {},
            'q1': {}
        }
        # Letras maiúsculas e minúsculas e _
        for c in [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + ['_']:
            transicoes['q0'][c] = 'q1'
            transicoes['q1'][c] = 'q1'
        # Dígitos só no estado q1
        for d in [str(i) for i in range(10)]:
            transicoes['q1'][d] = 'q1'
        inic = 'q0'
        finais = ['q1']
        super().__init__(estados, alfabeto, transicoes, inic, finais)
        
