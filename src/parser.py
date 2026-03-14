from tokens import TokenType
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token

    def eat(self, expected_type):
        token = self.peek()
        if token.type == expected_type:
            return self.advance()
        raise Exception(f"Syntax Error: Expected {expected_type}, got {token.type} at token '{token.value}'")

    def parse(self):
        """Entry point for parsing the file."""
        statements = []
        while self.peek().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        """Dispatches to specific parsing rules based on keywords."""
        token = self.peek()
        if token.type == TokenType.CLASS:
            return self.parse_class()
        elif token.type == TokenType.FUNC:
            return self.parse_function()
        elif token.type == TokenType.LET:
            return self.parse_declaration()
        elif token.type == TokenType.PRINT:
            return self.parse_print()
        else:
            # Handle plain assignments like 'age = 20;' or expressions [cite: 59, 60]
            expr = self.parse_expression()
            if self.peek().type == TokenType.STMT_END:
                self.eat(TokenType.STMT_END)
            return expr

    def parse_class(self):
        """Parses 'class Name:: ... ;;'[cite: 10, 13, 53]."""
        self.eat(TokenType.CLASS)
        name = self.eat(TokenType.ID).value
        self.eat(TokenType.D_COLON)
        
        body = []
        while self.peek().type != TokenType.CLASS_END and self.peek().type != TokenType.EOF:
            body.append(self.parse_statement())
            
        self.eat(TokenType.CLASS_END)
        return f"ClassNode({name}, Body: {body})" # Placeholder for ClassNode

    def parse_function(self):
        """Parses 'func Name(params): ... ;'."""
        self.eat(TokenType.FUNC)
        name = self.eat(TokenType.ID).value
        self.eat(TokenType.LPAREN)
        # For v0.1, we skip complex parameter parsing
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.COLON)
        
        body = []
        while self.peek().type != TokenType.STMT_END and self.peek().type != TokenType.EOF:
            body.append(self.parse_statement())
            
        self.eat(TokenType.STMT_END)
        return f"FuncNode({name}, Body: {body})" # Placeholder for FuncNode

    def parse_declaration(self):
        """let <type> <name> = <value>;[cite: 54, 55]."""
        self.eat(TokenType.LET)
        var_type_token = self.advance() # Get 'int', 'str', etc.
        name = self.eat(TokenType.ID).value
        
        initializer = None
        if self.peek().type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            initializer = self.parse_expression()
            
        if self.peek().type == TokenType.STMT_END:
            self.eat(TokenType.STMT_END)
        return VarDeclNode(var_type_token.value, name, initializer)

    def parse_print(self):
        """print(expr);[cite: 26, 41]."""
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        expr = self.parse_expression()
        self.eat(TokenType.RPAREN)
        if self.peek().type == TokenType.STMT_END:
            self.eat(TokenType.STMT_END)
        return PrintNode(expr)

    def parse_expression(self):
        """Handles UOM dot-access and binary operations."""
        left = self.parse_primary()
        
        # Handle Method/Member Access (UOM) [cite: 33, 51]
        while self.peek().type == TokenType.DOT:
            self.eat(TokenType.DOT)
            member = self.eat(TokenType.ID).value
            left = MemberAccessNode(left, member)
            
        # Handle Binary Operations (Assignment or Addition) [cite: 27, 59]
        if self.peek().type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            right = self.parse_expression()
            return f"Assignment({left} = {right})"
        
        if self.peek().type == TokenType.PLUS:
            op = self.eat(TokenType.PLUS)
            right = self.parse_expression()
            return BinaryOpNode(left, op, right)
            
        return left

    def parse_primary(self):
        """Parses base units like literals and function calls."""
        token = self.peek()
        
        if token.type in [TokenType.INT_LIT, TokenType.STR_LIT, TokenType.NUM_LIT]:
            return LiteralNode(self.advance())
            
        if token.type in [TokenType.ID, TokenType.INPUT, TokenType.INT_TYPE, TokenType.STR_TYPE]:
            name_node = VarAccessNode(self.advance())
            
            # Handle Function/Method Call with Arguments 
            if self.peek().type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                args = []
                if self.peek().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                self.eat(TokenType.RPAREN)
                return CallNode(name_node, args)
            
            return name_node
        
        raise Exception(f"Unexpected token in expression: {token}")