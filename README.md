# Mapple (MPPL) v0.2.0

Mapple is a small, beginner-oriented compiled language that currently transpiles `.mp` source files into Python and then executes the generated Python with the same interpreter that launched the compiler.

The implementation is intentionally strict: variables must be declared before use, declared types are checked during semantic analysis, and mixed-type operations require explicit conversion through Mapple's dot-style conversion syntax such as `.str`, `.int`, and `.num`.

This repository is an early compiler implementation, not a production language runtime. The core pipeline exists and works for the supported subset, but several language constructs are still placeholders or partially implemented.

## Current Version

The active compiler version is `0.2.0`.

The version is defined in [`src/main.py`](src/main.py):

```python
VERSION = "0.2.0"
```

You can verify it with:

```powershell
python src\main.py --version
```

Or, after installing the launcher on your PATH:

```powershell
mppl --version
```

Expected output:

```text
Mapple Compiler v0.2.0
```

## Requirements

- Python 3.10 or newer.
- A terminal that can run either the Windows batch launcher or the Unix-style shell launcher.
- No third-party Python packages are required.

The compiler uses only the Python standard library:

- `sys`
- `os`
- `subprocess`
- `enum`

## Repository Layout

```text
Mapple/
  README.md
  install.bat
  mppl.bat
  mppl
  setup_mac.sh
  code_examples/
    hello_world.mp
    hello_mapple.mp
    test_file.mp
    assignment_basic.mp
    assignment_expr_rhs.mp
    assignment_str_reassign.mp
    assignment_num_reassign.mp
    assignment_multiple.mp
    assignment_uom_rhs.mp
    assignment_uninit.mp
    assignment_type_error.mp
    assignment_type_error_num_to_int.mp
    assignment_type_error_int_to_str.mp
    assignment_undeclared.mp
    assignment_chain_error.mp
    assignment_invalid_target.mp
    lexer_error_unterminated_string.mp
    lexer_error_bad_number.mp
    lexer_error_unknown_char.mp
    parser_error_bad_type.mp
  Documentation/
    Input Method.txt
    MPPL Spec Doc.docx
    Roadmap.md
    notes_and_bugs_and updates_and_stuff.md
    struc.txt
    test.mp
    test_file_mp.txt
  src/
    ast_nodes.py
    code_generator.py
    lexer.py
    main.py
    parser.py
    semantic_analyzer.py
    tokens.py
```

Important paths:

- [`src/main.py`](src/main.py) is the CLI entry point and compiler pipeline coordinator.
- [`src/lexer.py`](src/lexer.py) converts raw source text into tokens.
- [`src/tokens.py`](src/tokens.py) defines token types and token metadata.
- [`src/parser.py`](src/parser.py) builds the current AST representation.
- [`src/ast_nodes.py`](src/ast_nodes.py) defines concrete AST node classes.
- [`src/semantic_analyzer.py`](src/semantic_analyzer.py) performs declaration and type checks.
- [`src/code_generator.py`](src/code_generator.py) emits Python code.
- [`code_examples/`](code_examples) contains runnable sample `.mp` programs.
- [`Documentation/Roadmap.md`](Documentation/Roadmap.md) contains the historical phase roadmap.

## How To Run

### Run Without Installing

From the project directory:

```powershell
python src\main.py code_examples\hello_world.mp
```

On macOS or Linux:

```bash
python3 src/main.py code_examples/hello_world.mp
```

When run normally, the compiler:

1. Reads the `.mp` file.
2. Lexes the source into tokens.
3. Parses the tokens into AST nodes.
4. Runs semantic validation.
5. Generates Python code.
6. Writes a generated Python file next to the input file.
7. Executes that generated Python file.

For example:

```powershell
python src\main.py code_examples\hello_world.mp
```

Creates:

```text
code_examples\hello_world_output.py
```

Then executes it.

### Show Generated Python Without Writing An Output File

Use `--show-python` when you want to inspect the generated Python:

```powershell
python src\main.py code_examples\hello_mapple.mp --show-python
```

Example generated output:

```python
name = "Mapple"
version = "v0.2.0"
print(("Current " + (str(name) + (" version is " + str(version)))))
```

