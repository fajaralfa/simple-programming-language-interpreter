from ast_nodes import BinaryExpr
from tokens import Token, TokenType
from ast_nodes import (
    Program, Statement, Expression,
    Assignment, Reassignment, IfStatement, WhileStatement,
    PrintStatement, Block,
    NumberExpr, StringExpr, BooleanExpr, VarExpr, UnaryExpr,
    OP
)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Program:
        program = Program()
        while not self._check(TokenType.EOF):
            program.statements.append(self._statement())
        return program

    # --- Helpers ---

    def _current(self) -> Token:
        return self.tokens[self.pos]

    def _check(self, token_type: str) -> bool:
        return self._current().type == token_type

    def _advance(self) -> Token:
        token = self._current()
        if not self._check(TokenType.EOF):
            self.pos += 1
        return token

    def _expect(self, token_type: str, msg: str | None = None) -> Token:
        if not self._check(token_type):
            raise SyntaxError(
                msg or f"Expected {token_type}, got {self._current().type} ({self._current().value!r}) at line {self._current().line}"
            )
        return self._advance()

    # --- Statements ---

    def _statement(self) -> Statement:
        token = self._current()

        if token.type == TokenType.VAR:
            return self._assignment()
        elif token.type == TokenType.IDENT:
            return self._reassignment()
        elif token.type == TokenType.IF:
            return self._if_statement()
        elif token.type == TokenType.WHILE:
            return self._while_statement()
        elif token.type == TokenType.PRINT:
            return self._print_statement()
        elif token.type == TokenType.LBRACE:
            return self._block()
        else:
            raise SyntaxError(f"Unexpected token {token.type} ({token.value!r}) at line {token.line}")

    def _assignment(self) -> Assignment:
        self._expect(TokenType.VAR)
        ident = self._expect(TokenType.IDENT).value
        self._expect(TokenType.ASSIGN)
        expr = self._expression()
        return Assignment(ident, expr)

    def _reassignment(self) -> Reassignment:
        ident = self._expect(TokenType.IDENT).value
        self._expect(TokenType.ASSIGN)
        expr = self._expression()
        return Reassignment(ident, expr)

    def _if_statement(self) -> IfStatement:
        self._expect(TokenType.IF)
        self._expect(TokenType.LPAREN)
        expr = self._expression()
        self._expect(TokenType.RPAREN)
        body = self._block()
        return IfStatement(expr, body)

    def _while_statement(self) -> WhileStatement:
        self._expect(TokenType.WHILE)
        self._expect(TokenType.LPAREN)
        expr = self._expression()
        self._expect(TokenType.RPAREN)
        body = self._block()
        return WhileStatement(expr, body)

    def _print_statement(self) -> PrintStatement:
        self._expect(TokenType.PRINT)
        self._expect(TokenType.LPAREN)
        expr = self._expression()
        self._expect(TokenType.RPAREN)
        return PrintStatement(expr)

    def _block(self) -> Block:
        self._expect(TokenType.LBRACE)
        statements = []
        while not self._check(TokenType.RBRACE) and not self._check(TokenType.EOF):
            statements.append(self._statement())
        self._expect(TokenType.RBRACE)
        return Block(statements)

    # --- Expressions (precedence climbing) ---

    def _expression(self) -> Expression:
        return self._or_expr()

    def _or_expr(self) -> Expression:
        left = self._and_expr()
        while self._check(TokenType.OR):
            self._advance()
            right = self._and_expr()
            left = BinaryExpr(OP.OR, left, right)
        return left

    def _and_expr(self) -> Expression:
        left = self._comparison()
        while self._check(TokenType.AND):
            self._advance()
            right = self._comparison()
            left = BinaryExpr(OP.AND, left, right)
        return left

    def _comparison(self) -> Expression:
        left = self._term()
        if self._current().type in (TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            op_token = self._advance()
            right = self._term()
            op = None
            match op_token.type:
                case TokenType.EQ:
                    op = OP.EQUAL
                case TokenType.NEQ:
                    op = OP.NOT_EQUAL
                case TokenType.LT:
                    op = OP.LT
                case TokenType.GT:
                    op = OP.GT
                case TokenType.LTE:
                    op = OP.LTE
                case TokenType.GTE:
                    op = OP.GTE
            return BinaryExpr(op, left, right)
        return left

    def _term(self) -> Expression:
        left = self._factor()
        while self._current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self._advance().value
            right = self._factor()
            if op == "+":
                left = BinaryExpr(OP.ADD, left, right)
            else:
                left = BinaryExpr(OP.SUB, left, right)
        return left

    def _factor(self) -> Expression:
        left = self._primary()
        while self._current().type in (TokenType.STAR, TokenType.SLASH):
            op = self._advance().value
            right = self._primary()
            if op == "*":
                left = BinaryExpr(OP.MUL, left, right)
            else:
                left = BinaryExpr(OP.DIV, left, right)
        return left

    def _primary(self) -> Expression:
        token = self._current()

        if token.type == TokenType.NUMBER:
            self._advance()
            return NumberExpr(token.value)
        elif token.type == TokenType.STRING:
            self._advance()
            return StringExpr(token.value)
        elif token.type == TokenType.TRUE:
            self._advance()
            return BooleanExpr(True)
        elif token.type == TokenType.FALSE:
            self._advance()
            return BooleanExpr(False)
        elif token.type == TokenType.IDENT:
            self._advance()
            return VarExpr(token.value)
        elif token.type == TokenType.NOT:
            self._advance()
            expr = self._primary()
            return UnaryExpr(OP.SUB, expr)
        elif token.type == TokenType.LPAREN:
            self._advance()
            expr = self._expression()
            self._expect(TokenType.RPAREN)
            return expr
        else:
            raise SyntaxError(f"Unexpected token {token.type} ({token.value!r}) at line {token.line}")   
