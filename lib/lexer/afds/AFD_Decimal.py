from AFD_Base import AutomatoFinitoD

class AFD_Decimal(AutomatoFinitoD):
    def __init__(self):
        estados = ['q0', 'q1', 'q2', 'q3']
        alfabeto = [str(i) for i in range(10)] + ['.']
        transicoes = {s:{} for s in estados}
        for d in [str(i) for i in range(10)]:
            if d != '0':
                transicoes['q0'][d] = 'q1'
            transicoes['q1'][d] = 'q1'
            transicoes['q2'][d] = 'q3'
            transicoes['q3'][d] = 'q3'
        transicoes['q1']['.'] = 'q2'
        inic = 'q0'
        finais = ['q3']
        super().__init__(estados, alfabeto, transicoes, inic, finais)
        
        

    