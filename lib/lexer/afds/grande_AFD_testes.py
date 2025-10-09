# Importa a função que constrói o AFD combinado
from AFN import combine_afds_to_nfa, nfa_to_dfa
from AFD_Comentario import AFD_Comentario
from AFD_Decimal import AFD_Decimal
from AFD_Identificador import AFD_Identificador
from AFD_INT import AFD_INT
from AFD_NotacaoCientifica import AFD_NotacaoCientifica
from AFD_Operadores import AFD_Operadores
from AFD_Separador import AFD_Separador
from AFD_String import AFD_String

# --- Construção do AFD único ---
afds = [
    AFD_Comentario(),
    AFD_Decimal(),
    AFD_Identificador(),
    AFD_INT(),
    AFD_NotacaoCientifica(),
    AFD_Operadores(),
    AFD_Separador(),
    AFD_String(),
]

# Definir prioridade de tokens (menor valor = maior prioridade)
token_types = [
    "COMENTARIO",
    "DECIMAL",
    "IDENTIFICADOR",
    "INTEIRO",
    "NOTACAO_CIENTIFICA",
    "OPERADOR",
    "SEPARADOR",
    "STRING"
]

token_priority = {t: i+1 for i, t in enumerate(token_types)}

# Construção do NFA combinado e conversão para DFA
nfa = combine_afds_to_nfa(afds, token_types)
dfa, dfa_rev = nfa_to_dfa(nfa, token_priority)

print("AFD combinado gerado com sucesso!")
print("AFD possui:", len(dfa.estados), "estados,", len(dfa.finais), "estados finais")


# --- Função de teste genérica ---
def testar(nome, exemplos):
    print(f"\n== {nome} ==")
    for cadeia in exemplos:
        resultado = dfa.aceita(cadeia)
        if not resultado:
            print(f"{cadeia!r:25} → Rejeitada")
        else:
            # percorre o caminho da cadeia para descobrir o estado final
            estado_atual = dfa.inicial
            for c in cadeia:
                estado_atual = dfa.transicoes.get(estado_atual, {}).get(c)
                if estado_atual is None:
                    break
            # recupera o tipo de token a partir do estado final
            token = dfa.token_finals.get(estado_atual, "DESCONHECIDO") if estado_atual else "DESCONHECIDO"
            print(f"{cadeia!r:25} → Aceita como {token}")


# --- Casos de teste ---

testar("Identificador", [
    "Data", "mean1", "_ok", "X_2", "var123",
    "1Invalid", "!", "data space"
])

testar("Comentário", [
    "// isso e um comentario\n", "//123\n", "//\n",
    "/ errado\n", "/coment\n", "/* bloco */", "// teste \n gfyyfk"
])

testar("Decimal", [
    "3.14", "0.5", "12.0", "999.999",
    "1.", ".5", "a.b", "3,14", "02.3"
])

testar("Inteiro", [
    "0", "123", "42", "999999",
    "42a", "a42", "", "1.0", "0005"
])

testar("Notação Científica", [
    "1.23e-4", "2E10", "0e0", "123e+5",
    "1e", "e10", "1.2e", "1.2e+"
])

testar("Operadores", [
    "+", "-", "*", "/", "==", "!=", "<=", ">=", ">", "<",
    "=>", "===", "++", "!"
])

testar("Separador", [
    " ", "\n", "\t", "\r", "  \n\t",
    "a", "1", "_", " \nX", ",", "("
])

testar("String", [
    '"Hello"', '"123"', '""', '"with space"',
    '"bad\n"', '"unclosed', 'noquotes'
])
