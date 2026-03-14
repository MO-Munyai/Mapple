import sys
from lexer import Lexer

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

        # 3. Initialize our Scanner (Lexer)
        lexer = Lexer(source_code)
        
        # 4. Generate the tokens
        tokens = lexer.scan_tokens()

        # 5. Print the results for debugging
        print(f"\n--- Compiling: {file_path} ---")
        print("Token Stream Generated:")
        for token in tokens:
            print(f"  {token}")
        
        print("\nLexical Analysis Successful!")

    except FileNotFoundError:
        print(f"Error: Could not find file '{file_path}'")
    except Exception as e:
        print(f"An error occurred during Lexing: {e}")

if __name__ == "__main__":
    run_compiler()