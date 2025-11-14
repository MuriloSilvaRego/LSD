## 1. Conjuntos **FIRST**

### Termos auxiliares:

* `RelOps = { ">", "<", ">=", "<=", "==", "!=" }`
* Em expressões, o *único* modo de começar um `Expression` (devido a `UnaryExpression`) inclui sinais unários.

### FIRST sets

```
FIRST(Program) = FIRST(StatementList)
               = { identifier, 'If', 'Print' }

FIRST(StatementList) = { identifier, 'If', 'Print' }

FIRST(Statement) = { identifier, 'If', 'Print' }

FIRST(Assignment) = { identifier }

FIRST(ConditionalStatement) = { 'If' }

FIRST(PrintStatement) = { 'Print' }

FIRST(Expression) = FIRST(RelationalExpression)
                  = FIRST(AdditiveExpression)
                  = FIRST(MultiplicativeExpression)
                  = FIRST(UnaryExpression)
                  = { '+', '-', integer_literal, decimal_literal,
                      string_literal, identifier, '[', '(' }

-- Observação: incluí '+' e '-' porque uma Expression pode iniciar por um Unary '+' ou '-'.

FIRST(RelationalExpression) = FIRST(AdditiveExpression) (mesmo conjunto acima)

FIRST(AdditiveExpression) = FIRST(MultiplicativeExpression) (mesmo conjunto acima)

FIRST(MultiplicativeExpression) = FIRST(UnaryExpression) (mesmo conjunto acima)

FIRST(UnaryExpression) = { '+', '-', integer_literal, decimal_literal,
                           string_literal, identifier, '[', '(' }

FIRST(PrimaryExpression) = { integer_literal, decimal_literal,
                             string_literal, identifier, '[', '(' }

FIRST(OptionalArgumentList) = FIRST(ArgumentList) ∪ { ε }
                           = { '+', '-', integer_literal, decimal_literal,
                               string_literal, identifier, '[', '(' , ε }

FIRST(ArgumentList) = FIRST(Expression) = { '+', '-', integer_literal,
                                            decimal_literal, string_literal,
                                            identifier, '[', '(' }

FIRST(OptionalExpressionList) = FIRST(ExpressionList) ∪ { ε }
                             = { '+','-', integer_literal, decimal_literal,
                                 string_literal, identifier, '[', '(' , ε }

FIRST(ExpressionList) = FIRST(Expression) = { '+','-',
                                              integer_literal, decimal_literal,
                                              string_literal, identifier, '[', '(' }
```

---

## 2. Conjuntos **FOLLOW**

Regra geral usada: para produção `A -> α B β`:

* tudo de FIRST(β) (exceto ε) vai para FOLLOW(B);
* se β ⇒* ε (ou β = ε), então FOLLOW(A) ⊆ FOLLOW(B).

Tomando `$` como símbolo de fim de entrada.

### Inicializações

```
FOLLOW(Program) = { $ }
```

### Cálculo por não-terminal

**FOLLOW(StatementList)**

* `Program → StatementList` ⇒ FOLLOW(StatementList) ⊇ FOLLOW(Program) = { $ }
* `ConditionalStatement → 'If' Expression StatementList 'End'` ⇒ `'End'` está imediatamente após `StatementList` ⇒ `'End'` ∈ FOLLOW(StatementList)

→ `FOLLOW(StatementList) = { $, 'End' }`

---

**FOLLOW(Statement)**

* `StatementList → Statement StatementList` ⇒ FIRST(StatementList) (que é { identifier, 'If', 'Print' }) ∈ FOLLOW(Statement)
* `ConditionalStatement → 'If' Expression Statement 'End'` ⇒ `'End'` ∈ FOLLOW(Statement)

→ `FOLLOW(Statement) = { identifier, 'If', 'Print', 'End' }`

(interpretado como: depois de um statement numa lista pode vir outro statement - tokens que iniciam statements; e em `If ... Statement End` vem `End`.)

---

**FOLLOW(Assignment)** — `Assignment` aparece apenas em `Statement → Assignment`
→ `FOLLOW(Assignment) = FOLLOW(Statement) = { identifier, 'If', 'Print', 'End' }`

**FOLLOW(ConditionalStatement)** — idem
→ `FOLLOW(ConditionalStatement) = FOLLOW(Statement) = { identifier, 'If', 'Print', 'End' }`

**FOLLOW(PrintStatement)** — idem
→ `FOLLOW(PrintStatement) = FOLLOW(Statement) = { identifier, 'If', 'Print', 'End' }`

---

**FOLLOW(Expression)**
Aparece em várias posições:

