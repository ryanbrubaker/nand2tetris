POP_VIRTUAL_FRAGMENT = """@{}
D=M
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

POP_TEMP_FRAGMENT = """@{}
D=A
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


POP_POINTER_FRAGMENT = """@SP
AM=M-1
D=M
@{}
M=D
"""

VIRTUAL_KEY_MAP = {
    "local":    "LCL",
    "argument": "ARG",
    "this":     "THIS",
    "that":     "THAT"  
}

STATIC_LOC_MAP = {
    "temp":     5,
    "static":   16
}

POINTER_LOC_MAP = {
    "0":    "THIS",
    "1":    "THAT"
}


class PopCommand:
    
    def __init__(self, segment, index, filename):
        self._code = ""
        if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            self._code = POP_VIRTUAL_FRAGMENT.format(VIRTUAL_KEY_MAP[segment], index)
        elif segment == "temp":
            self._code = POP_TEMP_FRAGMENT.format("R5", index)
        elif segment == "static":
            self._code = POP_POINTER_FRAGMENT.format(filename + "." + index)
        elif segment == "pointer":
            self._code = POP_POINTER_FRAGMENT.format(POINTER_LOC_MAP[index])

        
    @property
    def code(self):
        return self._code
    #
#
