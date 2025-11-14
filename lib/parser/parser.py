"""
Parser recursivo descendente para a linguagem LSD.
Implementa a gramática definida em grammar.md.
"""

from typing import List, Optional
import sys
import os

# Adiciona o diretório do lexer ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer', 'afds'))

from lexer3 import Lexer, Token, InputBuffer
from lsd_ast import (
    Program, Statement, Assignment, ConditionalStatement, PrintStatement,
    Expression, RelationalExpression, AdditiveExpression, MultiplicativeExpression,
    UnaryExpression, PrimaryExpression, IntegerLiteral, DecimalLiteral,
    StringLiteral, Identifier, FunctionCall, ListExpression, ParenthesizedExpression
)


class ParseError(Exception):
    """Exceção para erros de parsing."""
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        if token:
            super().__init__(f"{message} at line {token.line}, col {token.col}")
        else:
            super().__init__(message)


class Parser:
    """Parser recursivo descendente para LSD."""
    
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.tokens: List[Token] = []
        self.current = 0
        self.errors: List[str] = []
    
    def parse(self, source: str) -> Program:
        """Parse o código fonte e retorna a AST."""
        # Tokeniza sem filtrar separadores para poder detectar erros
        from lexer3 import InputBuffer
        buffer = InputBuffer(source)
        tokens = []
        erros = []
        safety_counter = 0
        max_steps = max(1000000, len(source) * 20)
        
        while True:
            safety_counter += 1
            if safety_counter > max_steps:
                raise RuntimeError("Tokenization exceeded maximum steps")
            
            tok, err = self.lexer.next_token(buffer)
            if err:
                erros.append(err)
                if buffer.at_end():
                    break
                else:
                    continue
            if tok is None:
                if not buffer.at_end():
                    buffer.advance(1)
                    continue
                else:
                    break
            if tok.type == "EOF":
                tokens.append(tok)
                break
            # Não filtra aqui - vamos filtrar depois mantendo separadores importantes
            tokens.append(tok)
        
        if erros:
            for err in erros:
                msg = err.get('msg', 'Erro desconhecido')
                line = err.get('line', 0)
                col = err.get('col', 0)
                self.errors.append(f"Erro léxico na linha {line}, coluna {col}: {msg}")
        
        # Filtra tokens, mantendo SEPARADOR importantes para detectar erros de sintaxe
        separadores_importantes = {"(", ")", "[", "]", ","}
        self.tokens = [
            t for t in tokens
            if t.type != "EOF" and (
                (t.type == "SEPARADOR" and t.lexeme in separadores_importantes) or
                (t.type != "SEPARADOR" and t.type != "COMENTARIO")
            )
        ]
        
        if not self.tokens:
            return Program(statements=[], line=1, col=1)
        
        try:
            program = self.parse_program()
            
            # Verifica se há tokens restantes (erro de sintaxe)
            if self.current_token():
                token = self.current_token()
                raise ParseError(
                    f"Token inesperado após o fim do programa: {token.type!r} ('{token.lexeme}')",
                    token
                )
            
            return program
        except ParseError as e:
            self.errors.append(str(e))
            raise
    
    def current_token(self) -> Optional[Token]:
        """Retorna o token atual."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None
    
    def peek_token(self, offset: int = 0) -> Optional[Token]:
        """Retorna o token na posição current + offset."""
        idx = self.current + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return None
    
    def advance(self) -> Optional[Token]:
        """Avança para o próximo token."""
        if self.current < len(self.tokens):
            self.current += 1
        return self.current_token()
    
    def match(self, *expected_types: str) -> bool:
        """Verifica se o token atual é um dos tipos esperados."""
        token = self.current_token()
        if token and token.type in expected_types:
            return True
        return False
    
    def consume(self, *expected_types: str) -> Token:
        """Consome um token do tipo esperado ou lança erro."""
        token = self.current_token()
        if not token:
            expected_str = " ou ".join(expected_types)
            raise ParseError(
                f"Esperado {expected_str}, mas encontrado fim do arquivo",
                None
            )
        
        if token.type not in expected_types:
            expected_str = " ou ".join(expected_types)
            raise ParseError(
                f"Esperado {expected_str}, mas encontrado {token.type!r} ('{token.lexeme}') na linha {token.line}, coluna {token.col}",
                token
            )
        
        self.advance()
        return token
    
    def consume_keyword(self, keyword: str) -> Token:
        """Consome uma palavra-chave (case-insensitive)."""
        token = self.current_token()
        if not token:
            raise ParseError(
                f"Esperado palavra-chave '{keyword}', mas encontrado fim do arquivo",
                None
            )
        
        # Verifica se é a keyword esperada (pode ser tipo KEYWORD ou o lexeme)
        is_keyword = (token.type.upper() == keyword.upper() or 
                     token.type == "KEYWORD" or
                     token.lexeme.upper() == keyword.upper())
        
        if not is_keyword:
            raise ParseError(
                f"Esperado palavra-chave '{keyword}', mas encontrado {token.type!r} ('{token.lexeme}') na linha {token.line}, coluna {token.col}",
                token
            )
        
        self.advance()
        return token
    
    def consume_operator(self, operator: str) -> Token:
        """Consome um operador específico."""
        token = self.current_token()
        if not token:
            raise ParseError(
                f"Esperado operador '{operator}', mas encontrado fim do arquivo",
                None
            )
        
        # Verifica se é operador e se o lexeme corresponde
        if token.type != "OPERADOR" or token.lexeme != operator:
            # Também pode ser um separador para parênteses/colchetes
            if operator in {"(", ")", "[", "]"} and token.lexeme == operator:
                self.advance()
                return token
            raise ParseError(
                f"Esperado operador '{operator}', mas encontrado {token.type!r} ('{token.lexeme}') na linha {token.line}, coluna {token.col}",
                token
            )
        
        self.advance()
        return token
    
    # ============ Métodos de parsing ============
    
    def parse_program(self) -> Program:
        """Program = StatementList"""
        statements = self.parse_statement_list()
        return Program(statements=statements, line=1, col=1)
    
    def parse_statement_list(self) -> List[Statement]:
        """StatementList = Statement { Statement }"""
        statements = []
        
        while self.current_token() and self._is_statement_start():
            stmt = self.parse_statement()
            statements.append(stmt)
            # Após parsear um statement, verifica se o próximo token é "End"
            # Se for, não tenta parsear mais statements
            if self.current_token() and self.current_token().lexeme.upper() == "END":
                break
        
        return statements
    
    def _is_statement_start(self) -> bool:
        """Verifica se o token atual inicia um statement."""
        token = self.current_token()
        if not token:
            return False
        
        # Não é statement se for "End" (fim de bloco)
        if self._is_keyword(token, "END"):
            return False
        
        # Verifica se é identificador ou keyword If/Print
        return (token.type == "IDENTIFICADOR" or 
                self._is_keyword(token, "IF") or 
                self._is_keyword(token, "PRINT"))
    
    def _is_keyword(self, token: Token, keyword: str) -> bool:
        """Verifica se o token é uma keyword específica (case-insensitive)."""
        if not token:
            return False
        return (token.type.upper() == keyword.upper() or 
                (token.type == "KEYWORD" and token.lexeme.upper() == keyword.upper()) or
                token.lexeme.upper() == keyword.upper())
    
    def _is_control_keyword(self, token: Token) -> bool:
        """Verifica se o token é uma keyword de controle (If, Print, End)."""
        if not token:
            return False
        return (token.type == "KEYWORD" and 
                token.lexeme.upper() in ("IF", "PRINT", "END"))
    
    def parse_statement(self) -> Statement:
        """Statement = Assignment | ConditionalStatement | PrintStatement"""
        token = self.current_token()
        if not token:
            raise ParseError("Esperado statement, mas encontrado fim do arquivo")
        
        # Assignment: identifier "=" Expression
        if token.type == "IDENTIFICADOR":
            # Lookahead para verificar se é atribuição
            if self.peek_token(1) and self.peek_token(1).lexeme == "=":
                return self.parse_assignment()
            else:
                # Pode ser um identifier sozinho (expressão), mas isso não é um statement válido
                raise ParseError("Esperado '=' após identificador", token)
        
        # ConditionalStatement: "If" Expression StatementList "End"
        if self._is_keyword(token, "IF"):
            return self.parse_conditional_statement()
        
        # PrintStatement: "Print" Expression | "Print" string_literal
        if self._is_keyword(token, "PRINT"):
            return self.parse_print_statement()
        
        raise ParseError(f"Token inesperado no início de statement: {token.type!r}", token)
    
    def parse_assignment(self) -> Assignment:
        """Assignment = identifier "=" Expression"""
        token = self.consume("IDENTIFICADOR")
        identifier = token.lexeme
        
        # Consome "=" (pode ser OPERADOR ou ATRIBUICAO dependendo do lexer)
        assign_token = self.current_token()
        if assign_token and assign_token.lexeme == "=":
            self.advance()
        else:
            raise ParseError("Esperado '=' após identificador", assign_token)
        
        expr = self.parse_expression()
        
        return Assignment(identifier=identifier, expression=expr, line=token.line, col=token.col)
    
    def parse_conditional_statement(self) -> ConditionalStatement:
        """ConditionalStatement = "If" Expression StatementList "End"
        
        Nota: Unificamos para sempre usar StatementList (resolve conflito LL(1))
        """
        if_token = self.consume_keyword("If")
        
        condition = self.parse_expression()
        
        # Parse StatementList (pode ter um ou mais statements)
        body = self.parse_statement_list()
        
        self.consume_keyword("End")
        
        return ConditionalStatement(condition=condition, body=body, line=if_token.line, col=if_token.col)
    
    def parse_print_statement(self) -> PrintStatement:
        """PrintStatement = "Print" Expression | "Print" string_literal"""
        print_token = self.consume_keyword("Print")
        
        token = self.current_token()
        if not token:
            raise ParseError("Esperado expressão ou string após 'Print'", None)
        
        # Se for string literal, pode usar diretamente
        if token.type == "STRING":
            str_token = self.consume("STRING")
            # Remove aspas
            value = str_token.lexeme.strip('"')
            
            # Verifica se há tokens inesperados após a string
            self._check_unexpected_token_after_expression()
            
            return PrintStatement(value=value, line=print_token.line, col=print_token.col)
        
        # Parse como Expression
        if self._is_keyword(token, "END"):
            raise ParseError("Esperado expressão após 'Print'", token)
        
        expr = self.parse_expression()
        self._check_unexpected_token_after_expression()
        return PrintStatement(value=expr, line=print_token.line, col=print_token.col)
    
    def parse_expression(self) -> Expression:
        """Expression = RelationalExpression"""
        return self.parse_relational_expression()
    
    def _parse_binary_expression(self, parse_left, parse_right, valid_ops: set, expr_class):
        """Método genérico para parsear expressões binárias (relacional, aditiva, multiplicativa)."""
        left = parse_left()
        operations = []
        
        while self.current_token() and self.current_token().type == "OPERADOR":
            token = self.current_token()
            # Para se encontrar keyword de controle
            if self._is_control_keyword(token):
                break
            # Verifica se é um operador válido
            if token.lexeme in valid_ops:
                self.advance()
                right = parse_right()
                operations.append((token.lexeme, right))
            else:
                break
        
        return expr_class(
            left=left,
            operations=operations,
            line=left.line,
            col=left.col
        )
    
    def parse_relational_expression(self) -> RelationalExpression:
        """RelationalExpression = AdditiveExpression { (">" | "<" | ">=" | "<=" | "==" | "!=") AdditiveExpression }"""
        return self._parse_binary_expression(
            self.parse_additive_expression,
            self.parse_additive_expression,
            {">", "<", ">=", "<=", "==", "!="},
            RelationalExpression
        )
    
    def parse_additive_expression(self) -> AdditiveExpression:
        """AdditiveExpression = MultiplicativeExpression { ("+" | "-") MultiplicativeExpression }"""
        return self._parse_binary_expression(
            self.parse_multiplicative_expression,
            self.parse_multiplicative_expression,
            {"+", "-"},
            AdditiveExpression
        )
    
    def parse_multiplicative_expression(self) -> MultiplicativeExpression:
        """MultiplicativeExpression = UnaryExpression { ("*" | "/") UnaryExpression }"""
        return self._parse_binary_expression(
            self.parse_unary_expression,
            self.parse_unary_expression,
            {"*", "/"},
            MultiplicativeExpression
        )
    
    def parse_unary_expression(self) -> UnaryExpression:
        """UnaryExpression = ("+" | "-") UnaryExpression | PrimaryExpression"""
        token = self.current_token()
        
        if token and token.type == "OPERADOR" and token.lexeme in {"+", "-"}:
            operator = token.lexeme
            self.advance()
            expr = self.parse_unary_expression()
            return UnaryExpression(operator=operator, expression=expr, line=token.line, col=token.col)
        
        # PrimaryExpression
        expr = self.parse_primary_expression()
        return UnaryExpression(operator=None, expression=expr, line=expr.line, col=expr.col)
    
    def parse_primary_expression(self) -> PrimaryExpression:
        """PrimaryExpression = integer_literal | decimal_literal | string_literal | 
                              identifier | identifier "(" OptionalArgumentList ")" |
                              "[" OptionalExpressionList "]" | "(" Expression ")"
        
        Nota: Left-factored para resolver conflito LL(1) com identifier
        """
        token = self.current_token()
        if not token:
            raise ParseError("Esperado expressão primária, mas encontrado fim do arquivo")
        
        # Não pode ser keywords de controle em expressões
        if self._is_control_keyword(token):
            keyword = token.lexeme.upper()
            if keyword == "END":
                raise ParseError(
                    f"Expressão incompleta: encontrado '{token.lexeme}' onde esperava-se expressão. Verifique se há um statement incompleto antes desta linha.",
                    token
                )
            raise ParseError(f"Palavra-chave '{token.lexeme}' não pode aparecer em expressão", token)
        
        # Literais
        if token.type == "INTEIRO":
            self.advance()
            return IntegerLiteral(value=int(token.lexeme), line=token.line, col=token.col)
        
        if token.type == "DECIMAL":
            self.advance()
            return DecimalLiteral(value=float(token.lexeme), line=token.line, col=token.col)
        
        if token.type == "STRING":
            self.advance()
            return StringLiteral(value=token.lexeme.strip('"'), line=token.line, col=token.col)
        
        # identifier ou identifier "(" OptionalArgumentList ")"
        # Também aceita KEYWORD que pode ser usado como identificador em expressões
        if token.type == "IDENTIFICADOR" or (token.type == "KEYWORD" and 
            token.lexeme not in ("If", "Print", "End")):
            name = token.lexeme
            self.advance()
            
            # Lookahead para verificar se é chamada de função
            # Como o lexer filtra SEPARADOR, detectamos chamadas pela presença de argumentos
            next_tok = self.current_token()
            if self._is_control_keyword(next_tok):
                return Identifier(name=name, line=token.line, col=token.col)
            
            # Verifica se há argumentos (token válido seguido de vírgula ou outro argumento)
            if next_tok and next_tok.type in ("INTEIRO", "DECIMAL", "STRING", "IDENTIFICADOR", "KEYWORD"):
                peek1 = self.peek_token(1)
                if peek1 and (peek1.lexeme == "," or peek1.type in ("INTEIRO", "DECIMAL", "STRING", "IDENTIFICADOR", "KEYWORD")):
                    return self.parse_function_call(name, token)
            
            return Identifier(name=name, line=token.line, col=token.col)
        
        # "[" OptionalExpressionList "]"
        if token.lexeme == "[" or (token.type == "SEPARADOR" and token.lexeme == "["):
            return self.parse_list_expression()
        
        # "(" Expression ")"
        if token.lexeme == "(" or (token.type == "SEPARADOR" and token.lexeme == "("):
            self.advance()
            expr = self.parse_expression()
            self._consume_separator(")")
            return ParenthesizedExpression(expression=expr, line=token.line, col=token.col)
        
        raise ParseError(f"Token inesperado em expressão primária: {token.type!r} ({token.lexeme!r})", token)
    
    def parse_function_call(self, name: str, name_token: Token) -> FunctionCall:
        """identifier "(" OptionalArgumentList ")" 
        
        Nota: Como o lexer filtra SEPARADOR (incluindo "(" e ")"), 
        detectamos chamadas de função pela presença de argumentos.
        """
        # Como os parênteses foram filtrados, começamos direto pelos argumentos
        arguments = []
        
        # Verifica se há argumentos (próximo token não é um operador ou fim)
        next_tok = self.current_token()
        if next_tok and next_tok.type in ("INTEIRO", "DECIMAL", "STRING", "IDENTIFICADOR", "KEYWORD", "OPERADOR"):
            # Verifica se não é um operador que encerraria a expressão
            if next_tok.type != "OPERADOR" or next_tok.lexeme not in ("=", ">", "<", ">=", "<=", "==", "!=", "+", "-", "*", "/"):
                # Pode ter argumentos
                peek1 = self.peek_token(1)
                if peek1 and (peek1.lexeme == "," or peek1.type in ("INTEIRO", "DECIMAL", "STRING", "IDENTIFICADOR", "KEYWORD")):
                    # Definitivamente tem argumentos
                    arguments = self.parse_argument_list()
                elif next_tok.type in ("INTEIRO", "DECIMAL", "STRING", "IDENTIFICADOR", "KEYWORD"):
                    # Pode ter um único argumento
                    arguments = [self.parse_expression()]
        
        return FunctionCall(name=name, arguments=arguments, line=name_token.line, col=name_token.col)
    
    def _check_unexpected_token_after_expression(self):
        """Verifica se há tokens inesperados após uma expressão (como parênteses extras)."""
        next_token = self.current_token()
        if next_token and next_token.type == "SEPARADOR" and next_token.lexeme == ")":
            raise ParseError(
                f"Token inesperado: ')' após expressão na linha {next_token.line}, coluna {next_token.col}. Esperado fim do statement ou nova linha.",
                next_token
            )
    
    def _consume_separator(self, expected: str) -> Token:
        """Consome um separador específico (parênteses, colchetes, vírgula)."""
        token = self.current_token()
        if not token:
            raise ParseError(f"Esperado '{expected}', mas encontrado fim do arquivo", None)
        
        if token.lexeme == expected or (token.type == "SEPARADOR" and token.lexeme == expected):
            self.advance()
            return token
        
        raise ParseError(
            f"Esperado '{expected}', mas encontrado {token.type!r} ('{token.lexeme}') na linha {token.line}, coluna {token.col}",
            token
        )
    
    def _parse_expression_list(self) -> List[Expression]:
        """Método auxiliar para parsear listas de expressões (argumentos ou elementos de lista)."""
        expressions = [self.parse_expression()]
        
        while self.current_token():
            token = self.current_token()
            if token.lexeme == "," or (token.type == "SEPARADOR" and token.lexeme == ","):
                self.advance()
                expressions.append(self.parse_expression())
            else:
                break
        return expressions
    
    def parse_argument_list(self) -> List[Expression]:
        """ArgumentList = Expression { "," Expression }"""
        return self._parse_expression_list()
    
    def parse_expression_list(self) -> List[Expression]:
        """ExpressionList = Expression { "," Expression }"""
        return self._parse_expression_list()
    
    def parse_list_expression(self) -> ListExpression:
        """ "[" OptionalExpressionList "]" """
        bracket_token = self.current_token()
        if not bracket_token:
            raise ParseError("Esperado '['", None)
        self.advance()  # consume "["
        
        elements = []
        # Verifica se há elementos (não é "]")
        next_token = self.current_token()
        if next_token and next_token.lexeme != "]" and not (next_token.type == "SEPARADOR" and next_token.lexeme == "]"):
            elements = self._parse_expression_list()
        
        self._consume_separator("]")
        return ListExpression(elements=elements, line=bracket_token.line, col=bracket_token.col)
