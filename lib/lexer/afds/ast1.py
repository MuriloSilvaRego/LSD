# ast.py
from typing import List, Optional, Any, Protocol

class NodoAST:
    def __init__(self, linha: int):
        self.linha = linha

    def aceitar(self, visitor):
        raise NotImplementedError

# ---------- Programa e Declarações ----------

class NodoPrograma(NodoAST):
    def __init__(self, declaracoes: List["NodoDeclaracao"]):
        super().__init__(0)
        self.declaracoes = declaracoes

    def aceitar(self, visitor):
        return visitor.visitar_programa(self)

class NodoDeclaracao(NodoAST):
    def __init__(self, linha: int):
        super().__init__(linha)

class NodoDeclaracaoFuncao(NodoDeclaracao):
    def __init__(self, nome: str, parametros: List["Parametro"], tipo_retorno: Optional[str], corpo: List["NodoComando"], linha: int):
        super().__init__(linha)
        self.nome = nome
        self.parametros = parametros
        self.tipo_retorno = tipo_retorno
        self.corpo = corpo

    def aceitar(self, visitor):
        return visitor.visitar_declaracao_funcao(self)

class Parametro:
    def __init__(self, nome: str, tipo: Optional[str]):
        self.nome = nome
        self.tipo = tipo

class NodoDeclaracaoVariavel(NodoDeclaracao):
    def __init__(self, nome: str, tipo_explicito: Optional[str], inicializador: Optional["NodoExpressao"], linha: int):
        super().__init__(linha)
        self.nome = nome
        self.tipo_explicito = tipo_explicito
        self.inicializador = inicializador

    def aceitar(self, visitor):
        return visitor.visitar_declaracao_variavel(self)

class NodoDeclaracaoClasse(NodoDeclaracao):
    def __init__(self, nome: str, campos: List[NodoDeclaracaoVariavel], metodos: List[NodoDeclaracaoFuncao], linha: int):
        super().__init__(linha)
        self.nome = nome
        self.campos = campos
        self.metodos = metodos

    def aceitar(self, visitor):
        return visitor.visitar_declaracao_classe(self)

# ---------- Comandos ----------

class NodoComando(NodoDeclaracao):
    def __init__(self, linha: int):
        super().__init__(linha)

class NodoComandoExpressao(NodoComando):
    def __init__(self, expressao: "NodoExpressao", linha: int):
        super().__init__(linha)
        self.expressao = expressao

    def aceitar(self, visitor):
        return visitor.visitar_comando_expressao(self)

class NodoComandoIf(NodoComando):
    def __init__(self, condicao: "NodoExpressao", bloco_entao: "NodoComando", bloco_senao: Optional["NodoComando"], linha: int):
        super().__init__(linha)
        self.condicao = condicao
        self.bloco_entao = bloco_entao
        self.bloco_senao = bloco_senao

    def aceitar(self, visitor):
        return visitor.visitar_comando_if(self)

class NodoComandoWhile(NodoComando):
    def __init__(self, condicao: "NodoExpressao", corpo: "NodoComando", linha: int):
        super().__init__(linha)
        self.condicao = condicao
        self.corpo = corpo

    def aceitar(self, visitor):
        return visitor.visitar_comando_while(self)

class NodoComandoFor(NodoComando):
    def __init__(self, inicializador: Optional[NodoComando], condicao: Optional["NodoExpressao"], incremento: Optional["NodoExpressao"], corpo: "NodoComando", linha: int):
        super().__init__(linha)
        self.inicializador = inicializador
        self.condicao = condicao
        self.incremento = incremento
        self.corpo = corpo

    def aceitar(self, visitor):
        return visitor.visitar_comando_for(self)

class NodoComandoReturn(NodoComando):
    def __init__(self, valor: Optional["NodoExpressao"], linha: int):
        super().__init__(linha)
        self.valor = valor

    def aceitar(self, visitor):
        return visitor.visitar_comando_return(self)

class NodoComandoBloco(NodoComando):
    def __init__(self, comandos: List[NodoComando], linha: int):
        super().__init__(linha)
        self.comandos = comandos

    def aceitar(self, visitor):
        return visitor.visitar_comando_bloco(self)

# ---------- Expressões ----------