This mode returns after printing the generated Python and does not write or execute an output file.

### Windows Launcher

The Windows launcher is [`mppl.bat`](mppl.bat):

```bat
@echo off
python "%~dp0src\main.py" %*
```

After the project directory is on your PATH, run:

```powershell
mppl code_examples\hello_world.mp
mppl --version
mppl --doctor
```

### Windows Install Script

Run:

```powershell
.\install.bat
```

The installer:

1. Checks that `python` is available.
2. Checks for an existing `mppl --version`.
3. Adds the current project directory to the user PATH using `setx`.
4. Asks you to restart the terminal so PATH changes apply.

Important limitation: `setx PATH "%PATH%;%CURRENT_DIR%"` writes the expanded current PATH back to the user PATH. On Windows, this can duplicate entries and may be affected by PATH length limits. Review your PATH if you use the installer repeatedly.

### macOS / Linux Launcher

The Unix-style launcher is [`mppl`](mppl):

```bash
#!/bin/zsh
python3 "$(dirname "$0")/src/main.py" "$@"
```

Make it executable:

```bash
chmod +x ./mppl
```

Then run:

```bash
./mppl code_examples/hello_world.mp
```

### macOS Setup Script

Run:

```bash
./setup_mac.sh
```

The script:

1. Checks for `python3`.
2. Marks `./mppl` executable.
3. Adds the current directory to `.zshrc` or `.bash_profile` if it is not already in PATH.

The project notes still list "fix the mac setup and files" as an outstanding item, so treat this script as useful but not heavily validated.

## CLI Reference

```text
mppl <filename>.mp [--show-python]
mppl --version
mppl --doctor
```

### `mppl <filename>.mp`

Compiles and runs a Mapple source file.

Example:

```powershell
mppl code_examples\test_file.mp
```

Output behavior:

- Writes generated Python to `<filename>_output.py`.
- Runs the generated file with `sys.executable`.
- Prints an execution failure message if the generated Python exits with a non-zero code.

### `mppl <filename>.mp --show-python`

Prints the generated Python code and exits before writing or executing an output file.

### `mppl --version`

Prints the compiler version.

### `mppl --doctor`

Prints diagnostic information:

- Python executable path.
- Python version.
- Compiler directory.
- Platform string.

Known issue: on some Windows terminals using legacy encodings such as `cp1252`, `--doctor` can crash while printing emoji characters with a `UnicodeEncodeError`. Setting UTF-8 output or removing emoji from the CLI strings would fix this.

## Language Features Currently Implemented

### Comments

Single-line comments start with `//`:

```mapple
// This is a comment
print("Hello World");
```

Block comments are not implemented.

### Statement Terminators

Every statement requires a `;` terminator:

```mapple
let str name = "Mapple";
print(name);
```

Semicolons are mandatory. A missing `;` is a hard syntax error at the parser stage.

### Variable Declarations

Variables are declared with:

```mapple
let <type> <name> = <expression>;
```

Examples:

```mapple
let str name = "Mapple";
let int age = 21;
let num weight = 72.5;
```

Declarations without initializers are accepted by the parser:

```mapple
let int age;
```

Generated Python:

```python
age = None
```

However, any attempt to read `age` before assigning it a value is a **semantic error**:

```mapple
let int age;
print(age);  // Semantic Error: Variable 'age' is declared but has no value.
```

The first successful assignment marks the variable as initialized and allows it to be read.

### Primitive Types

The current implementation recognizes these type keywords:

- `int`
- `num`
- `str`

The token and semantic layers also contain partial references to:

- `char`
- `bool`

`char` is not accepted as a declaration type keyword, but `char` literals (`'x'`) are fully supported as expressions — they lex, parse, and pass semantic analysis as type `char`. `bool` appears in UOM conversion rules (`.bool` is a valid conversion) but has no literal syntax, declaration keyword, or standalone type support.

### Literals

Implemented literals:

```mapple
42
3.14
"hello"
'x'
```

Important details:

