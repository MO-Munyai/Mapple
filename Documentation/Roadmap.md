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
- Symbol Table: Tracks variable names, types, initialization state, and existence.
- Type Safety: Enforces strict rules (e.g., preventing str + int).
- Validation: Ensures "Declaration Before Use", valid UOM method access, and callability checks.
- Widening: `int → num` implicit widening is supported in declarations, assignments, and arithmetic.

## Phase 5: Code Generation / Backend (Completed ✅)
- Strategy: Transpilation to Python 3.
- Translates Mapple AST nodes into equivalent Python code.
- Implements UOM (Unit of Measure) by wrapping variables in Python type-casters (int(), str(), float(), bool()).
- All scalar UOM methods (.int, .num, .str, .bool, .char) are implemented.

## Phase 5.1: Hardening & Bug Fixes (Active 🔧)
- Round 1 (Complete): Fixed 7 bugs covering parser arithmetic/assignment interaction (BUG-01),
  scalar callability (BUG-03), uninitialized variable detection (BUG-04), UOM lookup direction (BUG-07),
  .bool codegen (BUG-08), mandatory semicolons (BUG-15), and int→num widening (BUG-16).
- Round 2 (In Progress): Fixing interaction and regression issues discovered after Round 1.
  Char literals now parseable (NEW-06). Widening now applies in binary arithmetic (NEW-02).
  Remaining: input() arg validation (NEW-03), print() error quality (NEW-04),
  error priority (NEW-05), num storage precision (NEW-01).

## Phase 6: Runtime & Standard Library
- v0.1: Leverages Python's built-in print() and input().
- v0.2 Plan: Add file I/O and more advanced string manipulation methods.

## Phase 7: CLI / Build & Run (Completed ✅)
- Command: Created the mppl (Windows .bat) and mppl (Unix shell) tools.
- Workflow: One-shot command that Lexes, Parses, Analyzes, Generates, and Instantly Executes the code.
- Integration: Added to System PATH for global access.
- Flags: --version, --doctor, --show-python implemented.

## Upcoming Language Features

### Arithmetic Operators
- `-`, `*`, `%` are defined as token types but not yet emitted by the lexer.
- Semantic and code generation handlers are already written and ready.
- Plan: Add lexer support for these operators, extend the parser with proper precedence,
  and enable the `++` operator (currently lexed but not parsed).

### Functions (`func`)
- Parsing stub exists; function bodies are parsed but discarded as placeholder strings.
- Plan: Add real FuncDeclNode, scoped symbol table, parameter type checking, return type validation,
  and Python `def` code generation.

### Classes (`class`)
- Parsing stub exists; class bodies are discarded as placeholder strings.
- Plan: Full class model with fields, methods, constructors, and Python class output.
  Depends on functions being implemented first.

### Control Flow
- No if/else/while/for implemented yet.
- Plan: Phase 2 of language implementation after arithmetic and functions are stable.
