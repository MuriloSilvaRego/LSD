# parser_lsd.py
from token_lsd import TipoToken, Token as TokenInterno
from ast_lsd import *

# Mapeamento robusto de tokens externos (do lexer3.py) para TipoToken do parser
def map_external_token(ext_tok):
    # tenta coletar atributos do token externo com vários nomes possíveis
    tok_type = getattr(ext_tok, "type", None)
    if tok_type is None:
        tok_type = getattr(ext_tok, "tipo", None)
    if tok_type is None:
        tok_type = getattr(ext_tok, "tag", None)
    if tok_type is None:
        tok_type = getattr(ext_tok, "kind", None)

    lexeme = getattr(ext_tok, "lexeme", None)
    if lexeme is None:
        lexeme = getattr(ext_tok, "lexema", None)
    if lexeme is None:
        lexeme = getattr(ext_tok, "value", None)
    if lexeme is None:
        lexeme = ""

    linha = getattr(ext_tok, "line", None)
    if linha is None:
        linha = getattr(ext_tok, "linha", None)
    if linha is None:
        linha = getattr(ext_tok, "lin", -1)
    if linha is None:
        linha = -1

    coluna = getattr(ext_tok, "col", None)
    if coluna is None:
        coluna = getattr(ext_tok, "coluna", None)
    if coluna is None:
        coluna = -1

    # Normalize strings
    if isinstance(tok_type, str):
        tok_type_up = tok_type.upper()
    else:
        tok_type_up = str(tok_type).upper()

    lex_low = lexeme.lower() if isinstance(lexeme, str) else ""

    # Map token type by known external categories
    # Primeiro lidar com keywords (se lexer rotulou como KEYWORD)
    if tok_type_up in ("KEYWORD", "PALAVRA_CHAVE"):
        if lex_low == "if":
            mapped = TipoToken.IF
        elif lex_low == "print":
            mapped = TipoToken.PRINT
        elif lex_low == "end":
            mapped = TipoToken.END
        else:
            # outras keywords possíveis
            mapped = TipoToken.IDENT
    elif tok_type_up in ("IDENT", "IDENTIFICADOR", "ID", "VARIABLE"):
        mapped = TipoToken.IDENT
    elif tok_type_up in ("INTEIRO", "INT", "INTEGER", "NUMBER"):
        mapped = TipoToken.INT_LIT
    elif tok_type_up in ("DECIMAL", "DEC", "DECIMAL_LITERAL", "FLOAT"):
        mapped = TipoToken.DEC_LIT
    elif tok_type_up in ("STRING", "STR", "STRING_LITERAL"):
        mapped = TipoToken.STR_LIT
    elif tok_type_up in ("EOF",):
        mapped = TipoToken.EOF
    elif tok_type_up in ("OPERADOR", "OPERATOR", "SYMBOL"):
        # decide pelo lexema (caractere real)
        if lexeme == "=":
            mapped = TipoToken.EQ
        elif lexeme == "+":
            mapped = TipoToken.PLUS
        elif lexeme == "-":
            mapped = TipoToken.MINUS
        elif lexeme == "*":
            mapped = TipoToken.STAR
        elif lexeme == "/":
            mapped = TipoToken.SLASH
        elif lexeme == "(":
            mapped = TipoToken.LPAREN
        elif lexeme == ")":
            mapped = TipoToken.RPAREN
        elif lexeme == "[":
            mapped = TipoToken.LBRACK
        elif lexeme == "]":
            mapped = TipoToken.RBRACK
        elif lexeme == ",":
            mapped = TipoToken.COMMA
        elif lexeme == ">":
            mapped = TipoToken.GT
        elif lexeme == "<":
            mapped = TipoToken.LT
        elif lexeme == ">=":
            mapped = TipoToken.GE
        elif lexeme == "<=":
            mapped = TipoToken.LE
        elif lexeme == "==":
            mapped = TipoToken.EQEQ
        elif lexeme == "!=":
            mapped = TipoToken.NEQ
        else:
            # se for operador não mapeado, tratar como IDENT secundário
            mapped = TipoToken.IDENT
    else:
        # tentativa heurística: se lexema é um símbolo conhecido
        if lexeme == "(":
            mapped = TipoToken.LPAREN
        elif lexeme == ")":
            mapped = TipoToken.RPAREN
        elif lexeme == "[":
            mapped = TipoToken.LBRACK
        elif lexeme == "]":
            mapped = TipoToken.RBRACK
        elif lexeme == ",":
            mapped = TipoToken.COMMA
        elif lexeme == "+":
            mapped = TipoToken.PLUS
        elif lexeme == "-":
            mapped = TipoToken.MINUS
        elif lexeme == "*":
            mapped = TipoToken.STAR
        elif lexeme == "/":
            mapped = TipoToken.SLASH
        elif lexeme == "=":
            mapped = TipoToken.EQ
        elif tok_type_up == "EOF":
            mapped = TipoToken.EOF
        else:
            # fallback: tratar como identificador
            mapped = TipoToken.IDENT

    # criar token interno que o parser espera (tipo: TipoToken enum)
    return TokenInterno(mapped, lexeme, linha, coluna)


