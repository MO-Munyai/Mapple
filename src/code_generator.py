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
        return "" # Ignore nodes we can't generate yet

    # --- Generation Methods ---

    def visit_VarDeclNode(self, node):
        # Mapple: let int x = 5; -> Python: x = 5
        val = self.visit(node.initializer) if node.initializer else "None"
        return f"{node.name} = {val}"

    def visit_LiteralNode(self, node):
        # Strings need quotes, numbers don't
        if isinstance(node.value, str):
            return f'"{node.value}"'
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