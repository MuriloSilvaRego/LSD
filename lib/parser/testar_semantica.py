"""
Teste do Analisador Semântico e Inferência de Tipos
Demonstra verificação de tipos, declarações e compatibilidade
"""

import sys
import os

# Adiciona paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer', 'afds'))
sys.path.insert(0, os.path.dirname(__file__))

from lexer3 import Lexer
from parser import Parser, ParseError
from semantic_analyzer import SemanticAnalyzer, SemanticError, Type

# Código LSD para teste semântico
codigo_teste = """nota1 = 8.5
nota2 = 7.0
nota3 = 9.0
soma = nota1 + nota2 + nota3
media = soma / 3
If media >= 7.0
Print "Aprovado"
Print media
resultado = soma * 2
End
resultado_final = (soma * 2) / 3
valores = [nota1, nota2, nota3, media]
Print "Resultado final"
Print resultado_final"""

print("=" * 80)
print(" " * 20 + "TESTE DO ANALISADOR SEMANTICO LSD")
print(" " * 15 + "Inferencia de Tipos e Verificacao Semantica")
print("=" * 80)

print("\nCODIGO LSD PARA TESTE:")
print("-" * 80)
for i, line in enumerate(codigo_teste.split('\n'), 1):
    if line.strip():
        print(f"{i:3} | {line}")
print("-" * 80)

try:
    print("\n[1] Criando lexer e parser...")
    lexer = Lexer(palavras_chave=["If", "Print", "End", "CalculateMean", "CalculateSum"])
    parser = Parser(lexer)
    print("    [OK] Lexer e parser criados")
    
    print("\n[2] Fazendo parsing do codigo...")
    ast = parser.parse(codigo_teste)
    print("    [OK] Parsing concluido com sucesso!")
    
    print("\n[3] Criando analisador semantico...")
    analyzer = SemanticAnalyzer()
    print("    [OK] Analisador semantico criado")
    
    print("\n[4] Executando analise semantica...")
    result = analyzer.analyze(ast)
    print("    [OK] Analise semantica concluida!")
    
    print("\n" + "=" * 80)
    print("RESULTADOS DA ANALISE SEMANTICA:")
    print("=" * 80)
    
    # Mostra a tabela de símbolos
    print("\n[TABELA DE SIMBOLOS]")
    print("-" * 80)
    if result['symbols']:
        print(f"{'Variavel':<20} {'Tipo':<15}")
        print("-" * 80)
        for var_name, var_type in sorted(result['symbols'].items()):
            print(f"{var_name:<20} {var_type.value:<15}")
    else:
        print("Nenhuma variavel declarada")
    
    # Mostra erros
    print("\n[ERROS SEMANTICOS]")
    print("-" * 80)
    if result['errors']:
        for i, error in enumerate(result['errors'], 1):
            print(f"{i}. {error}")
    else:
        print("Nenhum erro semantico encontrado!")
    
    # Mostra warnings
    print("\n[AVISOS]")
    print("-" * 80)
    if result['warnings']:
        for i, warning in enumerate(result['warnings'], 1):
            print(f"{i}. {warning}")
    else:
        print("Nenhum aviso encontrado!")
    
    print("\n" + "=" * 80)
    if result['errors']:
        print("[RESULTADO] Analise semantica concluida com ERROS")
        print(f"Total de erros: {len(result['errors'])}")
    else:
        print("[SUCESSO] Analise semantica concluida sem erros!")
        print("Todos os tipos foram inferidos corretamente.")
    print("=" * 80)
    
except ParseError as e:
    print(f"\n[ERRO] Erro de parsing: {e.message}")
    if e.token:
        print(f"  Token: {e.token.type} ('{e.token.lexeme}') linha {e.token.line}, col {e.token.col}")
    sys.exit(1)
    
except SemanticError as e:
    print(f"\n[ERRO] Erro semantico: {e.message}")
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERRO] Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

