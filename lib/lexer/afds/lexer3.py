from AFN import dfa  # importa o DFA pronto
from AFN import dfa_rev

# --- estruturas simples ---
class Token:
    def __init__(self, tipo, lexema, linha, coluna):
        self.type = tipo
        self.lexeme = lexema
        self.line = linha
        self.col = coluna

    def __repr__(self):
        return f"Token({self.type!r}, {self.lexeme!r}, line={self.line}, col={self.col})"

class InputBuffer:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.len = len(texto)

    def peek(self, offset=0):
        idx = self.pos + offset
        return self.texto[idx] if idx < self.len else None

    def next(self):
        if self.pos < self.len:
            ch = self.texto[self.pos]
            self.pos += 1
            return ch
        return None

    def advance(self, n):
        self.pos = min(self.len, self.pos + n)

    def rollback(self, n):
        self.pos = max(0, self.pos - n)

    def at_end(self):
        return self.pos >= self.len

    def index(self):
        return self.pos

# --- Lexer ---
class Lexer:
    def __init__(self, palavras_chave=None):
        # DFA importado
        self.dfa = dfa
        self.dfa_rev = dfa_rev

        # palavras-chave armazenadas em lowercase para case-insensitive
        raw_kws = palavras_chave or ["If", "Print", "CalculateMean", "CalculateSum", "End"]
        self.palavras_chave = set(k.lower() for k in raw_kws)

        self.ignorar_whitespace = True
        self.whitespace_chars = set(" \t\r\n")

        # caracteres que podem iniciar operadores/atribuição (para heurística, opcional)
        self.operator_start_chars = set("+-*/%=!<>&|^:.?")

        # tipos considerados operacionais para regra composta (se precisar)
        self.operator_types = {"OPERADOR", "ATRIBUICAO"}

    def _pos_from_index(self, texto, index):
        linha = texto.count("\n", 0, index) + 1
        ultimo_n = texto.rfind("\n", 0, index)
        col = index - ultimo_n if ultimo_n != -1 else index + 1
        return linha, col

    # percorre DFA consumindo chars a partir do índice start e retorna (tamanho, ultimo_final_state)
    def _longest_match_from(self, texto, start):
        estado = self.dfa.inicial
        ultimo_final = None
        tamanho = 0
        j = start
        n = len(texto)
        # enquanto houver transição para o próximo caractere
        while j < n:
            c = texto[j]
            trans_row = self.dfa.transicoes.get(estado)
            if not trans_row:
                break
            # transições no seu DFA são indexadas por símbolo exato (assumindo single-char symbols)
            if c not in trans_row:
                break
            estado = trans_row[c]
            j += 1
            if estado in self.dfa.finais:
                ultimo_final = estado
                tamanho = j - start
        return tamanho, ultimo_final

    # next_token: interface para parser
    def next_token(self, buffer):
        texto = buffer.texto
        n = buffer.len

        # avançar sobre whitespace se necessário
        while not buffer.at_end() and self.ignorar_whitespace and buffer.peek() in self.whitespace_chars:
            buffer.next()

        if buffer.at_end():
            return Token("EOF", "", -1, -1), None

        i = buffer.index()
        tamanho, ultimo_final = self._longest_match_from(texto, i)

        if ultimo_final is None or tamanho == 0:
            # erro léxico: consumir até próximo whitespace ou caractere reconhecível minimamente
            k = i + 1
            while k < n and texto[k] not in self.whitespace_chars:
                # tentativa simples: se um próximo prefixo for reconhecível, parar antes dele
                look_t, look_f = self._longest_match_from(texto, k)
                if look_f is not None:
                    break
                k += 1
            lex_err = texto[i:k]
            linha, col = self._pos_from_index(texto, i)
            contexto = texto[max(0, i-10):min(n, k+10)].replace("\n", "\\n")
            erro = {
                "lexema": lex_err,
                "index": i,
                "line": linha,
                "col": col,
                "msg": f"Token inválido: {lex_err!r} at line {linha} col {col}; contexto='{contexto}'"
            }
            # avança buffer para não travar
            buffer.advance(max(1, k - i))
            return None, erro

        # temos um match; extrai lexema e tipo
        lexema = texto[i:i+tamanho]
        ultimo_final_state = ultimo_final
        token_type = self.dfa.token_finals.get(ultimo_final_state, "UNKNOWN")

        # palavras-chave case-insensitive
        tipo_final = "KEYWORD" if lexema.lower() in self.palavras_chave else token_type

        # posição linha/coluna
        linha, col = self._pos_from_index(texto, i)

        # avança buffer
        buffer.advance(tamanho)

        tok = Token(tipo_final, lexema, linha, col)
        return tok, None

    # tokenizer que retorna listas (útil para testes)
    def tokenize(self, texto):
        buffer = InputBuffer(texto)
        tokens = []
        erros = []
        while True:
            tok, err = self.next_token(buffer)
            if err:
                erros.append(err)
                continue
            if tok is None:
                # caso safety, seguir
                continue
            if tok.type == "EOF":
                tokens.append(tok)
                break
            # ignorar comentários e separadores no output, se desejado
            if tok.type == "COMENTARIO":
                continue
            if tok.type == "SEPARADOR":
                continue
            tokens.append(tok)
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
        print(f"{t.type:12} {t.lexeme!r:20} (line={t.line} col={t.col})")

    if erros:
        print("\nErros léxicos:")
        for e in erros:
            print(e["msg"])
    else:
        print("\nNenhum erro léxico encontrado.")
