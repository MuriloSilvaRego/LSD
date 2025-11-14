"""
Interpretador para a linguagem LSD.
Executa a AST gerada pelo parser.
"""

from typing import Dict, Any, List, Union
from lsd_ast import (
    Program, Statement, Assignment, ConditionalStatement, PrintStatement,
    Expression, RelationalExpression, AdditiveExpression, MultiplicativeExpression,
    UnaryExpression, PrimaryExpression, IntegerLiteral, DecimalLiteral,
    StringLiteral, Identifier, FunctionCall, ListExpression, ParenthesizedExpression
)


class InterpreterError(Exception):
    """Exceção para erros de interpretação."""
    def __init__(self, message: str, line: int = -1, col: int = -1):
        self.message = message
        self.line = line
        self.col = col
        super().__init__(f"{message} (linha {line}, coluna {col})" if line > 0 else message)


class Interpreter:
    """Interpretador para executar programas LSD."""
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.output: List[str] = []
    
    def interpret(self, program: Program) -> List[str]:
        """
        Interpreta o programa e retorna a saída.
        """
        self.variables = {}
        self.output = []
        
        try:
            for statement in program.statements:
                self._execute_statement(statement)
        except InterpreterError as e:
            self.output.append(f"[ERRO] {e.message}")
            raise
        
        return self.output
    
    def _execute_statement(self, statement: Statement) -> None:
        """Executa um statement."""
        if isinstance(statement, Assignment):
            self._execute_assignment(statement)
        elif isinstance(statement, ConditionalStatement):
            self._execute_conditional(statement)
        elif isinstance(statement, PrintStatement):
            self._execute_print(statement)
    
    def _execute_assignment(self, assignment: Assignment) -> None:
        """Executa uma atribuição: identifier = Expression"""
        value = self._evaluate_expression(assignment.expression)
        self.variables[assignment.identifier] = value
    
    def _execute_conditional(self, conditional: ConditionalStatement) -> None:
        """Executa um condicional: If Expression StatementList End"""
        condition_value = self._evaluate_expression(conditional.condition)
        
        # A condição deve ser um valor booleano
        if not isinstance(condition_value, bool):
            raise InterpreterError(
                f"Condição do 'If' deve ser booleana, mas encontrado {type(condition_value).__name__}",
                conditional.line,
                conditional.col
            )
        
        if condition_value:
            for statement in conditional.body:
                self._execute_statement(statement)
    
    def _execute_print(self, print_stmt: PrintStatement) -> None:
        """Executa um print: Print Expression ou Print string"""
        if isinstance(print_stmt.value, str):
            # Print com string literal
            self.output.append(print_stmt.value)
        else:
            # Print com expressão
            value = self._evaluate_expression(print_stmt.value)
            self.output.append(str(value))
    
    def _evaluate_expression(self, expression: Expression) -> Any:
        """Avalia uma expressão e retorna seu valor."""
        if isinstance(expression, RelationalExpression):
            return self._evaluate_relational_expression(expression)
        elif isinstance(expression, AdditiveExpression):
            return self._evaluate_additive_expression(expression)
        elif isinstance(expression, MultiplicativeExpression):
            return self._evaluate_multiplicative_expression(expression)
        elif isinstance(expression, UnaryExpression):
            return self._evaluate_unary_expression(expression)
        elif isinstance(expression, PrimaryExpression):
            return self._evaluate_primary_expression(expression)
        else:
            raise InterpreterError(f"Tipo de expressão não suportado: {type(expression).__name__}")
    
    def _evaluate_relational_expression(self, expr: RelationalExpression) -> Any:
        """Avalia expressão relacional."""
        left_value = self._evaluate_expression(expr.left)
        
        # Se não há operações, retorna o valor do lado esquerdo
        if not expr.operations:
            return left_value
        
        # Avalia cada operação relacional
        result = left_value
        for op, right_expr in expr.operations:
            right_value = self._evaluate_expression(right_expr)
            result = self._apply_relational_operator(op, result, right_value)
        
        return result
    
    def _evaluate_additive_expression(self, expr: AdditiveExpression) -> Any:
        """Avalia expressão aditiva."""
        result = self._evaluate_expression(expr.left)
        
        for op, right_expr in expr.operations:
            right_value = self._evaluate_expression(right_expr)
            result = self._apply_additive_operator(op, result, right_value)
        
        return result
    
    def _evaluate_multiplicative_expression(self, expr: MultiplicativeExpression) -> Any:
        """Avalia expressão multiplicativa."""
        result = self._evaluate_expression(expr.left)
        
        for op, right_expr in expr.operations:
            right_value = self._evaluate_expression(right_expr)
            result = self._apply_multiplicative_operator(op, result, right_value)
        
        return result
    
    def _evaluate_unary_expression(self, expr: UnaryExpression) -> Any:
        """Avalia expressão unária."""
        value = self._evaluate_expression(expr.expression)
        
        if expr.operator == "+":
            return +value
        elif expr.operator == "-":
            return -value
        
        return value
    
    def _evaluate_primary_expression(self, expr: PrimaryExpression) -> Any:
        """Avalia expressão primária."""
        if isinstance(expr, IntegerLiteral):
            return expr.value
        elif isinstance(expr, DecimalLiteral):
            return expr.value
        elif isinstance(expr, StringLiteral):
            return expr.value
        elif isinstance(expr, Identifier):
            if expr.name not in self.variables:
                raise InterpreterError(
                    f"Variável '{expr.name}' não foi declarada",
                    expr.line,
                    expr.col
                )
            return self.variables[expr.name]
        elif isinstance(expr, FunctionCall):
            return self._evaluate_function_call(expr)
        elif isinstance(expr, ListExpression):
            return self._evaluate_list_expression(expr)
        elif isinstance(expr, ParenthesizedExpression):
            return self._evaluate_expression(expr.expression)
        else:
            raise InterpreterError(f"Tipo de expressão primária não suportado: {type(expr).__name__}")
    
    def _evaluate_function_call(self, func_call: FunctionCall) -> Any:
        """Avalia chamada de função."""
        # Avalia os argumentos
        args = [self._evaluate_expression(arg) for arg in func_call.arguments]
        
        # Funções conhecidas
        if func_call.name == "CalculateMean":
            if len(args) != 1:
                raise InterpreterError(
                    f"CalculateMean espera 1 argumento, mas recebeu {len(args)}",
                    func_call.line,
                    func_call.col
                )
            if not isinstance(args[0], list):
                raise InterpreterError(
                    f"CalculateMean espera uma lista, mas recebeu {type(args[0]).__name__}",
                    func_call.line,
                    func_call.col
                )
            if not args[0]:
                return 0.0
            return sum(args[0]) / len(args[0])
        
        elif func_call.name == "CalculateSum":
            if len(args) != 1:
                raise InterpreterError(
                    f"CalculateSum espera 1 argumento, mas recebeu {len(args)}",
                    func_call.line,
                    func_call.col
                )
            if not isinstance(args[0], list):
                raise InterpreterError(
                    f"CalculateSum espera uma lista, mas recebeu {type(args[0]).__name__}",
                    func_call.line,
                    func_call.col
                )
            return sum(args[0])
        
        raise InterpreterError(
            f"Função '{func_call.name}' não está definida",
            func_call.line,
            func_call.col
        )
    
    def _evaluate_list_expression(self, list_expr: ListExpression) -> List[Any]:
        """Avalia expressão de lista."""
        return [self._evaluate_expression(elem) for elem in list_expr.elements]
    
    def _apply_relational_operator(self, op: str, left: Any, right: Any) -> bool:
        """Aplica operador relacional."""
        if op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        else:
            raise InterpreterError(f"Operador relacional desconhecido: {op}")
    
    def _apply_additive_operator(self, op: str, left: Any, right: Any) -> Any:
        """Aplica operador aditivo."""
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        else:
            raise InterpreterError(f"Operador aditivo desconhecido: {op}")
    
    def _apply_multiplicative_operator(self, op: str, left: Any, right: Any) -> Any:
        """Aplica operador multiplicativo."""
        if op == "*":
            return left * right
        elif op == "/":
            if right == 0:
                raise InterpreterError("Divisão por zero")
            return left / right
        else:
            raise InterpreterError(f"Operador multiplicativo desconhecido: {op}")