- Integer literals become `INT_LIT`.
- Decimal literals become `NUM_LIT`.
- Double-quoted strings become `STR_LIT`.
- Single-quoted characters become `CHAR_LIT`.
- Escape sequences are not implemented for strings or chars.
- Unterminated strings and chars are not reported with dedicated errors.
- Numeric scanning allows repeated dots, so malformed input like `1.2.3` can tokenize as a numeric literal and fail later or generate invalid Python.

### Print

`print` is implemented as a language keyword:

```mapple
print("Hello World");
```

Generated Python:

```python
print("Hello World")
```

`print` can receive any expression that passes semantic analysis.

### Input

`input` is implemented as a built-in call recognized by semantic analysis and code generation:

```mapple
let str name = input("Enter your name: ").str;
let int age = input("Enter your age: ").int;
let num weight = input("Enter your weight: ").num;
```

Generated Python:

```python
name = str(input("Enter your name: "))
age = int(input("Enter your age: "))
weight = float(input("Enter your weight: "))
```

Current behavior:

- `input(...)` semantically returns `str`.
- Conversions are expressed through member access such as `.int`, `.num`, and `.str`.
- Invalid user input is handled by Python at runtime, not by Mapple. For example, entering `abc` for `.int` raises Python's `ValueError`.

### Explicit Type Conversion

Mapple uses dot-style conversion syntax:

```mapple
age.str
input("Age: ").int
input("Weight: ").num
```

The generator maps these conversions to Python wrappers:

```python
str(age)
int(input("Age: "))
float(input("Weight: "))
```

Current generated mappings:

- `.int` -> `int(...)`
- `.num` -> `float(...)`
- `.str` -> `str(...)`

The semantic analyzer is designed to reject unsupported conversions before code generation.

### String Concatenation And Addition

The `+` operator is implemented for matching types:

```mapple
let str name = "Mapple";
let str version = "v0.2.0";

print("Current " + name.str + " version is " + version.str);
```

Supported semantic combinations:

- `str + str` returns `str`
- `int + int` returns `int`
- `num + num` returns `num`
- `int + num` or `num + int` returns `num` (implicit widening — `int` promotes to `num`)

Other mixed-type combinations are rejected. For example:

```mapple
let int age = 21;
print("Age: " + age);
```

This fails because `str + int` is not allowed. Use:

```mapple
print("Age: " + age.str);
```

### Declaration Before Use

Variables must be declared before they are read:

```mapple
print(name); // semantic error
let str name = "Mapple";
```

The semantic analyzer stores declared names in a symbol table and rejects unknown variable access.

### Duplicate Declaration Checks

Declaring the same variable name twice in the same current global symbol table is rejected:

```mapple
let str name = "A";
let str name = "B"; // semantic error
```

There is no lexical scope model yet, so all currently analyzed declarations share one symbol table.

## Compiler Architecture

The compiler is a direct multi-phase pipeline coordinated by `run_compiler()` in [`src/main.py`](src/main.py).

### 1. CLI And File Loading

`main.py` reads command-line arguments from `sys.argv`.

Special commands:

- `--version`
- `--doctor`

Compilation mode expects the first argument to be a source file path. The source file is read into a single string before compilation.

### 2. Lexical Analysis

Implemented in [`src/lexer.py`](src/lexer.py).

The lexer scans the source character by character and emits `Token` objects. Each token records:

- token type
- token value
- source line
- source column

The lexer handles:

- whitespace skipping
- line tracking
- `//` comments
- string literals
- char literals
- integer and decimal number literals
- identifiers
- keywords
- basic operators and punctuation
- greedy scanning for `::` and `;;`

Keyword mapping:

```python
{
    "let": TokenType.LET,
    "func": TokenType.FUNC,
    "class": TokenType.CLASS,
    "print": TokenType.PRINT,
    "input": TokenType.INPUT,
    "return": TokenType.RETURN,
    "int": TokenType.INT_TYPE,
    "num": TokenType.NUM_TYPE,
    "str": TokenType.STR_TYPE,
}
```

One important implementation detail: when an identifier appears after a dot, it is forced to `ID` rather than being treated as a keyword. This allows conversion syntax like:

```mapple
age.str
```

Without that rule, `str` would become `STR_TYPE` and member access parsing would fail.

### 3. Token Model