class ParserLSD:

    def __init__(self, external_tokens):
        # converte tokens externos (do lexer3.py) para tokens internos que o parser usa
        self.tokens = [map_external_token(t) for t in external_tokens]
        # garante EOF final
        if not self.tokens or self.tokens[-1].tipo != TipoToken.EOF:
            self.tokens.append(TokenInterno(TipoToken.EOF, "", -1, -1))

        self.pos = 0
        self.modo_panico = False
        self.teve_erro = False
        self.mensagens_erro = []

    # utilidades -----------------------------------------------------

    def is_at_end(self):
        return self.peek().tipo == TipoToken.EOF

    def peek(self):
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]

    def previous(self):
        # previous seguro: se pos == 0, retorna primeiro token
        if self.pos <= 0:
            return self.tokens[0]
        return self.tokens[self.pos - 1]

    def advance(self):
        if not self.is_at_end():
            self.pos += 1
        return self.previous()

    def verificar(self, tipo):
        if self.is_at_end():
            return False
        return self.peek().tipo == tipo

    def consumir(self, tipo, msg):
        if self.verificar(tipo):
            return self.advance()
        raise self.erro(self.peek(), msg)

    def erro(self, token, mensagem):
        if not self.modo_panico:
            self.teve_erro = True
            self.modo_panico = True
            txt = f"Erro na linha {token.linha}, coluna {token.coluna}: {mensagem}"
            self.mensagens_erro.append(txt)
            print(txt)
        return Exception(mensagem)

    def sincronizar(self):
        # Avança um token (se possível)
        if not self.is_at_end():
            self.advance()
        # caminha até um ponto de sincronização
        while not self.is_at_end():
            if self.previous().tipo == TipoToken.EOF:
                return
            if self.peek().tipo in (TipoToken.IF, TipoToken.PRINT, TipoToken.END, TipoToken.EOF):
                self.modo_panico = False
                return
            self.advance()

    # =========================================================
    # Programa
    # =========================================================

    def parsear_programa(self):
        statements = []
        while not self.is_at_end():
            try:
                st = self.parsear_statement()
                if st:
                    statements.append(st)
            except Exception:
                # Em caso de erro, sincroniza e continua
                self.sincronizar()
        return NodoPrograma(statements)

    # =========================================================
    # Statements
    # =========================================================

    def parsear_statement(self):
        try:
            self.modo_panico = False

            if self.verificar(TipoToken.IDENT):
                # Lookahead para assignment
                salv = self.pos
                id_tok = self.advance()

                if self.verificar(TipoToken.EQ):
                    self.advance()  # consome '='
                    expr = self.parsear_expression()
                    return NodoAssignment(id_tok.lexema, expr, id_tok.linha)

                # rollback se não for assignment
                self.pos = salv
                return self.parsear_expression_statement()

            if self.verificar(TipoToken.IF):
                return self.parsear_if_statement()

            if self.verificar(TipoToken.PRINT):
                return self.parsear_print_statement()

            if self.verificar(TipoToken.EOF):
                return None

            raise self.erro(self.peek(), "Esperado statement.")

        except Exception:
            self.sincronizar()
            return None

    def parsear_print_statement(self):
        t = self.consumir(TipoToken.PRINT, "Esperado 'Print'")
        expr = self.parsear_expression()
        return NodoPrint(expr, t.linha)

    def parsear_if_statement(self):
        t = self.consumir(TipoToken.IF, "Esperado 'If'")
        cond = self.parsear_expression()

        corpo = []
        while (not self.verificar(TipoToken.END)) and (not self.is_at_end()):
            st = self.parsear_statement()
            if st:
                corpo.append(st)

        self.consumir(TipoToken.END, "Esperado 'End'")
        return NodoIf(cond, corpo, t.linha)

    def parsear_expression_statement(self):
        linha = self.peek().linha
        expr = self.parsear_expression()
        # a gramática LSD não usa ';' — então tratamos expressão isolada como assignment-wrapper
        return NodoAssignment("__expr__", expr, linha)

    # =========================================================
    # Expressões
    # =========================================================

    def parsear_expression(self):
        return self.parsear_relational()

    def parsear_relational(self):
        expr = self.parsear_additive()

        while self.verificar(TipoToken.GT) or self.verificar(TipoToken.LT) \
            or self.verificar(TipoToken.GE) or self.verificar(TipoToken.LE) \
            or self.verificar(TipoToken.EQEQ) or self.verificar(TipoToken.NEQ):

            op = self.advance()
            right = self.parsear_additive()
            return_expr = NodoBinary(op.lexema, expr, right, op.linha)
            expr = return_expr

        return expr

    def parsear_additive(self):
        expr = self.parsear_multiplicative()

        while self.verificar(TipoToken.PLUS) or self.verificar(TipoToken.MINUS):
            op = self.advance()
            right = self.parsear_multiplicative()
            expr = NodoBinary(op.lexema, expr, right, op.linha)

        return expr

    def parsear_multiplicative(self):
        expr = self.parsear_unary()

        while self.verificar(TipoToken.STAR) or self.verificar(TipoToken.SLASH):
            op = self.advance()
            right = self.parsear_unary()
            expr = NodoBinary(op.lexema, expr, right, op.linha)

        return expr

    def parsear_unary(self):
        if self.verificar(TipoToken.PLUS) or self.verificar(TipoToken.MINUS):
            op = self.advance()
            right = self.parsear_unary()
            return NodoUnary(op.lexema, right, op.linha)

        return self.parsear_primary()

    # =========================================================
    # Primary
    # =========================================================

    def parsear_primary(self):
        # Literais
        if self.verificar(TipoToken.INT_LIT):
            t = self.advance()
            try:
                val = int(t.lexema)
            except Exception:
                val = float(t.lexema)
            return NodoLiteral(val, t.linha)

        if self.verificar(TipoToken.DEC_LIT):
            t = self.advance()
            return NodoLiteral(float(t.lexema), t.linha)

        if self.verificar(TipoToken.STR_LIT):
            t = self.advance()
            s = t.lexema
            if len(s) >= 2 and (s[0] == s[-1] == "'" or s[0] == s[-1] == '"'):
                s = s[1:-1]
            return NodoLiteral(s, t.linha)

        # Lista
        if self.verificar(TipoToken.LBRACK):
            t = self.advance()
            elementos = []
            if not self.verificar(TipoToken.RBRACK):
                elementos.append(self.parsear_expression())
                while self.verificar(TipoToken.COMMA):
                    self.advance()
                    elementos.append(self.parsear_expression())
            self.consumir(TipoToken.RBRACK, "Esperado ']' após lista")
            return NodoListExpr(elementos, t.linha)

        # Identificador / chamada
        if self.verificar(TipoToken.IDENT):
            id_tok = self.advance()

            if self.verificar(TipoToken.LPAREN):
                self.advance()
                args = []
                if not self.verificar(TipoToken.RPAREN):
                    args.append(self.parsear_expression())
                    while self.verificar(TipoToken.COMMA):
                        self.advance()
                        args.append(self.parsear_expression())
                self.consumir(TipoToken.RPAREN, "Esperado ')'")
                return NodoCall(NodoVariable(id_tok.lexema, id_tok.linha), args, id_tok.linha)

            return NodoVariable(id_tok.lexema, id_tok.linha)

        # Parênteses
        if self.verificar(TipoToken.LPAREN):
            self.advance()
            expr = self.parsear_expression()
            self.consumir(TipoToken.RPAREN, "Esperado ')'")
            return expr

        raise self.erro(self.peek(), "Esperado expressão")
