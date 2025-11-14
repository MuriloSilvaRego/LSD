"""
Parser para a linguagem LSD.

Este módulo contém:
- lsd_ast: Definições da Abstract Syntax Tree (AST)
- parser: Implementação do parser recursivo descendente
- semantic_analyzer: Analisador semântico e inferência de tipos
"""

from .parser import Parser, ParseError
from .lsd_ast import (
    Program, Statement, Assignment, ConditionalStatement, PrintStatement,
    Expression, RelationalExpression, AdditiveExpression, MultiplicativeExpression,
    UnaryExpression, PrimaryExpression, IntegerLiteral, DecimalLiteral,
    StringLiteral, Identifier, FunctionCall, ListExpression, ParenthesizedExpression
)
from .semantic_analyzer import SemanticAnalyzer, SemanticError, Type, SymbolTable
from .interpreter import Interpreter, InterpreterError

__all__ = [
    'Parser', 'ParseError',
    'Program', 'Statement', 'Assignment', 'ConditionalStatement', 'PrintStatement',
    'Expression', 'RelationalExpression', 'AdditiveExpression', 'MultiplicativeExpression',
    'UnaryExpression', 'PrimaryExpression', 'IntegerLiteral', 'DecimalLiteral',
    'StringLiteral', 'Identifier', 'FunctionCall', 'ListExpression', 'ParenthesizedExpression',
    'SemanticAnalyzer', 'SemanticError', 'Type', 'SymbolTable',
    'Interpreter', 'InterpreterError'
]

