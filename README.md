# 🍎 Mapple (MPPL) v0.1
**A beginner-friendly, strictly-typed compiled language.**

Mapple is designed to teach programming fundamentals by enforcing good habits (like mandatory variable declarations and no implicit type conversions) while keeping a clean, Python-inspired syntax.

## 🚀 Quick Start (Installation)
1. **Download**: Clone this repository to your computer.
## 📋 Requirements
- **Python 3.10 or higher**: Must be installed and added to your system PATH.

### Windows
1. **Set PATH**: 
   - Copy the full path to this `MPPL` folder.
   - Add it to your System **Environment Variables (PATH)**.

### macOS / Linux
1. Open terminal in the `MPPL` folder.
2. Run `chmod +x mppl`.
3. Add the folder to your path in `.zshrc` or `.bashrc`.
4. Run `./mppl script.mp`.

3. **Verify**: Open a new terminal and type `mppl`.

## ✍️ Your First Script (`hello.mp`)
Create a file named `hello.mp`:
```mapple
let str name = input("What is your name? ").str;
print("Hello " + name);
```

4. **Run `mppl script.mp`.** 
_________________________________________________________________________________________