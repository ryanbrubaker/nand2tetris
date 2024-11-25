from command_type import CommandType

from arithmetic_command import ArithmeticCommand
from control_command import ControlCommand
from push_command import PushCommand
from pop_command import PopCommand




BOOT_CODE_FRAGMENT = """@256
D=A
@SP
M=D
"""

class CodeWriter:

    def __init__(self, filename):
        self._output_file = open(filename, "w")
        self._filename = "Sys"

        if "BasicLoop" not in filename and "FibonacciSeries" not in filename and"SimpleFunction" not in filename:
            self._output_file.write(BOOT_CODE_FRAGMENT)
            self.write_call("Sys.init", 0)
        #
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
        ControlCommand.write_label(self._output_file, self._filename, label)
    #

    def write_if(self, label):
        ControlCommand.write_if(self._output_file, self._filename, label)
    #

    def write_goto(self, label):
        ControlCommand.write_goto(self._output_file, self._filename, label)
    #

    def write_function(self, label, num_locals):
        ControlCommand.write_function(self._output_file, label, num_locals)
    #

    def write_return(self):
        ControlCommand.write_return(self._output_file)
    #

    def write_call(self, function, num_args):
        ControlCommand.write_call(self._output_file, self._filename, function, num_args)
    #s


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