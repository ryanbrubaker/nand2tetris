from command_type import CommandType

from arithmetic_command import ArithmeticCommand
from push_command import PushCommand
from pop_command import PopCommand

class CodeWriter:
    def __init__(self, filename):
        self._output_file = open(filename, "w")
    #


    def write_arithmetic(self, command):
        command_code = ArithmeticCommand(command)
        self._output_file.write(command_code.code)

    #

    def write_push_pop(self, command, segment, index):
        command_code = self._command_factory(command, segment, index)
        self._output_file.write(command_code.code)
    #

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