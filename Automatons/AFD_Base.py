class AutomatoFinitoD:
    def __init__(self, estados, alfabeto, transicoes, inicial, finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes # transicoes[estado][simbolo] = novo_estado
        self.inicial = inicial
        self.finais = finais

    def aceita(self, palavra):
        estado_atual = self.inicial
        for simbolo in palavra:
            if simbolo not in self.alfabeto or estado_atual not in self.transicoes or simbolo not in self.transicoes[estado_atual]:
                return False
            estado_atual = self.transicoes[estado_atual][simbolo]
        return estado_atual in self.finais