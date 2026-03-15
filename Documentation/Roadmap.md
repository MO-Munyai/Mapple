# Mapple (MPPL) Compiler Roadmap

## Phase 1: Language Design (Completed ✅)
- Syntax & Semantics: Established a hybrid Python/Java style (let keyword, strict types, ; terminators).
- Grammar: Defined formal rules for variables, arithmetic, and UOM method calls.
- Formal Spec: Created the foundation for the Mapple Identity.

## Phase 2: Lexer / Tokenizer (Completed ✅)
- Scanning: Successfully breaking source code into meaningful tokens.
- Advanced Logic: Implemented "Greedy" scanning for :: and ;;.
- Debugging: Added Line and Column tracking for precise error reporting.

## Phase 3: Parser (Completed ✅)
- Engine: Built a Recursive Descent parser.
- Structure: Converts flat tokens into a hierarchical Abstract Syntax Tree (AST).
- Features: Handles variable declarations, print calls, and method chaining.

## Phase 4: Semantic Analysis (Completed ✅)
- Symbol Table: Tracks variable names, types, and existence.
- Type Safety: Enforces strict rules (e.g., preventing str + int).
- Validation: Ensures "Declaration Before Use" and valid UOM method access.

## Phase 5: Code Generation / Backend 
- Strategy: Transpilation to Python 3.
- Translates Mapple AST nodes into equivalent Python code.
- Implements UOM (Uniform Object Model) by wrapping variables in Python type-casters (int(), str()).
- Next Up: Implementing logic for Control Flow (if, while) and Assignment fixes.

## Phase 6: Runtime & Standard Library
- v0.1: Leverages Python's built-in print() and input().
- v0.2 Plan: Add file I/O and more advanced string manipulation methods.

## Phase 7: CLI / Build & Run
- Command: Created the mppl (Windows .bat) tool.
- Workflow: One-shot command that Lexes, Parses, Analyzes, Generates, and Instantly Executes the code.
- Integration: Added to System PATH for global access.