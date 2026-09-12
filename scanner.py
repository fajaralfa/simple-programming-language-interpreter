from tokens import *


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.tokens: list[Token] = []

    def scan(self) -> list[Token]:
        while self.pos < len(self.source):
            self._skip_whitespace()
            if self.pos >= len(self.source):
                break
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, None, self.line))
        return self.tokens

    def _skip_whitespace(self):
        while self.pos < len(self.source) and self.source[self.pos] in " \t\n\r":
            if self.source[self.pos] == "\n":
                self.line += 1
            self.pos += 1
        # Single-line comments
        if self.pos + 1 < len(self.source) and self.source[self.pos:self.pos+2] == "//":
            while self.pos < len(self.source) and self.source[self.pos] != "\n":
                self.pos += 1

    def _scan_token(self):
        ch = self.source[self.pos]

        # Multi-char operators
        if self.source[self.pos:self.pos+2] in ("==", "!=", "<=", ">="):
            two = self.source[self.pos:self.pos+2]
            mapping = {"==": TokenType.EQ, "!=": TokenType.NEQ,
                       "<=": TokenType.LTE, ">=": TokenType.GTE}
            self.tokens.append(Token(mapping[two], two, self.line))
            self.pos += 2
            return

        # Single-char operators / delimiters
        single = {
            "=": TokenType.ASSIGN,
            "<": TokenType.LT,
            ">": TokenType.GT,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "/": TokenType.SLASH,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            "{": TokenType.LBRACE,
            "}": TokenType.RBRACE,
        }
        if ch in single:
            self.tokens.append(Token(single[ch], ch, self.line))
            self.pos += 1
            return

        # Numbers
        if ch.isdigit():
            self._scan_number()
            return

        # Strings
        if ch in ('"', "'"):
            self._scan_string()
            return

        # Identifiers / keywords
        if ch.isalpha() or ch == "_":
            self._scan_ident()
            return

        raise SyntaxError(f"Unexpected character {ch!r} at line {self.line}")

    def _scan_number(self):
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self.pos += 1
        # Float
        if self.pos + 1 < len(self.source) and self.source[self.pos] == "." and self.source[self.pos+1].isdigit():
            self.pos += 1
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                self.pos += 1
            self.tokens.append(Token(TokenType.NUMBER, float(self.source[start:self.pos]), self.line))
        else:
            self.tokens.append(Token(TokenType.NUMBER, int(self.source[start:self.pos]), self.line))

    def _scan_string(self):
        quote = self.source[self.pos]
        self.pos += 1
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != quote:
            if self.source[self.pos] == "\n":
                self.line += 1
            self.pos += 1
        if self.pos >= len(self.source):
            raise SyntaxError(f"Unterminated string at line {self.line}")
        self.pos += 1  # closing quote
        self.tokens.append(Token(TokenType.STRING, self.source[start:self.pos-1], self.line))

    def _scan_ident(self):
        start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == "_"):
            self.pos += 1
        word = self.source[start:self.pos]
        token_type = KEYWORDS.get(word, TokenType.IDENT)
        self.tokens.append(Token(token_type, word, self.line))   
