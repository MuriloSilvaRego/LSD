"""
Script para gerar código LLVM IR a partir de arquivo LSD
"""

import sys
import os

# Adiciona paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib', 'lexer', 'afds'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib', 'parser'))

from lexer3 import Lexer
from parser import Parser, ParseError
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator, CodeGeneratorError

def gerar_llvm(arquivo_lsd, arquivo_saida="output.ll"):
    """Gera código LLVM IR a partir de arquivo LSD."""
    
    print("=" * 80)
    print(" " * 20 + "GERADOR DE CODIGO LLVM IR")
    print("=" * 80)
    
    # Lê o arquivo
    try:
        with open(arquivo_lsd, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"\n[ERRO] Arquivo '{arquivo_lsd}' não encontrado!")
        return False
    
    print(f"\n[1] Lendo arquivo: {arquivo_lsd}")
    print("-" * 80)
    print("CODIGO LSD:")
    for i, line in enumerate(codigo.split('\n'), 1):
        if line.strip():
            print(f"{i:3} | {line}")
    print("-" * 80)
    
    try:
        # [2] Parsing
        print("\n[2] PARSING")
        print("-" * 80)
        lexer = Lexer(palavras_chave=["If", "Print", "End", "CalculateMean", "CalculateSum"])
        parser = Parser(lexer)
        ast = parser.parse(codigo)
        print("[OK] Parsing concluido!")
        
        # [3] Análise Semântica
        print("\n[3] ANALISE SEMANTICA")
        print("-" * 80)
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        
        if result['errors']:
            print("[AVISO] Erros semanticos encontrados:")
            for error in result['errors']:
                print(f"  - {error}")
        else:
            print("[OK] Analise semantica concluida!")
        
        # [4] Geração de Código LLVM IR
        print("\n[4] GERACAO DE CODIGO LLVM IR")
        print("-" * 80)
        generator = CodeGenerator()
        llvm_code = generator.generate(ast)
        print("[OK] Codigo LLVM IR gerado!")
        
        # Salva arquivo
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(llvm_code)
        
        print(f"\n[SUCESSO] Codigo salvo em: {arquivo_saida}")
        print("\nPara compilar e executar:")
        print(f"  llc {arquivo_saida} -o output.s")
        print(f"  gcc output.s -o output")
        print(f"  ./output")
        
        return True
        
    except ParseError as e:
        print(f"\n[ERRO] Erro de parsing: {e.message}")
        return False
    except CodeGeneratorError as e:
        print(f"\n[ERRO] Erro na geracao de codigo: {e.message}")
        return False
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arquivo_lsd = sys.argv[1]
        arquivo_saida = sys.argv[2] if len(sys.argv) > 2 else "output.ll"
    else:
        arquivo_lsd = "gerar_llvm.lsd"
        arquivo_saida = "output.ll"
    
    gerar_llvm(arquivo_lsd, arquivo_saida)

