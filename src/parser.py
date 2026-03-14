from tokens import TokenType
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def eat(self, expected_type):
        """Consume a token if it matches the expected type, else throw error."""
        token = self.peek()
        if token.type == expected_type:
            self.pos += 1
            return token
        raise Exception(f"Syntax Error: Expected {expected_type}, got {token.type}")

    def parse(self):
        """Entry point: parses a list of statements until EOF."""
        statements = []
        while self.peek().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        """Decides which type of statement to parse."""
        token = self.peek()
        if token.type == TokenType.LET:
            return self.parse_declaration()
        elif token.type == TokenType.PRINT:
            return self.parse_print()
        else:
            # Fallback for expressions like 'age = 20;'
            expr = self.parse_expression()
            self.eat(TokenType.STMT_END)
            return expr

    def parse_declaration(self):
        """let <type> <name> = <value>;"""
        self.eat(TokenType.LET) # [cite: 54, 55]
        var_type = self.advance().value # Get 'int', 'str', etc.
        name = self.eat(TokenType.ID).value # Get the variable name [cite: 54]
        
        initializer = None
        if self.peek().type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN) # [cite: 55]
            initializer = self.parse_expression()
            
        self.eat(TokenType.STMT_END) # [cite: 9, 52]
        return VarDeclNode(var_type, name, initializer)

    def parse_print(self):
        """print(expression);"""
        self.eat(TokenType.PRINT) # [cite: 26, 41]
        self.eat(TokenType.LPAREN)
        expr = self.parse_expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.STMT_END) # [cite: 9, 52]
        return PrintNode(expr)

    def parse_expression(self):
        """For now, handles simple binary math and method calls."""
        # This is a simplified version for v0.1
        left = self.parse_primary()
        
        # Handle Dot Access (UOM)
        while self.peek().type == TokenType.DOT:
            self.eat(TokenType.DOT)
            member = self.eat(TokenType.ID).value
            left = MemberAccessNode(left, member)
            
        # Handle Addition
        if self.peek().type == TokenType.PLUS:
            op = self.eat(TokenType.PLUS)
            right = self.parse_expression()
            return BinaryOpNode(left, op, right)
            
        return left

    def parse_primary(self):
        """Parses the 'base' units: Numbers, IDs, or Function Calls."""
        token = self.peek()
        
        if token.type == TokenType.INT_LIT or token.type == TokenType.STR_LIT:
            return LiteralNode(self.advance())
            
        if token.type == TokenType.ID or token.type == TokenType.INPUT:
            name_token = self.advance()
            node = VarAccessNode(name_token)
            
            # If followed by '(', it's a function call
            if self.peek().type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                # Arguments could be added here later
                self.eat(TokenType.RPAREN)
                return CallNode(node, [])
            return node

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token