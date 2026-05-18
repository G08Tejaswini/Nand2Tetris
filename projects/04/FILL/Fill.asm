// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
(MAIN)
    @24576         // keyboard address
    D=M            // D = keyboard value
    @BLACK
    D;JNE          // if key pressed, fill black
    // otherwise fall through to WHITE

(WHITE)
    @16384
    D=A
    @addr
    M=D            // counter = 16384
    
(WLOOP)
    @addr
    D=M
    @24576
    D=D-A
    @MAIN
    D;JEQ          // if counter = 24576, done
    
    @addr
    A=M            // go to screen[counter]
    M=0            // write white
    @addr
    M=M+1          // counter++
    @WLOOP
    0;JMP


(BLACK)
    @16384
    D=A
    @addr
    M=D            // counter = 16384
    
(BLOOP)
    @addr
    D=M
    @24576
    D=D-A
    @MAIN
    D;JEQ          // if counter = 24576, done
    
    @addr
    A=M            // go to screen[counter]
    M=-1            // write black
    @addr
    M=M+1          // counter++
    @BLOOP
    0;JMP
    
    @MAIN
    0;JMP          // go back to keyboard check