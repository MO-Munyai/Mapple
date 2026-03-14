from tokens import TokenType, Token

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.tokens = []

    def peek(self):
        if self.pos + 1 >= len(self.source): return None
        return self.source[self.pos + 1]

    def advance(self):
        char = self.source[self.pos]
        self.pos += 1
        return char

    def scan_tokens(self):
        while self.pos < len(self.source):
            char = self.advance()

            if char.isspace(): continue
            
            # --- Character & String Literals ---
            if char == '"': self.add_string()
            elif char == "'": self.add_char()
            
            # --- Greedy Terminators (:: and ;;) --- [cite: 13, 53]
            elif char == ':':
                if self.peek() == ':':
                    self.advance() # Consume second :
                    self.tokens.append(Token(TokenType.D_COLON, "::"))
                else:
                    self.tokens.append(Token(TokenType.COLON, ":"))
            
            elif char == ';':
                if self.peek() == ';':
                    self.advance() # Consume second ;
                    self.tokens.append(Token(TokenType.CLASS_END, ";;"))
                else:
                    self.tokens.append(Token(TokenType.STMT_END, ";"))

            # --- Identifiers & Keywords ---
            elif char.isalpha(): self.add_identifier(char)
            
            # --- Numbers (Int vs Num) --- 
            elif char.isdigit(): self.add_number(char)

            # --- Operators --- [cite: 27]
            elif char == '+':
                if self.peek() == '+':
                    self.advance()
                    self.tokens.append(Token(TokenType.PLUS_PLUS, "++"))
                else:
                    self.tokens.append(Token(TokenType.PLUS, "+"))
            elif char == '.': self.tokens.append(Token(TokenType.DOT, "."))
            elif char == '=': self.tokens.append(Token(TokenType.ASSIGN, "="))
            elif char == '(': self.tokens.append(Token(TokenType.LPAREN, "("))
            elif char == ')': self.tokens.append(Token(TokenType.RPAREN, ")"))

        self.tokens.append(Token(TokenType.EOF))
        return self.tokens

    def add_string(self):
        value = ""
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            value += self.advance()
        self.advance() # Close "
        self.tokens.append(Token(TokenType.STR_LIT, value))

    def add_number(self, first_digit):
        value = first_digit
        is_num = False
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            if self.source[self.pos] == '.': is_num = True
            value += self.advance()
        
        t_type = TokenType.NUM_LIT if is_num else TokenType.INT_LIT
        self.tokens.append(Token(t_type, value))

    def add_identifier(self, first_char):
        value = first_char
        # Keep reading characters as long as they are letters, numbers, or underscores
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            value += self.advance()
        
        # Determine the Token Type
        keywords = {
            "let": TokenType.LET, "func": TokenType.FUNC, "class": TokenType.CLASS,
            "print": TokenType.PRINT, "input": TokenType.INPUT, "return": TokenType.RETURN,
            "int": TokenType.INT_TYPE, "num": TokenType.NUM_TYPE, "str": TokenType.STR_TYPE,
            "char": TokenType.CHAR_LIT, "bool": TokenType.STR_TYPE # Placeholder types
        }

        # --- OPTION 1 LOGIC: The Context Check ---
        # If the previous token was a DOT (.), treat this as an ID (method name), NOT a keyword/type
        if len(self.tokens) > 0 and self.tokens[-1].type == TokenType.DOT:
            t_type = TokenType.ID
        else:
            # Otherwise, check if it's a keyword. If not a keyword, it's a standard ID.
            t_type = keywords.get(value, TokenType.ID)
            
        self.tokens.append(Token(t_type, value))