"""
Analisador Semântico e Inferência de Tipos para a linguagem LSD.
Verifica tipos, declarações de variáveis e compatibilidade de operações.
"""

from typing import Dict, Optional, Union, List
from enum import Enum
from lsd_ast import (
    Program, Statement, Assignment, ConditionalStatement, PrintStatement,
    Expression, RelationalExpression, AdditiveExpression, MultiplicativeExpression,
    UnaryExpression, PrimaryExpression, IntegerLiteral, DecimalLiteral,
    StringLiteral, Identifier, FunctionCall, ListExpression, ParenthesizedExpression
)


class Type(Enum):
    """Tipos da linguagem LSD."""
    INT = "INT"
    DECIMAL = "DECIMAL"
    STRING = "STRING"
    LIST = "LIST"
    BOOL = "BOOL"
    UNKNOWN = "UNKNOWN"  # Para variáveis não declaradas ou erros


class SemanticError(Exception):
    """Exceção para erros semânticos."""
    def __init__(self, message: str, line: int = -1, col: int = -1):
        self.message = message
        self.line = line
        self.col = col
        super().__init__(f"{message} (linha {line}, coluna {col})" if line > 0 else message)


class SymbolTable:
    """Tabela de símbolos para armazenar variáveis e seus tipos."""
    
    def __init__(self):
        self.symbols: Dict[str, Type] = {}
    
    def declare(self, name: str, var_type: Type, line: int = -1, col: int = -1) -> None:
        """Declara uma variável na tabela de símbolos."""
        if name in self.symbols:
            raise SemanticError(
                f"Variável '{name}' já foi declarada anteriormente",
                line, col
            )
        self.symbols[name] = var_type
    
    def get_type(self, name: str, line: int = -1, col: int = -1) -> Type:
        """Retorna o tipo de uma variável."""
        if name not in self.symbols:
            raise SemanticError(
                f"Variável '{name}' não foi declarada",
                line, col
            )
        return self.symbols[name]
    
    def update(self, name: str, var_type: Type) -> None:
        """Atualiza o tipo de uma variável (para inferência)."""
        self.symbols[name] = var_type


