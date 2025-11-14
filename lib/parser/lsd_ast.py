"""
Abstract Syntax Tree (AST) para a linguagem LSD.
Representa a estrutura sintática do programa após o parsing.
"""

from typing import List, Optional, Union
from dataclasses import dataclass, field


# ============ Nós da AST ============

@dataclass
class ASTNode:
    """Classe base para todos os nós da AST."""
    line: int = -1
    col: int = -1


@dataclass
class Program(ASTNode):
    """Programa completo - lista de statements."""
    statements: List['Statement'] = None
    
    def __post_init__(self):
        if self.statements is None:
            self.statements = []


@dataclass
class Statement(ASTNode):
    """Classe base para statements."""
    pass


@dataclass
class Assignment(Statement):
    """Atribuição: identifier = Expression"""
    identifier: str = ""
    expression: 'Expression' = None


@dataclass
class ConditionalStatement(Statement):
    """Condicional: If Expression StatementList End"""
    condition: 'Expression' = None
    body: List['Statement'] = field(default_factory=list)


@dataclass
class PrintStatement(Statement):
    """Print: Print Expression ou Print string_literal"""
    value: Union['Expression', str] = None  # Expression ou string literal


@dataclass
class Expression(ASTNode):
    """Classe base para expressões."""
    pass


@dataclass
class RelationalExpression(Expression):
    """Expressão relacional: AdditiveExpression [op AdditiveExpression]*"""
    left: 'AdditiveExpression' = None
    operations: List[tuple] = field(default_factory=list)  # Lista de (operador, AdditiveExpression)


@dataclass
class AdditiveExpression(Expression):
    """Expressão aditiva: MultiplicativeExpression [op MultiplicativeExpression]*"""
    left: 'MultiplicativeExpression' = None
    operations: List[tuple] = field(default_factory=list)  # Lista de (operador, MultiplicativeExpression)


@dataclass
class MultiplicativeExpression(Expression):
    """Expressão multiplicativa: UnaryExpression [op UnaryExpression]*"""
    left: 'UnaryExpression' = None
    operations: List[tuple] = field(default_factory=list)  # Lista de (operador, UnaryExpression)


@dataclass
class UnaryExpression(Expression):
    """Expressão unária: [+|-] UnaryExpression ou PrimaryExpression"""
    operator: Optional[str] = None  # '+' ou '-' ou None
    expression: 'Expression' = None  # UnaryExpression ou PrimaryExpression


@dataclass
class PrimaryExpression(Expression):
    """Expressão primária: literal, identifier, chamada de função, lista, parênteses"""
    pass


@dataclass
class IntegerLiteral(PrimaryExpression):
    """Literal inteiro."""
    value: int = 0


@dataclass
class DecimalLiteral(PrimaryExpression):
    """Literal decimal."""
    value: float = 0.0


@dataclass
class StringLiteral(PrimaryExpression):
    """Literal string."""
    value: str = ""


@dataclass
class Identifier(PrimaryExpression):
    """Identificador (variável)."""
    name: str = ""


@dataclass
class FunctionCall(PrimaryExpression):
    """Chamada de função: identifier(ArgumentList)"""
    name: str = ""
    arguments: List['Expression'] = field(default_factory=list)


@dataclass
class ListExpression(PrimaryExpression):
    """Lista: [ExpressionList]"""
    elements: List['Expression'] = field(default_factory=list)


@dataclass
class ParenthesizedExpression(PrimaryExpression):
    """Expressão entre parênteses: (Expression)"""
    expression: 'Expression' = None

