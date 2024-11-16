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

FUNCTION_DECL_FRAGMENT = """({}.{})
@LCL
A=M
"""
FUNCTION_INIT_ARGS_FRAGMENT = """M=0
A=A+1
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



class CodeWriter:
    def __init__(self, filename):
        self._output_file = open(filename, "w")
    #

    def set_filename(self, filename):
        self._filename = filename

    def write_arithmetic(self, command):
        command_code = ArithmeticCommand(command)
        self._output_file.write(command_code.code)

    #

    def write_push_pop(self, command, segment, index):
        command_code = self._command_factory(command, segment, index)
        self._output_file.write(command_code.code)
    #

    def write_label(self, label):
        self._output_file.write(f"({self._filename}.{label})\n")

    def write_if(self, label):
        self._output_file.write(GOTO_IF_FRAGMENT.format(self._filename, label))

    def write_goto(self, label):
        self._output_file.write(GOTO_FRAGMENT.format(self._filename, label))

    def write_function(self, label, num_args):
        self._output_file.write(FUNCTION_DECL_FRAGMENT.format(self._filename, label))
        arg_init_code = FUNCTION_INIT_ARGS_FRAGMENT * int(num_args)
        # remove last address increment
        arg_init_code = arg_init_code[:len(arg_init_code) - 6]
        self._output_file.write(arg_init_code)

    def write_return(self):
        self._output_file.write(SET_RETURN_VALUE_FRAGMENT)
        self._output_file.write(SET_RETURN_STACK_POINTER_FRAGMENT)
        self._output_file.write(RESTORE_CALLEE_STATE_FRAGMENT)

    def close(self):
        self._output_file.write("(END)\n@END\n0;JMP")
        self._output_file.close()
    #

    def _command_factory(self, command, segment, index):
        if command == CommandType.C_PUSH:
            return PushCommand(segment, index)
        elif command == CommandType.C_POP:
            return PopCommand(segment, index)
    #

#