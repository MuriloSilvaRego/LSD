# --- lexer3_adaptado.py ---
from AFN import dfa, dfa_rev  # mantém compatibilidade
from typing import Optional

class Token:
    def __init__(self, tipo, lexema, linha, coluna):
        self.type = tipo
        self.lexeme = lexema
        self.line = linha
        self.col = coluna

    def __repr__(self):
        return f"Token({self.type!r}, {self.lexeme!r}, line={self.line}, col={self.col})"

class InputBuffer:
    def __init__(self, texto: str):
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

class Lexer:
    def __init__(self, palavras_chave=None, dfa_obj=None, ignorar_whitespace=True):
        # permite passar dfa explicitamente (ou usa importado)
        self.dfa = dfa_obj if dfa_obj is not None else dfa
        self.dfa_rev = dfa_rev

        # validar formato mínimo do DFA e dar mensagens úteis
        self._validate_dfa_shape()

        raw_kws = palavras_chave or ["If", "Print", "CalculateMean", "CalculateSum", "End"]
        self.palavras_chave = set(k.lower() for k in raw_kws)

        self.ignorar_whitespace = ignorar_whitespace
        self.whitespace_chars = set(" \t\r\n")

        # heurísticas opcionais
        self.operator_start_chars = set("+-*/%=!<>&|^:.?")
        self.operator_types = {"OPERADOR", "ATRIBUICAO"}

    def _validate_dfa_shape(self):
        # checagens leves para dar mensagens claras
        missing = []
        for attr in ("inicial", "finais", "transicoes", "token_finals"):
            if not hasattr(self.dfa, attr):
                missing.append(attr)
        if missing:
            raise ValueError(f"DFA fornecido está incompleto — faltando atributos: {missing}. "
                             "O DFA deve ter 'inicial', 'finais', 'transicoes', 'token_finals'.")

    def _pos_from_index(self, texto, index):
        linha = texto.count("\n", 0, index) + 1
        ultimo_n = texto.rfind("\n", 0, index)
        col = index - ultimo_n if ultimo_n != -1 else index + 1
        return linha, col

    def _longest_match_from(self, texto, start):
        """
        Percorre transições do DFA consumindo caractere a caractere.
        Retorna (tamanho_do_lexema, estado_final_ultimo_reconhecido)
        """
        estado = self.dfa.inicial
        ultimo_final = None
        tamanho = 0
        j = start
        n = len(texto)

        # Se o DFA usar transições com chaves não-exatas, este método
        # precisa ser alinhado com a representação do seu DFA.
        while j < n:
            c = texto[j]
            trans_row = self.dfa.transicoes.get(estado)
            if not trans_row:
                break

            # trans_row é esperado como dict: símbolo_char -> próximo_estado
            # se seu DFA usa classes (ex: 'DIGIT') você pode adaptar aqui
            if c not in trans_row:
                break
            estado = trans_row[c]
            j += 1
            if estado in self.dfa.finais:
                ultimo_final = estado
                tamanho = j - start
        return tamanho, ultimo_final

    def next_token(self, buffer: InputBuffer):
        texto = buffer.texto
        n = buffer.len

        # consumir whitespace
        while not buffer.at_end() and self.ignorar_whitespace and buffer.peek() in self.whitespace_chars:
            buffer.next()

        if buffer.at_end():
            return Token("EOF", "", -1, -1), None

        i = buffer.index()
        tamanho, ultimo_final = self._longest_match_from(texto, i)

        if ultimo_final is None or tamanho == 0:
            # erro léxico: avançar minimamente para evitar loop infinito
            k = i + 1
            while k < n and texto[k] not in self.whitespace_chars:
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

        lexema = texto[i:i+tamanho]
        ultimo_final_state = ultimo_final
        # depois de obter lexema e token_type do DFA:
        token_type = self.dfa.token_finals.get(ultimo_final_state, "UNKNOWN")
        if token_type == "IDENTIFIER" and lexema.lower() in self.palavras_chave:
            # usar nome do keyword como token type (preserva qual keyword)
            tipo_final = lexema  # ou lexema.capitalize() / lexema.upper() conforme sua convenção
        else:
            tipo_final = token_type


        tipo_final = "KEYWORD" if lexema.lower() in self.palavras_chave else token_type
        linha, col = self._pos_from_index(texto, i)
        buffer.advance(tamanho)

        tok = Token(tipo_final, lexema, linha, col)
        return tok, None

    def tokenize(self, texto):
        buffer = InputBuffer(texto)
        tokens = []
        erros = []
        safety_counter = 0
        max_steps = max(1000000, len(texto) * 20)  # evita loops infinitos

        while True:
            safety_counter += 1
            if safety_counter > max_steps:
                raise RuntimeError("Tokenization exceeded maximum steps — possível loop infinito.")

            tok, err = self.next_token(buffer)
            if err:
                erros.append(err)
                # continue (já avançamos no buffer em caso de erro)
                if buffer.at_end():
                    break
                else:
                    continue
            if tok is None:
                # segurança: se None e não erro, avança 1 char para não travar
                if not buffer.at_end():
                    buffer.advance(1)
                    continue
                else:
                    break
            if tok.type == "EOF":
                tokens.append(tok)
                break
            # filtragem opcional (quem chama decide se quer filtrar)
            if tok.type in ("COMENTARIO", "SEPARADOR"):
                continue
            tokens.append(tok)
        return tokens, erros

# fim lexer3_adaptado.py
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