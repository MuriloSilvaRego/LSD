# 📊 Guia de Visualização da Árvore AST - Linguagem LSD

## 🌳 O que é a Árvore AST?

A **Abstract Syntax Tree (AST)** é uma representação hierárquica da estrutura sintática do código fonte. Ela mostra como o parser organizou o código em uma árvore de nós, onde cada nó representa uma construção da linguagem.

### Por que é importante?

- **Visualização**: Permite ver a estrutura do código de forma organizada
- **Depuração**: Ajuda a entender como o parser interpretou o código
- **Análise**: Facilita a compreensão da hierarquia de expressões e statements
- **Apresentação**: Demonstra o funcionamento do parser de forma visual

---

## 🚀 Como Usar

### Método 1: Usando o Script `mostrar_arvore.py`

Este é o método mais simples e recomendado para apresentações:

```bash
cd lib/parser
python mostrar_arvore.py
```

O script irá:
1. Parsear um código LSD de exemplo
2. Gerar a AST
3. Exibir a árvore de forma hierárquica e visual

### Método 2: Usando no Seu Próprio Código

```python
import sys
import os

# Adiciona paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer', 'afds'))
sys.path.insert(0, os.path.dirname(__file__))

from lexer3 import Lexer
from parser import Parser
from lsd_ast import Program

# Seu código LSD
codigo = """nota1 = 8.5
nota2 = 7.0
soma = nota1 + nota2
Print soma"""

# Parsear
lexer = Lexer(palavras_chave=["If", "Print", "End"])
parser = Parser(lexer)
ast = parser.parse(codigo)

# Visualizar (usando a função do mostrar_arvore.py)
from mostrar_arvore import mostrar_arvore
mostrar_arvore(ast)
```

---

## 📋 Estrutura da Árvore

### Níveis da Hierarquia

A árvore AST é organizada em níveis hierárquicos:

```
Program (raiz)
├── Statement (Assignment, Conditional, Print)
│   ├── Expression (Relational, Additive, Multiplicative, Unary)
│   │   └── PrimaryExpression (Literal, Identifier, FunctionCall, List)
│   └── ...
```

### Tipos de Nós

#### 1. **Program** (Raiz)
- Contém a lista de todos os statements do programa

#### 2. **Statements**
- **Assignment**: Atribuições (`x = 10`)
- **ConditionalStatement**: Condicionais (`If ... End`)
- **PrintStatement**: Impressões (`Print ...`)

#### 3. **Expressões**
- **RelationalExpression**: Comparações (`>`, `<`, `>=`, etc.)
- **AdditiveExpression**: Somas e subtrações (`+`, `-`)
- **MultiplicativeExpression**: Multiplicações e divisões (`*`, `/`)
- **UnaryExpression**: Operadores unários (`+`, `-`)

#### 4. **Expressões Primárias**
- **IntegerLiteral**: Números inteiros (`10`, `42`)
- **DecimalLiteral**: Números decimais (`8.5`, `3.14`)
- **StringLiteral**: Strings (`"texto"`)
- **Identifier**: Variáveis (`x`, `soma`)
- **FunctionCall**: Chamadas de função (`CalculateMean(...)`)
- **ListExpression**: Listas (`[1, 2, 3]`)
- **ParenthesizedExpression**: Parênteses (`(x + y)`)

---

## 📖 Exemplos Práticos

### Exemplo 1: Atribuição Simples

**Código LSD:**
```lsd
x = 10
```

**Árvore AST:**
```
Program
  Assignment: x
    RelationalExpression (operadores: sem operadores)
      Left:
        AdditiveExpression (operadores: sem operadores)
          Left:
            MultiplicativeExpression (operadores: sem operadores)
              Left:
                UnaryExpression
                  IntegerLiteral: 10
```

### Exemplo 2: Expressão Aritmética

**Código LSD:**
```lsd
soma = nota1 + nota2
```

**Árvore AST:**
```
Program
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
```

### Exemplo 3: Condicional

**Código LSD:**
```lsd
If media >= 7.0
Print "Aprovado"
End
```

**Árvore AST:**
```
Program
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
    Body (1 statements):
      PrintStatement: "Aprovado"
```

### Exemplo 4: Expressão Complexa

**Código LSD:**
```lsd
resultado = (x + y) * 2
```

**Árvore AST:**
```
Program
  Assignment: resultado
    RelationalExpression (operadores: sem operadores)
      Left:
        AdditiveExpression (operadores: sem operadores)
          Left:
            MultiplicativeExpression (operadores: *)
              Left:
                UnaryExpression
                  ParenthesizedExpression: (Expression)
                    RelationalExpression (operadores: sem operadores)
                      Left:
                        AdditiveExpression (operadores: +)
                          Left:
                            MultiplicativeExpression (operadores: sem operadores)
                              Left:
                                UnaryExpression
                                  Identifier: x
                          Operador: +
                          MultiplicativeExpression (operadores: sem operadores)
                            Left:
                              UnaryExpression
                                Identifier: y
              Operador: *
              UnaryExpression
                IntegerLiteral: 2
```