Implemented in [`src/tokens.py`](src/tokens.py).

`TokenType` is an `Enum` with categories for:

- keywords and types
- literals
- operators and symbols
- block delimiters
- parentheses
- EOF

The token set is larger than the currently supported parser and lexer behavior. For example, `MINUS`, `MUL`, and `MOD` exist in `TokenType`, but the lexer does not currently emit them.

### 4. Parsing

Implemented in [`src/parser.py`](src/parser.py).

The parser is a recursive descent parser. Its `parse()` method reads statements until EOF and returns a list of AST nodes.

Currently parsed concrete AST nodes:

- `VarDeclNode`
- `AssignmentNode`
- `PrintNode`
- `LiteralNode`
- `VarAccessNode`
- `BinaryOpNode`
- `CallNode`
- `MemberAccessNode`

Partially parsed placeholders (not real AST nodes):

- classes
- functions

Classes and functions currently return string placeholders like:

```text
ClassNode(Name, Body: ...)
FuncNode(Name, Body: ...)
```

Those placeholders are skipped by semantic analysis and code generation. The code generator raises an error if it encounters any non-string node without a registered generator, so new node types cannot be accidentally silenced.

### 5. AST Nodes

Implemented in [`src/ast_nodes.py`](src/ast_nodes.py).

The current AST model separates:

- expressions: literals, variable access, binary operations, calls, member access
- statements: variable declarations, assignment, and print calls

The AST is intentionally small. It is enough for the current language subset but not yet expressive enough for full control flow, scoped functions, classes, or return statements.

### 6. Semantic Analysis

Implemented in [`src/semantic_analyzer.py`](src/semantic_analyzer.py).

Semantic analysis walks the AST before code generation and enforces the current static rules:

- variables must be declared before use
- variables must be initialized before they are read
- variable names cannot be redeclared in the same symbol table
- initializer expression type must match declared variable type (`int → num` widening is the only implicit exception)
- `+` works on matching `str`, `int`, or `num` operands; `int + num` / `num + int` is also valid via widening
- numeric operators (`-`, `*`, `%`) require matching numeric types or a valid widening
- member conversion must be valid according to the UOM conversion table
- scalar types (`int`, `num`, `str`, `char`, `bool`) cannot be called as functions
- `input(...)` returns `str`
- `print(...)` accepts any valid expression

The symbol table is currently a single dictionary mapping variable names to `(type, is_initialized)` tuples:

```python
{
    "<variable_name>": ("<type>", True | False)
}
```

There is no nested scope, function scope, class scope, import scope, or module boundary yet.

### 7. Code Generation

Implemented in [`src/code_generator.py`](src/code_generator.py).

The code generator walks the semantically valid AST and emits Python source text.

Current generation examples:

Mapple:

```mapple
let str name = "Mapple";
print("Hello " + name.str);
```

Python:

```python
name = "Mapple"
print(("Hello " + str(name)))
```

Generation is intentionally direct. There is no bytecode, VM, optimizer, linker, package system, or standalone executable output.

### 8. Output And Execution

In normal mode, `main.py` writes generated Python next to the input file:

```text
<source_name>_output.py
```

It then executes that file using:

```python
subprocess.run([sys.executable, output_file])
```

This means Mapple programs run with the same Python interpreter used to launch the compiler.

## Current Examples

### Hello World

[`code_examples/hello_world.mp`](code_examples/hello_world.mp):

```mapple
print("Hello World");
```

### Version Example

[`code_examples/hello_mapple.mp`](code_examples/hello_mapple.mp):

```mapple
let str name = "Mapple";
let str version = "v0.2.0";

print("Current " + name.str + " version is " + version.str);
```

### Input And Conversion Example

[`code_examples/test_file.mp`](code_examples/test_file.mp):

```mapple
let str name = input("Enter your name: ").str;

let str surname = input("Enter your surname: ").str;

let int age = input("Enter your age: ").int;

let num weight = input("Enter your weight: ").num;

print("Hello " + name.str + " " + surname);
print("You are " + age.str + " years old.");
print("You weigh " + weight.str + " kgs");
```

Generated Python in `--show-python` mode:

