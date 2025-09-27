from AFD_Base import AutomatoFinitoD

class AFD_NotacaoCientifica(AutomatoFinitoD):
    def __init__(self):
        estados = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']
        alfabeto = [str(i) for i in range(10)] + ['.', 'e', 'E', '+', '-']
        transicoes = {s:{} for s in estados}
        # Parte inteira
        for d in [str(i) for i in range(10)]:
            if d != "0":
                transicoes['q0'][d] = 'q1'
            transicoes['q1'][d] = 'q1'
        transicoes['q1']['.'] = 'q2'
        for d in [str(i) for i in range(10)]:
            transicoes['q2'][d] = 'q3'
            transicoes['q3'][d] = 'q3'
        for e in ['e', 'E']:
            transicoes['q1'][e] = 'q4'
            transicoes['q3'][e] = 'q4'
        for s in ['+', '-']:
            transicoes['q4'][s] = 'q5'
        for d in [str(i) for i in range(10)]:
            transicoes['q4'][d] = 'q6'
            transicoes['q5'][d] = 'q6'
            transicoes['q6'][d] = 'q6'
        inic = 'q0'
        finais = ['q6']
        super().__init__(estados, alfabeto, transicoes, inic, finais)
        
        

