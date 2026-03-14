class ASTNode:
    """Base class for all AST nodes."""
    pass

# --- Expressions (Things that have a value) ---

class LiteralNode(ASTNode):
    """Represents a constant value: 5, 10.5, "Hello", true."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Literal({self.value})"

class VarAccessNode(ASTNode):
    """Represents using a variable: x, age, name."""
    def __init__(self, token):
        self.token = token
        self.name = token.value

    def __repr__(self):
        return f"Var({self.name})"

class BinaryOpNode(ASTNode):
    """Represents math: 5 + 10, x * 2."""
    def __init__(self, left, op_token, right):
        self.left = left
        self.op = op_token
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left} {self.op.value} {self.right})"

# --- Statements (Complete instructions) ---

class VarDeclNode(ASTNode):
    """Represents 'let <type> <name> = <value>;'"""
    def __init__(self, var_type, name, initializer=None):
        self.var_type = var_type     # e.g., 'int'
        self.name = name             # e.g., 'age'
        self.initializer = initializer # The expression after the '='

    def __repr__(self):
        return f"VarDecl({self.var_type} {self.name} = {self.initializer})"

class PrintNode(ASTNode):
    """Represents 'print(...);'"""
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Print({self.expression})"
    
class CallNode(ASTNode):
    """Represents a function call: input("Enter")"""
    def __init__(self, callee, arguments):
        self.callee = callee      # Usually a VarAccessNode ('input')
        self.arguments = arguments # List of expressions

    def __repr__(self):
        return f"Call({self.callee}({self.arguments}))"

class MemberAccessNode(ASTNode):
    """Represents a dot access: object.method"""
    def __init__(self, obj, member):
        self.obj = obj       # The thing before the dot
        self.member = member # The ID after the dot

    def __repr__(self):
        return f"MemberAccess({self.obj}.{self.member})"