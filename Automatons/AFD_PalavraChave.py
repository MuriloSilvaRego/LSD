from AFD_Base import AutomatoFinitoD

class AFD_PalavrasChave(AutomatoFinitoD):
    def __init__(self, palavras):
        estados = ['q0']
        transicoes = {'q0': {}}
        finais = []
        alfabeto = set()

        estado_count = 1  # contador para estados únicos

        for palavra in palavras:
            atual = 'q0'
            for letra in palavra:
                alfabeto.add(letra)
                if letra not in transicoes[atual]:
                    novo_estado = f'q{estado_count}'
                    estado_count += 1
                    estados.append(novo_estado)
                    transicoes[atual][letra] = novo_estado
                    transicoes[novo_estado] = {}
                    atual = novo_estado
                else:
                    atual = transicoes[atual][letra]
            finais.append(atual)

        super().__init__(estados, list(alfabeto), transicoes, 'q0', finais)