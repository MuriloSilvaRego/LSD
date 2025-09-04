#  Especificação – Gramática da LSD 

## 1) Gramática formal

### Conjunto de Variáveis (não-terminais) — **V**

```
V = {
  Program, StatementList, Statement,
  Assignment, ConditionalStatement, PrintStatement,
  Expression, RelationalExpression, AdditiveExpression,
  MultiplicativeExpression, UnaryExpression, PrimaryExpression,
  OptionalArgumentList, ArgumentList, OptionalExpressionList, ExpressionList
}
```

### Conjunto de Terminais — **T**

```
T = {
  If, Print, End,
  CalculateMean, CalculateSum,
  identifier, integer_literal, decimal_literal, string_literal,
  '=', '+', '-', '*', '/', '(', ')', '[', ']', ',',
  '>', '<', '>=', '<=', '==', '!='
}
```

> Palavras-chave são **case-insensitive**; identificadores são **case-sensitive**.

### Símbolo Inicial — **S**

```
S = Program
```

### Produções (CFG em estilo EBNF)

#### Estrutura do programa

```
Program        → StatementList
StatementList  → Statement StatementList | Statement
```

#### Comandos

```
Statement      → Assignment
               | ConditionalStatement
               | PrintStatement
```

#### Atribuição

```
Assignment     → identifier '=' Expression
```

#### Condicional

```
ConditionalStatement → 'If' Expression Statement 'End'
                     | 'If' Expression StatementList 'End'
```

#### Escrita

```
PrintStatement → 'Print' Expression
               | 'Print' string_literal
```

#### Expressões (com precedência)

```
Expression               → RelationalExpression

RelationalExpression     → AdditiveExpression ( ('>' | '<' | '>=' | '<=' | '==' | '!=') AdditiveExpression )*
AdditiveExpression       → MultiplicativeExpression ( ('+' | '-') MultiplicativeExpression )*
MultiplicativeExpression → UnaryExpression ( ('*' | '/') UnaryExpression )*
UnaryExpression          → ('+' | '-') UnaryExpression | PrimaryExpression
PrimaryExpression        → integer_literal
                         | decimal_literal
                         | string_literal
                         | identifier
                         | identifier '(' OptionalArgumentList ')'
                         | '[' OptionalExpressionList ']'
                         | '(' Expression ')'
```

#### Listas

```
OptionalArgumentList → ArgumentList | ε
ArgumentList         → Expression (',' Expression)*

OptionalExpressionList → ExpressionList | ε
ExpressionList         → Expression (',' Expression)*
```

---

## 2) Classificação na Hierarquia de Chomsky

* **Tipo:** **2 — Livre de Contexto (CFG)**

**Justificativa:**

* Cada produção tem um único não-terminal no lado esquerdo.
* Estruturas aninhadas (`If … End`, chamadas de função, listas, vetores) não são regulares.
* A linguagem pode ser reconhecida por autômato de pilha.

---

## 3) Exemplos de derivações

### (A) Atribuição com vetor

Programa:

```sdl
Data = [1, 2, 3, 4, 5]
```

Derivação:

```
Program
⇒ StatementList
⇒ Statement
⇒ Assignment
⇒ identifier '=' Expression
⇒ Data '=' PrimaryExpression
⇒ Data '=' '[' ExpressionList ']'
⇒ Data '=' [1, 2, 3, 4, 5]
```

---

### (B) Chamada de função + atribuição

Programa:

```sdl
Mean = CalculateMean(Data)
```

Derivação:

```
Program
⇒ StatementList
⇒ Statement
⇒ Assignment
⇒ identifier '=' Expression
⇒ Mean '=' PrimaryExpression
⇒ Mean '=' identifier '(' ArgumentList ')'
⇒ Mean '=' CalculateMean(Data)
```

---

### (C) If de 1 linha

Programa:

```sdl
If Mean > 3 Print "Above the mean" End
```

Derivação:

```
Program
⇒ StatementList
⇒ Statement
⇒ ConditionalStatement
⇒ 'If' Expression Statement 'End'
⇒ 'If' (RelationalExpression) PrintStatement 'End'
⇒ 'If' (Mean > 3) Print "Above the mean" End
```

---

### (D) If em bloco

Programa:

```sdl
If Sum < 100
  Print "Total below 100"
  Print Sum
End
```

Derivação:

```
Program
⇒ StatementList
⇒ Statement
⇒ ConditionalStatement
⇒ 'If' Expression StatementList 'End'
⇒ 'If' (Sum < 100) (PrintStatement PrintStatement) 'End'
⇒ 'If' (Sum < 100) (Print "Total below 100" Print Sum) End
```

---

## 4) Ambiguidades e estratégias

1. **Precedência de operadores**
   → resolvida pela hierarquia `Relational > Additive > Multiplicative > Unary > Primary`.

2. **If de uma linha vs. bloco**
   → duas formas separadas na gramática, ambas fechando com `End`.

3. **Print com string vs. expressão**
   → atualmente limitado a **um argumento**. Futuro pode permitir lista.

4. **Funções vs. variáveis**
   → diferenciado por `identifier '(' ... ')'`.

5. **Vetores literais vs. indexação futura**
   → pode-se separar produções no futuro (`Primary → '[' ... ']'` vs. `Primary '[' Expression ']'`).

6. **Palavras-chave vs. identificadores**
   → palavras-chave são reservadas no léxico.

---
