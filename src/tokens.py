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
    
    # Block Logic (Our Greedy Tokens)
    COLON = auto(); D_COLON = auto()        # : and ::
    STMT_END = auto(); CLASS_END = auto()  # ; and ;;
    
    LPAREN = auto(); RPAREN = auto()
    EOF = auto() # End of File

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"