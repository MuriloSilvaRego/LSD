# 🚀 LSD - Linguagem de Programação

Um compilador/interpretador completo implementado em Python, com suporte a análise léxica, sintática, semântica e geração de código LLVM IR.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Características](#características)
- [Instalação Rápida](#instalação-rápida)
- [Uso Básico](#uso-básico)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Documentação](#documentação)
- [Exemplos](#exemplos)
- [Requisitos](#requisitos)
- [Contribuindo](#contribuindo)

---

## 🎯 Sobre o Projeto

LSD é uma linguagem de programação simples e didática, desenvolvida como projeto acadêmico. O sistema inclui:

- **Analisador Léxico (Lexer)**: Tokenização do código fonte
- **Analisador Sintático (Parser)**: Construção da AST (Abstract Syntax Tree)
- **Analisador Semântico**: Verificação de tipos e inferência
- **Interpretador**: Execução direta do código
- **Gerador de Código**: Tradução para LLVM IR

---

## ✨ Características

### Funcionalidades da Linguagem

- ✅ Variáveis e atribuições
- ✅ Operações aritméticas (+, -, *, /)
- ✅ Operações relacionais (>, <, >=, <=, ==, !=)
- ✅ Estruturas condicionais (`If...End`)
- ✅ Comando de impressão (`Print`)
- ✅ Literais: inteiros, decimais, strings
- ✅ Expressões com parênteses
- ✅ Funções built-in (`CalculateMean`, `CalculateSum`)
- ✅ Listas

### Componentes do Sistema

- ✅ **Lexer**: Tokenização completa com detecção de erros
- ✅ **Parser**: Parser recursivo descendente LL(1)
- ✅ **AST**: Árvore sintática hierárquica
- ✅ **Análise Semântica**: Inferência de tipos automática
- ✅ **Interpretador**: Execução direta
- ✅ **Code Generator**: Geração de LLVM IR válido

---

## 🚀 Instalação Rápida

### Requisitos

- **Python 3.7+** (obrigatório)
- **LLVM** (opcional, apenas para compilar LLVM IR)
- **GCC** (opcional, apenas para compilar executáveis)

### Passo 1: Verificar Python

```bash
python --version
```

### Passo 2: Clonar/Baixar o Projeto

```bash
git clone <url-do-repositorio>
cd LSD
```

### Passo 3: Testar Instalação

```bash
python executar_lsd.py exemplo_completo.lsd
```

Se funcionar, está tudo pronto! 🎉

**📖 Para instruções detalhadas, veja [Manual de Instalação](docs/MANUAL_INSTALACAO.md)**

---

## 💻 Uso Básico

### Executar um Programa LSD

```bash
python executar_lsd.py meu_programa.lsd
```

### Gerar Código LLVM IR

```bash
python gerar_llvm.py meu_programa.lsd
```

### Exemplo de Código LSD

```lsd
nota1 = 8.5
nota2 = 7.0
soma = nota1 + nota2
media = soma / 2
Print "Media calculada:"
Print media
If media >= 7.0
Print "Aprovado"
End
```

**📖 Para mais exemplos, veja [Exemplos](docs/MANUAL_INSTALACAO.md#exemplos-práticos)**

---

## 📁 Estrutura do Projeto

```
LSD/
├── README.md                    # Este arquivo
├── executar_lsd.py             # Script executor principal
├── gerar_llvm.py               # Gerador de LLVM IR
├── exemplo_completo.lsd        # Exemplo completo
├── gerar_llvm.lsd              # Exemplo para LLVM
├── docs/                        # 📚 Documentação completa
│   ├── MANUAL_INSTALACAO.md    # Guia de instalação
│   ├── MANUAL_UTILIZACAO.md    # Guia de utilização
│   ├── RELATORIO_FINAL.md      # Relatório do projeto
│   ├── grammar.md              # Gramática da linguagem
│   ├── FIRST_FOLLOW.md         # Análise FIRST/FOLLOW
│   └── grammar_parser.md         # Gramática do parser
├── lib/
│   ├── lexer/                  # Analisador léxico
│   │   └── afds/
│   │       └── lexer3.py       # Implementação do lexer
│   └── parser/                 # Analisador sintático/semântico
│       ├── parser.py           # Parser principal
│       ├── lsd_ast.py          # Definições da AST
│       ├── semantic_analyzer.py # Analisador semântico
│       ├── code_generator.py   # Gerador LLVM IR
│       ├── interpreter.py      # Interpretador
│       ├── mostrar_arvore.py   # Visualizador de AST
│       ├── README.md           # Documentação do parser
│       ├── README_ARVORE_AST.md # Guia da árvore AST
│       ├── README_LLVM.md      # Guia LLVM IR
│       ├── COMPILAR_LLVM.md    # Como compilar LLVM
│       └── testar_*.py         # Scripts de teste
```

---

## 📚 Documentação

### Manuais Principais

- **[Manual de Instalação](docs/MANUAL_INSTALACAO.md)** - Guia completo de instalação e uso
- **[Manual de Utilização](docs/MANUAL_UTILIZACAO.md)** - Como usar cada componente
- **[Relatório Final](docs/RELATORIO_FINAL.md)** - Verificação completa dos requisitos

### Documentação Técnica

- **[Gramática](docs/grammar.md)** - Definição formal da linguagem
- **[FIRST/FOLLOW](docs/FIRST_FOLLOW.md)** - Análise LL(1)
- **[Guia da Árvore AST](lib/parser/README_ARVORE_AST.md)** - Como visualizar e entender a AST
- **[Guia LLVM IR](lib/parser/README_LLVM.md)** - Geração de código LLVM
- **[Como Compilar LLVM](lib/parser/COMPILAR_LLVM.md)** - Instruções de compilação

---

## 📝 Exemplos

### Exemplo 1: Programa Simples

```lsd
x = 10
y = 20
soma = x + y
Print "A soma e:"
Print soma
```

### Exemplo 2: Com Condicional

```lsd
idade = 18
If idade >= 18
Print "Maior de idade"
End
```

### Exemplo 3: Exemplo Completo

Execute o exemplo completo incluído:

```bash
python executar_lsd.py exemplo_completo.lsd
```

**📖 Veja mais exemplos em [Manual de Instalação - Exemplos](docs/MANUAL_INSTALACAO.md#exemplos-práticos)**

---

## 🛠️ Scripts Disponíveis

### `executar_lsd.py`

Executa código LSD usando o interpretador.

```bash
python executar_lsd.py arquivo.lsd
```

### `gerar_llvm.py`

Gera código LLVM IR a partir de arquivo LSD.

```bash
python gerar_llvm.py arquivo.lsd
```

### Scripts de Teste

- `lib/parser/testar_parser.py` - Testa o parser
- `lib/parser/testar_semantica.py` - Testa análise semântica
- `lib/parser/testar_geracao_codigo.py` - Testa geração LLVM IR
- `lib/parser/mostrar_arvore.py` - Visualiza AST

---

## 📊 Status do Projeto

✅ **PROJETO 100% COMPLETO**

Todos os requisitos implementados:

- ✅ Manual de Utilização
- ✅ Manual de Instalação/Roteiro Detalhado
- ✅ Analisador Léxico (Lexer)
- ✅ Analisador Sintático (Parser - criação da AST)
- ✅ Analisador Semântico
- ✅ Gerador de Código (tradução da AST para LLVM IR)

**📖 Veja [Relatório Final](docs/RELATORIO_FINAL.md) para verificação completa**

---

## 🔧 Requisitos

### Obrigatórios

- **Python 3.7+**
  - Windows: [python.org](https://www.python.org/downloads/)
  - Linux: `sudo apt-get install python3`
  - macOS: Já incluído ou `brew install python3`

### Opcionais

- **LLVM** (para compilar LLVM IR)
  - Windows: [LLVM Releases](https://github.com/llvm/llvm-project/releases)
  - Linux: `sudo apt-get install llvm`
  - macOS: `brew install llvm`

- **GCC** (para compilar executáveis)
  - Windows: [MinGW-w64](https://www.mingw-w64.org/)
  - Linux: `sudo apt-get install gcc`
  - macOS: Xcode Command Line Tools

---

## 🐛 Solução de Problemas

### Erro: "python: comando não encontrado"

- Windows: Use `py` em vez de `python`
- Linux/macOS: Use `python3` em vez de `python`

### Erro: "Arquivo não encontrado"

- Verifique se está na raiz do projeto
- Use caminho completo: `python executar_lsd.py C:\caminho\arquivo.lsd`

### Erro: "ModuleNotFoundError"

- Certifique-se de estar na raiz do projeto
- O script configura os paths automaticamente

**📖 Veja [Manual de Instalação - Solução de Problemas](docs/MANUAL_INSTALACAO.md#solução-de-problemas) para mais ajuda**

---

## 📖 Aprendendo a Linguagem

### Estrutura Básica

```lsd
variavel = valor
Print "Texto"
Print variavel
```

### Operações

```lsd
a = 10
b = 5
soma = a + b
produto = a * b
divisao = a / b
```

### Condicionais

```lsd
x = 10
If x > 5
Print "Maior que 5"
End
```

**📖 Veja [Manual de Instalação - Criando Seus Próprios Exemplos](docs/MANUAL_INSTALACAO.md#criando-seus-próprios-exemplos)**

---

## 🎓 Para Iniciantes

1. **Instale Python** (se ainda não tiver)
2. **Baixe o projeto**
3. **Teste com o exemplo:**
   ```bash
   python executar_lsd.py exemplo_completo.lsd
   ```
4. **Crie seu primeiro programa:**
   - Crie `teste.lsd` com código simples
   - Execute: `python executar_lsd.py teste.lsd`
5. **Leia os erros** - eles indicam linha e coluna exatas

**📖 Veja [Manual de Instalação - Para Iniciantes](docs/MANUAL_INSTALACAO.md#para-iniciantes)**

---

## 📄 Licença

Este é um projeto acadêmico desenvolvido para fins educacionais.

---

## 👥 Autores

Desenvolvido como projeto acadêmico de compiladores.

---

## 🎉 Começando Agora

```bash
# 1. Teste o exemplo completo
python executar_lsd.py exemplo_completo.lsd

# 2. Crie seu primeiro programa
echo 'x = 10\nPrint x' > meu_programa.lsd

# 3. Execute
python executar_lsd.py meu_programa.lsd
```

**Boa programação! 🚀**

---

**Última atualização**: 2025  
**Versão**: 1.0
