class TokenType:
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENT = "IDENT"

    # Keywords
    VAR = "VAR"
    IF = "IF"
    WHILE = "WHILE"
    PRINT = "PRINT"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    TRUE = "TRUE"
    FALSE = "FALSE"

    # Operators
    ASSIGN = "ASSIGN"        # =
    EQ = "EQ"                # ==
    NEQ = "NEQ"              # !=
    LT = "LT"                # <
    GT = "GT"                # >
    LTE = "LTE"              # <=
    GTE = "GTE"              # >=
    PLUS = "PLUS"            # +
    MINUS = "MINUS"          # -
    STAR = "STAR"            # *
    SLASH = "SLASH"          # /

    # Delimiters
    LPAREN = "LPAREN"        # (
    RPAREN = "RPAREN"        # )
    LBRACE = "LBRACE"        # {
    RBRACE = "RBRACE"        # }

    EOF = "EOF"


class Token:
    def __init__(self, type: str, value, line: int = 0):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line})"


KEYWORDS = {
    "var": TokenType.VAR,
    "if": TokenType.IF,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}   
