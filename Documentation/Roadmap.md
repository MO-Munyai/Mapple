# Compiled Programming Language Roadmap

## Phase 1: Language Design
- Decide syntax and semantics (Python-like, simple, compiled language).
- Features for v1: `let` variables, integers, arithmetic (`+ - * /`), `print`.
- Create a formal spec document with grammar and rules.
- Merge Phase 4 semantic analysis here: variable declaration checks, type checks.

## Phase 2: Lexer / Tokenizer
- Build your own lexer: split source code into tokens.
- Tokens: keywords (`let`, `print`), identifiers, numbers, operators, symbols.
- Ignore whitespace and comments.
- Output: token stream for parser.

## Phase 3: Parser
- Build your own parser (recursive descent recommended).
- Convert tokens into an AST (Abstract Syntax Tree).
- AST represents structure: operations, variables, statements.
- Example AST: Assign(x, Add(Number(5), Number(3))).

## Phase 4: Semantic Analysis (Merged with Phase 1)
- Ensure variables are declared before use.
- Check types and operation validity.
- Maintain symbol tables.

## Phase 5: Code Generation / Backend
- Options for compiling:
  1. Use LLVM as backend to generate machine code.
  2. Compile to C code and use `gcc/clang`.
  3. Build a VM and generate bytecode (easier for early stages).
- For first version, LLVM or C code generation is practical.

## Phase 6: Runtime & Standard Library
- Minimal runtime: `print()` mapping to system calls.
- Expandable later: I/O, math functions, arrays, strings.

## Phase 7: CLI / Build & Run
- Create a compiler script `mylangc`.
- Example workflow:
  ```bash
  mylangc examples/hello.me
  ./hello
  ```
- `mylangc` handles lexing, parsing, code generation, and produces an executable.

## Repo Setup
- Possible structure:
```
language/
  docs/
    spec.md
    roadmap.md
  src/
    lexer.py
    parser.py
    ast.py
    codegen.py
    main.py
  examples/
    hello.me
  tests/
  scripts/
    mylangc
  README.md
  LICENSE
```
