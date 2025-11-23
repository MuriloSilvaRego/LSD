"""
Script para executar código LSD
Demonstra o fluxo completo: parsing, análise semântica e interpretação
"""

import sys
import os

# Adiciona paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib', 'lexer', 'afds'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib', 'parser'))

from lexer3 import Lexer
from parser import Parser, ParseError
from semantic_analyzer import SemanticAnalyzer, SemanticError
from interpreter import Interpreter, InterpreterError

def executar_arquivo_lsd(arquivo_lsd):
    """Executa um arquivo LSD."""
    
    print("=" * 80)
    print(" " * 25 + "EXECUTOR LSD")
    print(" " * 20 + "Compilador/Interpretador Completo")
    print("=" * 80)
    
    # Lê o arquivo
    try:
        with open(arquivo_lsd, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"\n[ERRO] Arquivo '{arquivo_lsd}' não encontrado!")
        return False
    except Exception as e:
        print(f"\n[ERRO] Erro ao ler arquivo: {e}")
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
        print("\n[2] ANALISE LEXICA E SINTATICA")
        print("-" * 80)
        lexer = Lexer(palavras_chave=["If", "Print", "End", "CalculateMean", "CalculateSum"])
        parser = Parser(lexer)
        ast = parser.parse(codigo)
        print("[OK] Parsing concluido com sucesso!")
        print(f"    - Numero de statements: {len(ast.statements)}")
        
        # [3] Análise Semântica
        print("\n[3] ANALISE SEMANTICA")
        print("-" * 80)
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        
        if result['errors']:
            print("[ERRO] Erros semanticos encontrados:")
            for error in result['errors']:
                print(f"  - {error}")
            return False
        
        if result['warnings']:
            print("[AVISO] Avisos encontrados:")
            for warning in result['warnings']:
                print(f"  - {warning}")
        
        print("[OK] Analise semantica concluida sem erros!")
        print("\nTabela de Simbolos:")
        for var_name, var_type in sorted(result['symbols'].items()):
            print(f"  - {var_name}: {var_type.value}")
        
        # [4] Interpretação
        print("\n[4] EXECUCAO DO PROGRAMA")
        print("-" * 80)
        interpreter = Interpreter()
        output = interpreter.interpret(ast)
        
        print("[OK] Execucao concluida!")
        print("\n" + "=" * 80)
        print("SAIDA DO PROGRAMA:")
        print("=" * 80)
        for line in output:
            print(line)
        print("=" * 80)
        
        return True
        
    except ParseError as e:
        print(f"\n[ERRO] Erro de parsing: {e.message}")
        if e.token:
            print(f"  Token: {e.token.type} ('{e.token.lexeme}') linha {e.token.line}, col {e.token.col}")
        return False
        
    except SemanticError as e:
        print(f"\n[ERRO] Erro semantico: {e.message}")
        return False
        
    except InterpreterError as e:
        print(f"\n[ERRO] Erro de interpretacao: {e.message}")
        return False
        
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Verifica argumentos
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        arquivo = "exemplo_completo.lsd"
    
    sucesso = executar_arquivo_lsd(arquivo)
    
    if sucesso:
        print("\n" + "=" * 80)
        print("[SUCESSO] Programa executado com sucesso!")
        print("=" * 80)
        sys.exit(0)
    else:
        print("\n" + "=" * 80)
        print("[FALHA] Programa nao pode ser executado devido a erros.")
        print("=" * 80)
        sys.exit(1)

