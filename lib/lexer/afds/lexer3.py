from AFN import dfa  # importa o DFA pronto
from AFN import dfa_rev  

class Lexer:
    def __init__(self, palavras_chave=None):
        # usa o DFA pronto
        self.dfa = dfa
        self.dfa_rev = dfa_rev

        self.palavras_chave = set(palavras_chave or ["If", "Print", "CalculateMean", "CalculateSum", "End"])
        self.ignorar_whitespace = True
        self.whitespace_chars = set(" \t\r\n")

        # caracteres que podem iniciar operadores/atribuição (ajustar se necessário)
        self.operator_start_chars = set("+-*/%=!<>&|^:.?")

        # tipos considerados operacionais para a regra de erro composto
        self.operator_types = {"OPERADOR", "ATRIBUICAO"}

    def _pos_from_index(self, texto, index):
        linha = texto.count("\n", 0, index) + 1
        ultimo_n = texto.rfind("\n", 0, index)
        col = index - ultimo_n if ultimo_n != -1 else index + 1
        return linha, col
    
    def _run_dfa(self, palavra):
        """
        Percorre o DFA e retorna o último estado final alcançado
        """
        estado = self.dfa.inicial
        ultimo_final = None
        for c in palavra:
            if estado not in self.dfa.transicoes or c not in self.dfa.transicoes[estado]:
                break
            estado = self.dfa.transicoes[estado][c]
            if estado in self.dfa.finais:
                ultimo_final = estado
        return ultimo_final
    
    def _longest_match_from(self, texto, start):
        """
        Retorna (tamanho_token, ultimo_final_state) para o maior prefixo reconhecido a partir de start.
        """
        estado = self.dfa.inicial
        ultimo_final = None
        tamanho = 0
        j = start
        n = len(texto)
        while j < n:
            c = texto[j]
            if estado not in self.dfa.transicoes or c not in self.dfa.transicoes[estado]:
                break
            estado = self.dfa.transicoes[estado][c]
            j += 1
            if estado in self.dfa.finais:
                ultimo_final = estado
                tamanho = j - start
        return tamanho, ultimo_final

    def tokenize(self, texto):
        i = 0
        n = len(texto)
        tokens = []
        erros = []

        while i < n:
            if self.ignorar_whitespace and texto[i] in self.whitespace_chars:
                i += 1
                continue

            tamanho_token, ultimo_final = self._longest_match_from(texto, i)

            if ultimo_final is None or tamanho_token == 0:
                # Nenhum token válido
                k = i + 1
                while k < n and texto[k] not in self.whitespace_chars:
                    k += 1
                lex_err = texto[i:k]
                linha, col = self._pos_from_index(texto, i)
                contexto = texto[max(0, i-10):min(n, k+10)].replace("\n", "\\n")
                erros.append({
                    "lexema": lex_err, "index": i, "line": linha, "col": col,
                    "msg": f"Token inválido: {lex_err!r} at line {linha} col {col}; contexto='{contexto}'"
                })
                i = k
                continue

            lexema = texto[i:i+tamanho_token]
            token_type = self.dfa.token_finals.get(ultimo_final, "UNKNOWN")
            tipo_final = "KEYWORD" if lexema in self.palavras_chave else token_type

            lookahead_idx = i + tamanho_token
            if (tipo_final in self.operator_types and
                lookahead_idx < n and
                texto[lookahead_idx] not in self.whitespace_chars and
                texto[lookahead_idx] in self.operator_start_chars):

                # tenta ver se a partir de lookahead_idx existe um operador/atrib válido
                next_tamanho, next_final = self._longest_match_from(texto, lookahead_idx)
                next_type = self.dfa.token_finals.get(next_final, None) if next_final is not None else None

                if next_final is not None and next_type in self.operator_types:
                    # marca erro sobre toda a sequência contígua sem whitespace
                    k = lookahead_idx + next_tamanho
                    # incluir também quaisquer operadores adicionais colados (ex: ====)
                    # estende k até o próximo whitespace
                    while k < n and texto[k] not in self.whitespace_chars:
                        k += 1
                    lex_err = texto[i:k]
                    linha, col = self._pos_from_index(texto, i)
                    contexto = texto[max(0, i-10):min(n, k+10)].replace("\n", "\\n")
                    erros.append({
                        "lexema": lex_err, "index": i, "line": linha, "col": col,
                        "msg": f"Token inválido composto: {lex_err!r} at line {linha} col {col}; contexto='{contexto}'"
                    })
                    i = k
                    continue

            # caso normal: aceita token
            tokens.append({"type": tipo_final, "lexeme": lexema, "index": i})
            i += tamanho_token

        return tokens, erros


# --- Teste rápido ---
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
        X === "TESTE
        
        a++b
        
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