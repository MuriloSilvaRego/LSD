"""
Teste da Arvore AST
Mostra a estrutura da arvore sintatica de forma visual
"""

import sys
import os

# Adiciona paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer', 'afds'))
sys.path.insert(0, os.path.dirname(__file__))

from lexer3 import Lexer
from parser import Parser, ParseError
from lsd_ast import (
    Program, Assignment, ConditionalStatement, PrintStatement,
    RelationalExpression, AdditiveExpression, MultiplicativeExpression,
    UnaryExpression, IntegerLiteral, DecimalLiteral, StringLiteral,
    Identifier, FunctionCall, ListExpression, ParenthesizedExpression
)

# Código LSD para demonstrar a árvore
codigo_demo = """nota1 = 8.5
nota2 = 7.0
soma = nota1 + nota2
media = soma / 2
If media >= 7.0
Print "Aprovado"
Print media
End
valores = [nota1, nota2, media]
Print "Resultado final"
Print valores"""


def mostrar_arvore(node, indent=0, max_depth=15, current_depth=0):
    """Mostra a arvore AST de forma hierarquica."""
    if current_depth > max_depth:
        return
    
    espacos = "  " * indent
    
    if isinstance(node, Program):
        print(f"{espacos}Program")
        for stmt in node.statements:
            mostrar_arvore(stmt, indent + 1, max_depth, current_depth + 1)
    
    elif isinstance(node, Assignment):
        print(f"{espacos}Assignment: {node.identifier}")
        mostrar_arvore(node.expression, indent + 1, max_depth, current_depth + 1)
    
    elif isinstance(node, ConditionalStatement):
        print(f"{espacos}ConditionalStatement (If ... End)")
        print(f"{espacos}  Condition:")
        mostrar_arvore(node.condition, indent + 2, max_depth, current_depth + 1)
        print(f"{espacos}  Body ({len(node.body)} statements):")
        for stmt in node.body:
            mostrar_arvore(stmt, indent + 2, max_depth, current_depth + 1)
    
    elif isinstance(node, PrintStatement):
        if isinstance(node.value, str):
            print(f'{espacos}PrintStatement: "{node.value}"')
        else:
            print(f"{espacos}PrintStatement:")
            mostrar_arvore(node.value, indent + 1, max_depth, current_depth + 1)
    
    elif isinstance(node, (RelationalExpression, AdditiveExpression, MultiplicativeExpression)):
        # Expressões binárias têm o mesmo padrão
        tipo = type(node).__name__
        ops = ", ".join([op for op, _ in node.operations]) if node.operations else "sem operadores"
        print(f"{espacos}{tipo} (operadores: {ops})")
        print(f"{espacos}  Left:")
        mostrar_arvore(node.left, indent + 2, max_depth, current_depth + 1)
        for op, right in node.operations:
            print(f"{espacos}  Operador: {op}")
            mostrar_arvore(right, indent + 2, max_depth, current_depth + 1)
    
    elif isinstance(node, UnaryExpression):
        op_str = f" (operador: {node.operator})" if node.operator else ""
        print(f"{espacos}UnaryExpression{op_str}")
        mostrar_arvore(node.expression, indent + 1, max_depth, current_depth + 1)
    
    elif isinstance(node, IntegerLiteral):
        print(f"{espacos}IntegerLiteral: {node.value}")
    
    elif isinstance(node, DecimalLiteral):
        print(f"{espacos}DecimalLiteral: {node.value}")
    
    elif isinstance(node, StringLiteral):
        print(f'{espacos}StringLiteral: "{node.value}"')
    
    elif isinstance(node, Identifier):
        print(f"{espacos}Identifier: {node.name}")
    
    elif isinstance(node, FunctionCall):
        print(f"{espacos}FunctionCall: {node.name}({len(node.arguments)} argumentos)")
        for i, arg in enumerate(node.arguments, 1):
            print(f"{espacos}  Argumento {i}:")
            mostrar_arvore(arg, indent + 2, max_depth, current_depth + 1)
    
    elif isinstance(node, ListExpression):
        print(f"{espacos}ListExpression ({len(node.elements)} elementos)")
        for i, elem in enumerate(node.elements, 1):
            print(f"{espacos}  Elemento {i}:")
            mostrar_arvore(elem, indent + 2, max_depth, current_depth + 1)
    
    elif isinstance(node, ParenthesizedExpression):
        print(f"{espacos}ParenthesizedExpression: (Expression)")
        mostrar_arvore(node.expression, indent + 1, max_depth, current_depth + 1)
    
    else:
        print(f"{espacos}{type(node).__name__}")


print("=" * 80)
print(" " * 25 + "TESTE DA ARVORE AST")
print(" " * 20 + "Parser LSD - Estrutura Sintatica")
print("=" * 80)

print("\nCODIGO LSD:")
print("-" * 80)
for i, line in enumerate(codigo_demo.split('\n'), 1):
    if line.strip():
        print(f"{i:3} | {line}")
print("-" * 80)

try:
    print("\n[1] Criando lexer e parser...")
    lexer = Lexer(palavras_chave=["If", "Print", "End", "CalculateMean", "CalculateSum"])
    parser = Parser(lexer)
    print("    [OK] Lexer e parser criados")
    
    print("\n[2] Fazendo parsing...")
    ast = parser.parse(codigo_demo)
    print("    [OK] Parsing concluido!")
    
    print("\n" + "=" * 80)
    print("ARVORE AST GERADA:")
    print("=" * 80)
    mostrar_arvore(ast, max_depth=15)
    print("=" * 80)
    
    print("\nINFORMACOES DA ARVORE:")
    if isinstance(ast, Program):
        print(f"  - Tipo raiz: {type(ast).__name__}")
        print(f"  - Numero de statements: {len(ast.statements)}")
    
    print("\n" + "=" * 80)
    print("[SUCESSO] Arvore AST gerada com sucesso!")
    print("=" * 80)
    
except ParseError as e:
    print(f"\n[ERRO] Erro de parsing: {e.message}")
    if e.token:
        print(f"  Token: {e.token.type} ('{e.token.lexeme}') linha {e.token.line}, col {e.token.col}")
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERRO] Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
