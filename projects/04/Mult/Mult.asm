// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.
@R2           // "Go to RAM address 2"
M=0           // "Set that value to 0"  (initialize the sum)

(LOOP)        // "This spot is called LOOP"

@R1           // "Go to RAM address 1"
D=M           // "Put whatever's in R1 into D"  (D = counter)

@END          // "Remember where END is"
D;JLE         // "If D ≤ 0, go to END"  (exit loop if counter done)

@R0           // "Go to RAM address 0"
D=M           // "Put R0's value into D"  (D = the number to add)

@R2           // "Go to the sum (R2)"
M=D+M         // "Add D to the sum and store it"

@R1           // "Go to R1"
M=M-1         // "Decrease counter by 1"

@LOOP         // "Remember where LOOP is"
0;JMP         // "Jump to LOOP no matter what"

(END)         // "This spot is called END"
@END          // "Stay here forever"
0;JMP         //  (program finished)