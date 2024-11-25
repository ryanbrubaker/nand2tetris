
GOTO_IF_FRAGMENT = """@SP
AM=M-1
D=M
@{}.{}
D;JNE
"""


GOTO_FRAGMENT = """@{}.{}
0;JMP
"""



FUNCTION_DECL_FRAGMENT = """({})
@LCL
A=M
"""
FUNCTION_INIT_LOCALS_FRAGMENT = """M=0
A=A+1
"""

SET_SP_PAST_LOCALS_FRAGMENT = """D=A
@SP
M=D
"""



STORE_RET_ADDR_FRAGMENT = """@5
D=A
@LCL
A=M-D
D=M
@R14
M=D
"""
SET_RETURN_VALUE_FRAGMENT = """@SP
A=M-1
D=M
@ARG
A=M
M=D
"""
# Address is already set to @ARG from SET_RETURN_VALUE_FRAGMENT
SET_RETURN_STACK_POINTER_FRAGMENT = """A=A+1
D=A
@SP
M=D
"""

RESTORE_CALLEE_STATE_FRAGMENT = """@LCL
AM=M-1
D=M
@THAT
M=D
@LCL
AM=M-1
D=M
@THIS
M=D
@LCL
AM=M-1
D=M
@ARG
M=D
@LCL
AM=M-1
D=M
@LCL
M=D
"""


PUSH_GENERATED_ADDR_TO_STACK_FRAGMENT = """@{}
D=A
@SP
A=M
M=D
@SP
M=M+1
"""


STORE_CALLEE_STATE_FRAGMENT = """@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
"""

SET_ARG_ADDR_FRAGMENT = """@{}
D=A
@SP
A=M-D
D=A
@ARG
M=D
"""

SET_LCL_FRAGMENT = """@SP
D=M
@LCL
M=D
"""

CALL_FUNCTION_FRAGMENT = """@{}
0;JMP
"""

RETURN_LABEL_FRAGMENT = """({})
"""



JUMP_TO_RET_ADDR_FRAGMENT = """@R14
A=M
0;JMP
"""

### This module is implemented as just class methods to isolate all
### the control code fragments in this module.
class ControlCommand:

    RETURN_CALL_COUNT = 0


    @classmethod
    def write_label(cls, output_file, filename, label):
        output_file.write(f"({filename}.{label})\n")
    #


    @classmethod
    def write_if(cls, output_file, filename, label):
        output_file.write(GOTO_IF_FRAGMENT.format(filename, label))
    #


    @classmethod
    def write_goto(cls, output_file, filename, label):
        output_file.write(GOTO_FRAGMENT.format(filename, label))
    #


    @classmethod
    def write_function(cls, output_file, label, num_locals):
        output_file.write(FUNCTION_DECL_FRAGMENT.format(label))
        locals_init_code = FUNCTION_INIT_LOCALS_FRAGMENT * int(num_locals)
        output_file.write(locals_init_code)
        output_file.write(SET_SP_PAST_LOCALS_FRAGMENT)
    #

    
    @classmethod
    def write_call(cls, output_file, filename, function, num_args):
        count_str = str(ControlCommand.RETURN_CALL_COUNT)
        generated_label = filename + ".RETURN_" + count_str
        ControlCommand.RETURN_CALL_COUNT += 1

        output_file.write(PUSH_GENERATED_ADDR_TO_STACK_FRAGMENT.format(generated_label))
        output_file.write(STORE_CALLEE_STATE_FRAGMENT)
        output_file.write(SET_ARG_ADDR_FRAGMENT.format(5 + int(num_args)))
        output_file.write(SET_LCL_FRAGMENT)
        output_file.write(CALL_FUNCTION_FRAGMENT.format(function))
        output_file.write(RETURN_LABEL_FRAGMENT.format(generated_label))


    @classmethod
    def write_return(cls, output_file):
        output_file.write(STORE_RET_ADDR_FRAGMENT)
        output_file.write(SET_RETURN_VALUE_FRAGMENT)
        output_file.write(SET_RETURN_STACK_POINTER_FRAGMENT)
        output_file.write(RESTORE_CALLEE_STATE_FRAGMENT)
        output_file.write(JUMP_TO_RET_ADDR_FRAGMENT)