from ast_nodes import *

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = {}

    def define(self, name, value):
        self.vars[name] = value

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise UndefinedVariableError(name)

    def set(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise UndefinedVariableError(name)

    def exists(self, name):
        if name in self.vars:
            return True
        if self.parent:
            return self.parent.exists(name)
        return False


class UndefinedVariableError(Exception):
    pass


class VM:
    def __init__(self):
        self.global_scope = Scope()

    def run(self, program: Program):
        self.execute_block(program.statements, self.global_scope)

    # --- Statements ---

    def execute_block(self, statements, scope):
        for stmt in statements:
            self.execute(stmt, scope)

    def execute(self, stmt, scope):
        match stmt:
            case Assignment():
                value = self.eval(stmt.expr, scope)
                scope.define(stmt.ident, value)

            case Reassignment():
                value = self.eval(stmt.expr, scope)
                if not scope.exists(stmt.ident):
                    raise UndefinedVariableError(stmt.ident)
                scope.set(stmt.ident, value)

            case IfStatement():
                if self.eval(stmt.expr, scope):
                    self.execute(stmt.statement, Scope(scope))

            case WhileStatement():
                while self.eval(stmt.expr, scope):
                    self.execute(stmt.statement, Scope(scope))

            case PrintStatement():
                print(self.eval(stmt.expr, scope))

            case Block():
                self.execute_block(stmt.statements, Scope(scope))

    # --- Expressions ---

    def eval(self, expr, scope):
        match expr:
            case NumberExpr() | StringExpr() | BooleanExpr():
                return expr.val

            case VarExpr():
                return scope.get(expr.name)

            case BinaryExpr(OP.ADD, left, right):
                return self.eval(expr.left, scope) + self.eval(expr.right, scope)

            case BinaryExpr(OP.SUB, left, right):
                return self.eval(expr.left, scope) - self.eval(expr.right, scope)

            case BinaryExpr(OP.MUL, left, right):
                return self.eval(expr.left, scope) * self.eval(expr.right, scope)

            case BinaryExpr(OP.DIV, left, right):
                b = self.eval(expr.right, scope)
                if b == 0:
                    raise ZeroDivisionError("division by zero")
                return self.eval(expr.left, scope) / b

            case BinaryExpr() if expr.op in {OP.EQUAL, OP.NOT_EQUAL, OP.LT, OP.GT, OP.LE, OP.GE}:
                a, b = self.eval(expr.left, scope), self.eval(expr.right, scope)
                return {"==": a == b, "!=": a != b, "<": a < b,
                        ">": a > b, "<=": a <= b, ">=": a >= b}[expr.op]

            case BinaryExpr(OP.AND, left, right):
                return self.eval(expr.left, scope) and self.eval(expr.right, scope)

            case BinaryExpr(OP.AND, left, right):
                return self.eval(expr.left, scope) or self.eval(expr.right, scope)

            case UnaryExpr(OP.NOT, term):
                return not self.eval(expr.expr, scope)   

            case _:
                raise ValueError(f"Unknown expression: {type(expr).__name__} {expr}")


