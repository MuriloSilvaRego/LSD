"""
Teste do Parser LSD com código complexo
Um único código complexo que demonstra todas as funcionalidades
"""

import sys
import os

# Adiciona paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer', 'afds'))
sys.path.insert(0, os.path.dirname(__file__))

from lexer3 import Lexer
from parser import Parser, ParseError
from lsd_ast import Program, Assignment, ConditionalStatement, PrintStatement

# Código LSD complexo para teste
codigo_teste = """nota1 = 8.5
nota2 = 7.0
nota3 = 9.0
soma = nota1 + nota2 + nota3
media = soma / 3
If media >= 7.0
Print ("Aprovado")
Print media
resultado = soma * 2
End
resultado_final = (soma * 2) / 3
valores = [nota1, nota2, nota3, media]
expressao = -(nota1 * 2) + (nota2 / 2) * 3
Print "Resultado final"
Print resultado_final"""

print("=" * 80)
print(" " * 25 + "TESTE DO PARSER LSD")
print(" " * 20 + "Codigo Complexo - Teste Unico")
print("=" * 80)

print("\nCODIGO LSD PARA TESTE:")
print("-" * 80)
for i, line in enumerate(codigo_teste.split('\n'), 1):
    if line.strip():
        print(f"{i:3} | {line}")
print("-" * 80)

try:
    print("\n[1] Criando lexer...")
    lexer = Lexer(palavras_chave=["If", "Print", "End", "CalculateMean", "CalculateSum"])
    print("    [OK] Lexer criado")
    
    print("\n[2] Criando parser...")
    parser = Parser(lexer)
    print("    [OK] Parser criado")
    
    print("\n[3] Fazendo parsing do codigo...")
    ast = parser.parse(codigo_teste)
    print("    [OK] Parsing concluido com sucesso!")
    
    print("\n[4] Analisando estrutura da AST...")
    if isinstance(ast, Program):
        print(f"    [OK] AST raiz: Program")
        print(f"    [OK] Numero de statements: {len(ast.statements)}")
        
        # Conta tipos de statements
        assignments = sum(1 for s in ast.statements if isinstance(s, Assignment))
        conditionals = sum(1 for s in ast.statements if isinstance(s, ConditionalStatement))
        prints = sum(1 for s in ast.statements if isinstance(s, PrintStatement))
        
        print(f"\n    Estrutura do programa:")
        print(f"      - Assignments: {assignments}")
        print(f"      - Conditionals: {conditionals}")
        print(f"      - Prints: {prints}")
        
        print(f"\n    Detalhamento dos statements:")
        for i, stmt in enumerate(ast.statements, 1):
            if isinstance(stmt, Assignment):
                print(f"      {i}. Assignment: {stmt.identifier}")
            elif isinstance(stmt, ConditionalStatement):
                print(f"      {i}. ConditionalStatement (If ... End) com {len(stmt.body)} statements no corpo")
            elif isinstance(stmt, PrintStatement):
                if isinstance(stmt.value, str):
                    print(f"      {i}. PrintStatement: \"{stmt.value}\"")
                else:
                    print(f"      {i}. PrintStatement: <Expression>")
    
    if parser.errors:
        print(f"\n[AVISO] {len(parser.errors)} aviso(s) encontrado(s):")
        for err in parser.errors:
            print(f"  - {err}")
    else:
        print("\n[OK] Nenhum erro ou aviso encontrado!")
    
    print("\n" + "=" * 80)
    print("[SUCESSO] Parser funcionando perfeitamente!")
    print("O codigo complexo foi parseado com sucesso.")
    print("=" * 80)
    
except ParseError as e:
    print(f"\n" + "=" * 80)
    print("[ERRO] Erro de parsing detectado!")
    print("=" * 80)
    print(f"\nMensagem: {e.message}")
    if e.token:
        print(f"\nLocalizacao do erro:")
        print(f"  - Linha: {e.token.line}")
        print(f"  - Coluna: {e.token.col}")
        print(f"  - Token encontrado: {e.token.type} ('{e.token.lexeme}')")
        
        # Mostra a linha do código com o erro
        linhas = codigo_teste.split('\n')
        if e.token.line <= len(linhas):
            linha_erro = linhas[e.token.line - 1]
            print(f"\nLinha {e.token.line} do codigo:")
            print(f"  {linha_erro}")
            # Mostra um indicador na coluna do erro
            if e.token.col > 0:
                # Ajusta o indicador para apontar para o início do token
                indicador = " " * (e.token.col - 1) + "^" + "~" * max(0, len(e.token.lexeme) - 1)
                print(f"  {indicador}")
        
        # Extrai o que é esperado da mensagem
        if "Esperado" in e.message:
            partes = e.message.split("Esperado")
            if len(partes) > 1:
                esperado = partes[1].strip()
                print(f"\nO que e esperado: {esperado}")
    else:
        print(f"\nLocalizacao: Fim do arquivo")
    
    # Mostra erros do lexer se houver
    if parser.errors:
        print(f"\nErros adicionais:")
        for err in parser.errors:
            print(f"  - {err}")
    
    print("\n" + "=" * 80)
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERRO] Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

