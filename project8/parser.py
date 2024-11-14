
from command_type import CommandType

class Parser:

    def __init__(self, filename):
        self._code_lines = []
        
        with open(filename) as file:
            for line in file:
                line = line.strip()
                if not line.startswith('//') and len(line) > 0:
                    self._code_lines.append(line)
                    
                #
            #
        #

        self._num_lines = len(self._code_lines)
        self._current_line = 0
        self._set_current_tokens()
    #

    def has_more_lines(self):
        return self._num_lines > 0 and self._current_line < self._num_lines
    #

    def advance(self):
        self._current_line += 1
        self._set_current_tokens()
    #

    def command_type(self):
        return CommandType.COMMAND_TYPE_MAP[self._command_tokens[0]]
    #

    def arg1(self):
        if self.command_type() == CommandType.C_ARITHMETIC:
            return self._command_tokens[0]
        elif (self.command_type() == CommandType.C_PUSH or self.command_type() == CommandType.C_POP or
               self.command_type() == CommandType.C_LABEL or self.command_type() == CommandType.C_IF):
            return self._command_tokens[1]
    
    #

    def arg2(self):
        if self.command_type() == CommandType.C_PUSH or self.command_type() == CommandType.C_POP:
            return self._command_tokens[2]
    #


    def _set_current_tokens(self):
        if self._current_line < self._num_lines:
            self._current_command = self._code_lines[self._current_line]
            self._command_tokens = self._current_command.split(" ")
        #
    #
#