#  **Definição Formal da Gramática da Linguagem LSD**

G = (V, Σ, P, S)

onde:

---

## **V — Variáveis (Não-terminais)**

```
{
  Program, StatementList, Statement,
  Assignment, ConditionalStatement, PrintStatement,
  Expression, RelationalExpression, AdditiveExpression,
  MultiplicativeExpression, UnaryExpression, PrimaryExpression,
  OptionalArgumentList, ArgumentList,
  OptionalExpressionList, ExpressionList
}
```

---

## **Σ — Terminais (Símbolos léxicos)**

Palavras-chave (case-insensitive), símbolos e literais:

```
{
  If, Print, End, CalculateMean, CalculateSum,
  identifier, integer_literal, decimal_literal, string_literal,
  '=', '+', '-', '*', '/', '(', ')', '[', ']', ',', 
  '>', '<', '>=', '<=', '==', '!='
}
```

---

## **S — Símbolo Inicial**

```
Program
```

---

## **P — Regras de Produção (EBNF)**


---

#  **Gramática em EBNF (Extended Backus–Naur Form)**

```ebnf
Program              = StatementList ;

StatementList        = Statement { Statement } ;

Statement            = Assignment
                     | ConditionalStatement
                     | PrintStatement ;

Assignment           = identifier "=" Expression ;

ConditionalStatement = "If" Expression Statement "End"
                     | "If" Expression StatementList "End" ;

PrintStatement       = "Print" Expression
                     | "Print" string_literal ;

Expression           = RelationalExpression ;

RelationalExpression = AdditiveExpression
                       { ( ">" | "<" | ">=" | "<=" | "==" | "!=" )
                         AdditiveExpression } ;

AdditiveExpression   = MultiplicativeExpression
                       { ( "+" | "-" ) MultiplicativeExpression } ;

MultiplicativeExpression = UnaryExpression
                           { ( "*" | "/" ) UnaryExpression } ;

UnaryExpression      = ( "+" | "-" ) UnaryExpression
                     | PrimaryExpression ;

PrimaryExpression    = integer_literal
                     | decimal_literal
                     | string_literal
                     | identifier
                     | identifier "(" OptionalArgumentList ")"
                     | "[" OptionalExpressionList "]"
                     | "(" Expression ")" ;

OptionalArgumentList = ArgumentList | ε ;

ArgumentList         = Expression { "," Expression } ;

OptionalExpressionList = ExpressionList | ε ;

ExpressionList       = Expression { "," Expression } ;
```

---

#  **Gramática em BNF (Backus–Naur Form)**

```bnf
<Program> ::= <StatementList>

<StatementList> ::= <Statement> <StatementList>
                  | <Statement>

<Statement> ::= <Assignment>
              | <ConditionalStatement>
              | <PrintStatement>

<Assignment> ::= identifier "=" <Expression>

<ConditionalStatement> ::= "If" <Expression> <Statement> "End"
                         | "If" <Expression> <StatementList> "End"

<PrintStatement> ::= "Print" <Expression>
                   | "Print" string_literal

<Expression> ::= <RelationalExpression>

<RelationalExpression> ::= <AdditiveExpression> <RelationalTail>

<RelationalTail> ::= ( ">" | "<" | ">=" | "<=" | "==" | "!=" )
                     <AdditiveExpression> <RelationalTail>
                   | ε

<AdditiveExpression> ::= <MultiplicativeExpression> <AdditiveTail>

<AdditiveTail> ::= ( "+" | "-" ) <MultiplicativeExpression> <AdditiveTail>
                 | ε

<MultiplicativeExpression> ::= <UnaryExpression> <MultiplicativeTail>

<MultiplicativeTail> ::= ( "*" | "/" ) <UnaryExpression> <MultiplicativeTail>
                       | ε

<UnaryExpression> ::= ( "+" | "-" ) <UnaryExpression>
                    | <PrimaryExpression>

<PrimaryExpression> ::= integer_literal
                      | decimal_literal
                      | string_literal
                      | identifier
                      | identifier "(" <OptionalArgumentList> ")"
                      | "[" <OptionalExpressionList> "]"
                      | "(" <Expression ")" >

<OptionalArgumentList> ::= <ArgumentList>
                         | ε

<ArgumentList> ::= <Expression> <ArgumentTail>

<ArgumentTail> ::= "," <Expression> <ArgumentTail>
                 | ε

<OptionalExpressionList> ::= <ExpressionList>
                           | ε

<ExpressionList> ::= <Expression> <ExpressionTail>

<ExpressionTail> ::= "," <Expression> <ExpressionTail>
                   | ε
```