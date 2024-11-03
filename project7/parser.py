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

        self._num_lines = len(self._code_lines) - 1
        self._current_line = -1
    #

    def has_more_lines(self):
        return self._num_lines > 0 and self._current_line < self._num_lines
    #

    def advance(self):
        self._current_line += 1
        self._current_command = self._code_lines[self._current_line]
    #

    def command_type(self):
        return 0
    #

    def arg1(self):
        return self._current_command
    #

    def arg2(self):
        return 0
    #
    
#