class NodoExpressao(NodoAST):
    def __init__(self, linha: int):
        super().__init__(linha)

class NodoExpressaoLiteral(NodoExpressao):
    def __init__(self, valor: Any, linha: int):
        super().__init__(linha)
        self.valor = valor

    def aceitar(self, visitor):
        return visitor.visitar_expressao_literal(self)

class NodoExpressaoVariavel(NodoExpressao):
    def __init__(self, nome: str, linha: int):
        super().__init__(linha)
        self.nome = nome

    def aceitar(self, visitor):
        return visitor.visitar_expressao_variavel(self)

class NodoExpressaoBinaria(NodoExpressao):
    def __init__(self, operador: str, esquerda: NodoExpressao, direita: NodoExpressao, linha: int):
        super().__init__(linha)
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita

    def aceitar(self, visitor):
        return visitor.visitar_expressao_binaria(self)

class NodoExpressaoUnaria(NodoExpressao):
    def __init__(self, operador: str, operando: NodoExpressao, linha: int):
        super().__init__(linha)
        self.operador = operador
        self.operando = operando

    def aceitar(self, visitor):
        return visitor.visitar_expressao_unaria(self)

class NodoExpressaoAtribuicao(NodoExpressao):
    def __init__(self, nome: str, valor: NodoExpressao, linha: int):
        super().__init__(linha)
        self.nome = nome
        self.valor = valor

    def aceitar(self, visitor):
        return visitor.visitar_expressao_atribuicao(self)

class NodoExpressaoChamada(NodoExpressao):
    def __init__(self, funcao: NodoExpressao, argumentos: List[NodoExpressao], linha: int):
        super().__init__(linha)
        self.funcao = funcao
        self.argumentos = argumentos

    def aceitar(self, visitor):
        return visitor.visitar_expressao_chamada(self)

class NodoExpressaoAcesso(NodoExpressao):
    def __init__(self, objeto: NodoExpressao, propriedade: str, linha: int):
        super().__init__(linha)
        self.objeto = objeto
        self.propriedade = propriedade

    def aceitar(self, visitor):
        return visitor.visitar_expressao_acesso(self)

class NodoExpressaoAgrupamento(NodoExpressao):
    def __init__(self, expressao: NodoExpressao, linha: int):
        super().__init__(linha)
        self.expressao = expressao

    def aceitar(self, visitor):
        return visitor.visitar_expressao_agrupamento(self)

class NodoErro(NodoDeclaracao):
    def __init__(self):
        super().__init__(0)

    def aceitar(self, visitor):
        return visitor.visitar_erro(self)

# ---------- Visitor interface (Protocol) ----------
class VisitorAST(Protocol):
    def visitar_programa(self, nodo: NodoPrograma): ...
    def visitar_declaracao_funcao(self, nodo: NodoDeclaracaoFuncao): ...
    def visitar_declaracao_variavel(self, nodo: NodoDeclaracaoVariavel): ...
    def visitar_declaracao_classe(self, nodo: NodoDeclaracaoClasse): ...

    def visitar_comando_expressao(self, nodo: NodoComandoExpressao): ...
    def visitar_comando_if(self, nodo: NodoComandoIf): ...
    def visitar_comando_while(self, nodo: NodoComandoWhile): ...
    def visitar_comando_for(self, nodo: NodoComandoFor): ...
    def visitar_comando_return(self, nodo: NodoComandoReturn): ...
    def visitar_comando_bloco(self, nodo: NodoComandoBloco): ...

    def visitar_expressao_literal(self, nodo: NodoExpressaoLiteral): ...
    def visitar_expressao_variavel(self, nodo: NodoExpressaoVariavel): ...
    def visitar_expressao_binaria(self, nodo: NodoExpressaoBinaria): ...
    def visitar_expressao_unaria(self, nodo: NodoExpressaoUnaria): ...
    def visitar_expressao_atribuicao(self, nodo: NodoExpressaoAtribuicao): ...
    def visitar_expressao_chamada(self, nodo: NodoExpressaoChamada): ...
    def visitar_expressao_acesso(self, nodo: NodoExpressaoAcesso): ...
    def visitar_expressao_agrupamento(self, nodo: NodoExpressaoAgrupamento): ...

    def visitar_erro(self, nodo: NodoErro): ...