```python
name = str(input("Enter your name: "))
surname = str(input("Enter your surname: "))
age = int(input("Enter your age: "))
weight = float(input("Enter your weight: "))
print(("Hello " + (str(name) + (" " + surname))))
print(("You are " + (str(age) + " years old.")))
print(("You weigh " + (str(weight) + " kgs")))
```

## Error Handling

Compiler errors are currently caught by a broad exception handler in `main.py`:

```text
COMPILER ERROR: <message>
```

The lexer records line and column metadata, and parser errors include token values in some cases, but diagnostics are not yet consistently source-span based.

Examples of current errors:

- syntax errors from unexpected tokens
- semantic errors for undeclared variables
- semantic errors for duplicate declarations
- type mismatch errors
- unsupported member conversion errors
- Python runtime errors from generated code

Runtime errors from generated Python are not wrapped in a Mapple-specific diagnostic system.

## Limitations And Known Gaps

### Language Surface

- No `if` statements.
- No `else` statements.
- No `while` loops.
- No `for` loops.
- No arrays or lists.
- No dictionaries or maps.
- No imports or modules.
- No package system.
- No user-defined operators.
- No boolean literals.
- No comparison operators.
- No logical operators.
- No unary operators.
- No string interpolation.
- No multiline strings.
- No block comments.

### Variables And Assignment

- Declaration with initialization works.
- Assignment parsing produces a real `AssignmentNode` (not a placeholder).
- Declaration-before-assignment is enforced: assigning to an undeclared name is a semantic error.
- Assignment type compatibility is enforced: the right-hand side must match the declared type.
- Assignment code generation emits a Python assignment statement.
- Uninitialized variables (`let int x;`) generate `None` in Python. Reading one before its first assignment is a semantic error. Assigning to it marks it as initialized and allows subsequent reads.
- Chained assignment (`a = b = 5`) is rejected by the parser.
- The left-hand side of an assignment must be a plain variable name; using a literal or expression on the left is a syntax error.
- There is no runtime type enforcement after code generation.

### Functions

- `func` is tokenized and partially parsed.
- Function parameters are not implemented.
- Function calls are only meaningfully implemented for built-in `input`.
- `return` is tokenized but not parsed or generated.
- Parsed functions are placeholder strings, not real AST nodes.
- Function bodies are not emitted as Python functions.
- There is no function scope.

### Classes

- `class`, `::`, and `;;` are tokenized.
- Class blocks are partially parsed.
- Parsed classes are placeholder strings, not real AST nodes.
- Class bodies are not semantically modeled.
- Class definitions are not emitted as Python classes.
- There is no object construction, field access, method dispatch, inheritance, or visibility model.

### Arithmetic

- `+` is lexed, parsed, semantically checked, and generated.
- `-`, `*`, and `%` exist as token types but are not emitted by the lexer.
- `/` is emitted by the lexer and has semantic rules, but the parser does not currently parse it as a binary operator.
- Operator precedence is not implemented. `+` parsing is recursive and right-associative.
- Parenthesized expressions are not implemented except for function and print call syntax.

### Type System

- The current type system is intentionally simple and global.
- Only `int`, `num`, and `str` are usable declaration types.
- `char` literals are fully usable in expressions but `char` is not a valid declaration type keyword.
- `bool` appears in conversion tables but is not otherwise implemented.
- There is no inference.
- There are no nullable rules.
- There are no generics.
- There are no user-defined types.
- There is no separate compile-time representation for functions or classes.

### Conversion Model

- `.int`, `.num`, and `.str` generate Python casts.
- Invalid casts fail at Python runtime rather than through Mapple-specific runtime errors.
- Invalid casts are caught at semantic analysis and produce a clear error before code generation.

### Lexer And Parser Robustness

- Strings do not support escape sequences.
- Unterminated strings do not raise a dedicated lexer error.
- Unterminated chars do not raise a dedicated lexer error.
- Unknown characters are silently ignored if no branch handles them.
- The lexer only starts identifiers with alphabetic characters, not underscores.
- The lexer allows underscores after the first identifier character.
- Numeric scanning accepts any number of dots.
- Error recovery is not implemented. The compiler stops at the first raised exception.
- Several parser docstrings contain stale citation markers.

