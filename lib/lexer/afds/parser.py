from typing import List, Optional
from ast1 import *
from dataclasses import dataclass

# Exceção para erros de parsing
class ErroParser(Exception):
    def __init__(self, mensagem: str, token=None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.token = token
    def __str__(self):
        return self.mensagem

# Parser compatível com o Token do seu lexer (token.type, token.lexeme, token.line, token.col)
class Parser:
    def __init__(self, tokens: List):
        self.tokens = tokens
        self.posicao_atual = 0
        self.teve_erro = False
        self.modo_panico = False
        self.mensagens_erro: List[str] = []

    # ---------- utilitários ----------
    def peek(self):
        if self.posicao_atual >= len(self.tokens):
            return self.tokens[-1]  # deve haver EOF no fim
        return self.tokens[self.posicao_atual]

    def anterior(self):
        return self.tokens[self.posicao_atual - 1]

    def at_end(self):
        t = self.peek()
        return t.type == "EOF" or t.type == "FIM"  # tolerância

    def advance(self):
        if not self.at_end():
            self.posicao_atual += 1
        return self.anterior()

    # checa se token atual tem type exato OR é KEYWORD com lexeme = palavra (case-insensitive)
    def _is_keyword(self, palavra: str):
        t = self.peek()
        return (t.type == "KEYWORD" and t.lexeme.lower() == palavra.lower())

    # checa se token atual tem type em types (strings) OR (if a lexeme for fornecida) lexeme == symbol
    def _check(self, *types_or_lexemes):
        if self.at_end(): return False
        t = self.peek()
        for x in types_or_lexemes:
            # se x é string compare por tipo, por keyword-lexeme ou por lexeme textual
            if isinstance(x, str):
                if t.type == x:
                    return True
                if t.type == "KEYWORD" and t.lexeme.lower() == x.lower():
                    return True
                if getattr(t, "lexeme", None) == x:
                    return True
        return False

    def verificar(self, tipo_or_lexeme):
        return self._check(tipo_or_lexeme)

    def consumir(self, esperado, mensagem):
        if self._check(esperado):
            return self.advance()
        raise self.erro_parser(self.peek(), mensagem)

    def erro_parser(self, token, mensagem):
        self.reportar_erro(token, mensagem)
        raise ErroParser(mensagem, token)

    def reportar_erro(self, token, mensagem):
        if self.modo_panico:
            return
        self.teve_erro = True
        self.modo_panico = True
        localizacao = f"Linha {getattr(token, 'line', '?')}, coluna {getattr(token, 'col', '?')}"
        if token.type == "EOF":
            msg = f"Erro [{localizacao}]: {mensagem} (no fim do arquivo)"
        else:
            msg = f"Erro [{localizacao}]: {mensagem} (próximo a '{token.lexeme}')"
        self.mensagens_erro.append(msg)
        print(msg)

    def sincronizar(self):
        self.advance()
        while not self.at_end():
            # heurística: ponto-e-vírgula
            if getattr(self.anterior(), "lexeme", None) == ';' or self._check(';', 'PONTO_VIRGULA'):
                return
            # tokens que iniciam declarações/comandos
            if self._check('If', 'Print', 'FUNCTION', 'VAR', 'CLASS'):
                return
            self.advance()

    # ========== entrada ==========
    def parse_program(self):
        declaracoes = []
        while not self.at_end():
            try:
                declaracoes.append(self.parse_declaracao())
            except ErroParser:
                self.sincronizar()
        return NodoPrograma(declaracoes)

    # ---------- declarações ----------
    def parse_declaracao(self):
        self.modo_panico = False
        # funções/vars/classes opcionais (heurística)
        if self._check('FUNCTION', 'function'):
            return self.parse_declaracao_funcao()
        if self._check('VAR', 'var'):
            return self.parse_declaracao_variavel()
        if self._check('CLASS', 'class'):
            return self.parse_declaracao_classe()
        # senão é comando
        return self.parse_comando()

    def parse_declaracao_funcao(self):
        palavra = self.consumir('FUNCTION', "Esperado palavra-chave 'function'")
        nome = self.consumir('IDENTIFICADOR', "Esperado nome da função")
        self.consumir('(', "Esperado '(' após nome da função")
        parametros = []
        if not self._check(')'):
            while True:
                if len(parametros) >= 255:
                    self.erro_parser(self.peek(), "Não pode ter mais de 255 parâmetros")
                nome_param = self.consumir('IDENTIFICADOR', "Esperado nome do parâmetro")
                tipo_param = None
                if self._check(':', 'DOIS_PONTOS'):
                    self.advance()
                    token_tipo = self.consumir('IDENTIFICADOR', "Esperado tipo do parâmetro")
                    tipo_param = token_tipo.lexeme
                parametros.append(Parametro(nome_param.lexeme, tipo_param))
                if not self._check(','):
                    break
                self.advance()
        self.consumir(')', "Esperado ')' após parâmetros")
        tipo_retorno = None
        if self._check(':', 'DOIS_PONTOS'):
            self.advance()
            token_tipo = self.consumir('IDENTIFICADOR', "Esperado tipo de retorno")
            tipo_retorno = token_tipo.lexeme
        self.consumir('{', "Esperado '{' antes do corpo da função")
        corpo = self.parse_bloco()
        return NodoDeclaracaoFuncao(nome.lexeme, parametros, tipo_retorno, corpo, nome.line)

    def parse_declaracao_variavel(self):
        palavra = self.consumir('VAR', "Esperado 'var'")
        nome = self.consumir('IDENTIFICADOR', "Esperado nome da variável")
        tipo_explicito = None
        if self._check(':', 'DOIS_PONTOS'):
            self.advance()
            token_tipo = self.consumir('IDENTIFICADOR', "Esperado tipo da variável")
            tipo_explicito = token_tipo.lexeme
        inicializador = None
        if self._check('=', 'IGUAL', 'ATRIBUICAO'):
            self.advance()
            inicializador = self.parse_expressao()
        self.consumir(';', "Esperado ';' após declaração de variável")
        return NodoDeclaracaoVariavel(nome.lexeme, tipo_explicito, inicializador, palavra.line)

    def parse_declaracao_classe(self):
        palavra = self.consumir('CLASS', "Esperado 'class'")
        nome = self.consumir('IDENTIFICADOR', "Esperado nome da classe")
        self.consumir('{', "Esperado '{' antes do corpo da classe")
        metodos = []
        campos = []
        while not self._check('}', 'CHAVE_DIR') and not self.at_end():
            if self._check('FUNCTION', 'function'):
                metodos.append(self.parse_declaracao_funcao())
            elif self._check('VAR', 'var'):
                campos.append(self.parse_declaracao_variavel())
            else:
                raise self.erro_parser(self.peek(), "Esperado declaração de método ou campo na classe")
        self.consumir('}', "Esperado '}' após corpo da classe")
        return NodoDeclaracaoClasse(nome.lexeme, campos, metodos, palavra.line)

    # ---------- comandos ----------
    def parse_comando(self):
        # importante: reconhecer Print aqui antes de cair em comando_expressao
        if self._check('If', 'IF'):
            return self.parse_comando_if()
        if self._check('Print', 'PRINT'):
            return self.parse_print()
        if self._check('While', 'WHILE'):
            return self.parse_comando_while()
        if self._check('For', 'FOR'):
            return self.parse_comando_for()
        if self._check('Return', 'RETURN'):
            return self.parse_comando_return()
        if self._check('{', 'CHAVE_ESQ'):
            return self.parse_comando_bloco()
        # senao expressão
        return self.parse_comando_expressao()

    def parse_comando_if(self):
        palavra = self.consumir('If', "Esperado 'if'")
        # opcionalmente '(' e ')', mas na sua gramática LSD If Expression Statement End
        # adaptamos para aceitar ambos estilos: If (expr) stmt End  OR If expr stmt End
        has_paren = False
        if self._check('('):
            has_paren = True
            self.advance()
        cond = self.parse_expressao()
        if has_paren:
            self.consumir(')', "Esperado ')' após condição do if")
        # parsea statement ou bloco
        bloco_entao = self.parse_comando()
        bloco_senao = None
        if self._check('Else', 'ELSE'):
            self.advance()
            bloco_senao = self.parse_comando()
        # aceitar 'End' keyword opcional (sua gramática usa 'End' para fechar)
        if self._check('End', 'END'):
            self.advance()
        return NodoComandoIf(cond, bloco_entao, bloco_senao, palavra.line)

    def parse_comando_while(self):
        palavra = self.consumir('While', "Esperado 'while'")
        if self._check('('):
            self.advance()
        cond = self.parse_expressao()
        if self._check(')'):
            self.advance()
        corpo = self.parse_comando()
        return NodoComandoWhile(cond, corpo, palavra.line)

    def parse_comando_for(self):
        palavra = self.consumir('For', "Esperado 'for'")
        self.consumir('(', "Esperado '(' após 'for'")
        inicializador = None
        if self._check(';'):
            self.advance()
        elif self._check('VAR', 'var'):
            inicializador = self.parse_declaracao_variavel()
        else:
            inicializador = self.parse_comando_expressao()
        condicao = None
        if not self._check(';'):
            condicao = self.parse_expressao()
        self.consumir(';', "Esperado ';' após condição do for")
        incremento = None
        if not self._check(')'):
            incremento = self.parse_expressao()
        self.consumir(')', "Esperado ')' após cláusulas do for")
        corpo = self.parse_comando()
        return NodoComandoFor(inicializador, condicao, incremento, corpo, palavra.line)

    def parse_comando_return(self):
        palavra = self.consumir('Return', "Esperado 'return'")
        valor = None
        if not self._check(';'):
            valor = self.parse_expressao()
        self.consumir(';', "Esperado ';' após return")
        return NodoComandoReturn(valor, palavra.line)

    def parse_comando_bloco(self):
        chave = self.consumir('{', "Esperado '{'")
        comandos = self.parse_bloco()
        return NodoComandoBloco(comandos, chave.line)

    def parse_bloco(self):
        comandos = []
        while not self._check('}', 'CHAVE_DIR') and not self.at_end():
            comandos.append(self.parse_declaracao())
        self.consumir('}', "Esperado '}' após bloco")
        return comandos

    def parse_comando_expressao(self):
        linha = getattr(self.peek(), "line", 0)
        expr = self.parse_expressao()
        # aceitar ; ou fim (se houver)
        if self._check(';'):
            self.advance()
        return NodoComandoExpressao(expr, linha)

    # ---------- novo: parsing de Print ----------
    def parse_print(self):
        palavra = self.consumir('Print', "Esperado 'Print'")
        linha = palavra.line
        # aceitar forma com parênteses: Print( ... )
        used_paren = False
        if self._check('('):
            used_paren = True
            self.advance()

        # se próximo for string literal, consumir como literal
        if self._check('STRING', 'string_literal'):
            t = self.advance()
            lex = t.lexeme
            if len(lex) >= 2 and ((lex[0] == '"' and lex[-1] == '"') or (lex[0] == "'" and lex[-1] == "'")):
                valor = lex[1:-1]
            else:
                valor = lex
            expr_node = NodoExpressaoLiteral(valor, t.line)
        else:
            # caso padrão: aceitar uma expressão
            expr_node = self.parse_expressao()

        if used_paren:
            # se abriu paren, fecha
            self.consumir(')', "Esperado ')' após argumentos de Print")

        # opcionalmente consumir ';' se houver
        if self._check(';'):
            self.advance()

        # por enquanto representamos Print como um NodoComandoExpressao contendo a expressão/literal
        return NodoComandoExpressao(expr_node, linha)

    # ---------- expressões (precedência) ----------
    def parse_expressao(self):
        return self.parse_atribuicao()

    def parse_atribuicao(self):
        esquerda = self.parse_ou_logico()
        if self._check('=', 'IGUAL', 'ATRIBUICAO'):
            operador = self.advance()
            valor = self.parse_atribuicao()
            if isinstance(esquerda, NodoExpressaoVariavel):
                return NodoExpressaoAtribuicao(esquerda.nome, valor, operador.line)
            raise self.erro_parser(operador, "Alvo de atribuição inválido")
        return esquerda

    def parse_ou_logico(self):
        esquerda = self.parse_e_logico()
        while self._check('OU', 'OR'):
            op = self.advance()
            direita = self.parse_e_logico()
            esquerda = NodoExpressaoBinaria(op.lexeme, esquerda, direita, op.line)
        return esquerda

    def parse_e_logico(self):
        esquerda = self.parse_igualdade()
        while self._check('E', 'AND'):
            op = self.advance()
            direita = self.parse_igualdade()
            esquerda = NodoExpressaoBinaria(op.lexeme, esquerda, direita, op.line)
        return esquerda

    def parse_igualdade(self):
        esquerda = self.parse_comparacao()
        while self._check('==', 'IGUAL_IGUAL', '!=', 'DIFERENTE'):
            op = self.advance()
            direita = self.parse_comparacao()
            esquerda = NodoExpressaoBinaria(op.lexeme, esquerda, direita, op.line)
        return esquerda

    def parse_comparacao(self):
        esquerda = self.parse_adicao()
        while self._check('>', 'MAIOR') or self._check('<', 'MENOR') or self._check('>=', 'MAIOR_IGUAL') or self._check('<=', 'MENOR_IGUAL'):
            op = self.advance()
            direita = self.parse_adicao()
            esquerda = NodoExpressaoBinaria(op.lexeme, esquerda, direita, op.line)
        return esquerda

    def parse_adicao(self):
        esquerda = self.parse_multiplicacao()
        while self._check('+', 'MAIS') or self._check('-', 'MENOS'):
            op = self.advance()
            direita = self.parse_multiplicacao()
            esquerda = NodoExpressaoBinaria(op.lexeme, esquerda, direita, op.line)
        return esquerda

    def parse_multiplicacao(self):
        esquerda = self.parse_unario()
        while self._check('*', 'VEZES') or self._check('/', 'DIVIDE') or self._check('%', 'MODULO'):
            op = self.advance()
            direita = self.parse_unario()
            esquerda = NodoExpressaoBinaria(op.lexeme, esquerda, direita, op.line)
        return esquerda

    def parse_unario(self):
        if self._check('!', 'NAO') or self._check('-', 'MENOS'):
            op = self.advance()
            direita = self.parse_unario()
            return NodoExpressaoUnaria(op.lexeme, direita, op.line)
        return self.parse_chamada()

    def parse_chamada(self):
        expr = self.parse_primario()
        while True:
            if self._check('('):
                expr = self.finalizar_chamada(expr)
            elif self._check('.', 'PONTO'):
                self.advance()
                nome = self.consumir('IDENTIFICADOR', "Esperado nome de propriedade após '.'")
                expr = NodoExpressaoAcesso(expr, nome.lexeme, nome.line)
            else:
                break
        return expr

    def finalizar_chamada(self, funcao_expr):
        paren = self.consumir('(', "Esperado '('")
        argumentos = []
        if not self._check(')'):
            while True:
                if len(argumentos) >= 255:
                    self.erro_parser(self.peek(), "Não pode ter mais de 255 argumentos")
                argumentos.append(self.parse_expressao())
                if not self._check(','):
                    break
                self.advance()
        self.consumir(')', "Esperado ')' após argumentos")
        return NodoExpressaoChamada(funcao_expr, argumentos, paren.line)

    def parse_primario(self):
        # true/false/null handling (if lexer produces these tokens)
        if self._check('TRUE', 'true'):
            t = self.advance()
            return NodoExpressaoLiteral(True, t.line)
        if self._check('FALSE', 'false'):
            t = self.advance()
            return NodoExpressaoLiteral(False, t.line)
        if self._check('NULL', 'null'):
            t = self.advance()
            return NodoExpressaoLiteral(None, t.line)

        # numeros: seu lexer distingue INTEIRO/DECIMAL - adaptamos
        # if self._CheckNumeric = None:  # placeholder to avoid linter issue
        #     pass

        if self._check('INTEIRO', 'integer_literal', 'NUMERO'):
            t = self.advance()
            try:
                val = int(t.lexeme)
            except Exception:
                val = int(float(t.lexeme))
            return NodoExpressaoLiteral(val, t.line)
        if self._check('DECIMAL', 'decimal_literal', 'NUMERO_DECIMAL'):
            t = self.advance()
            val = float(t.lexeme)
            return NodoExpressaoLiteral(val, t.line)

        # string
        if self._check('STRING', 'string_literal'):
            t = self.advance()
            lex = t.lexeme
            # tenta remover aspas se presentes
            if len(lex) >= 2 and ((lex[0] == '"' and lex[-1] == '"') or (lex[0] == "'" and lex[-1] == "'")):
                valor = lex[1:-1]
            else:
                valor = lex
            return NodoExpressaoLiteral(valor, t.line)

        # identifier (variável ou chamada)
        if self._check('IDENTIFICADOR', 'identifier'):
            t = self.advance()
            return NodoExpressaoVariavel(t.lexeme, t.line)

        # agrupamento
        if self._check('('):
            paren = self.advance()
            expr = self.parse_expressao()
            self.consumir(')', "Esperado ')' após expressão")
            return NodoExpressaoAgrupamento(expr, paren.line)

        raise self.erro_parser(self.peek(), "Esperado expressão")
