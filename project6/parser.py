from ainstruction import AInstruction
from cinstruction import CInstruction


class Parser:
    def __init__(self):
        self._instructions = []
    #
    
    def parse(self, filename, symbol_table):

        # First pass through to get labels and cache lines of code
        code_lines = []
        with open(filename) as file:
            line_num = 0
            for line in file:
                line = line.strip()

                if line.startswith('('):
                    symbol_table.add_label(line.replace('(', '').replace(')', ''), line_num)
                elif not line.startswith('//') and len(line) > 0:
                    code_lines.append(line)
                    line_num += 1
                #
            #
        #

        # Second pass through to parse code
        for line in code_lines:
            if line.startswith('@'):
                if not line[1:].isnumeric():
                    symbol_table.add_variable(line[1:])
                self._instructions.append(AInstruction(line[1:]))
                line_num += 1
            else:
                if len(line) > 0:
                    self._instructions.append(CInstruction(line))
                    line_num += 1
            #
        #
    #

    @property
    def instructions(self):
        return self._instructions
#