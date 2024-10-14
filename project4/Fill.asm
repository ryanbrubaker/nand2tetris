
@fillBit
M=0

// Infinite loop to see if key is prssed
(MAINLOOP)
@KBD
D=M

@PRESSED
D;JNE

// No key pressed, set fillBit to 0 and call FILLSCREEN
@fillBit
M=0
@FILLSCREEN
0;JMP


// Key pressed, set fillBit to 1 and call FILLSCREEN
(PRESSED)
@fillBit
M=-1
@FILLSCREEN
0;JMP

(FILLSCREEN)
@8192
D=A
@numBlocks
M=D

// Initialize counter
@i
M=0

@SCREEN
D=A
@currentWord
M=D


(FILLLOOP)
@i
D=M
@numBlocks
D=D-M
@MAINLOOP
D;JEQ

// Fill screen with fillBit
@fillBit
D=M
@currentWord
A=M
M=D

// Advance i and currentWord
@i
M=M+1
@currentWord
M=M+1
@FILLLOOP
0;JMP

