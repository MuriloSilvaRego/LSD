# 🔧 Guia de Geração de Código LLVM IR

## 📋 Visão Geral

Este módulo implementa a geração de código **LLVM IR (Intermediate Representation)** a partir da AST da linguagem LSD. O LLVM IR é uma linguagem intermediária que pode ser compilada para várias arquiteturas.

## 🎯 O que é LLVM IR?

**LLVM IR** é uma representação intermediária de código que:
- É independente de arquitetura
- Pode ser otimizada pelo LLVM
- Pode ser compilada para várias plataformas (x86, ARM, etc.)
- É legível e estruturada

## 🚀 Como Usar

### Método 1: Usando o Script de Teste

```bash
cd lib/parser
python testar_geracao_codigo.py
```

O script irá:
1. Parsear código LSD
2. Realizar análise semântica
3. Gerar código LLVM IR
4. Salvar em `output.ll`

### Método 2: Usando no Seu Código

```python
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

# Análise semântica (opcional, mas recomendado)
analyzer = SemanticAnalyzer()
result = analyzer.analyze(ast)

# Gerar código LLVM IR
generator = CodeGenerator()
llvm_code = generator.generate(ast)

# Salvar ou usar
print(llvm_code)
```

## 📝 Exemplo de Código Gerado

### Código LSD:
```lsd
nota1 = 8.5
nota2 = 7.0
soma = nota1 + nota2
Print soma
```

### LLVM IR Gerado:
```llvm
; LLVM IR gerado para linguagem LSD
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

declare i32 @printf(i8*, ...)

define i32 @main() {
entry:
  %0 = fadd double 0.000000e+00, 8.500000e+00
  %1 = alloca double, align 8
  store double %0, double* %1, align 8
  %2 = fadd double 0.000000e+00, 7.000000e+00
  %3 = alloca double, align 8
  store double %2, double* %3, align 8
  %4 = load double, double* %1, align 8
  %5 = load double, double* %3, align 8
  %6 = fadd double %4, %5
  %7 = alloca double, align 8
  store double %6, double* %7, align 8
  %8 = load double, double* %7, align 8
  call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.0, i64 0, i64 0), double %8)
  ret i32 0
}

@str.0 = private unnamed_addr constant [4 x i8] c"%f\n\00"
```

## 🔍 Estrutura do Código LLVM IR

### Componentes Principais

1. **Cabeçalho**: Define target e data layout
2. **Declarações Externas**: Funções como `printf`
3. **Função main**: Contém todo o código do programa
4. **Constantes Globais**: Strings e outros valores constantes

### Tipos de Instruções

- **alloca**: Aloca memória para variáveis
- **store**: Armazena valor em memória
- **load**: Carrega valor da memória
- **fadd/fsub/fmul/fdiv**: Operações aritméticas com double
- **fcmp**: Comparações de ponto flutuante
- **br**: Branch (salto condicional ou incondicional)
- **call**: Chamada de função
- **ret**: Retorno de função

## 🛠️ Compilando e Executando

### ⚠️ IMPORTANTE: Instalar LLVM Primeiro

Antes de compilar, você precisa ter o LLVM instalado. Veja o guia completo em `COMPILAR_LLVM.md`.

**Resumo rápido:**
- **Windows**: Baixe de https://github.com/llvm/llvm-project/releases e instale
- **Linux**: `sudo apt-get install llvm`
- **macOS**: `brew install llvm`

### Passo 1: Gerar o Código LLVM IR

```bash
python testar_geracao_codigo.py
```

Isso gera `output.ll` (agora com target correto para seu sistema)

### Passo 2: Compilar para Assembly

**Windows:**
```powershell
llc output.ll -o output.s
```

**Linux/macOS:**
```bash
llc output.ll -o output.s
```

**Se der erro "llc não encontrado":**
- Verifique se LLVM está instalado
- Verifique se está no PATH
- Veja `COMPILAR_LLVM.md` para instruções detalhadas

### Passo 3: Compilar para Executável

**Windows (MinGW):**
```powershell
gcc output.s -o output.exe
```

**Linux/macOS:**
```bash
gcc output.s -o output
```

### Passo 4: Executar

**Windows:**
```powershell
.\output.exe
```

**Linux/macOS:**
```bash
./output
```

### 🎯 Alternativa: Usar Apenas o Interpretador

Se você não tem LLVM instalado, pode usar apenas o interpretador:

```bash
python executar_lsd.py exemplo_completo.lsd
```

Isso executa o código diretamente sem precisar compilar!

## 📊 Mapeamento LSD → LLVM IR

### Tipos

| LSD | LLVM IR |
|-----|---------|
| INT | `i32` (convertido para `double`) |
| DECIMAL | `double` |
| STRING | `[N x i8]` (array de bytes) |
| BOOL | `i1` (convertido para `double` quando necessário) |

### Operações

| LSD | LLVM IR |
|-----|---------|
| `+` | `fadd double` |
| `-` | `fsub double` |
| `*` | `fmul double` |
| `/` | `fdiv double` |
| `>` | `fcmp ogt double` |
| `<` | `fcmp olt double` |
| `>=` | `fcmp oge double` |
| `<=` | `fcmp ole double` |
| `==` | `fcmp oeq double` |
| `!=` | `fcmp one double` |

### Statements

| LSD | LLVM IR |
|-----|---------|
| `x = expr` | `alloca` + `store` |
| `If cond ... End` | `fcmp` + `br` (branch condicional) |
| `Print expr` | `call @printf` |

## ⚠️ Limitações Atuais

1. **Listas**: Não totalmente suportadas (requer arrays LLVM)
2. **Funções**: `CalculateMean` e `CalculateSum` retornam valores placeholder
3. **Strings**: Suportadas apenas em `Print`
4. **Tipos**: Todos os números são tratados como `double`

## 🔧 Melhorias Futuras

- [ ] Suporte completo para arrays/listas
- [ ] Implementação real de `CalculateMean` e `CalculateSum`
- [ ] Otimizações LLVM
- [ ] Suporte para mais tipos de dados
- [ ] Geração de código para outras arquiteturas

## 📚 Referências

- [LLVM Language Reference](https://llvm.org/docs/LangRef.html)
- [LLVM IR Tutorial](https://llvm.org/docs/tutorial/)

---

**Criado para**: Projeto LSD - Compilador/Interpretador  
**Última atualização**: 2025

