
// Initialize accumulator variable
@sum
M=0

// Initialize counter variable
@i
M=0

(LOOP)

// Check loop condition and terminate if i = @R0
@i
D=M
@R0
D=D-M
@STOP
D;JEQ

// Otherwise add R1 to sum
@R1
D=M
@sum
M=D+M

// And increment counter
@i
M=M+1
@LOOP
0;JMP

(STOP)
@sum
D=M
@R2
M=D

(END)
@END
0;JMP