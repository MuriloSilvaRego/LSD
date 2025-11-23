"""
Teste do Gerador de Código LLVM IR
Demonstra a geração de código LLVM a partir da AST
"""

import sys
import os

# Adiciona paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer', 'afds'))
sys.path.insert(0, os.path.dirname(__file__))

from lexer3 import Lexer
from parser import Parser, ParseError
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator, CodeGeneratorError

# Código LSD de exemplo
codigo_lsd = """nota1 = 8.5
nota2 = 7.0
soma = nota1 + nota2
media = soma / 2
If media >= 7.0
Print "Aprovado"
Print media
End"""

print("=" * 80)
print(" " * 20 + "GERADOR DE CODIGO LLVM IR")
print(" " * 15 + "Linguagem LSD -> LLVM IR")
print("=" * 80)

print("\nCODIGO LSD:")
print("-" * 80)
for i, line in enumerate(codigo_lsd.split('\n'), 1):
    if line.strip():
        print(f"{i:3} | {line}")
print("-" * 80)

try:
    # [1] Parsing
    print("\n[1] PARSING")
    print("-" * 80)
    lexer = Lexer(palavras_chave=["If", "Print", "End", "CalculateMean", "CalculateSum"])
    parser = Parser(lexer)
    ast = parser.parse(codigo_lsd)
    print("[OK] Parsing concluido!")
    print(f"    - Numero de statements: {len(ast.statements)}")
    
    # [2] Análise Semântica (opcional, mas recomendado)
    print("\n[2] ANALISE SEMANTICA")
    print("-" * 80)
    analyzer = SemanticAnalyzer()
    result = analyzer.analyze(ast)
    
    if result['errors']:
        print("[AVISO] Erros semanticos encontrados:")
        for error in result['errors']:
            print(f"  - {error}")
    else:
        print("[OK] Analise semantica concluida sem erros!")
    
    # [3] Geração de Código LLVM IR
    print("\n[3] GERACAO DE CODIGO LLVM IR")
    print("-" * 80)
    generator = CodeGenerator()
    llvm_code = generator.generate(ast)
    print("[OK] Codigo LLVM IR gerado com sucesso!")
    
    print("\n" + "=" * 80)
    print("CODIGO LLVM IR GERADO:")
    print("=" * 80)
    print(llvm_code)
    print("=" * 80)
    
    # Salva em arquivo
    output_file = "output.ll"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(llvm_code)
    print(f"\n[INFO] Codigo salvo em: {output_file}")
    print("\nPara compilar e executar:")
    print(f"  llc {output_file} -o output.s")
    print(f"  gcc output.s -o output")
    print(f"  ./output")
    
except ParseError as e:
    print(f"\n[ERRO] Erro de parsing: {e.message}")
    if e.token:
        print(f"  Token: {e.token.type} ('{e.token.lexeme}') linha {e.token.line}, col {e.token.col}")
    sys.exit(1)
    
except CodeGeneratorError as e:
    print(f"\n[ERRO] Erro na geracao de codigo: {e.message}")
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERRO] Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

