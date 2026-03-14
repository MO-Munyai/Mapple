import sys
from lexer import Lexer
from parser import Parser

def run_compiler():
    # 1. Check if the user provided a file path
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>.mp")
        return

    file_path = sys.argv[1]

    try:
        # 2. Open and read the Mapple source file
        with open(file_path, 'r') as file:
            source_code = file.read()

        # 3. Lexical Analysis (Tokens)
        lexer = Lexer(source_code)
        tokens = lexer.scan_tokens()

        print(f"\n--- Compiling: {file_path} ---")
        
        # 4. Parsing (Tree)
        parser = Parser(tokens)
        ast = parser.parse()

        print("Abstract Syntax Tree (AST) Generated:")
        for node in ast:
            print(f"  {node}")
        
        print("\nParsing Successful!")

    except FileNotFoundError:
        print(f"Error: Could not find file '{file_path}'")
    except Exception as e:
        # This will catch Syntax Errors from the parser
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_compiler()