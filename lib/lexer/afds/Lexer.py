# lexer_com_erros.py
from AFD_Identificador import AFD_Identificador
from AFD_INT import AFD_INT
from AFD_Decimal import AFD_Decimal
from AFD_NotacaoCientifica import AFD_NotacaoCientifica
from AFD_String import AFD_String
from AFD_Comentario import AFD_Comentario
from AFD_Atribuicao import AFD_Atribuicao
from AFD_Operadores import AFD_Operadores
from AFD_Separador import AFD_Separador


class Lexer:
    def __init__(self, palavras_chave=None):
        self.automatos = []
        # Registrar automatos com prioridade
        self.register("COMMENT", AFD_Comentario(), priority=100)
        self.register("STRING", AFD_String(), priority=90)
        self.register("SCIENTIFIC", AFD_NotacaoCientifica(), priority=80)
        self.register("DECIMAL", AFD_Decimal(), priority=75)
        self.register("INT", AFD_INT(), priority=70)
        self.register("IDENTIFIER", AFD_Identificador(), priority=50)
        self.register("ASSIGN", AFD_Atribuicao(), priority=45)
        self.register("OPERATOR", AFD_Operadores(), priority=40)
        self.register("SEPARATOR", AFD_Separador(), priority=30)

        self.palavras_chave = set(
            palavras_chave or ["If", "Print", "CalculateMean", "CalculateSum", "End"]
        )
        self.ignorar_whitespace = True
        self.whitespace_chars = set(" \t\r\n")

    def register(self, name, automato, priority=0):
        self.automatos.append((name, automato, priority))

    def _pos_from_index(self, texto, index):
        linha = texto.count("\n", 0, index) + 1
        ultimo_n = texto.rfind("\n", 0, index)
        if ultimo_n == -1:
            col = index + 1
        else:
            col = index - ultimo_n
        return linha, col

    def tokenize(self, texto):
        i = 0
        n = len(texto)
        tokens = []
        erros = []

        while i < n:
            if self.ignorar_whitespace and texto[i] in self.whitespace_chars:
                i += 1
                continue

            melhor_len = 0
            candidatos = []

            # Encontrar o maior prefixo aceito por algum automato
            for j in range(i + 1, n + 1):
                trecho = texto[i:j]
                for name, automato, prio in self.automatos:
                    try:
                        aceita = automato.aceita(trecho)
                    except Exception:
                        aceita = False
                    if aceita:
                        L = len(trecho)
                        if L > melhor_len:
                            melhor_len = L
                            candidatos = [(name, trecho, prio)]
                        elif L == melhor_len and L > 0:
                            candidatos.append((name, trecho, prio))

            if melhor_len == 0:
                # Nenhum automato aceitou -> erro léxico
                j = i + 1
                while j < n and texto[j] not in self.whitespace_chars:
                    j += 1
                lex_err = texto[i:j]
                linha, col = self._pos_from_index(texto, i)
                contexto = texto[max(0, i - 10):min(n, j + 10)].replace("\n", "\\n")
                msg = f"Token inválido: {lex_err!r} at idx={i} line={linha} col={col}; contexto='{contexto}'"
                erros.append({"lexema": lex_err, "index": i, "line": linha, "col": col, "msg": msg})
                i = j
                continue

            # Desempate por maior prioridade
            nome, lexema, _ = sorted(candidatos, key=lambda x: (-x[2], x[0]))[0]

            # Adicionar token
            if nome == "COMMENT":
                tokens.append({"type": nome, "lexeme": lexema, "index": i})
            elif lexema in self.palavras_chave:
                tokens.append({"type": "KEYWORD", "lexeme": lexema, "index": i})
            else:
                tokens.append({"type": nome, "lexeme": lexema, "index": i})

            i += melhor_len

        return tokens, erros


# Exemplo de execução
if __name__ == "__main__":
    src = '''
        If x = 10
        Print "Valor: " // mostra valor
        10.54
        10e-2 x = 25
        Print("teste")
        
        -pe
        %pppp
        12 58.+6
        
        
        $invalid_token 123
        End
        '''
    lexer = Lexer(palavras_chave=["If", "Print", "End", "CalculateMean", "CalculateSum"])
    tokens, erros = lexer.tokenize(src)

    print("Tokens:")
    for t in tokens:
        line, col = lexer._pos_from_index(src, t["index"])
        print(f"{t['type']:12} {t['lexeme']!r:20} (line={line} col={col})")

    if erros:
        print("\nErros léxicos:")
        for e in erros:
            print(e["msg"])
    else:
        print("\nNenhum erro léxico encontrado.")