### Code Generation

- Code generation targets Python source only.
- There is no standalone binary output.
- There is no source map from generated Python back to Mapple lines.
- Placeholder parser outputs for classes and functions are ignored (they are plain Python strings, not real AST nodes).
- Unknown AST node types cause a `Code Generation Error` rather than being silently ignored.
- Generated files are written beside the source file and can overwrite previous generated output with the same name.

### CLI And Installation

- The CLI catches all exceptions and prints only the exception message.
- `--doctor` can fail on Windows consoles that cannot encode emoji.
- `install.bat` modifies user PATH with `setx`, which may duplicate entries or hit Windows PATH length behavior.
- The macOS setup script is noted in project docs as needing fixes.
- The Unix launcher uses `#!/bin/zsh`, so systems without `zsh` should invoke the compiler with `python3 src/main.py` or adjust the shebang.

### Testing

- There is no automated test runner. Validation is manual through sample `.mp` files and `--show-python`.
- The `code_examples/` directory contains 20 `.mp` files covering happy paths and error cases for assignment, type errors, lexer errors, and parser errors.
- There are no unit tests for lexer, parser, semantic analyzer, code generator, or CLI in isolation.
- There is no CI configuration.

## Development Notes

### Smoke tests (should all compile and run)

```powershell
python src\main.py --version
python src\main.py code_examples\hello_world.mp --show-python
python src\main.py code_examples\hello_mapple.mp --show-python
python src\main.py code_examples\assignment_basic.mp --show-python
python src\main.py code_examples\assignment_expr_rhs.mp --show-python
python src\main.py code_examples\assignment_str_reassign.mp --show-python
python src\main.py code_examples\assignment_num_reassign.mp --show-python
python src\main.py code_examples\assignment_multiple.mp --show-python
python src\main.py code_examples\assignment_uom_rhs.mp --show-python
python src\main.py code_examples\assignment_uninit.mp --show-python
```

### Error tests (should all produce a COMPILER ERROR)

```powershell
python src\main.py code_examples\assignment_type_error.mp
python src\main.py code_examples\assignment_type_error_num_to_int.mp
python src\main.py code_examples\assignment_type_error_int_to_str.mp
python src\main.py code_examples\assignment_undeclared.mp
python src\main.py code_examples\assignment_chain_error.mp
python src\main.py code_examples\assignment_invalid_target.mp
python src\main.py code_examples\parser_error_bad_type.mp
python src\main.py code_examples\lexer_error_unterminated_string.mp
python src\main.py code_examples\lexer_error_bad_number.mp
python src\main.py code_examples\lexer_error_unknown_char.mp
```

Running without `--show-python` writes generated files:

```powershell
python src\main.py code_examples\hello_world.mp
```

This creates or overwrites:

```text
code_examples\hello_world_output.py
```

## Development Phases

The next focused work is organized into six implementation phases. This section should be updated whenever a phase is completed so the README continues to reflect the real compiler status.

Status legend:

- `Current` means this is the active focus.
- `Planned` means work has not started or is not complete enough to document as supported.
- `Complete` means the feature works end to end through lexing, parsing, semantic analysis, code generation, examples, and tests or repeatable manual verification.

### Phase 1: Assignment

Status: `Complete`

Goal: make reassignment work as a first-class language feature end-to-end.

Implemented:

