# 📖 Manual de Utilização - Linguagem LSD

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Componentes do Sistema](#componentes-do-sistema)
3. [Como Usar Cada Componente](#como-usar-cada-componente)
4. [Exemplos Completos](#exemplos-completos)
5. [Referência Rápida](#referência-rápida)

---

## 🎯 Visão Geral

O sistema LSD é um compilador/interpretador completo que processa código na linguagem LSD através de várias etapas:

```
Código LSD → Lexer → Parser → AST → Análise Semântica → Interpretador/LLVM IR
```

---

## 🔧 Componentes do Sistema

### 1. Analisador Léxico (Lexer)
- **Arquivo**: `lib/lexer/afds/lexer3.py`
- **Função**: Converte código fonte em tokens
- **Saída**: Lista de tokens

### 2. Analisador Sintático (Parser)
- **Arquivo**: `lib/parser/parser.py`
- **Função**: Converte tokens em AST (Abstract Syntax Tree)
- **Saída**: Árvore sintática (AST)

### 3. Analisador Semântico
- **Arquivo**: `lib/parser/semantic_analyzer.py`
- **Função**: Verifica tipos, declarações e compatibilidade
- **Saída**: Tabela de símbolos, erros e warnings

### 4. Interpretador
- **Arquivo**: `lib/parser/interpreter.py`
- **Função**: Executa a AST diretamente
- **Saída**: Resultado da execução

### 5. Gerador de Código LLVM IR
- **Arquivo**: `lib/parser/code_generator.py`
- **Função**: Converte AST em código LLVM IR
- **Saída**: Código LLVM IR (`.ll`)

---

## 🚀 Como Usar Cada Componente

### 1. Analisador Léxico (Lexer)

#### Uso Básico

```python
from lexer3 import Lexer, InputBuffer

lexer = Lexer(palavras_chave=["If", "Print", "End"])
buffer = InputBuffer("x = 10")

token, erro = lexer.next_token(buffer)
while token and token.type != "EOF":
    print(f"Token: {token.type} = '{token.lexeme}'")
    token, erro = lexer.next_token(buffer)
```

#### O que faz:
- Lê o código fonte
- Identifica tokens (palavras-chave, números, operadores, etc.)
- Retorna tokens um por um

---

### 2. Analisador Sintático (Parser)

#### Uso Básico

```python
from lexer3 import Lexer
from parser import Parser

lexer = Lexer(palavras_chave=["If", "Print", "End"])
parser = Parser(lexer)

codigo = """x = 10
y = 20
soma = x + y"""

ast = parser.parse(codigo)
print(f"Programa parseado: {len(ast.statements)} statements")
```

#### O que faz:
- Recebe código fonte
- Usa o lexer para obter tokens
- Constrói a AST (árvore sintática)
- Retorna um objeto `Program` com a AST

#### Visualizar AST:

```python
from mostrar_arvore import mostrar_arvore

mostrar_arvore(ast)
```

---

### 3. Analisador Semântico

#### Uso Básico

```python
from semantic_analyzer import SemanticAnalyzer

analyzer = SemanticAnalyzer()
result = analyzer.analyze(ast)

# Verificar erros
if result['errors']:
    print("Erros encontrados:")
    for error in result['errors']:
        print(f"  - {error}")

# Ver tipos inferidos
print("\nTabela de símbolos:")
for var, tipo in result['symbols'].items():
    print(f"  {var}: {tipo.value}")
```

#### O que faz:
- Analisa a AST
- Infere tipos de variáveis
- Verifica compatibilidade de tipos
- Detecta variáveis não declaradas
- Retorna erros, warnings e tabela de símbolos

---

### 4. Interpretador

#### Uso Básico

```python
from interpreter import Interpreter

interpreter = Interpreter()
output = interpreter.interpret(ast)

# Mostrar saída
for line in output:
    print(line)
```

#### O que faz:
- Executa a AST diretamente
- Avalia expressões
- Executa statements
- Retorna a saída do programa

---

### 5. Gerador de Código LLVM IR

#### Uso Básico

```python
from code_generator import CodeGenerator

generator = CodeGenerator()
llvm_code = generator.generate(ast)

# Salvar em arquivo
with open('output.ll', 'w') as f:
    f.write(llvm_code)
```

#### O que faz:
- Converte AST em código LLVM IR
- Gera código que pode ser compilado
- Retorna string com código LLVM IR

---

## 📝 Exemplos Completos

### Exemplo 1: Fluxo Completo (Interpretador)

```python
import sys
import os

# Adiciona paths
sys.path.insert(0, os.path.join('lib', 'lexer', 'afds'))
sys.path.insert(0, os.path.join('lib', 'parser'))

from lexer3 import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from interpreter import Interpreter

# Código LSD
codigo = """nota1 = 8.5
nota2 = 7.0
soma = nota1 + nota2
media = soma / 2
Print "Media:"
Print media"""

# [1] Parsear
lexer = Lexer(palavras_chave=["If", "Print", "End"])
parser = Parser(lexer)
ast = parser.parse(codigo)

# [2] Análise semântica
analyzer = SemanticAnalyzer()
result = analyzer.analyze(ast)

if result['errors']:
    print("Erros:", result['errors'])
    exit(1)

# [3] Executar
interpreter = Interpreter()
output = interpreter.interpret(ast)

# [4] Mostrar resultado
for line in output:
    print(line)
```

**Saída:**
```
Media:
7.75
```

---

### Exemplo 2: Gerar Código LLVM IR

```python
import sys
import os

sys.path.insert(0, os.path.join('lib', 'lexer', 'afds'))
sys.path.insert(0, os.path.join('lib', 'parser'))

from lexer3 import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator

# Código LSD
codigo = """x = 10
y = 20
soma = x + y
Print soma"""

# Parsear
lexer = Lexer(palavras_chave=["If", "Print", "End"])
parser = Parser(lexer)
ast = parser.parse(codigo)

# Análise semântica
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

# Gerar LLVM IR
generator = CodeGenerator()
llvm_code = generator.generate(ast)

# Salvar
with open('output.ll', 'w') as f:
    f.write(llvm_code)

print("Código LLVM IR gerado em output.ll")
```

---

### Exemplo 3: Visualizar AST

```python
import sys
import os

sys.path.insert(0, os.path.join('lib', 'lexer', 'afds'))
sys.path.insert(0, os.path.join('lib', 'parser'))

from lexer3 import Lexer
from parser import Parser
from mostrar_arvore import mostrar_arvore

codigo = """x = 10
y = 20
soma = x + y"""

lexer = Lexer(palavras_chave=["If", "Print", "End"])
parser = Parser(lexer)
ast = parser.parse(codigo)

mostrar_arvore(ast)
```

---

## 📊 Referência Rápida

### Scripts Prontos

| Script | Função |
|--------|--------|
| `testar_parser.py` | Testa o parser |
| `testar_semantica.py` | Testa análise semântica |
| `testar_geracao_codigo.py` | Testa geração de código LLVM |
| `mostrar_arvore.py` | Visualiza a árvore AST |

### Classes Principais

| Classe | Módulo | Função |
|--------|--------|--------|
| `Lexer` | `lexer3` | Análise léxica |
| `Parser` | `parser` | Análise sintática |
| `SemanticAnalyzer` | `semantic_analyzer` | Análise semântica |
| `Interpreter` | `interpreter` | Execução |
| `CodeGenerator` | `code_generator` | Geração LLVM IR |

### Tipos de Dados

| LSD | Python | LLVM IR |
|-----|--------|---------|
| INT | `int` | `i32` → `double` |
| DECIMAL | `float` | `double` |
| STRING | `str` | `[N x i8]` |
| LIST | `list` | (não totalmente suportado) |
| BOOL | `bool` | `i1` → `double` |

---

## 🎓 Dicas de Uso

### Para Desenvolvimento

1. **Sempre faça análise semântica** antes de executar
2. **Visualize a AST** para entender o que foi parseado
3. **Teste com exemplos simples** primeiro
4. **Leia as mensagens de erro** - elas são descritivas

### Para Apresentação

1. **Use `mostrar_arvore.py`** para demonstrar a AST
2. **Mostre o fluxo completo**: código → tokens → AST → execução
3. **Demonstre detecção de erros** com exemplos intencionais
4. **Compare código LSD com LLVM IR** gerado

---

## 📚 Documentação Adicional

- **Manual de Instalação**: `docs/MANUAL_INSTALACAO.md`
- **Guia da Árvore AST**: `lib/parser/README_ARVORE_AST.md`
- **Guia LLVM IR**: `lib/parser/README_LLVM.md`
- **Gramática**: `grammar.md`

---

**Última atualização**: 2025
**Versão**: 1.0

