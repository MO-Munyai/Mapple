from tokens import TokenType
from ast_nodes import *

class SymbolTable:
    def __init__(self):
        self.symbols = {}  # name -> (type, is_initialized)

    def define(self, name, symbol_type, initialized=True):
        self.symbols[name] = (symbol_type, initialized)

    def lookup(self, name):
        entry = self.symbols.get(name)
        return entry[0] if entry else None

    def is_initialized(self, name):
        entry = self.symbols.get(name)
        return entry[1] if entry else False

    def mark_initialized(self, name):
        entry = self.symbols.get(name)
        if entry:
            self.symbols[name] = (entry[0], True)

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
            if init_type != node.var_type and not self._is_widening(init_type, node.var_type):
                raise Exception(f"Type Mismatch: Cannot assign {init_type} to {node.var_type} variable '{node.name}'.")

        self.symbol_table.define(node.name, node.var_type, initialized=node.initializer is not None)
        return node.var_type

    def visit_LiteralNode(self, node):
        mapping = {
            TokenType.INT_LIT: "int",
            TokenType.STR_LIT: "str",
            TokenType.NUM_LIT: "num",
            TokenType.CHAR_LIT: "char"
        }
        result = mapping.get(node.token.type)
        if result is None:
            raise Exception(
                f"Semantic Error: Unrecognized literal token type '{node.token.type}' "
                f"with value '{node.value}'."
            )
        return result

    def visit_VarAccessNode(self, node):
        var_type = self.symbol_table.lookup(node.name)
        if not var_type:
            raise Exception(f"Semantic Error: Variable '{node.name}' used before declaration.")
        if not self.symbol_table.is_initialized(node.name):
            raise Exception(
                f"Semantic Error: Variable '{node.name}' is declared but has no value. "
                f"Assign a value before using it."
            )
        return var_type

    def visit_AssignmentNode(self, node):
        target_type = self.symbol_table.lookup(node.name)
        if not target_type:
            raise Exception(
                f"Semantic Error: Variable '{node.name}' assigned before declaration. "
                f"Declare it first with 'let {'{type}'} {node.name} = ...;'."
            )

        value_type = self.visit(node.value)
        if value_type is None:
            raise Exception(
                f"Semantic Error: The expression assigned to '{node.name}' "
                "has no resolvable type. Check the right-hand side expression."
            )
        if value_type != target_type and not self._is_widening(value_type, target_type):
            raise Exception(
                f"Type Mismatch: Cannot assign {value_type} to {target_type} "
                f"variable '{node.name}'. Use a {target_type} expression, "
                f"or convert with .{target_type}."
            )

        self.symbol_table.mark_initialized(node.name)
        return target_type

    def visit_BinaryOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.op.type

        if left_type is None or right_type is None:
            raise Exception(
                f"Semantic Error: Cannot apply operator '{node.op.value}' — "
                f"one or both operands have no resolvable type "
                f"(left: {left_type}, right: {right_type})."
            )

        if op == TokenType.PLUS:
            if left_type == "str" and right_type == "str":
                return "str"
            if left_type == "int" and right_type == "int":
                return "int"
            if left_type == "num" and right_type == "num":
                return "num"
            raise Exception(
                f"Semantic Error: Cannot add {left_type} and {right_type}. "
                "Both sides must be the same type. Use .str to convert first."
            )

        if op in [TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.MOD]:
            if left_type == right_type and left_type in ["int", "num"]:
                return left_type
            raise Exception(
                f"Semantic Error: Operator '{node.op.value}' requires matching numeric types "
                f"(int or num), got {left_type} and {right_type}."
            )

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

    _SCALAR_TYPES = {"int", "num", "str", "char", "bool"}
    _ALLOWED_WIDENINGS = {("int", "num")}

    def _is_widening(self, from_type, to_type):
        return (from_type, to_type) in self._ALLOWED_WIDENINGS

    def visit_CallNode(self, node):
        if isinstance(node.callee, VarAccessNode) and node.callee.name == "input":
            return "str"

        callee_type = self.visit(node.callee)
        if callee_type in self._SCALAR_TYPES:
            callee_name = node.callee.name if isinstance(node.callee, VarAccessNode) else repr(node.callee)
            raise Exception(
                f"Semantic Error: '{callee_name}' is of type '{callee_type}' and is not callable. "
                "Only functions can be called."
            )
        return callee_type

    def visit_PrintNode(self, node):
        # print() can take any valid expression [cite: 26, 46]
        self.visit(node.expression)
        return None
