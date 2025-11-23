"""
Gerador de Código LLVM IR para a linguagem LSD.
Converte a AST em código LLVM IR (Intermediate Representation).
"""

from typing import Dict, List, Optional
from lsd_ast import (
    Program, Statement, Assignment, ConditionalStatement, PrintStatement,
    Expression, RelationalExpression, AdditiveExpression, MultiplicativeExpression,
    UnaryExpression, PrimaryExpression, IntegerLiteral, DecimalLiteral,
    StringLiteral, Identifier, FunctionCall, ListExpression, ParenthesizedExpression
)


class CodeGeneratorError(Exception):
    """Exceção para erros na geração de código."""
    def __init__(self, message: str, line: int = -1, col: int = -1):
        self.message = message
        self.line = line
        self.col = col
        super().__init__(f"{message} (linha {line}, coluna {col})" if line > 0 else message)


class CodeGenerator:
    """Gerador de código LLVM IR."""
    
    def __init__(self):
        self.llvm_code: List[str] = []
        self.variable_counter = 0
        self.string_counter = 0
        self.label_counter = 0
        self.variables: Dict[str, str] = {}  # nome_variavel -> registro_llvm
        self.strings: Dict[str, str] = {}  # string -> nome_global
        self.current_function = "main"
    
    def generate(self, program: Program) -> str:
        """
        Gera código LLVM IR a partir da AST.
        Retorna o código LLVM IR completo.
        """
        self.llvm_code = []
        self.variable_counter = 0
        self.string_counter = 0
        self.label_counter = 0
        self.variables = {}
        self.strings = {}
        
        # Cabeçalho LLVM
        self._emit_header()
        
        # Declarações de funções externas (printf, etc)
        self._emit_external_declarations()
        
        # Função main
        self._emit_function_start("main")
        
        # Gera código para cada statement
        for statement in program.statements:
            self._generate_statement(statement)
        
        # Finaliza função main
        self._emit_function_end()
        
        # Emite strings globais
        self._emit_string_constants()
        
        return "\n".join(self.llvm_code)
    
    def _emit_header(self):
        """Emite o cabeçalho do módulo LLVM."""
        import platform
        
        self.llvm_code.append("; LLVM IR gerado para linguagem LSD")
        self.llvm_code.append("; Target: x86-64")
        self.llvm_code.append("")
        
        # Detecta o sistema operacional e ajusta o target
        system = platform.system()
        if system == "Windows":
            # Windows x64
            self.llvm_code.append("target datalayout = \"e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128\"")
            self.llvm_code.append("target triple = \"x86_64-pc-windows-msvc\"")
        elif system == "Darwin":  # macOS
            self.llvm_code.append("target datalayout = \"e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128\"")
            self.llvm_code.append("target triple = \"x86_64-apple-darwin\"")
        else:  # Linux
            self.llvm_code.append("target datalayout = \"e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128\"")
            self.llvm_code.append("target triple = \"x86_64-pc-linux-gnu\"")
        
        self.llvm_code.append("")
    
    def _emit_external_declarations(self):
        """Emite declarações de funções externas."""
        # printf para imprimir strings e números
        self.llvm_code.append("declare i32 @printf(i8*, ...)")
        self.llvm_code.append("")
    
    def _emit_function_start(self, name: str):
        """Emite o início de uma função."""
        self.llvm_code.append(f"define i32 @{name}() {{")
        self.llvm_code.append("entry:")
        self.current_function = name
    
    def _emit_function_end(self):
        """Emite o fim de uma função."""
        self.llvm_code.append("  ret i32 0")
        self.llvm_code.append("}")
        self.llvm_code.append("")
    
    def _emit_string_constants(self):
        """Emite constantes de string globais."""
        for string_value, global_name in self.strings.items():
            # Escapa caracteres especiais para LLVM
            escaped = self._escape_string_for_llvm(string_value)
            str_len = len(string_value) + 1  # +1 para null terminator
            self.llvm_code.append(f"@{global_name} = private unnamed_addr constant [{str_len} x i8] c\"{escaped}\\00\"")
            self.llvm_code.append("")
    
    def _generate_statement(self, statement: Statement) -> None:
        """Gera código LLVM para um statement."""
        if isinstance(statement, Assignment):
            self._generate_assignment(statement)
        elif isinstance(statement, ConditionalStatement):
            self._generate_conditional(statement)
        elif isinstance(statement, PrintStatement):
            self._generate_print(statement)
    
    def _generate_assignment(self, assignment: Assignment) -> None:
        """Gera código para atribuição: identifier = Expression"""
        # Avalia a expressão
        result_reg = self._generate_expression(assignment.expression)
        
        # Armazena o resultado na variável
        if assignment.identifier not in self.variables:
            # Primeira atribuição - cria variável
            var_reg = self._new_register()
            self.variables[assignment.identifier] = var_reg
            self.llvm_code.append(f"  {var_reg} = alloca double, align 8")
        
        var_reg = self.variables[assignment.identifier]
        self.llvm_code.append(f"  store double {result_reg}, double* {var_reg}, align 8")
    
    def _generate_conditional(self, conditional: ConditionalStatement) -> None:
        """Gera código para condicional: If Expression StatementList End"""
        # Avalia a condição - deve retornar um valor booleano (i1)
        # Se a condição é uma expressão relacional, já retorna i1
        condition_reg = self._generate_expression(conditional.condition)
        
        # Se condition_reg é double (resultado de expressão relacional convertida),
        # precisamos convertê-lo de volta para i1
        # Mas se já é i1 (de uma comparação direta), usamos diretamente
        
        # Labels para if/else
        if_label = self._new_label("if")
        end_label = self._new_label("end")
        
        # Se a condição é uma expressão relacional, ela já foi convertida para double
        # Precisamos verificar se é diferente de 0.0
        cmp_reg = self._new_register()
        self.llvm_code.append(f"  {cmp_reg} = fcmp one double {condition_reg}, 0.000000e+00")
        
        # Branch condicional
        self.llvm_code.append(f"  br i1 {cmp_reg}, label %{if_label}, label %{end_label}")
        self.llvm_code.append("")
        self.llvm_code.append(f"{if_label}:")
        
        # Gera código do corpo
        for statement in conditional.body:
            self._generate_statement(statement)
        
        # Branch para o fim
        self.llvm_code.append(f"  br label %{end_label}")
        self.llvm_code.append("")
        self.llvm_code.append(f"{end_label}:")
    
    def _generate_print(self, print_stmt: PrintStatement) -> None:
        """Gera código para print: Print Expression ou Print string"""
        if isinstance(print_stmt.value, str):
            # Print string literal
            global_name = self._get_string_constant(print_stmt.value)
            self.llvm_code.append(f"  call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([{len(print_stmt.value) + 1} x i8], [{len(print_stmt.value) + 1} x i8]* @{global_name}, i64 0, i64 0))")
        else:
            # Print expressão numérica
            value_reg = self._generate_expression(print_stmt.value)
            # Usa formato para double com quebra de linha
            format_str = self._get_string_constant("%f\n")
            format_len = len("%f\n") + 1  # +1 para null terminator
            self.llvm_code.append(f"  call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([{format_len} x i8], [{format_len} x i8]* @{format_str}, i64 0, i64 0), double {value_reg})")
    
    def _generate_expression(self, expression: Expression) -> str:
        """
        Gera código LLVM para uma expressão e retorna o registro do resultado.
        """
        if isinstance(expression, RelationalExpression):
            return self._generate_relational_expression(expression)
        elif isinstance(expression, AdditiveExpression):
            return self._generate_additive_expression(expression)
        elif isinstance(expression, MultiplicativeExpression):
            return self._generate_multiplicative_expression(expression)
        elif isinstance(expression, UnaryExpression):
            return self._generate_unary_expression(expression)
        elif isinstance(expression, PrimaryExpression):
            return self._generate_primary_expression(expression)
        else:
            raise CodeGeneratorError(f"Tipo de expressão não suportado: {type(expression).__name__}")
    
    def _generate_relational_expression(self, expr: RelationalExpression) -> str:
        """Gera código para expressão relacional."""
        left_reg = self._generate_expression(expr.left)
        
        # Se não há operações, retorna o valor do lado esquerdo
        if not expr.operations:
            return left_reg
        
        # Avalia cada operação relacional
        result_reg = left_reg
        for op, right_expr in expr.operations:
            right_reg = self._generate_expression(right_expr)
            result_reg = self._apply_relational_operator(op, result_reg, right_reg)
        
        # result_reg agora é i1 (booleano)
        # Para uso em expressões aritméticas, convertemos para double
        # Mas para uso em condicionais, mantemos como i1 seria melhor
        # Por enquanto, convertemos para double para compatibilidade
        bool_reg = self._new_register()
        self.llvm_code.append(f"  {bool_reg} = uitofp i1 {result_reg} to double")
        return bool_reg
    
    def _generate_additive_expression(self, expr: AdditiveExpression) -> str:
        """Gera código para expressão aditiva."""
        result_reg = self._generate_expression(expr.left)
        
        for op, right_expr in expr.operations:
            right_reg = self._generate_expression(right_expr)
            result_reg = self._apply_additive_operator(op, result_reg, right_reg)
        
        return result_reg
    
    def _generate_multiplicative_expression(self, expr: MultiplicativeExpression) -> str:
        """Gera código para expressão multiplicativa."""
        result_reg = self._generate_expression(expr.left)
        
        for op, right_expr in expr.operations:
            right_reg = self._generate_expression(right_expr)
            result_reg = self._apply_multiplicative_operator(op, result_reg, right_reg)
        
        return result_reg
    
    def _generate_unary_expression(self, expr: UnaryExpression) -> str:
        """Gera código para expressão unária."""
        value_reg = self._generate_expression(expr.expression)
        
        if expr.operator == "+":
            return value_reg
        elif expr.operator == "-":
            neg_reg = self._new_register()
            self.llvm_code.append(f"  {neg_reg} = fneg double {value_reg}")
            return neg_reg
        
        return value_reg
    
    def _generate_primary_expression(self, expr: PrimaryExpression) -> str:
        """Gera código para expressão primária."""
        if isinstance(expr, IntegerLiteral):
            # Converte inteiro para double
            reg = self._new_register()
            self.llvm_code.append(f"  {reg} = sitofp i32 {expr.value} to double")
            return reg
        elif isinstance(expr, DecimalLiteral):
            # Literal decimal - usa formato científico LLVM
            reg = self._new_register()
            # Converte para notação científica LLVM (ex: 8.5 -> 8.500000e+00)
            if expr.value == 0.0:
                value_str = "0.000000e+00"
            else:
                # Formata em notação científica
                import math
                if abs(expr.value) >= 1.0 or expr.value == 0.0:
                    exp = 0
                    mantissa = expr.value
                    while abs(mantissa) >= 10.0:
                        mantissa /= 10.0
                        exp += 1
                    while abs(mantissa) < 1.0 and mantissa != 0.0:
                        mantissa *= 10.0
                        exp -= 1
                else:
                    exp = int(math.floor(math.log10(abs(expr.value))))
                    mantissa = expr.value / (10.0 ** exp)
                
                sign = "-" if expr.value < 0 else ""
                value_str = f"{sign}{abs(mantissa):.6f}e{exp:+03d}"
            
            self.llvm_code.append(f"  {reg} = fadd double 0.000000e+00, {value_str}")
            return reg
        elif isinstance(expr, StringLiteral):
            # Strings não são retornadas como registros, são tratadas separadamente
            raise CodeGeneratorError("StringLiteral não pode ser usado como expressão numérica")
        elif isinstance(expr, Identifier):
            # Carrega valor da variável
            if expr.name not in self.variables:
                raise CodeGeneratorError(
                    f"Variável '{expr.name}' não foi declarada",
                    expr.line,
                    expr.col
                )
            var_reg = self.variables[expr.name]
            load_reg = self._new_register()
            self.llvm_code.append(f"  {load_reg} = load double, double* {var_reg}, align 8")
            return load_reg
        elif isinstance(expr, FunctionCall):
            return self._generate_function_call(expr)
        elif isinstance(expr, ListExpression):
            raise CodeGeneratorError("ListExpression não suportado na geração de código LLVM")
        elif isinstance(expr, ParenthesizedExpression):
            return self._generate_expression(expr.expression)
        else:
            raise CodeGeneratorError(f"Tipo de expressão primária não suportado: {type(expr).__name__}")
    
    def _generate_function_call(self, func_call: FunctionCall) -> str:
        """Gera código para chamada de função."""
        if func_call.name == "CalculateMean":
            if len(func_call.arguments) != 1:
                raise CodeGeneratorError(
                    f"CalculateMean espera 1 argumento, mas recebeu {len(func_call.arguments)}",
                    func_call.line,
                    func_call.col
                )
            # Por simplicidade, retorna 0.0 (implementação completa requeriria arrays)
            reg = self._new_register()
            self.llvm_code.append(f"  {reg} = fadd double 0.000000e+00, 0.000000e+00")
            return reg
        
        elif func_call.name == "CalculateSum":
            if len(func_call.arguments) != 1:
                raise CodeGeneratorError(
                    f"CalculateSum espera 1 argumento, mas recebeu {len(func_call.arguments)}",
                    func_call.line,
                    func_call.col
                )
            # Por simplicidade, retorna 0.0
            reg = self._new_register()
            self.llvm_code.append(f"  {reg} = fadd double 0.000000e+00, 0.000000e+00")
            return reg
        
        raise CodeGeneratorError(
            f"Função '{func_call.name}' não está definida",
            func_call.line,
            func_call.col
        )
    
    def _apply_relational_operator(self, op: str, left_reg: str, right_reg: str) -> str:
        """Aplica operador relacional e retorna registro booleano."""
        result_reg = self._new_register()
        
        if op == ">":
            self.llvm_code.append(f"  {result_reg} = fcmp ogt double {left_reg}, {right_reg}")
        elif op == "<":
            self.llvm_code.append(f"  {result_reg} = fcmp olt double {left_reg}, {right_reg}")
        elif op == ">=":
            self.llvm_code.append(f"  {result_reg} = fcmp oge double {left_reg}, {right_reg}")
        elif op == "<=":
            self.llvm_code.append(f"  {result_reg} = fcmp ole double {left_reg}, {right_reg}")
        elif op == "==":
            self.llvm_code.append(f"  {result_reg} = fcmp oeq double {left_reg}, {right_reg}")
        elif op == "!=":
            self.llvm_code.append(f"  {result_reg} = fcmp one double {left_reg}, {right_reg}")
        else:
            raise CodeGeneratorError(f"Operador relacional desconhecido: {op}")
        
        return result_reg
    
    def _apply_additive_operator(self, op: str, left_reg: str, right_reg: str) -> str:
        """Aplica operador aditivo."""
        result_reg = self._new_register()
        
        if op == "+":
            self.llvm_code.append(f"  {result_reg} = fadd double {left_reg}, {right_reg}")
        elif op == "-":
            self.llvm_code.append(f"  {result_reg} = fsub double {left_reg}, {right_reg}")
        else:
            raise CodeGeneratorError(f"Operador aditivo desconhecido: {op}")
        
        return result_reg
    
    def _apply_multiplicative_operator(self, op: str, left_reg: str, right_reg: str) -> str:
        """Aplica operador multiplicativo."""
        result_reg = self._new_register()
        
        if op == "*":
            self.llvm_code.append(f"  {result_reg} = fmul double {left_reg}, {right_reg}")
        elif op == "/":
            self.llvm_code.append(f"  {result_reg} = fdiv double {left_reg}, {right_reg}")
        else:
            raise CodeGeneratorError(f"Operador multiplicativo desconhecido: {op}")
        
        return result_reg
    
    def _new_register(self) -> str:
        """Gera um novo nome de registro LLVM."""
        reg = f"%{self.variable_counter}"
        self.variable_counter += 1
        return reg
    
    def _new_label(self, prefix: str) -> str:
        """Gera um novo label."""
        label = f"{prefix}{self.label_counter}"
        self.label_counter += 1
        return label
    
    def _get_string_constant(self, string_value: str) -> str:
        """Obtém ou cria uma constante de string global."""
        if string_value not in self.strings:
            global_name = f"str.{self.string_counter}"
            self.string_counter += 1
            self.strings[string_value] = global_name
        return self.strings[string_value]
    
    def _escape_string_for_llvm(self, s: str) -> str:
        """Escapa uma string para uso em LLVM IR."""
        result = []
        for char in s:
            if char == '\\':
                result.append('\\5C')
            elif char == '\n':
                result.append('\\0A')
            elif char == '\r':
                result.append('\\0D')
            elif char == '\t':
                result.append('\\09')
            elif char == '"':
                result.append('\\22')
            elif ord(char) < 32 or ord(char) > 126:
                # Caracteres não-ASCII ou especiais - escapa como hex
                result.append(f'\\{ord(char):02X}')
            else:
                # Caracteres normais, incluindo '%' que não precisa ser escapado aqui
                result.append(char)
        return ''.join(result)

