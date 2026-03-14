class SymbolTable:
    def __init__(self):
        # A simple dictionary: { 'variable_name': 'type' }
        self.symbols = {}

    def define(self, name, symbol_type):
        """Register a new variable."""
        self.symbols[name] = symbol_type

    def lookup(self, name):
        """Check if a variable exists and return its type."""
        return self.symbols.get(name)

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, ast):
        """Walks through the list of AST nodes."""
        for node in ast:
            self.visit(node)

    def visit(self, node):
        """Dispatcher to visit different node types."""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined.")

    # --- Visit Methods ---

    def visit_VarDeclNode(self, node):
        # 1. Check if variable is already defined
        if self.symbol_table.lookup(node.name):
            raise Exception(f"Semantic Error: Variable '{node.name}' already declared.")
        
        # 2. Add to symbol table
        self.symbol_table.define(node.name, node.var_type)
        print(f"Defined {node.name} as {node.var_type}")

    def visit_VarAccessNode(self, node):
        # 1. Ensure variable was declared before use
        var_type = self.symbol_table.lookup(node.name)
        if not var_type:
            raise Exception(f"Semantic Error: Variable '{node.name}' used before declaration.")
        return var_type