"""
Teste de Erros Semânticos
Demonstra detecção de erros semânticos comuns
"""

import sys
import os

# Adiciona paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer', 'afds'))
sys.path.insert(0, os.path.dirname(__file__))

from lexer3 import Lexer
from parser import Parser, ParseError
from semantic_analyzer import SemanticAnalyzer, SemanticError

# Código com erros semânticos intencionais
codigo_com_erros = """x = 10
y = "texto"
z = x + y
variavel_nao_declarada = nao_existe
If "nao_e_bool"
Print "teste"
End
lista = [1, 2, "texto"]
resultado = lista * 2"""

print("=" * 80)
print(" " * 25 + "TESTE DE ERROS SEMANTICOS")
print(" " * 20 + "Detecao de Erros Semanticos Comuns")
print("=" * 80)

print("\nCODIGO LSD COM ERROS INTENCIONAIS:")
print("-" * 80)
for i, line in enumerate(codigo_com_erros.split('\n'), 1):
    if line.strip():
        print(f"{i:3} | {line}")
print("-" * 80)

try:
    print("\n[1] Fazendo parsing...")
    lexer = Lexer(palavras_chave=["If", "Print", "End"])
    parser = Parser(lexer)
    ast = parser.parse(codigo_com_erros)
    print("    [OK] Parsing concluido")
    
    print("\n[2] Executando analise semantica...")
    analyzer = SemanticAnalyzer()
    result = analyzer.analyze(ast)
    print("    [OK] Analise semantica concluida")
    
    print("\n" + "=" * 80)
    print("ERROS SEMANTICOS DETECTADOS:")
    print("=" * 80)
    
    if result['errors']:
        print(f"\nTotal de erros encontrados: {len(result['errors'])}\n")
        for i, error in enumerate(result['errors'], 1):
            print(f"[ERRO {i}]")
            print(f"  {error}")
            print()
    else:
        print("\nNenhum erro semantico detectado (isso nao deveria acontecer neste teste)")
    
    if result['warnings']:
        print("\nAVISOS:")
        print("-" * 80)
        for i, warning in enumerate(result['warnings'], 1):
            print(f"{i}. {warning}")
    
    print("\n" + "=" * 80)
    print("TIPOS INFERIDOS (antes dos erros):")
    print("-" * 80)
    if result['symbols']:
        for var_name, var_type in sorted(result['symbols'].items()):
            print(f"  {var_name}: {var_type.value}")
    print("=" * 80)
    
except ParseError as e:
    print(f"\n[ERRO] Erro de parsing: {e.message}")
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERRO] Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

