# ast_lsd.py
# AST minimalista para a linguagem LSD (Python)

class NodoAST:
    def __init__(self, linha):
        self.linha = linha

    def aceitar(self, visitor):
        raise NotImplementedError()


# ======== PROGRAMA ========

class NodoPrograma(NodoAST):
    def __init__(self, statements):
        super().__init__(0)
        self.statements = statements

    def aceitar(self, visitor):
        return visitor.visitar_programa(self)


# ======== STATEMENTS ========

class NodoStatement(NodoAST):
    pass


class NodoAssignment(NodoStatement):
    def __init__(self, nome, expressao, linha):
        super().__init__(linha)
        self.nome = nome
        self.expressao = expressao

    def aceitar(self, visitor):
        return visitor.visitar_assignment(self)


class NodoIf(NodoStatement):
    def __init__(self, condicao, corpo, linha):
        super().__init__(linha)
        self.condicao = condicao
        self.corpo = corpo

    def aceitar(self, visitor):
        return visitor.visitar_if(self)


class NodoPrint(NodoStatement):
    def __init__(self, expressao, linha):
        super().__init__(linha)
        self.expressao = expressao

    def aceitar(self, visitor):
        return visitor.visitar_print(self)


# ======== EXPRESSÕES ========

class NodoExpression(NodoAST):
    pass


class NodoLiteral(NodoExpression):
    def __init__(self, valor, linha):
        super().__init__(linha)
        self.valor = valor

    def aceitar(self, visitor):
        return visitor.visitar_literal(self)


class NodoVariable(NodoExpression):
    def __init__(self, nome, linha):
        super().__init__(linha)
        self.nome = nome

    def aceitar(self, visitor):
        return visitor.visitar_variable(self)


class NodoBinary(NodoExpression):
    def __init__(self, operador, esquerda, direita, linha):
        super().__init__(linha)
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita

    def aceitar(self, visitor):
        return visitor.visitar_binary(self)


class NodoUnary(NodoExpression):
    def __init__(self, operador, operando, linha):
        super().__init__(linha)
        self.operador = operador
        self.operando = operando

    def aceitar(self, visitor):
        return visitor.visitar_unary(self)


class NodoCall(NodoExpression):
    def __init__(self, callee, argumentos, linha):
        super().__init__(linha)
        self.callee = callee
        self.argumentos = argumentos

    def aceitar(self, visitor):
        return visitor.visitar_call(self)


class NodoListExpr(NodoExpression):
    def __init__(self, elementos, linha):
        super().__init__(linha)
        self.elementos = elementos

    def aceitar(self, visitor):
        return visitor.visitar_list_expr(self)


# Visitor base
class VisitorAST:
    def visitar_programa(self, nodo): pass
    def visitar_assignment(self, nodo): pass
    def visitar_if(self, nodo): pass
    def visitar_print(self, nodo): pass
    def visitar_literal(self, nodo): pass
    def visitar_variable(self, nodo): pass
    def visitar_binary(self, nodo): pass
    def visitar_unary(self, nodo): pass
    def visitar_call(self, nodo): pass
    def visitar_list_expr(self, nodo): pass
