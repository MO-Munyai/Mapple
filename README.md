# 🍎 Mapple (MPPL) v0.1
**A beginner-friendly, strictly-typed compiled language.**

Mapple is designed to teach programming fundamentals by enforcing good habits (like mandatory variable declarations and no implicit type conversions) while keeping a clean, Python-inspired syntax.

## 🚀 Quick Start (Installation)
1. **Download**: Clone this repository to your computer.
2. **Set PATH**: 
   - Copy the full path to this `MPPL` folder.
   - Add it to your System **Environment Variables (PATH)**.
3. **Verify**: Open a new terminal and type `mppl`.

## ✍️ Your First Script (`hello.mp`)
Create a file named `hello.mp`:
```mapple
let str name = input("What is your name? ").str;
print("Hello " + name);