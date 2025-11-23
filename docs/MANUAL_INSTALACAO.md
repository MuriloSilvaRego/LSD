# 📘 Manual de Instalação e Utilização - Linguagem LSD

## 📋 Índice

1. [Requisitos do Sistema](#requisitos-do-sistema)
2. [Instalação Passo a Passo](#instalação-passo-a-passo)
3. [Como Compilar um Programa LSD](#como-compilar-um-programa-lsd)
4. [Exemplos Práticos](#exemplos-práticos)
5. [Criando Seus Próprios Exemplos](#criando-seus-próprios-exemplos)
6. [Scripts Disponíveis](#scripts-disponíveis)
7. [Solução de Problemas](#solução-de-problemas)
8. [Recursos Adicionais](#recursos-adicionais)
9. [Checklist de Verificação](#checklist-de-verificação)
10. [Para Iniciantes](#para-iniciantes)

---

## 🔧 Requisitos do Sistema

### Obrigatórios

- **Python 3.7 ou superior**
  - Verificar: `python --version` ou `python3 --version`
  - Download: [python.org](https://www.python.org/downloads/)

### Opcionais (para compilar LLVM IR)

- **LLVM** (para compilar código LLVM IR)
  - Windows: [LLVM Releases](https://github.com/llvm/llvm-project/releases)
  - Linux: `sudo apt-get install llvm`
  - macOS: `brew install llvm`

- **GCC** (compilador C)
  - Windows: [MinGW-w64](https://www.mingw-w64.org/)
  - Linux: `sudo apt-get install gcc`
  - macOS: Já incluído no Xcode Command Line Tools

---

## 📦 Instalação Passo a Passo

### Passo 1: Verificar Python

Abra o terminal (PowerShell no Windows, Terminal no Linux/macOS) e execute:

```bash
python --version
```

**Resultado esperado**: `Python 3.7.x` ou superior

**Se não tiver Python instalado:**
- Windows: Baixe do site oficial e marque "Add Python to PATH"
- Linux: `sudo apt-get install python3`
- macOS: Já vem instalado, ou use `brew install python3`

### Passo 2: Baixar/Clonar o Projeto

Se você já tem o projeto, pule para o Passo 3.

**Opção A - Se o projeto está em um repositório Git:**
```bash
git clone <url-do-repositorio>
cd LSD
```

**Opção B - Se você tem os arquivos:**
- Navegue até a pasta do projeto no terminal
- Exemplo: `cd C:\Users\pedrov\Desktop\LSD\LSD`

### Passo 3: Verificar Estrutura do Projeto

O projeto deve ter a seguinte estrutura:

```
LSD/
├── lib/
│   ├── lexer/
│   │   └── afds/
│   │       └── lexer3.py
│   └── parser/
│       ├── parser.py
│       ├── lsd_ast.py
│       ├── semantic_analyzer.py
│       ├── code_generator.py
│       └── ...
└── README.md
```

### Passo 4: Testar Instalação

Execute um teste simples:

```bash
cd lib/parser
python testar_parser.py
```

**Resultado esperado**: Mensagem de sucesso do parser

---

## 🚀 Como Compilar um Programa LSD

### Método 1: Usando o Script Executor (Mais Simples) ⭐

Este é o método mais fácil! O projeto já vem com um script pronto que faz tudo automaticamente.

#### Como Executar

**Executar qualquer arquivo .lsd:**

```bash
python executar_lsd.py nome_do_arquivo.lsd
```

**Windows:**
```powershell
python executar_lsd.py nome_do_arquivo.lsd
```

**Linux/macOS:**
```bash
python3 executar_lsd.py nome_do_arquivo.lsd
```

**Exemplo:**
```bash
python executar_lsd.py exemplo_completo.lsd
```

**O que o script faz automaticamente:**
1. ✅ Lê o arquivo LSD
2. ✅ Faz análise léxica (tokenização)
3. ✅ Faz análise sintática (parsing)
4. ✅ Faz análise semântica (verificação de tipos)
5. ✅ Executa o programa
6. ✅ Mostra a saída

**Você não precisa criar nenhum script Python!** O `executar_lsd.py` já faz tudo.

---

### Método 2: Gerando Código LLVM IR (Avançado)

Este método gera código LLVM IR que pode ser compilado para executável.

#### Gerar LLVM IR

**Uso:**
```bash
python gerar_llvm.py arquivo.lsd [output.ll]
```

**Exemplo:**
```bash
python gerar_llvm.py gerar_llvm.lsd
```

Isso cria o arquivo `output.ll` com código LLVM IR.

**O que o script faz:**
1. ✅ Lê o arquivo LSD
2. ✅ Faz parsing
3. ✅ Análise semântica
4. ✅ Gera código LLVM IR
5. ✅ Salva em arquivo

#### Compilar para Assembly (requer LLVM instalado)

```bash
llc output.ll -o output.s
```

**Nota**: Se `llc` não for encontrado, instale o LLVM (veja Requisitos do Sistema ou `lib/parser/COMPILAR_LLVM.md`).

#### Compilar para Executável (requer GCC instalado)

**Linux/macOS:**
```bash
gcc output.s -o output
./output
```

**Windows (MinGW):**
```powershell
gcc output.s -o output.exe
.\output.exe
```

**Nota**: Se `gcc` não for encontrado, instale o GCC (veja Requisitos do Sistema).

---

## 📝 Exemplos Práticos

### 1. Exemplo Simples

**Descrição**: Exemplo básico com variáveis e operações aritméticas.

**Código:**
```lsd
x = 10
y = 20
soma = x + y
Print "A soma de x e y e:"
Print soma
```

**Executar:**
```bash
python executar_lsd.py exemplo_simples.lsd
```

**Saída esperada:**
```
A soma de x e y e:
30
```

---

### 2. Exemplo com Condicional

**Descrição**: Demonstra uso de condicionais (If/End).

**Código:**
```lsd
idade = 18
Print "Idade:"
Print idade
If idade >= 18
Print "Maior de idade"
End
If idade < 18
Print "Menor de idade"
End
```

**Executar:**
```bash
python executar_lsd.py exemplo_condicional.lsd
```

---

### 3. Exemplo com Expressões Complexas

**Descrição**: Demonstra precedência de operadores e expressões complexas.

**Código:**
```lsd
a = 10
b = 5
c = 2
resultado1 = a + b * c
resultado2 = (a + b) * c
Print "Resultado 1 (a + b * c):"
Print resultado1
Print "Resultado 2 ((a + b) * c):"
Print resultado2
```

**Executar:**
```bash
python executar_lsd.py exemplo_expressoes.lsd
```

---

### 4. Exemplo Completo ⭐

**Descrição**: Exemplo completo demonstrando todas as funcionalidades.

**Características:**
- Múltiplas variáveis
- Operações aritméticas
- Condicionais
- Múltiplos prints
- Expressões complexas

**Executar:**
```bash
python executar_lsd.py exemplo_completo.lsd
```

**Saída esperada:**
```
=== Sistema de Notas ===
Nota 1:
8.5
Nota 2:
7.0
Nota 3:
9.0
Soma das notas:
24.5
Media final:
8.166666666666666
Status: APROVADO
Resultado (x10):
81.66666666666666
```

---

### 5. Gerar LLVM IR

**Descrição**: Exemplo simples para gerar código LLVM IR.

**Código:**
```lsd
x = 10
y = 20
z = x + y
Print "Soma de x e y:"
Print z
resultado = z * 2
Print "Resultado (x2):"
Print resultado
```

**Gerar LLVM IR:**
```bash
python gerar_llvm.py gerar_llvm.lsd
```

Isso cria o arquivo `output.ll` com código LLVM IR.

---

## 📚 Criando Seus Próprios Exemplos

### Estrutura Básica

```lsd
variavel = valor
Print "Texto"
Print variavel
```

### Com Condicional

```lsd
x = 10
If x > 5
Print "Maior que 5"
End
```

### Com Expressões

```lsd
a = 10
b = 5
resultado = a + b * 2
Print resultado
```

---

## 💡 Dicas

1. **Comece simples**: Use exemplos básicos como base
2. **Teste incrementalmente**: Adicione uma linha por vez
3. **Veja os erros**: As mensagens de erro são descritivas e indicam linha/coluna
4. **Use prints**: Para debugar, adicione prints intermediários

---

## 🔍 Visualizar Árvore AST

Para ver a estrutura da árvore sintática:

```bash
cd lib/parser
python mostrar_arvore.py
```

Isso mostra a estrutura hierárquica da AST do código.

---

## 🛠️ Solução de Problemas

### Problema 1: "python: comando não encontrado"

**Solução:**
- Windows: Use `py` em vez de `python`
- Linux/macOS: Use `python3` em vez de `python`
- Ou adicione Python ao PATH do sistema

### Problema 2: "Arquivo não encontrado"

**Solução:**
- Verifique se está na pasta correta (raiz do projeto)
- Use caminho completo: `python executar_lsd.py C:\caminho\completo\arquivo.lsd`
- Verifique se o arquivo `.lsd` existe

### Problema 3: "ModuleNotFoundError: No module named 'lexer3'"

**Solução:**
- Certifique-se de estar na raiz do projeto (não dentro de `lib/parser`)
- Execute `python executar_lsd.py` da raiz do projeto
- O script já configura os paths automaticamente

### Problema 4: "Erro de parsing"

**Solução:**
- Verifique a sintaxe do código
- Consulte `grammar.md` para a gramática correta
- A mensagem de erro indica linha e coluna exatas

### Problema 5: "Erro semântico"

**Solução:**
- Verifique se variáveis foram declaradas antes de usar
- Verifique compatibilidade de tipos
- A mensagem de erro indica qual variável e qual tipo é esperado

### Problema 6: "llc: comando não encontrado"

**Solução:**
- Instale o LLVM (veja Requisitos do Sistema)
- Ou use apenas o interpretador (Método 1) - não precisa de LLVM
- Veja `lib/parser/COMPILAR_LLVM.md` para instruções detalhadas

### Problema 7: "gcc: comando não encontrado"

**Solução:**
- Instale o GCC (veja Requisitos do Sistema)
- Ou use apenas o interpretador (Método 1) - não precisa de GCC
- Windows: Instale MinGW-w64

---

## 🛠️ Scripts Disponíveis

### `executar_lsd.py` ⭐

**O que faz**: Executa código LSD usando o interpretador.

**Uso:**
```bash
python executar_lsd.py arquivo.lsd
```

**Processo automático:**
1. ✅ Lê o arquivo LSD
2. ✅ Faz parsing
3. ✅ Análise semântica
4. ✅ Executa o programa
5. ✅ Mostra a saída

---

### `gerar_llvm.py`

**O que faz**: Gera código LLVM IR a partir de arquivo LSD.

**Uso:**
```bash
python gerar_llvm.py arquivo.lsd [output.ll]
```

**Processo automático:**
1. ✅ Lê o arquivo LSD
2. ✅ Faz parsing
3. ✅ Análise semântica
4. ✅ Gera código LLVM IR
5. ✅ Salva em arquivo

---

### Scripts de Teste (Avançados)

- `lib/parser/testar_parser.py` - Testa o parser
- `lib/parser/testar_semantica.py` - Testa análise semântica
- `lib/parser/testar_geracao_codigo.py` - Testa geração de código
- `lib/parser/mostrar_arvore.py` - Visualiza a árvore AST

---

## 📚 Recursos Adicionais

### Documentação

- **README Principal**: `README.md`
- **Manual de Utilização**: `docs/MANUAL_UTILIZACAO.md`
- **Exemplos**: `EXEMPLOS.md`
- **Guia da Árvore AST**: `lib/parser/README_ARVORE_AST.md`
- **Guia LLVM IR**: `lib/parser/README_LLVM.md`
- **Como Compilar LLVM**: `lib/parser/COMPILAR_LLVM.md`
- **Gramática**: `grammar.md`

---

## ✅ Checklist de Verificação

Antes de usar, verifique:

- [ ] Python 3.7+ instalado (`python --version`)
- [ ] Projeto baixado/clonado
- [ ] Estrutura de pastas correta
- [ ] `executar_lsd.py` existe na raiz do projeto
- [ ] `exemplo_completo.lsd` existe na raiz do projeto
- [ ] Teste: `python executar_lsd.py exemplo_completo.lsd` funciona
- [ ] (Opcional) LLVM instalado (para compilar LLVM IR)
- [ ] (Opcional) GCC instalado (para compilar executável)

**Teste rápido:**
```bash
python executar_lsd.py exemplo_completo.lsd
```

Se isso funcionar, está tudo pronto! 🎉

---

## 🎓 Para Iniciantes

Se você nunca usou Python antes:

1. **Instale Python** do site oficial (https://www.python.org/downloads/)
   - ⚠️ **IMPORTANTE**: Marque "Add Python to PATH" durante a instalação
2. **Abra o terminal** na pasta do projeto
   - Windows: PowerShell ou CMD
   - Linux/macOS: Terminal
3. **Teste se funciona:**
   ```bash
   python executar_lsd.py exemplo_completo.lsd
   ```
4. **Crie seu primeiro programa:**
   - Crie um arquivo `teste.lsd`:
     ```lsd
     x = 10
     Print x
     ```
   - Execute: `python executar_lsd.py teste.lsd`
5. **Leia os erros** - eles indicam exatamente o que está errado (linha e coluna)
6. **Use os exemplos** como referência

**Dica**: Comece sempre com programas simples e vá adicionando complexidade aos poucos!

---

**Última atualização**: 2025
**Versão**: 1.0

