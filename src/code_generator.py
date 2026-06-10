from tokens import TokenType
from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.output = []

    def generate(self, ast):
        """Main entry point to turn the AST into Python code string."""
        for node in ast:
            line = self.visit(node)
            if line:
                self.output.append(line)
        return "\n".join(self.output)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Placeholder strings returned by the parser for unimplemented constructs (class, func)
        # are intentionally skipped until those AST nodes are fully implemented.
        if isinstance(node, str):
            return ""
        raise Exception(
            f"Code Generation Error: No generator implemented for node type "
            f"'{type(node).__name__}'. This is an internal compiler error."
        )

    # --- Generation Methods ---

    def visit_VarDeclNode(self, node):
        # Mapple: let int x = 5; -> Python: x = 5
        val = self.visit(node.initializer) if node.initializer else "None"
        return f"{node.name} = {val}"

    def visit_AssignmentNode(self, node):
        value = self.visit(node.value)
        return f"{node.name} = {value}"

    def visit_LiteralNode(self, node):
        # Emit source-shaped Python literals based on the original token type.
        if node.token.type == TokenType.STR_LIT:
            return f'"{node.value}"'
        if node.token.type == TokenType.CHAR_LIT:
            return f"'{node.value}'"
        return str(node.value)

    def visit_VarAccessNode(self, node):
        return node.name

    def visit_BinaryOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"({left} {node.op.value} {right})"

    def visit_PrintNode(self, node):
        expr = self.visit(node.expression)
        return f"print({expr})"

    def visit_CallNode(self, node):
        # For v0.1: handle input()
        if isinstance(node.callee, VarAccessNode) and node.callee.name == "input":
            prompt = self.visit(node.arguments[0]) if node.arguments else '""'
            return f"input({prompt})"
        return f"{self.visit(node.callee)}()"

    def visit_MemberAccessNode(self, node):
        """Crucial: Turns Mapple .int/.num/.str into Python wrappers."""
        obj_code = self.visit(node.obj)
        method = node.member

        if method == "int":
            return f"int({obj_code})"
        if method == "num":
            return f"float({obj_code})"
        if method == "str":
            return f"str({obj_code})"
            
        return obj_code # Default/No-op