---

## 🎯 Dicas para Apresentação

### 1. **Comece com Exemplos Simples**
- Mostre primeiro uma atribuição simples (`x = 10`)
- Depois uma expressão aritmética (`soma = a + b`)
- Por fim, exemplos mais complexos

### 2. **Explique a Hierarquia**
- Mostre como as expressões são aninhadas
- Explique a precedência de operadores (multiplicação antes de adição)
- Demonstre como parênteses alteram a estrutura

### 3. **Compare Código e Árvore**
- Mostre o código LSD lado a lado com a árvore
- Aponte como cada parte do código vira um nó na árvore
- Explique a correspondência entre sintaxe e estrutura

### 4. **Use Cores/Formatação**
- Se possível, use cores diferentes para diferentes tipos de nós
- Destaque a raiz (Program) e os nós principais
- Mostre a hierarquia com indentação clara

---

## 🔍 Interpretando a Árvore

### Como Ler a Árvore

1. **Comece pela raiz**: Sempre comece pelo nó `Program`
2. **Desça hierarquicamente**: Cada nível de indentação é um nível mais profundo na árvore
3. **Leia da esquerda para direita**: A ordem dos nós reflete a ordem de execução
4. **Observe os operadores**: Operadores aparecem entre os operandos

### Exemplo de Leitura

Para `soma = nota1 + nota2`:

1. **Program**: O programa completo
2. **Assignment: soma**: Uma atribuição à variável `soma`
3. **RelationalExpression**: A expressão (sem operadores relacionais)
4. **AdditiveExpression**: Expressão aditiva com operador `+`
5. **Left**: Lado esquerdo (`nota1`)
6. **Operador: +**: O operador de adição
7. **Right**: Lado direito (`nota2`)

---

## 🛠️ Personalização

### Modificar o Código de Exemplo

Edite o arquivo `mostrar_arvore.py` e altere a variável `codigo_demo`:

```python
codigo_demo = """seu codigo aqui
mais linhas
"""
```

### Ajustar Profundidade Máxima

Na função `mostrar_arvore()`, ajuste o parâmetro `max_depth`:

```python
mostrar_arvore(ast, max_depth=20)  # Aumenta a profundidade
```

### Adicionar Mais Informações

Você pode modificar a função `mostrar_arvore()` para exibir mais detalhes:

```python
# Exemplo: mostrar linha e coluna
print(f"{espacos}Assignment: {node.identifier} (linha {node.line})")
```

---

## 📝 Resumo para Apresentação

### Pontos Principais a Destacar

1. ✅ **A árvore mostra a estrutura sintática do código**
2. ✅ **Cada nó representa uma construção da linguagem**
3. ✅ **A hierarquia reflete a precedência de operadores**
4. ✅ **A árvore é gerada automaticamente pelo parser**
5. ✅ **É usada para análise semântica e interpretação**

### Fluxo de Demonstração Sugerido

1. **Mostre o código LSD** (exemplo simples)
2. **Execute o `mostrar_arvore.py`**
3. **Explique a estrutura da árvore** (nível por nível)
4. **Compare código e árvore** (mostre correspondências)
5. **Demonstre com exemplo mais complexo**
6. **Explique como a árvore é usada** (semântica, interpretação)

---

## ❓ Perguntas Frequentes

### Q: Por que a árvore é tão profunda para expressões simples?

**R:** A árvore segue a hierarquia da gramática. Mesmo expressões simples passam por todos os níveis (Relational → Additive → Multiplicative → Unary → Primary) para manter a consistência.

### Q: Como a árvore mostra a precedência de operadores?

**R:** A precedência é refletida na hierarquia. Operadores de maior precedência (multiplicação) ficam mais profundos, e operadores de menor precedência (adição) ficam mais acima.

### Q: Posso modificar a árvore?

**R:** A árvore é gerada pelo parser e não deve ser modificada diretamente. Modificações devem ser feitas no código fonte LSD.

---

## 📚 Arquivos Relacionados

- `mostrar_arvore.py`: Script para visualizar a árvore
- `parser.py`: Gera a AST a partir do código
- `lsd_ast.py`: Define a estrutura dos nós da AST
- `testar_parser.py`: Testa o parser e gera ASTs

---

**Criado para**: Projeto LSD - Compilador/Interpretador  
**Última atualização**: 2025

