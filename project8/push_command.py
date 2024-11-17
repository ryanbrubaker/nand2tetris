PUSH_CONSTANT_FRAGMENT ="""@{}
D=A
@SP
A=M
M=D
@SP
M=M+1
"""

PUSH_VIRTUAL_FRAGMENT = """@{}
D=M
@{}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
"""

PUSH_TEMP_FRAGMENT = """@{}
D=A
@{}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
"""


PUSH_POINTER_FRAGMENT = """@{}
D=M
@SP
A=M
M=D
@SP
M=M+1
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

class PushCommand:
    
    def __init__(self, segment, index, filename):
        self._code = ""
        if segment == "constant":
            self._code = PUSH_CONSTANT_FRAGMENT.format(index)
        elif segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            self._code = PUSH_VIRTUAL_FRAGMENT.format(VIRTUAL_KEY_MAP[segment], index)
        elif segment == "temp":
            self._code = PUSH_TEMP_FRAGMENT.format("R5", index) 
        elif segment == "static":
            self._code = PUSH_POINTER_FRAGMENT.format(filename + "." + index)
        elif segment == "pointer":
            self._code = PUSH_POINTER_FRAGMENT.format(POINTER_LOC_MAP[index])

        
    @property
    def code(self):
        return self._code
    #
#
