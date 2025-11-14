import sys
from pathlib import Path

# Garante que o diretório atual está no path
sys.path.insert(0, str(Path(__file__).parent))

from lexer3 import Lexer
from parser_lsd import ParserLSD
from ast_lsd import (
    NodoPrograma, NodoAssignment, NodoIf, NodoPrint,
    NodoLiteral, NodoVariable, NodoBinary, NodoUnary,
    NodoCall, NodoListExpr, VisitorAST
)


src = '''
    If x == 10
        Print("Valor:")
    y == 25
    Print y

    a = 20 + 5 * (3 - 1)

    End 
'''


def print_ast(node, indent=0):
    """Imprime a AST recursivamente (debug)."""
    prefix = "  " * indent
    print(f"{prefix}{node.__class__.__name__}")

    for attr, value in vars(node).items():
        if isinstance(value, list):
            print(f"{prefix}  {attr}: [")
            for item in value:
                if hasattr(item, '__class__'):
                    print_ast(item, indent + 2)
                else:
                    print(f"{prefix}    {item}")
            print(f"{prefix}  ]")

        elif hasattr(value, '__class__') and "Nodo" in value.__class__.__name__:
            print(f"{prefix}  {attr}:")
            print_ast(value, indent + 2)

        else:
            print(f"{prefix}  {attr}: {value}")


def main():
    lexer = Lexer(
        palavras_chave=["If", "Print", "End", "CalculateMean", "CalculateSum"]
    )

    tokens, erros_lexicos = lexer.tokenize(src)

    if erros_lexicos:
        print("Erros léxicos encontrados:", erros_lexicos)
        return

    # print("Quantidade de tokens:", len(tokens))
    # print(tokens)

    parser = ParserLSD(tokens)
    ast = parser.parsear_programa()

    # print("\n=== AST GERADA ===")
    # print_ast(ast)

    print("\n=== Visitor ===")

    # ============================
    # VISITOR DE DEBUG CORRIGIDO
    # ============================
    # class DebugVisitor(VisitorAST):
    #     def visitar_programa(self, nodo):
    #         print("Visitando Programa")
    #         for st in nodo.statements:
    #             st.aceitar(self)

    #     def visitar_assignment(self, nodo):
    #         print(f"Visitando Assignment: {nodo.nome}")
    #         nodo.expressao.aceitar(self)

    #     def visitar_if(self, nodo):
    #         print("Visitando If")
    #         nodo.condicao.aceitar(self)
    #         for st in nodo.corpo:
    #             st.aceitar(self)

    #     def visitar_print(self, nodo):
    #         print("Visitando Print")
    #         nodo.expressao.aceitar(self)

    #     def visitar_literal(self, nodo):
    #         print(f"Visitando Literal: {nodo.valor}")

    #     def visitar_variable(self, nodo):
    #         print(f"Visitando Variable: {nodo.nome}")

    #     def visitar_binary(self, nodo):
    #         print(f"Visitando Binary: {nodo.operador}")
    #         nodo.esquerda.aceitar(self)
    #         nodo.direita.aceitar(self)

    #     def visitar_unary(self, nodo):
    #         print(f"Visitando Unary: {nodo.operador}")
    #         nodo.operando.aceitar(self)

    #     def visitar_call(self, nodo):
    #         print(f"Visitando Call: {nodo.callee}")
    #         for arg in nodo.argumentos:
    #             arg.aceitar(self)

    #     def visitar_list_expr(self, nodo):
    #         print(f"Visitando ListExpr com {len(nodo.elementos)} elementos")
    #         for el in nodo.elementos:
    #             el.aceitar(self)

    # visitor = DebugVisitor()
    # ast.aceitar(visitor)


if __name__ == "__main__":
    main()
