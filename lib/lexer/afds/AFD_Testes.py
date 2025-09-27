# Importações dos autômatos
from AFD_Identificador import AFD_Identificador
from AFD_Atribuicao import AFD_Atribuicao
from AFD_Comentario import AFD_Comentario
from AFD_Decimal import AFD_Decimal
from AFD_INT import AFD_INT
from AFD_NotacaoCientifica import AFD_NotacaoCientifica
from AFD_Operadores import AFD_Operadores
from AFD_Separador import AFD_Separador
from AFD_String import AFD_String

# Função genérica de teste
def testar(nome, instancia, exemplos):
    print(f"\n== {nome} ==")
    for cadeia in exemplos:
        resultado = instancia.aceita(cadeia)
        print(f"{cadeia!r:25} → {'Aceita' if resultado else 'Rejeitada'}")


# 1. Identificadores
afd_id = AFD_Identificador()
testar("Identificador", afd_id, [
    "Data", "mean1", "_ok", "X_2", "var123",
    "1Invalid", "!", "data space"
])

# 2. Atribuição
afd_atr = AFD_Atribuicao()
testar("Atribuição", afd_atr, [
    "=", " = ", "==", "=>", "===", " =="
])

# 3. Comentário (linha única)
afd_com = AFD_Comentario()
testar("Comentário", afd_com, [
    "// isso e um comentario\n", "//123\n", "//\n",
    "/ errado\n", "/coment\n", "/* bloco */", "// teste \n gfyyfk"
])

# 4. Decimal
afd_dec = AFD_Decimal()
testar("Decimal", afd_dec, [
    "3.14", "0.5", "12.0", "999.999",
    "1.", ".5", "a.b", "3,14", "02.3"
])

# 5. Inteiro
afd_int = AFD_INT()
testar("Inteiro", afd_int, [
    "0", "123", "42", "999999",
    "42a", "a42", "", "1.0", "0005"
])

# 6. Notação Científica
afd_sci = AFD_NotacaoCientifica()
testar("Notação Científica", afd_sci, [
    "1.23e-4", "2E10", "0e0", "123e+5",
    "1e", "e10", "1.2e", "1.2e+"
])

# 7. Operadores
afd_op = AFD_Operadores()
testar("Operadores", afd_op, [
    "+", "-", "*", "/", "==", "!=", "<=", ">=", ">", "<",
    "=>", "===", "++", "!"
])

# 8. Separador
afd_sep = AFD_Separador()
testar("Separador", afd_sep, [
    " ", "\n", "\t", "\r", "  \n\t",
    "a", "1", "_", " \nX", ",", "("
])

# 9. String
afd_str = AFD_String()
testar("String", afd_str, [
    '"Hello"', '"123"', '""', '"with space"',
    '"bad\n"', '"unclosed', 'noquotes'
])