* `Assignment -> identifier '=' Expression` ⇒ FOLLOW(Expression) ⊇ FOLLOW(Assignment) = { identifier, 'If', 'Print', 'End' }
* `PrintStatement -> 'Print' Expression` ⇒ FOLLOW(Expression) ⊇ FOLLOW(PrintStatement) = { identifier, 'If', 'Print', 'End' }
* `PrimaryExpression -> '(' Expression ')'` ⇒ `')'` ∈ FOLLOW(Expression)
* `ArgumentList` / `ExpressionList` contextos (`(... , ...)` ou `[...]`) ⇒ `','` e `')'` e `']'` podem seguir uma Expression dentro de listas.

Assim:

```
FOLLOW(Expression) ⊇ { ')', ']', ',', identifier, 'If', 'Print', 'End' }
```

(esses símbolos cobrem: fecho de parênteses, fecho de colchetes, separador de lista, e o que segue uma expressão quando ela termina uma instrução—próximo statement ou End).

---

**FOLLOW(RelationalExpression)**
`Expression -> RelationalExpression` ⇒ FOLLOW(RelationalExpression) = FOLLOW(Expression)
→ `FOLLOW(RelationalExpression) = { ')', ']', ',', identifier, 'If', 'Print', 'End' }`

---

**FOLLOW(AdditiveExpression)**
Na produção de `RelationalExpression`, um `AdditiveExpression` pode ser seguido por um operador relacional (se houver comparação) ou, se não houver, o que segue o `RelationalExpression`.
Portanto:

```
FOLLOW(AdditiveExpression) = { '>', '<', '>=', '<=', '==', '!=',
                               ')', ']', ',', identifier, 'If', 'Print', 'End' }
```

---

**FOLLOW(MultiplicativeExpression)**
Semelhante (pode ser seguido por `+` ou `-`, ou por símbolos em FOLLOW(AdditiveExpression)):

```
FOLLOW(MultiplicativeExpression) = { '+', '-', '>', '<', '>=', '<=', '==', '!=',
                                     ')', ']', ',', identifier, 'If', 'Print', 'End' }
```

---

**FOLLOW(UnaryExpression)**
Segue a mesma propagação:

```
FOLLOW(UnaryExpression) = { '*', '/', '+', '-', '>', '<', '>=', '<=', '==', '!=',
                            ')', ']', ',', identifier, 'If', 'Print', 'End' }
```

( `*` e `/` aparecem porque vêm imediatamente após um `UnaryExpression` em `MultiplicativeExpression` )

---

**FOLLOW(PrimaryExpression)**
`PrimaryExpression` é a base — o que pode seguir é o mesmo que FOLLOW(UnaryExpression):

```
FOLLOW(PrimaryExpression) = { '*', '/', '+', '-', '>', '<', '>=', '<=', '==', '!=',
                              ')', ']', ',', identifier, 'If', 'Print', 'End' }
```

---

**FOLLOW(OptionalArgumentList)**
Usado em `identifier '(' OptionalArgumentList ')'` ⇒ imediatamente segue `')'`:

```
FOLLOW(OptionalArgumentList) = { ')' }
```

**FOLLOW(ArgumentList)**
Num contexto de chamada `identifier '(' ArgumentList ')'` ⇒

```
FOLLOW(ArgumentList) = { ')' }
```

**FOLLOW(OptionalExpressionList)**
Usado em ` '[' OptionalExpressionList ']'` ⇒

```
FOLLOW(OptionalExpressionList) = { ']' }
```

**FOLLOW(ExpressionList)**
Como `OptionalExpressionList -> ExpressionList`, e `']'` segue `OptionalExpressionList`, então:

```
FOLLOW(ExpressionList) ⊇ { ']' }
```

Além disso, dentro da lista um `Expression` pode ser seguido por `,` (se houver mais). Mas `FOLLOW(ExpressionList)` em si (como símbolo completo) é `']'`.




## 3. A gramática é **LL(1)** ? — **Resposta justificada**

**Resposta direta:** **Não — a gramática, na forma apresentada, *não é LL(1)***.

**Justificativa (conflitos encontrados):**

1. **Produção de `StatementList`**

   ```
   StatementList → Statement StatementList | Statement
   ```

   Essas duas produções para `StatementList` têm exatamente o mesmo símbolo inicial (`Statement`). Logo:

   ```
   FIRST(Statement StatementList) ∩ FIRST(Statement) ≠ ∅
   ```

   (na verdade, são iguais). Em LL(1) precisamos que, para um não-terminal com múltiplas produções, as FIRST das alternativas sejam disjuntas (ou, se uma alternativa puder derivar ε, que FIRST(do outra) e FOLLOW do não-terminal sejam disjuntos adequadamente). Assim, **conflito LL(1)**.
   Observação: isto é redundante — a forma EBNF mais apropriada `StatementList = Statement { Statement }` é equivalente e **fatorada**, e essa forma EBNF sim é compatível com análise LL(1). Portanto, é mais um problema de apresentação/forma (não difícil de consertar).

