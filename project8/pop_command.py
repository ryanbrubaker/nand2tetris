POP_VIRTUAL_FRAGMENT = """@{}
D={}
@{}
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
"""

POP_DIRECT_FRAGMENT = """@SP
AM=M-1
D=M
@{}
M=D
"""

VIRTUAL_KEY_MAP = {
    "local":    "LCL",
    "argument": "ARG",
    "this":     "THIS",
    "that":     "THAT",
    "temp":     "R5"
}


POINTER_LOC_MAP = {
    "0":    "THIS",
    "1":    "THAT"
}


class PopCommand:
    
    def __init__(self, segment, index, filename):
        self._code = ""
        if segment == "local" or segment == "argument" or segment == "this" or segment == "that" or segment == "temp":
            A_or_M = "A" if segment == "temp" else "M"
            self._code = POP_VIRTUAL_FRAGMENT.format(VIRTUAL_KEY_MAP[segment], A_or_M, index)
        elif segment == "static":
            self._code = POP_DIRECT_FRAGMENT.format(filename + "." + index)
        elif segment == "pointer":
            self._code = POP_DIRECT_FRAGMENT.format(POINTER_LOC_MAP[index])

        
    @property
    def code(self):
        return self._code
    #
#
