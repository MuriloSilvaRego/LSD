import sys
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

from lexer3 import Lexer  # seu lexer
from parser import Parser
from ast1 import NodoPrograma

src = '''
    If x = 10
    Print("Valor:") 

    y = 25
    Print(y);
    End
'''

lexer = Lexer(palavras_chave=["If", "Print", "End", "CalculateMean", "CalculateSum"])
tokens, erros_lexicos = lexer.tokenize(src)

# for t in tokens:
#     print(t)
parser = Parser(tokens)
ast = parser.parse_program()

# ast é um NodoPrograma - utilize visitor para percorrer