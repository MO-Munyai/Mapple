from tokens import TokenType, Token

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def peek(self):
        if self.pos >= len(self.source): return None
        return self.source[self.pos]

    def advance(self):
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def add_token(self, t_type, value=None):
        """Helper to capture current line/col when creating a token."""
        # We subtract len(str(value)) to point to the START of the token
        val_str = str(value) if value is not None else ""
        col_start = max(1, self.column - len(val_str))
        self.tokens.append(Token(t_type, value, self.line, col_start))

    def scan_tokens(self):
        while self.pos < len(self.source):
            char = self.advance()

            if char.isspace():
                continue
            
            # --- Comments --- 
            if char == '/':
                if self.peek() == '/':
                    while self.pos < len(self.source) and self.source[self.pos] != '\n':
                        self.advance()
                    continue 
                else:
                    self.add_token(TokenType.DIV, "/")
            
            # --- Literals ---
            elif char == '"': self.add_string()
            elif char == "'": self.add_char()
            
            # --- Greedy Terminators --- 
            elif char == ':':
                if self.peek() == ':':
                    self.advance()
                    self.add_token(TokenType.D_COLON, "::")
                else:
                    self.add_token(TokenType.COLON, ":")
            
            elif char == ';':
                if self.peek() == ';':
                    self.advance()
                    self.add_token(TokenType.CLASS_END, ";;")
                else:
                    self.add_token(TokenType.STMT_END, ";")

            # --- Identifiers & Keywords ---
            elif char.isalpha(): self.add_identifier(char)
            
            # --- Numbers --- 
            elif char.isdigit(): self.add_number(char)

            # --- Operators ---
            elif char == '+':
                if self.peek() == '+':
                    self.advance()
                    self.add_token(TokenType.PLUS_PLUS, "++")
                else:
                    self.add_token(TokenType.PLUS, "+")
            elif char == '.': self.add_token(TokenType.DOT, ".")
            elif char == '=': self.add_token(TokenType.ASSIGN, "=")
            elif char == '(': self.add_token(TokenType.LPAREN, "(")
            elif char == ')': self.add_token(TokenType.RPAREN, ")")

            else:
                raise Exception(
                    f"Lexer Error: Unexpected character '{char}' "
                    f"(line {self.line}, column {self.column - 1})."
                )

        self.add_token(TokenType.EOF, "EOF")
        return self.tokens

    def add_string(self):
        start_line = self.line
        value = ""
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            value += self.advance()
        if self.pos >= len(self.source):
            raise Exception(
                f"Lexer Error: Unterminated string literal starting at line {start_line}."
            )
        self.advance()  # consume closing "
        self.add_token(TokenType.STR_LIT, value)

    def add_char(self):
        start_line = self.line
        if self.pos >= len(self.source):
            raise Exception(
                f"Lexer Error: Unterminated character literal at line {start_line}."
            )
        value = self.advance()
        if self.pos >= len(self.source) or self.source[self.pos] != "'":
            raise Exception(
                f"Lexer Error: Unterminated or invalid character literal at line {start_line}. "
                "Character literals must contain exactly one character enclosed in single quotes."
            )
        self.advance()  # consume closing '
        self.add_token(TokenType.CHAR_LIT, value)

    def add_number(self, first_digit):
        value = first_digit
        dot_count = 0
        start_line = self.line
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            if self.source[self.pos] == '.':
                dot_count += 1
                if dot_count > 1:
                    raise Exception(
                        f"Lexer Error: Malformed numeric literal '{value}.' "
                        f"at line {start_line}. A number can have at most one decimal point."
                    )
            value += self.advance()
        t_type = TokenType.NUM_LIT if dot_count == 1 else TokenType.INT_LIT
        self.add_token(t_type, value)

    def add_identifier(self, first_char):
        value = first_char
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            value += self.advance()
        
        keywords = {
            "let": TokenType.LET, "func": TokenType.FUNC, "class": TokenType.CLASS,
            "print": TokenType.PRINT, "input": TokenType.INPUT, "return": TokenType.RETURN,
            "int": TokenType.INT_TYPE, "num": TokenType.NUM_TYPE, "str": TokenType.STR_TYPE
        }

        if len(self.tokens) > 0 and self.tokens[-1].type == TokenType.DOT:
            t_type = TokenType.ID
        else:
            t_type = keywords.get(value, TokenType.ID)
            
        self.add_token(t_type, value)