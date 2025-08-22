# Linguagem Simples de Dados (SDL) – Especificação Semana 3

## ✔ 1. Especificação Formal do Alfabeto (Σ)

O alfabeto da SDL é baseado em um subconjunto simplificado do alfabeto latino, dígitos decimais e símbolos especiais necessários para operações básicas.

**Definição formal:**

\[
\Sigma = \{a, b, …, z, A, B, …, Z, 0, 1, …, 9, +, -, *, /, =, (, ), [, ], ", ,, ., ␣, \n \}
\]

- **Letras:** `a–z`, `A–Z`  
- **Dígitos:** `0–9`  
- **Símbolos:** `+ - * / = ( ) [ ] " , .`  
- **Separadores:** espaço (`␣`), quebra de linha (`\n`)  

---

## ✔ 2. Definição Formal de Todos os Tokens

Tokens são elementos léxicos da linguagem. Abaixo estão as definições formais com **regex compatível com Python**, exemplos e comentários.

| **Tipo de Token**    | **Regex Python**                        | **Exemplos**           | **Observações** |
|----------------------|----------------------------------------|-----------------------|----------------|
| **Identificadores**  | `[A-Za-z_][A-Za-z0-9_]*`               | `Data`, `mean1`, `X_2`| Não pode começar com dígito; não pode coincidir com palavras-chave |
| **Inteiros**         | `\d+`                                   | `123`, `0`, `42`      | Apenas dígitos inteiros |
| **Decimais**         | `\d+\.\d+`                              | `3.14`, `0.5`         | Número com ponto decimal |
| **Notação científica** | `(\d+(\.\d+)?)([eE][+-]?\d+)`        | `1.23e-4`             | Opcional; permite `e` ou `E` |
| **Operadores**       | `[\+\-\*/]`                             | `+`, `-`, `*`, `/`    | Operadores aritméticos básicos |
| **Palavras-chave**   | `\b(If|Print|CalculateMean|CalculateSum|End)\b` | `If`, `Print` | Não podem ser usadas como identificadores |
| **Strings**          | `"(.*?)"`                               | `"Above the mean"`    | Aspas duplas, conteúdo livre |
| **Comentários**      | `//.*`                                  | `// This is a comment`| Apenas linha única |

---

## ✔ 3. Exemplos de Programas Válidos

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

## ✔ 4. Registro de Projeto com Decisões de Design e Justificativas

### Sensibilidade a maiúsculas/minúsculas
- Palavras-chave são **case-insensitive** (`If` == `if`).  
- Identificadores são **case-sensitive** (`mean` ≠ `Mean`).  

### Espaços em branco e quebras de linha
- Usados apenas como **separadores**, não são tokens.  

### Prevenção de ambiguidades
- Identificadores **não podem começar com dígitos**.  
- Palavras-chave **não podem ser reutilizadas** como identificadores.  

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






