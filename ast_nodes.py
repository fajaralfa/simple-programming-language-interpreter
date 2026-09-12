from dataclasses import field
from dataclasses import dataclass

class OP:
    ADD        = "+"
    SUB        = "-"
    MUL        = "*"
    DIV        = "/"
    MOD        = "%"
    ASSIGN     = "="
    EQUAL      = "=="
    NOT_EQUAL  = "!="
    LT         = "<"
    LE         = "<="
    GT         = ">"
    GE         = ">="
    AND        = "&&"
    OR         = "||"
    NOT        = "!"


class Program:
    def __init__(self, statements=None):
        self.statements = [];

class Statement:
    def __init__(self):
        pass

class Expression:
    def __init__(self):
        pass

@dataclass
class Assignment(Statement):
    ident: str
    expr: Expression

@dataclass
class Reassignment(Statement):
    ident: str
    expr: Expression

@dataclass
class IfStatement(Statement):
    expr: Expression
    statement: Statement

@dataclass
class PrintStatement(Statement):
    expr: Expression

@dataclass
class WhileStatement(Statement):
    expr: Expression
    statement: Statement

@dataclass
class Block(Statement):
    statements: list = field(default_factory=list)

@dataclass
class NumberExpr(Expression):
    val: float

@dataclass
class StringExpr(Expression):
    val: str

@dataclass
class BooleanExpr(Expression):
    val: bool

@dataclass
class VarExpr(Expression):
    name: str

@dataclass
class BinaryExpr(Expression):
    op: str
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.op=} {self.left=} {self.right=}"

@dataclass
class UnaryExpr(Expression):
    op: str
    term: Expression