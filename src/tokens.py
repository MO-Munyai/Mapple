from enum import Enum, auto

class TokenType(Enum):
    # Keywords & Types
    LET = auto(); FUNC = auto(); CLASS = auto()
    PRINT = auto(); INPUT = auto(); RETURN = auto()
    INT_TYPE = auto(); NUM_TYPE = auto(); STR_TYPE = auto()
    
    # Literals
    ID = auto(); INT_LIT = auto(); NUM_LIT = auto()
    STR_LIT = auto(); CHAR_LIT = auto()
    
    # Operators & Symbols
    ASSIGN = auto(); PLUS = auto(); MINUS = auto()
    MUL = auto(); DIV = auto(); MOD = auto()
    PLUS_PLUS = auto(); DOT = auto()
    
    # Block Logic
    COLON = auto(); D_COLON = auto()        # : and ::
    STMT_END = auto(); CLASS_END = auto()  # ; and ;;
    
    LPAREN = auto(); RPAREN = auto()
    EOF = auto()

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        # Professional formatting: [Line:Col] Type: Value
        return f"[{self.line}:{self.column}] {self.type.name}: {repr(self.value)}"