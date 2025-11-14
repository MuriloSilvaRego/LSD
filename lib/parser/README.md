# Sistema de Parser e Interpretador LSD

Sistema completo de análise e execução para a linguagem LSD, incluindo parser recursivo descendente, análise semântica com inferência de tipos e interpretador.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Usar](#como-usar)
- [Visualizando a Árvore AST](#visualizando-a-árvore-ast)
- [Componentes Principais](#componentes-principais)
- [Exemplos](#exemplos)

---

## 🎯 Visão Geral

Este sistema implementa um compilador/interpretador completo para a linguagem LSD, com as seguintes funcionalidades:

1. **Análise Léxica** (Lexer) - Tokenização do código fonte
2. **Análise Sintática** (Parser) - Geração da Abstract Syntax Tree (AST)
3. **Análise Semântica** - Verificação de tipos e inferência
4. **Interpretação** - Execução do código

---

## 📁 Estrutura do Projeto

```
lib/parser/
├── parser.py                    # Parser recursivo descendente
├── lsd_ast.py                   # Definições dos nós da AST
├── semantic_analyzer.py         # Analisador semântico e inferência de tipos
├── interpreter.py               # Interpretador para execução
├── mostrar_arvore.py           # Visualizador da árvore AST ⭐
├── testar_parser.py            # Teste do parser
├── testar_semantica.py         # Teste da análise semântica
├── testar_erros_semanticos.py  # Teste de detecção de erros
└── README.md                    # Este arquivo
```

---

## 🚀 Como Usar

### 1. Parsing Básico

```python
from lexer3 import Lexer
from parser import Parser

lexer = Lexer(palavras_chave=["If", "Print", "End"])
parser = Parser(lexer)
ast = parser.parse("x = 10\ny = 20\nsoma = x + y")
```

### 2. Análise Semântica

```python
from semantic_analyzer import SemanticAnalyzer

analyzer = SemanticAnalyzer()
result = analyzer.analyze(ast)

# Verifica erros
if result['errors']:
    for error in result['errors']:
        print(f"Erro: {error}")

# Mostra tipos inferidos
for var, tipo in result['symbols'].items():
    print(f"{var}: {tipo.value}")
```

### 3. Interpretação

```python
from interpreter import Interpreter

interpreter = Interpreter()
output = interpreter.interpret(ast)

for line in output:
    print(line)
```

---

## 🌳 Visualizando a Árvore AST

**Esta é a parte mais importante para apresentação!** A árvore AST mostra a estrutura hierárquica do código parseado.

### Como Visualizar

Execute o arquivo `mostrar_arvore.py`:

```bash
python mostrar_arvore.py
```

### Exemplo de Saída

Para o código:
```lsd
nota1 = 8.5
nota2 = 7.0
soma = nota1 + nota2
media = soma / 2
If media >= 7.0
Print "Aprovado"
Print media
End
```

A árvore gerada será:

```
Program
  Assignment: nota1
    RelationalExpression (operadores: sem operadores)
      Left:
        AdditiveExpression (operadores: sem operadores)
          Left:
            MultiplicativeExpression (operadores: sem operadores)
              Left:
                UnaryExpression
                  DecimalLiteral: 8.5
  Assignment: nota2
    RelationalExpression (operadores: sem operadores)
      Left:
        AdditiveExpression (operadores: sem operadores)
          Left:
            MultiplicativeExpression (operadores: sem operadores)
              Left:
                UnaryExpression
                  DecimalLiteral: 7.0
  Assignment: soma
    RelationalExpression (operadores: sem operadores)
      Left:
        AdditiveExpression (operadores: +)
          Left:
            MultiplicativeExpression (operadores: sem operadores)
              Left:
                UnaryExpression
                  Identifier: nota1
          Operador: +
            MultiplicativeExpression (operadores: sem operadores)
              Left:
                UnaryExpression
                  Identifier: nota2
  Assignment: media
    RelationalExpression (operadores: sem operadores)
      Left:
        AdditiveExpression (operadores: sem operadores)
          Left:
            MultiplicativeExpression (operadores: /)
              Left:
                UnaryExpression
                  Identifier: soma
              Operador: /
                UnaryExpression
                  IntegerLiteral: 2
  ConditionalStatement (If ... End)
    Condition:
      RelationalExpression (operadores: >=)
        Left:
          AdditiveExpression (operadores: sem operadores)
            Left:
              MultiplicativeExpression (operadores: sem operadores)
                Left:
                  UnaryExpression
                    Identifier: media
        Operador: >=
          AdditiveExpression (operadores: sem operadores)
            Left:
              MultiplicativeExpression (operadores: sem operadores)
                Left:
                  UnaryExpression
                    DecimalLiteral: 7.0
    Body (2 statements):
      PrintStatement: "Aprovado"
      PrintStatement:
        RelationalExpression (operadores: sem operadores)
          Left:
            AdditiveExpression (operadores: sem operadores)
              Left:
                MultiplicativeExpression (operadores: sem operadores)
                  Left:
                    UnaryExpression
                      Identifier: media
```

### Estrutura da Árvore

A árvore mostra:

1. **Nível Raiz**: `Program` - contém todos os statements
2. **Statements**: 
   - `Assignment` - atribuições (variável = expressão)
   - `ConditionalStatement` - condicionais (If ... End)
   - `PrintStatement` - prints
3. **Expressões** (hierarquia de precedência):
   - `RelationalExpression` - comparações (>, <, >=, <=, ==, !=)
   - `AdditiveExpression` - adição/subtração (+, -)
   - `MultiplicativeExpression` - multiplicação/divisão (*, /)
   - `UnaryExpression` - operadores unários (+, -)
   - `PrimaryExpression` - literais, identificadores, funções, listas
4. **Literais**:
   - `IntegerLiteral` - números inteiros
   - `DecimalLiteral` - números decimais
   - `StringLiteral` - strings
   - `Identifier` - variáveis
   - `FunctionCall` - chamadas de função
   - `ListExpression` - listas

### Personalizando a Visualização

Você pode modificar o código em `mostrar_arvore.py` para personalizar a apresentação:

```python
# Alterar a profundidade máxima
mostrar_arvore(ast, max_depth=10)  # Limita a 10 níveis

# Modificar a indentação
espacos = "    " * indent  # 4 espaços por nível
```

---

## 🔧 Componentes Principais

### 1. Parser (`parser.py`)

- **Tipo**: Parser recursivo descendente LL(1)
- **Função**: Converte código fonte em AST
- **Método principal**: `parse(source: str) -> Program`

### 2. AST (`lsd_ast.py`)

- **Tipo**: Definições de nós usando dataclasses
- **Função**: Representa a estrutura sintática do programa
- **Nós principais**: Program, Statement, Expression, Literals

### 3. Analisador Semântico (`semantic_analyzer.py`)

- **Tipo**: Analisador semântico com inferência de tipos
- **Função**: Verifica tipos, declarações e compatibilidade
- **Método principal**: `analyze(program: Program) -> Dict`

### 4. Interpretador (`interpreter.py`)

- **Tipo**: Interpretador de árvore
- **Função**: Executa a AST e produz saída
- **Método principal**: `interpret(program: Program) -> List[str]`

---

## 📝 Exemplos

### Exemplo 1: Código Simples

```lsd
x = 10
y = 20
soma = x + y
Print soma
```

**Árvore AST**:
```
Program
  Assignment: x
    RelationalExpression
      Left: AdditiveExpression
        Left: MultiplicativeExpression
          Left: UnaryExpression
            IntegerLiteral: 10
  Assignment: y
    ...
  Assignment: soma
    ...
  PrintStatement
    ...
```

### Exemplo 2: Com Condicional

```lsd
nota = 8.5
If nota >= 7.0
Print "Aprovado"
End
```

**Árvore AST**:
```
Program
  Assignment: nota
    ...
  ConditionalStatement
    Condition:
      RelationalExpression (operadores: >=)
        Left: ... (nota)
        Operador: >=
          ... (7.0)
    Body:
      PrintStatement: "Aprovado"
```

### Exemplo 3: Com Lista

```lsd
valores = [1, 2, 3, 4, 5]
soma = CalculateSum(valores)
Print soma
```

**Árvore AST**:
```
Program
  Assignment: valores
    ListExpression (5 elementos)
      Elemento 1: IntegerLiteral: 1
      Elemento 2: IntegerLiteral: 2
      ...
  Assignment: soma
    FunctionCall: CalculateSum(1 argumentos)
      Argumento 1: Identifier: valores
  PrintStatement
    ...
```

---

## 🎓 Para Apresentação

### Dicas para Apresentar a Árvore

1. **Comece com código simples**: Mostre um exemplo básico primeiro
2. **Explique a hierarquia**: Mostre como as expressões são aninhadas
3. **Demonstre precedência**: Mostre como `2 + 3 * 4` é parseado
4. **Mostre diferentes tipos**: Literais, variáveis, funções, listas
5. **Compare código e árvore**: Mostre lado a lado o código e sua representação

### Exemplo de Apresentação

```
1. Mostrar código LSD
   ↓
2. Executar mostrar_arvore.py
   ↓
3. Explicar a estrutura hierárquica
   ↓
4. Destacar nós importantes
   ↓
5. Mostrar como a precedência é respeitada
```

---

## 🐛 Tratamento de Erros

O sistema detecta e reporta erros em três níveis:

1. **Erros Léxicos**: Tokens inválidos
2. **Erros Sintáticos**: Estrutura incorreta (parse)
3. **Erros Semânticos**: Tipos incompatíveis, variáveis não declaradas

Todos os erros incluem linha e coluna para fácil localização.

---

## 📚 Tipos Suportados

- **INT**: Números inteiros
- **DECIMAL**: Números decimais
- **STRING**: Strings
- **LIST**: Listas de valores
- **BOOL**: Resultado de expressões relacionais

---

## 🔍 Testes

Execute os testes para verificar o funcionamento:

```bash
# Teste do parser
python testar_parser.py

# Teste da análise semântica
python testar_semantica.py

# Teste de detecção de erros
python testar_erros_semanticos.py

# Visualizar árvore
python mostrar_arvore.py
```

---

## 📖 Referências

- Gramática: `grammar.md`
- FIRST/FOLLOW: `FIRST_FOLLOW.md`
- Especificação da linguagem LSD

---

## 👨‍💻 Autor

Sistema desenvolvido para o projeto de Compiladores/Interpretadores.

---

**Última atualização**: 2024

