# Nand2Tetris

Building a modern computer from first principles — from NAND gates to an operating system.

This repository contains my completed projects from the [Nand2Tetris](https://www.nand2tetris.org/) course (*The Elements of Computing Systems* by Nisan & Schocken).

---

## What Is This?

Nand2Tetris takes you through building a complete computer system, layer by layer:

1. **Hardware** — Logic gates → ALU → RAM → CPU → Computer
2. **Software** — Assembler → VM Translator → Compiler → Operating System

The end result? A working computer that can run Tetris — all built from scratch.

---

## Projects

| # | Project | Description | Status |
|---|---------|-------------|--------|
| 01 | Boolean Logic | 15 logic gates built from NAND | ✅ |
| 02 | Boolean Arithmetic | Half-Adder, Full-Adder, ALU | ✅ |
| 03 | Sequential Logic | Registers, RAM, Program Counter | ✅ |
| 04 | Machine Language | Mult.asm, Fill.asm in Hack Assembly | ✅ |
| 05 | Computer Architecture | CPU, Memory, Computer chips | ✅ |
| 06 | Assembler | Hack Assembler written in Python | ✅ |
| 07 | VM Translator (Part I) | Stack arithmetic translator | 🚧 |
| 08 | VM Translator (Part II) | Program flow & function calls	 | ⬜ |
| 09|  High-Level Language | Write a game in Jack (Tetris!) | ⬜ |
| 10 | Compiler I | Jack compiler — syntax analysis | ⬜ |
| 11 | Compiler II | Jack compiler — code generation | ⬜ |
| 12 | Operating System | OS + run Tetris on YOUR computer | ⬜ |


---

## Tools Used

- **Hardware Simulator** — For testing .hdl chip designs
- **CPU Emulator** — For running Hack assembly programs
- **VM Emulator** — For testing VM code
- **Python** — For the Assembler and VM Translator

---

## How to Use

Each project folder contains:
- `.hdl` files (hardware designs)
- `.asm` files (assembly programs)
- `.py` files (assembler/translator)

To test a hardware chip:
1. Open the Nand2Tetris Hardware Simulator
2. Load the `.hdl` file
3. Run the corresponding `.tst` script

To run the assembler:
```bash
python projects/06/assembler.py projects/06/add/Add.asm


What I Learned

How transistors form logic gates, gates form chips, chips form a CPU

The Hack machine language and assembly programming

How compilers translate high-level code to machine code


Acknowledgements
Built while following the incredible Nand2Tetris course. If you're curious about how computers really work, I can't recommend it enough.