- The parser produces real `AssignmentNode` objects (not placeholder strings).
- The semantic analyzer enforces declaration-before-assignment.
- The semantic analyzer enforces assignment type compatibility.
- The code generator emits Python assignment statements.
- The lexer, parser, semantic analyzer, and code generator are all stricter (see [Stricter Validation](#stricter-validation) below).

#### Happy Path Examples

| File | What it tests | Expected output |
|---|---|---|
| [`assignment_basic.mp`](code_examples/assignment_basic.mp) | Reassign an int variable to a literal | `25` |
| [`assignment_expr_rhs.mp`](code_examples/assignment_expr_rhs.mp) | RHS uses the variable in an expression | `21` |
| [`assignment_str_reassign.mp`](code_examples/assignment_str_reassign.mp) | Reassign a str variable | `world` |
| [`assignment_num_reassign.mp`](code_examples/assignment_num_reassign.mp) | Reassign a num variable | `9.81` |
| [`assignment_multiple.mp`](code_examples/assignment_multiple.mp) | Multiple variables each reassigned | `10` then `hello` |
| [`assignment_uom_rhs.mp`](code_examples/assignment_uom_rhs.mp) | UOM type conversion result on RHS | `20` |
| [`assignment_uninit.mp`](code_examples/assignment_uninit.mp) | Assign to a variable declared without initializer | `99` |

Run a happy-path example:

```powershell
python src\main.py code_examples\assignment_basic.mp --show-python
```

Expected generated Python:

```python
age = 20
age = 25
print(str(age))
```

#### Error Examples

Each of these must produce a compiler error — not silently compile or produce wrong output.

**Semantic errors (type and declaration)**

| File | What it tests | Expected error |
|---|---|---|
| [`assignment_type_error.mp`](code_examples/assignment_type_error.mp) | Assign str to int variable | Type Mismatch |
| [`assignment_type_error_num_to_int.mp`](code_examples/assignment_type_error_num_to_int.mp) | Assign num literal to int variable | Type Mismatch |
| [`assignment_type_error_int_to_str.mp`](code_examples/assignment_type_error_int_to_str.mp) | Assign int literal to str variable | Type Mismatch |
| [`assignment_undeclared.mp`](code_examples/assignment_undeclared.mp) | Assign to a name that was never declared | Semantic Error |

**Syntax errors (parser)**

| File | What it tests | Expected error |
|---|---|---|
| [`assignment_chain_error.mp`](code_examples/assignment_chain_error.mp) | Chained assignment `a = b = 5` | Syntax Error |
| [`assignment_invalid_target.mp`](code_examples/assignment_invalid_target.mp) | Literal on left-hand side `5 = 20` | Syntax Error |
| [`parser_error_bad_type.mp`](code_examples/parser_error_bad_type.mp) | Invalid type keyword `let foo x = 5` | Syntax Error |

**Lexer errors**

| File | What it tests | Expected error |
|---|---|---|
| [`lexer_error_unterminated_string.mp`](code_examples/lexer_error_unterminated_string.mp) | String missing closing `"` | Lexer Error |
| [`lexer_error_bad_number.mp`](code_examples/lexer_error_bad_number.mp) | Number with two decimal points `1.2.3` | Lexer Error |
| [`lexer_error_unknown_char.mp`](code_examples/lexer_error_unknown_char.mp) | Unrecognized character `@` | Lexer Error |

#### Stricter Validation

As part of Phase 1 completion, the compiler now enforces stricter rules at every stage:

**Lexer**

- Unterminated string literals raise a dedicated lexer error with the line number.
- Unterminated or multi-character char literals raise a dedicated lexer error.
- Numeric literals with more than one decimal point (e.g. `1.2.3`) raise a dedicated lexer error.
- Any unrecognized character (e.g. `@`, `#`, `!`) raises a lexer error with line and column instead of being silently skipped.

**Parser**

- `let` declarations require an explicit type keyword (`int`, `num`, or `str`). Any other token after `let` raises a syntax error with the line number.

**Semantic Analyzer**

- When a type-mismatch assignment is rejected, the error message includes the expected type and a hint to use the appropriate UOM conversion (e.g. `.int`).
- Binary operations guard against operands whose type could not be resolved, producing a clear error rather than a confusing `None` comparison.
- Literal nodes with unrecognized token types raise an explicit semantic error instead of returning `None` silently.

**Code Generator**

- AST node types without a registered generator raise a `Code Generation Error` instead of being silently skipped. This makes it impossible for a new AST node to be added without also adding its generator.

### Phase 2: Control Flow

Status: `Planned`

Goal: add decision-making and loops.

Expected scope:

- `if`
- `else`
- comparison operators
- boolean expressions
- likely `while` before `for`
- block parsing rules

Current state:

- No control-flow keywords are implemented.
- No comparison operators are tokenized or parsed.
- `bool` appears in semantic conversion planning but is not a complete language type yet.

Completion criteria:

- Define exact syntax for control-flow blocks.
- Implement lexer tokens for required keywords and operators.
- Add AST nodes for conditionals and loops.
- Add semantic checks for boolean conditions.
- Generate valid Python control-flow code with correct indentation.
- Add examples and verification coverage.
- Update this README when control flow is supported.

### Phase 3: Arrays

Status: `Planned`

Goal: add ordered collections.

Expected scope:

- array literal syntax
- typed array declarations
- indexing
- assignment to array elements
- length or count access
- possibly append/remove operations later

Current state:

- No array/list tokenization, parsing, semantic model, or code generation exists.
- There is no generic type syntax yet.

Completion criteria:

- Decide array type syntax.
- Implement array literals and index access.
- Enforce element type consistency.
- Generate Python list-backed output.
- Add examples for declaration, read, write, and invalid type usage.
- Update this README when arrays are supported.

### Phase 4: Functions

Status: `Planned`

Goal: implement user-defined functions end to end.

Current state:

- `func` and `return` are tokenized.
- Function syntax is partially parsed.
- Parameters are skipped.
- Function declarations currently become string placeholders instead of real AST nodes.
- Function code is not generated.
- There is no function scope.
- Function calls are only meaningfully implemented for built-in `input`.

Completion criteria:

- Add real function declaration, parameter, call, and return AST nodes.
- Implement parameter parsing with types.
- Add function symbol table entries.
- Add scoped local variables.
- Validate argument count and argument types.
- Validate return type behavior.
- Generate Python `def` functions.
- Add examples and verification coverage.
- Update this README when functions are supported.

### Phase 5: Modules

Status: `Planned`

Goal: split Mapple programs across files.

Expected scope:

- module/import syntax
- source file resolution
- symbol visibility rules
- duplicate module handling
- generated Python organization

Current state:

- The compiler reads exactly one input source file.
- There is no import syntax.
- There is no module namespace model.
- There is no package or dependency resolution system.

Completion criteria:

- Define module syntax and lookup rules.
- Load multiple `.mp` files safely.
- Prevent circular import failures or report them clearly.
- Add module-level symbol tables.
- Generate executable Python for multi-file programs.
- Add examples covering imports and module boundaries.
- Update this README when modules are supported.

### Phase 6: Classes

Status: `Planned`

Goal: implement user-defined classes after functions and modules are stable.

Current state:

- `class`, `::`, and `;;` are tokenized.
- Class blocks are partially parsed.
- Class declarations currently become string placeholders instead of real AST nodes.
- Class bodies are not semantically modeled.
- No Python class output is generated.

Completion criteria:

- Add real class, field, method, constructor, and member access AST nodes.
- Define object construction syntax.
- Add class symbol tables and instance member lookup.
- Validate field and method access.
- Generate Python classes.
- Add examples and verification coverage.
- Update this README when classes are supported.

### Supporting Work Across All Phases

These items support the six focused phases and should be handled when they become necessary for the active phase:

1. Add automated tests for lexer, parser, semantic analyzer, generator, and CLI behavior.
2. Replace placeholder parser outputs with real AST nodes.
3. Add proper source diagnostics with line and column reporting throughout all compiler phases.
4. ~~Fix conversion table direction~~ — done (BUG-07). Add tests for every allowed and rejected conversion.
5. ~~Decide whether semicolons are mandatory~~ — done (BUG-15). Semicolons are now mandatory on every statement.
6. Implement operator precedence as soon as expressions grow beyond the current simple `+` behavior.
7. Remove emoji from CLI output or explicitly configure UTF-8-safe output.
8. Harden install scripts to avoid PATH duplication and shell-specific assumptions.

## Project Status

Mapple v0.2.0 is best understood as a working educational compiler prototype for a small strict subset:

- variable declarations
- string, integer, and decimal literals
- print
- input
- explicit conversion
- simple `+` expressions
- declaration-before-use checking
- basic Python transpilation and execution

It is not yet a complete general-purpose language. The compiler pipeline is in place, which gives the project a solid base for incremental language work, but many syntax forms exposed by the token set and documentation still need real AST, semantic, and code generation support.
