from command_type import CommandType

from arithmetic_command import ArithmeticCommand
from push_command import PushCommand
from pop_command import PopCommand


GOTO_IF_FRAGMENT = """@SP
AM=M-1
D=M
@{}
D;JNE
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
        self._output_file.write(GOTO_IF_FRAGMENT.format(f"{self._filename}.{label}"))


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