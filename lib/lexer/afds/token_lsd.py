# token_lsd.py

from enum import Enum

class TipoToken(Enum):
    IF = "IF"
    PRINT = "PRINT"
    END = "END"

    IDENT = "IDENT"

    INT_LIT = "INT_LIT"
    DEC_LIT = "DEC_LIT"
    STR_LIT = "STR_LIT"

    EQ = "="
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"

    LPAREN = "("
    RPAREN = ")"
    LBRACK = "["
    RBRACK = "]"
    COMMA = ","

    GT = ">"
    LT = "<"
    GE = ">="
    LE = "<="
    EQEQ = "=="
    NEQ = "!="

    EOF = "EOF"


class Token:
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        return f"Token({self.tipo}, '{self.lexema}', line={self.linha}, col={self.coluna})"
