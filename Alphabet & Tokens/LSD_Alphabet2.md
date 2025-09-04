# Linguagem Simples de Dados (LSD) – Especificação Semana 4

## 1. Especificação Formal do Alfabeto (Σ)

O alfabeto da LSD é baseado em um subconjunto simplificado do alfabeto latino, dígitos decimais e símbolos especiais necessários para operações básicas.

**Definição formal:**

\[
\Sigma = \{ a..z, A..Z, 0..9, +, -, *, /, =, (, ), [, ], ", ,, ., >, <, !, \_, ␣, \n \}
\]

- **Letras:** `a–z`, `A–Z`  
- **Dígitos:** `0–9`  
- **Símbolos:** `+ - * / = ( ) [ ] " , . > < ! _`   
- **Separadores:** espaço (`␣`), quebra de linha (`\n`)  

---

## 2. Definição Formal de Todos os Tokens (Regex)

Tokens são elementos léxicos da linguagem. Abaixo estão as definições formais com **regex compatível com Python**, exemplos e comentários.

| **Token**            | **Regex (Python/PCRE)**                  | **Exemplos**             | **Observações** |
|-----------------------|------------------------------------------|--------------------------|-----------------|
| **Identificadores**   | `[A-Za-z_][A-Za-z0-9_]*`                 | `Data`, `mean1`, `X_2`   | Não podem coincidir com palavras-chave |
| **Inteiros**          | `\d+`                                   | `123`, `0`, `42`         | Apenas inteiros positivos nesta versão |
| **Decimais**          | `\d+\.\d+`                              | `3.14`, `0.5`            | Ponto obrigatório |
| **Notação científica**| `\d+(\.\d+)?[eE][+-]?\d+`               | `1.23e-4`, `2E10`        | `e` ou `E` |
| **Operadores**        | `\+|\-|\*|/|==|!=|>=|<=|>|<`            | `+`, `-`, `*`, `/`, `<=` | Inclui relacionais |
| **Atribuição**        | `=`                                     | `=`                      | Diferente de `==` |
| **Palavras-chave**    | `\b(If|Print|CalculateMean|CalculateSum|End)\b` | `If`, `End` | São **case-insensitive** |
| **Strings**           | `"[^"\n]*"`                             | `"Hello"`, `"123"`       | Sem escapes nesta versão |
| **Comentários**       | `//.*`                                  | `// a comment`           | Apenas linha única |
| **Separadores**       | `[ \t\r\n]+`                            | `␣`, `\n`                | Ignorados pelo parser |

---

## 3. Exemplos de Programas Válidos

### Exemplo 1 – Cálculo de média simples
```python
Data = [1, 2, 3, 4, 5]
Mean = CalculateMean(Data)
If Mean > 3 Print 'Above the mean'
End

```

## Exemplo 2 – Soma e condição

```python

Values = [10, 20, 30]
Sum = CalculateSum(Values)
If Sum < 100 Print "Total below 100"
End

```

## Exemplo 3 – Uso de comentários

```python

N = [2, 4, 6]
Mean = CalculateMean(N)
Print "The mean is: "
Print Mean
End

```

## 4. Registro de Projeto com Decisões de Design e Justificativas

### Sensibilidade a maiúsculas/minúsculas
- Palavras-chave são **case-insensitive** (`If` == `if`).  
- Identificadores são **case-sensitive** (`mean` ≠ `Mean`).  

### Espaços em branco e quebras de linha
- Usados apenas como **separadores**, não são tokens.  

### Prevenção de ambiguidades
- Identificadores **não podem começar com dígitos**.  
- Palavras-chave **não podem ser reutilizadas** como identificadores.
- Regras de precedência: **palavras-chave > identificadores**. 

### Strings
- Apenas **strings entre aspas duplas** (`"..."`) são suportadas.  
- **Sem suporte a caracteres de escape** (`\n`, `\t`) nesta versão inicial.  

### Comentários
- Apenas **comentários de linha única** (`//`) são suportados.  
- Comentários de bloco (`/* ... */`) estão fora do escopo inicial.  

### Decisões pedagógicas
- Minimizar a complexidade da sintaxe para iniciantes.  
- Restringir recursos aos essenciais para facilitar o parsing.  
- Definição de tokens já prepara o terreno para **extensões futuras** (condições, loops, expressões mais complexas).  
  

## 5. Análise de Ambiguidades e Regras de Resolução

### 5.1 Identificadores vs. Palavras-chave

- **Problema:** regex de identificadores poderia capturar palavras-chave.
- **Solução:** palavras-chave têm prioridade maior na análise léxica.

### 5.2 `=` (atribuição) vs. `==` (comparação)

- **Problema:** ambos começam com `=`.
- **Solução:** analisador léxico deve verificar **primeiro os operadores compostos** (`==`, `!=`, `<=`, `>=`), depois o `=`simples.

### 5.3 Operadores relacionais sobrepostos (`<`, `<=`, `>`, `>=`)

- **Problema:** `<` pode ser confundido com `<=`.
- **Solução:** mesma regra — **preferir tokens mais longos** quando há sobreposição.

### 5.4 Strings vs. comentários

- **Problema:** `//` dentro de uma string poderia ser interpretado como comentário.
- **Solução:** strings têm prioridade sobre comentários. O `//` só é reconhecido fora de aspas.

### 5.5 Espaços em branco
- **Problema:** podem gerar tokens vazios se não tratados.
- **Solução:** whitespace é consumido pelo analisador e **ignorado** como token.

### 5.6 Internacionalização de identificadores
- **Problema:** incluir caracteres não-ASCII (`ç`,` ã`,` ü`) poderia gerar incompatibilidades de regex/compilador.
- **Solução:** versão inicial **restringe identificadores ao ASCII básico (`A-Z, a-z, 0-9, _`).** Futuras versões podem expandir para Unicode.


