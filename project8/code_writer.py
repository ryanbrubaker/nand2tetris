from command_type import CommandType

from arithmetic_command import ArithmeticCommand
from push_command import PushCommand
from pop_command import PopCommand


GOTO_IF_FRAGMENT = """@SP
AM=M-1
D=M
@{}.{}
D;JNE
"""

GOTO_FRAGMENT = """@{}.{}
0;JMP
"""

#FUNCTION_DECL_FRAGMENT = """({}.{})
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





################################################################


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

JUMP_TO_RET_ADDR_FRAGMENT = """@R14
A=M
0;JMP
"""


########################################################################

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


BOOT_CODE_FRAGMENT = """@256
D=A
@SP
M=D
"""

class CodeWriter:
    RETURN_CALL_COUNT = 0

    def __init__(self, filename):
        self._output_file = open(filename, "w")
        self._filename = ""

        self._output_file.write(BOOT_CODE_FRAGMENT)
        self.write_call("Sys.init", 0)
    #

    def set_filename(self, filename):
        self._filename = filename

    def write_arithmetic(self, command):
        command_code = ArithmeticCommand(command)
        self._output_file.write(command_code.code)

    #

    def write_push_pop(self, command, segment, index):
        command_code = self._command_factory(command, segment, index, self._filename)
        self._output_file.write(command_code.code)
    #

    def write_label(self, label):
        self._output_file.write(f"({self._filename}.{label})\n")

    def write_if(self, label):
        self._output_file.write(GOTO_IF_FRAGMENT.format(self._filename, label))

    def write_goto(self, label):
        self._output_file.write(GOTO_FRAGMENT.format(self._filename, label))

    def write_function(self, label, num_locals):
        self._output_file.write(FUNCTION_DECL_FRAGMENT.format(label))
        locals_init_code = FUNCTION_INIT_LOCALS_FRAGMENT * int(num_locals)
        self._output_file.write(locals_init_code)
        self._output_file.write(SET_SP_PAST_LOCALS_FRAGMENT)

    def write_return(self):
        self._output_file.write(STORE_RET_ADDR_FRAGMENT)
        self._output_file.write(SET_RETURN_VALUE_FRAGMENT)
        self._output_file.write(SET_RETURN_STACK_POINTER_FRAGMENT)
        self._output_file.write(RESTORE_CALLEE_STATE_FRAGMENT)
        self._output_file.write(JUMP_TO_RET_ADDR_FRAGMENT)

    def write_call(self, function, num_args):
        count_str = str(CodeWriter.RETURN_CALL_COUNT)
        generated_label = self._filename + ".RETURN_" + count_str
        CodeWriter.RETURN_CALL_COUNT += 1

        self._output_file.write(PUSH_GENERATED_ADDR_TO_STACK_FRAGMENT.format(generated_label))
        self._output_file.write(STORE_CALLEE_STATE_FRAGMENT)
        self._output_file.write(SET_ARG_ADDR_FRAGMENT.format(5 + int(num_args)))
        self._output_file.write(SET_LCL_FRAGMENT)
        self._output_file.write(CALL_FUNCTION_FRAGMENT.format(function))
        self._output_file.write(RETURN_LABEL_FRAGMENT.format(generated_label))


    def close(self):
        self._output_file.write("(END)\n@END\n0;JMP")
        self._output_file.close()
    #

    def _command_factory(self, command, segment, index, filename):
        if command == CommandType.C_PUSH:
            return PushCommand(segment, index, filename)
        elif command == CommandType.C_POP:
            return PopCommand(segment, index, filename)
    #

#