class SemanticAnalyzer:
    """Analisador semântico com inferência de tipos."""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def analyze(self, program: Program) -> Dict[str, Union[Type, List[str]]]:
        """
        Analisa semanticamente o programa e retorna informações sobre tipos.
        Retorna: {'errors': [...], 'warnings': [...], 'symbols': {...}}
        """
        self.errors = []
        self.warnings = []
        self.symbol_table = SymbolTable()
        
        try:
            # Primeira passagem: coleta todas as declarações de variáveis
            self._collect_declarations(program)
            # Segunda passagem: analisa tipos e verificações semânticas
            self._analyze_program(program)
        except SemanticError as e:
            self.errors.append(str(e))
        
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'symbols': dict(self.symbol_table.symbols)
        }
    
    def _collect_declarations(self, program: Program) -> None:
        """Primeira passagem: coleta todas as declarações de variáveis."""
        for statement in program.statements:
            if isinstance(statement, Assignment):
                # Declara a variável como UNKNOWN inicialmente
                if statement.identifier not in self.symbol_table.symbols:
                    self.symbol_table.declare(
                        statement.identifier,
                        Type.UNKNOWN,
                        statement.line,
                        statement.col
                    )
            elif isinstance(statement, ConditionalStatement):
                # Coleta declarações dentro do condicional
                for stmt in statement.body:
                    if isinstance(stmt, Assignment):
                        if stmt.identifier not in self.symbol_table.symbols:
                            self.symbol_table.declare(
                                stmt.identifier,
                                Type.UNKNOWN,
                                stmt.line,
                                stmt.col
                            )
    
    def _analyze_program(self, program: Program) -> None:
        """Analisa o programa completo."""
        for statement in program.statements:
            self._analyze_statement(statement)
    
    def _analyze_statement(self, statement: Statement) -> None:
        """Analisa um statement."""
        if isinstance(statement, Assignment):
            self._analyze_assignment(statement)
        elif isinstance(statement, ConditionalStatement):
            self._analyze_conditional(statement)
        elif isinstance(statement, PrintStatement):
            self._analyze_print(statement)
    
    def _analyze_assignment(self, assignment: Assignment) -> None:
        """Analisa uma atribuição: identifier = Expression"""
        # Infere o tipo da expressão (pode usar variáveis já declaradas)
        expr_type = self._infer_expression_type(assignment.expression)
        
        # Se a variável já existe, verifica compatibilidade
        if assignment.identifier in self.symbol_table.symbols:
            existing_type = self.symbol_table.symbols[assignment.identifier]
            # Se a variável era UNKNOWN, pode receber qualquer tipo
            if existing_type == Type.UNKNOWN:
                if expr_type != Type.UNKNOWN:
                    self.symbol_table.update(assignment.identifier, expr_type)
            # Se a variável já tem um tipo específico, verifica compatibilidade
            elif not self._are_compatible(existing_type, expr_type) and expr_type != Type.UNKNOWN:
                self.errors.append(
                    f"Tipo incompatível na atribuição: '{assignment.identifier}' "
                    f"é {existing_type.value}, mas recebeu {expr_type.value} "
                    f"(linha {assignment.line}, coluna {assignment.col})"
                )
            # Atualiza o tipo se for mais específico
            elif expr_type != Type.UNKNOWN and expr_type != existing_type:
                self.symbol_table.update(assignment.identifier, expr_type)
        else:
            # Variável não foi coletada na primeira passagem (não deveria acontecer)
            # Declara com o tipo inferido
            self.symbol_table.declare(
                assignment.identifier,
                expr_type if expr_type != Type.UNKNOWN else Type.UNKNOWN,
                assignment.line,
                assignment.col
            )
    
    def _analyze_conditional(self, conditional: ConditionalStatement) -> None:
        """Analisa um condicional: If Expression StatementList End"""
        # A condição deve ser do tipo BOOL
        condition_type = self._infer_expression_type(conditional.condition)
        
        if condition_type != Type.BOOL:
            self.errors.append(
                f"Condição do 'If' deve ser do tipo BOOL, mas encontrado {condition_type.value} "
                f"(linha {conditional.line}, coluna {conditional.col})"
            )
        
        # Analisa o corpo do condicional
        for statement in conditional.body:
            self._analyze_statement(statement)
    
    def _analyze_print(self, print_stmt: PrintStatement) -> None:
        """Analisa um print: Print Expression ou Print string"""
        if isinstance(print_stmt.value, str):
            # Print com string literal - sempre válido
            return
        
        # Print com expressão - infere o tipo
        expr_type = self._infer_expression_type(print_stmt.value)
        # Qualquer tipo pode ser impresso, então não há erro aqui
    
    def _infer_expression_type(self, expression: Expression) -> Type:
        """Infere o tipo de uma expressão."""
        if isinstance(expression, RelationalExpression):
            return self._infer_relational_expression(expression)
        elif isinstance(expression, AdditiveExpression):
            return self._infer_additive_expression(expression)
        elif isinstance(expression, MultiplicativeExpression):
            return self._infer_multiplicative_expression(expression)
        elif isinstance(expression, UnaryExpression):
            return self._infer_unary_expression(expression)
        elif isinstance(expression, PrimaryExpression):
            return self._infer_primary_expression(expression)
        else:
            return Type.UNKNOWN
    
    def _infer_relational_expression(self, expr: RelationalExpression) -> Type:
        """Infere tipo de expressão relacional."""
        # Analisa o lado esquerdo
        left_type = self._infer_expression_type(expr.left)
        
        # Se não há operações relacionais, retorna o tipo do lado esquerdo
        if not expr.operations:
            return left_type
        
        # Para cada operação relacional
        for op, right_expr in expr.operations:
            right_type = self._infer_expression_type(right_expr)
            
            # Verifica compatibilidade dos tipos
            if not self._are_comparable(left_type, right_type):
                self.errors.append(
                    f"Tipos incompatíveis em operação relacional '{op}': "
                    f"{left_type.value} e {right_type.value} não podem ser comparados "
                    f"(linha {expr.line}, coluna {expr.col})"
                )
        
        # Expressões relacionais com operadores sempre retornam BOOL
        return Type.BOOL
    
    def _infer_additive_expression(self, expr: AdditiveExpression) -> Type:
        """Infere tipo de expressão aditiva."""
        left_type = self._infer_expression_type(expr.left)
        
        for op, right_expr in expr.operations:
            right_type = self._infer_expression_type(right_expr)
            
            # Verifica compatibilidade
            result_type = self._get_arithmetic_result_type(left_type, right_type, op)
            if result_type == Type.UNKNOWN:
                self.errors.append(
                    f"Operação '{op}' inválida entre tipos {left_type.value} e {right_type.value} "
                    f"(linha {expr.line}, coluna {expr.col})"
                )
            left_type = result_type
        
        return left_type
    
    def _infer_multiplicative_expression(self, expr: MultiplicativeExpression) -> Type:
        """Infere tipo de expressão multiplicativa."""
        left_type = self._infer_expression_type(expr.left)
        
        for op, right_expr in expr.operations:
            right_type = self._infer_expression_type(right_expr)
            
            # Verifica compatibilidade
            result_type = self._get_arithmetic_result_type(left_type, right_type, op)
            if result_type == Type.UNKNOWN:
                self.errors.append(
                    f"Operação '{op}' inválida entre tipos {left_type.value} e {right_type.value} "
                    f"(linha {expr.line}, coluna {expr.col})"
                )
            left_type = result_type
        
        return left_type
    
    def _infer_unary_expression(self, expr: UnaryExpression) -> Type:
        """Infere tipo de expressão unária."""
        expr_type = self._infer_expression_type(expr.expression)
        
        # Operadores unários + e - só funcionam com números
        if expr.operator in ("+", "-"):
            if expr_type not in (Type.INT, Type.DECIMAL):
                self.errors.append(
                    f"Operador unário '{expr.operator}' não pode ser aplicado a tipo {expr_type.value} "
                    f"(linha {expr.line}, coluna {expr.col})"
                )
                return Type.UNKNOWN
        
        return expr_type
    
    def _infer_primary_expression(self, expr: PrimaryExpression) -> Type:
        """Infere tipo de expressão primária."""
        if isinstance(expr, IntegerLiteral):
            return Type.INT
        elif isinstance(expr, DecimalLiteral):
            return Type.DECIMAL
        elif isinstance(expr, StringLiteral):
            return Type.STRING
        elif isinstance(expr, Identifier):
            # Tenta obter o tipo da tabela de símbolos
            if expr.name in self.symbol_table.symbols:
                return self.symbol_table.symbols[expr.name]
            else:
                # Variável não declarada - adiciona erro mas continua análise
                self.errors.append(
                    f"Variável '{expr.name}' não foi declarada antes do uso "
                    f"(linha {expr.line}, coluna {expr.col})"
                )
                return Type.UNKNOWN
        elif isinstance(expr, FunctionCall):
            return self._infer_function_call(expr)
        elif isinstance(expr, ListExpression):
            return self._infer_list_expression(expr)
        elif isinstance(expr, ParenthesizedExpression):
            return self._infer_expression_type(expr.expression)
        else:
            return Type.UNKNOWN
    
    def _infer_function_call(self, func_call: FunctionCall) -> Type:
        """Infere tipo de chamada de função."""
        # Analisa os argumentos
        for arg in func_call.arguments:
            self._infer_expression_type(arg)
        
        # Funções conhecidas
        if func_call.name == "CalculateMean":
            # CalculateMean retorna DECIMAL
            if len(func_call.arguments) != 1:
                self.errors.append(
                    f"CalculateMean espera 1 argumento, mas recebeu {len(func_call.arguments)} "
                    f"(linha {func_call.line}, coluna {func_call.col})"
                )
            else:
                arg_type = self._infer_expression_type(func_call.arguments[0])
                if arg_type != Type.LIST:
                    self.errors.append(
                        f"CalculateMean espera LIST, mas recebeu {arg_type.value} "
                        f"(linha {func_call.line}, coluna {func_call.col})"
                    )
            return Type.DECIMAL
        
        elif func_call.name == "CalculateSum":
            # CalculateSum retorna INT ou DECIMAL (depende dos elementos)
            if len(func_call.arguments) != 1:
                self.errors.append(
                    f"CalculateSum espera 1 argumento, mas recebeu {len(func_call.arguments)} "
                    f"(linha {func_call.line}, coluna {func_call.col})"
                )
            else:
                arg_type = self._infer_expression_type(func_call.arguments[0])
                if arg_type != Type.LIST:
                    self.errors.append(
                        f"CalculateSum espera LIST, mas recebeu {arg_type.value} "
                        f"(linha {func_call.line}, coluna {func_call.col})"
                    )
            # Por padrão, retorna DECIMAL (pode ser refinado)
            return Type.DECIMAL
        
        # Função desconhecida - retorna UNKNOWN
        self.warnings.append(
            f"Função '{func_call.name}' não reconhecida, tipo inferido como UNKNOWN "
            f"(linha {func_call.line}, coluna {func_call.col})"
        )
        return Type.UNKNOWN
    
    def _infer_list_expression(self, list_expr: ListExpression) -> Type:
        """Infere tipo de lista."""
        if not list_expr.elements:
            # Lista vazia - tipo UNKNOWN (poderia ser refinado)
            return Type.LIST
        
        # Verifica se todos os elementos têm tipos compatíveis
        element_types = [self._infer_expression_type(elem) for elem in list_expr.elements]
        
        # Verifica consistência de tipos (todos devem ser numéricos ou todos strings)
        first_type = element_types[0]
        for i, elem_type in enumerate(element_types[1:], 1):
            if not self._are_compatible_for_list(first_type, elem_type):
                self.warnings.append(
                    f"Lista contém tipos mistos: {first_type.value} e {elem_type.value} "
                    f"(linha {list_expr.line}, coluna {list_expr.col})"
                )
        
        return Type.LIST
    
    def _are_comparable(self, type1: Type, type2: Type) -> bool:
        """Verifica se dois tipos podem ser comparados."""
        # Números podem ser comparados entre si
        if type1 in (Type.INT, Type.DECIMAL) and type2 in (Type.INT, Type.DECIMAL):
            return True
        # Strings podem ser comparadas entre si
        if type1 == Type.STRING and type2 == Type.STRING:
            return True
        # Mesmo tipo sempre comparável
        if type1 == type2:
            return True
        return False
    
    def _are_compatible(self, type1: Type, type2: Type) -> bool:
        """Verifica se dois tipos são compatíveis para atribuição."""
        # Mesmo tipo sempre compatível
        if type1 == type2:
            return True
        # INT e DECIMAL são compatíveis (promoção)
        if type1 in (Type.INT, Type.DECIMAL) and type2 in (Type.INT, Type.DECIMAL):
            return True
        return False
    
    def _are_compatible_for_list(self, type1: Type, type2: Type) -> bool:
        """Verifica se dois tipos são compatíveis para estar na mesma lista."""
        # Números são compatíveis entre si
        if type1 in (Type.INT, Type.DECIMAL) and type2 in (Type.INT, Type.DECIMAL):
            return True
        # Mesmo tipo sempre compatível
        return type1 == type2
    
    def _get_arithmetic_result_type(self, type1: Type, type2: Type, op: str) -> Type:
        """Retorna o tipo resultante de uma operação aritmética."""
        # Operações aritméticas só funcionam com números
        if type1 not in (Type.INT, Type.DECIMAL) or type2 not in (Type.INT, Type.DECIMAL):
            return Type.UNKNOWN
        
        # Se qualquer operando é DECIMAL, o resultado é DECIMAL
        if type1 == Type.DECIMAL or type2 == Type.DECIMAL:
            return Type.DECIMAL
        
        # Ambos são INT
        return Type.INT

