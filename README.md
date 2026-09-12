# Simple Programming Language Interpreter

## Grammar

```
program   = { statement } ;

statement = "var" ident "=" expr
          | ident "=" expr
          | "if" "(" expr ")" statement
          | "while" "(" expr ")" statement
          | "print" "(" expr ")"
          | "{" { statement } "}" ;

expr      = or_expr ;
or_expr   = and_expr { "or" and_expr } ;
and_expr  = comparison { "and" comparison } ;
comparison= term { ("==" | "!=" | "<" | ">" | "<=" | ">=") term } ;
term      = factor { ("+" | "-") factor } ;
factor    = unary { ("*" | "/") unary } ;
unary     = "not" unary
          | primary ;
primary   = NUMBER
          | STRING
          | "true"
          | "false"
          | ident
          | "(" expr ")" ;

ident     = LETTER { LETTER | DIGIT | "_" } ;
NUMBER    = DIGIT { DIGIT } ["." DIGIT { DIGIT }] ;
STRING    = '"' { any char except '"' } '"'
          | "'" { any char except "'" } "'" ;   
```