2. **Produção de `ConditionalStatement`**

   ```
   ConditionalStatement → 'If' Expression Statement 'End'
                        | 'If' Expression StatementList 'End'
   ```

   Ambas começam por `'If' Expression`. O problema concreto: após `'If' Expression` vem `Statement` ou `StatementList`. Mas `StatementList` pode começar por um `Statement` — isto é, ambas as alternativas compartilham a mesma sequência inicial. Logo há **conflito de escolha com um único símbolo de lookahead** (se o parser vê `'If' Expression` não sabe, só com 1 token de lookahead, se vai ver `Statement` seguida de `End` ou uma `StatementList` que pode conter vários `Statement`s; na prática a forma `StatementList = Statement {Statement}` torna desnecessária a segunda produção; você pode unificar para `ConditionalStatement -> 'If' Expression StatementList 'End'` e usar StatementList onde necessário). Portanto, nesta forma há um **conflito LL(1)**.

3. **Produção de `PrimaryExpression` com `identifier`**

   ```
   PrimaryExpression → identifier
                     | identifier '(' OptionalArgumentList ')'
                     | ...
   ```

   Duas alternativas compartilham o mesmo símbolo inicial `identifier`. Sem left-factoring isto causa conflito LL(1). Solução clássica: left-factorizar:

   ```
   PrimaryExpression → identifier PrimaryTail
   PrimaryTail → "(" OptionalArgumentList ")" | ε
   ```

   Assim, com 1 token de lookahead (quando vê `identifier`), o parser decide entrar em `PrimaryTail` e aí o próximo token (se é `'('` ou não) decide qual alternativa seguir — isto é LL(1)-compatível.

4. **Outros pontos**

   * As regras de repetição escritas em EBNF (`{ ... }`) são normalmente fáceis de transformar em forma LL(1) (right-recursive ou factorizada).
   * Operadores e precedência estão bem separadas — essa parte é amigável ao parser LL(1) (desde que você não tenha produções que comecem com o mesmo terminal sem se left-factorizar).

---

## 4. Sugestões práticas para tornar a gramática LL(1)

1. **Transformar `StatementList` para forma repetitiva EBNF (ou equivalente right-recursive):**

   ```ebnf
   StatementList = Statement { Statement } ;
   ```

   ou em BNF:

   ```
   StatementList -> Statement StatementList' 
   StatementList' -> Statement StatementList' | ε
   ```

   Isso remove o conflito entre duas alternativas idênticas.

2. **Unificar as alternativas do `ConditionalStatement`**:

   * Use apenas `ConditionalStatement -> 'If' Expression StatementList 'End'` e permita que `StatementList` seja apenas um `Statement` para o caso "one-line" (ou mantenha distinção por token especial — ex.: newline — se desejar diferenciar 1-linha vs bloco sem ambiguidade).

3. **Left-factorizar `PrimaryExpression` para resolver o problema do `identifier`:**

   ```ebnf
   PrimaryExpression = integer_literal
                     | decimal_literal
                     | string_literal
                     | identifier PrimarySuffix
                     | "[" OptionalExpressionList "]"
                     | "(" Expression ")" ;

   PrimarySuffix = "(" OptionalArgumentList ")" | ε ;
   ```

   Assim, ao ver `identifier` o parser olha o próximo token e decide se é chamada (`'('`) ou variável (`ε`), sem ambiguidade.

4. **Simplificar `PrintStatement`**: manter só `Print Expression` (já cobre `Print string_literal` porque `Expression → PrimaryExpression` e `PrimaryExpression → string_literal`).

5. **Após a refatoração**, recalcular os conjuntos FIRST/FOLLOW e verificar que para cada não-terminal com várias alternativas:

   * FIRST(alternativa_i) ∩ FIRST(alternativa_j) = ∅ (para i ≠ j), e
   * se alguma alternativa tem ε em FIRST, então FIRST(alternativa_k) ∩ FOLLOW(A) = ∅ para todo k ≠ ε-alternativa.

Se essas condições forem satisfeitas para todos os não-terminais, então a gramática é LL(1).

---

## 5. Resumo final (resposta curta)

* **FIRST / FOLLOW** foram calculados (ver secção 2 e 3 acima).
* **A gramática, tal como apresentada**, **não é LL(1)** por causa de conflitos evidentes (ex.: `StatementList`, `PrimaryExpression` com `identifier`, e a forma dupla de `ConditionalStatement`).
* **Porém**: esses conflitos são resolvíveis com transformações habituais (left-factoring, reescrever listas em forma repetitiva, unificar alternativas redundantes). Após tais alterações a gramática **pode ser convertida** em uma forma LL(1) adequada para um parser preditivo recursivo-descendente.
