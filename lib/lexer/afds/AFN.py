EPS = None  # símbolo para epsilon nas transições do NFA

from AFD_Comentario import AFD_Comentario
from AFD_Decimal import AFD_Decimal
from AFD_Identificador import AFD_Identificador
from AFD_INT import AFD_INT
from AFD_NotacaoCientifica import AFD_NotacaoCientifica
from AFD_Operadores import AFD_Operadores
from AFD_Separador import AFD_Separador
from AFD_String import AFD_String
from AFD_Base import AutomatoFinitoD

# --- Combinação AFDs -> AFN com mapeamento de token ---
def combine_afds_to_nfa(afds, token_types):
    estados = set()
    alfabeto = set()
    transicoes = {}
    finais = set()
    token_map = {}  # estado final -> tipo de token

    start = "S_COMBINED"
    estados.add(start)
    transicoes[start] = {}

    for i, (afd, ttype) in enumerate(zip(afds, token_types)):
        prefix = f"A{i}_"  # prefixo para renomear
        for s in afd.estados:
            ns = prefix + s
            estados.add(ns)
            transicoes.setdefault(ns, {})

        for sym in afd.alfabeto:
            alfabeto.add(sym)

        for s, row in afd.transicoes.items():
            ns = prefix + s
            for sym, dest in row.items():
                nd = prefix + dest
                transicoes[ns].setdefault(sym, set()).add(nd)

        # ligação por epsilon do estado inicial global para o inicial do afd
        transicoes[start].setdefault(EPS, set()).add(prefix + afd.inicial)

        # marca estado final e mapeia tipo de token
        for f in afd.finais:
            final_state = prefix + f
            finais.add(final_state)
            token_map[final_state] = ttype

    for s in list(estados):
        transicoes.setdefault(s, {})

    return {
        "estados": estados,
        "alfabeto": alfabeto,
        "transicoes": transicoes,
        "inicial": start,
        "finais": finais,
        "token_map": token_map
    }

# --- Operações auxiliares ---
def epsilon_closure(states, trans):
    stack = list(states)
    closure = set(states)
    while stack:
        s = stack.pop()
        eps_dests = trans.get(s, {}).get(EPS)
        if eps_dests:
            for d in eps_dests:
                if d not in closure:
                    closure.add(d)
                    stack.append(d)
    return closure

def move(states, symbol, trans):
    resultados = set()
    for s in states:
        dests = trans.get(s, {}).get(symbol)
        if dests:
            resultados.update(dests)
    return resultados

# --- AFN -> AFD com prioridade de token ---
def nfa_to_dfa(nfa, token_priority):
    trans = nfa["transicoes"]
    alphabet = set(nfa["alfabeto"])
    start = nfa["inicial"]
    finals_nfa = nfa["finais"]
    token_map = nfa["token_map"]

    start_closure = frozenset(epsilon_closure({start}, trans))

    dfa_states_map = {start_closure: "D0"}
    dfa_rev = {"D0": start_closure}
    dfa_trans = {}
    dfa_finals = {}  # estado -> token_type
    queue = [start_closure]
    counter = 1

    while queue:
        T = queue.pop(0)
        T_name = dfa_states_map[T]
        dfa_trans[T_name] = {}

        # Se algum estado é final no NFA, define token com maior prioridade
        final_tokens = [token_map[s] for s in T if s in finals_nfa]
        if final_tokens:
            # escolher token com menor valor (maior prioridade)
            dfa_finals[T_name] = min(final_tokens, key=lambda t: token_priority[t])

        for a in sorted(alphabet):
            moved = move(T, a, trans)
            if not moved:
                continue
            closure = frozenset(epsilon_closure(moved, trans))
            if closure not in dfa_states_map:
                dfa_states_map[closure] = f"D{counter}"
                dfa_rev[f"D{counter}"] = closure
                counter += 1
                queue.append(closure)
            dfa_trans[T_name][a] = dfa_states_map[closure]

    dfa_estados = list(dfa_trans.keys())
    dfa_inicial = dfa_states_map[start_closure]
    dfa_alfabeto = sorted(list(alphabet))
    dfa_finais_list = sorted(list(dfa_finals.keys()))

    dfa = AutomatoFinitoD(dfa_estados, dfa_alfabeto, dfa_trans, dfa_inicial, dfa_finais_list)
    dfa.token_finals = dfa_finals  # guarda o tipo de token em cada estado final

    return dfa, dfa_rev

# --- Execução ---
afds = [
    AFD_Comentario(),
    AFD_Decimal(),
    AFD_Identificador(),
    AFD_INT(),
    AFD_NotacaoCientifica(),
    AFD_Operadores(),
    AFD_Separador(),
    AFD_String()
]

token_types = [
    "COMENTARIO",
    "DECIMAL",
    "IDENTIFICADOR",
    "INTEIRO",
    "NOT_CIEN",
    "OPERADOR",
    "SEPARADOR",
    "STRING"
]

token_priority = {
    "COMENTARIO": 1,
    "STRING": 2,
    "DECIMAL": 3,
    "INTEIRO": 4,
    "NOT_CIEN": 5,
    "IDENTIFICADOR": 6,
    "OPERADOR": 7,
    "SEPARADOR": 8,
}

nfa = combine_afds_to_nfa(afds, token_types)
dfa, dfa_rev = nfa_to_dfa(nfa, token_priority)

print("AFD combinado gerado com sucesso!")
print("AFD possui:", len(dfa.estados), "estados,", len(dfa.finais), "estados finais")
