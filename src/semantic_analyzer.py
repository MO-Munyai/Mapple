from tokens import TokenType
from ast_nodes import *

class SymbolTable:
    def __init__(self):
        # Maps variable name to its data type
        self.symbols = {}

    def define(self, name, symbol_type):
        self.symbols[name] = symbol_type

    def lookup(self, name):
        return self.symbols.get(name)

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        # Define valid method conversions for UOM [cite: 74, 75, 84]
        self.valid_methods = {
            "int": ["str", "num"],
            "num": ["str", "int"],
            "str": ["int", "num", "char", "bool"],
            "bool": ["str"]
        }

    def analyze(self, ast):
        for node in ast:
            self.visit(node)

    def visit(self, node):
        """Dispatcher that returns the data type of the visited node."""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # If we encounter a string representation of a node (like placeholders used in parser)
        if isinstance(node, str): return None
        raise Exception(f"Semantic Error: No visit_{type(node).__name__} method defined.")

    # --- Visit Methods ---

    def visit_VarDeclNode(self, node):
        # 1. Prevent duplicate declarations
        if self.symbol_table.lookup(node.name):
            raise Exception(f"Semantic Error: Variable '{node.name}' is already declared.")
        
        # 2. If there is an initializer (= value), check type consistency [cite: 28, 51]
        if node.initializer:
            init_type = self.visit(node.initializer)
            if init_type != node.var_type:
                raise Exception(f"Type Mismatch: Cannot assign {init_type} to {node.var_type} variable '{node.name}'.")

        self.symbol_table.define(node.name, node.var_type)
        return node.var_type

    def visit_LiteralNode(self, node):
        # Map token types to Mapple types [cite: 48]
        mapping = {
            TokenType.INT_LIT: "int",
            TokenType.STR_LIT: "str",
            TokenType.NUM_LIT: "num",
            TokenType.CHAR_LIT: "char"
        }
        return mapping.get(node.token.type)

    def visit_VarAccessNode(self, node):
        # Check declaration before use
        var_type = self.symbol_table.lookup(node.name)
        if not var_type:
            raise Exception(f"Semantic Error: Variable '{node.name}' used before declaration.")
        return var_type

    def visit_BinaryOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.op.type

        if op == TokenType.PLUS:
            if left_type == "str" and right_type == "str":
                return "str"
            if left_type == "int" and right_type == "int":
                return "int"
            if left_type == "num" and right_type == "num":
                return "num"
            
            # If it reaches here, it's a mix (like str + int), so we CRASH.
            raise Exception(f"Semantic Error: Cannot add {left_type} and {right_type}. Use .str!")

        # Math Rules (Subtraction, Multiplication, etc.) [cite: 27]
        if op in [TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.MOD]:
            if left_type == right_type and left_type in ["int", "num"]:
                return left_type
            raise Exception(f"Semantic Error: Operator {node.op.value} requires matching numeric types.")

    def visit_MemberAccessNode(self, node):
        """Handles UOM calls: age.str or input().int[cite: 74, 75]."""
        obj_type = self.visit(node.obj)
        method = node.member # e.g., 'str', 'int'

        # Rule: Any type can call its own name as a method (no-op) or a valid conversion
        if method == obj_type:
            return obj_type
        
        # Check if the conversion is allowed in our UOM rules [cite: 84]
        if method in self.valid_methods and obj_type in self.valid_methods[method]:
            return method
            
        raise Exception(f"Semantic Error: Type {obj_type} has no method .{method}")

    def visit_CallNode(self, node):
        """Validates function calls[cite: 26, 31]."""
        # For v0.1, we assume 'input' always returns a 'str' that needs casting 
        if isinstance(node.callee, VarAccessNode) and node.callee.name == "input":
            return "str"
        
        # For other calls, visit the callee to find its type
        return self.visit(node.callee)

    def visit_PrintNode(self, node):
        # print() can take any valid expression [cite: 26, 46]
        self.visit(node.expression)
        return None