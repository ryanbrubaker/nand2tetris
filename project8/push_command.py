PUSH_CONSTANT_FRAGMENT ="""@{}
D=A
@SP
A=M
M=D
@SP
M=M+1
"""

PUSH_VIRTUAL_FRAGMENT = """@{}
D={}
@{}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
"""

# PUSH_TEMP_FRAGMENT = """@{}
# D=A
# @{}
# A=D+A
# D=M
# @SP
# A=M
# M=D
# @SP
# M=M+1
# """


PUSH_DIRECT_FRAGMENT = """@{}
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
    "that":     "THAT",
    "temp":     "R5"
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
        elif segment == "local" or segment == "argument" or segment == "this" or segment == "that" or segment == "temp":
            A_or_M = "A" if segment == "temp" else "M"
            self._code = PUSH_VIRTUAL_FRAGMENT.format(VIRTUAL_KEY_MAP[segment], A_or_M, index)
        elif segment == "static":
            self._code = PUSH_DIRECT_FRAGMENT.format(filename + "." + index)
        elif segment == "pointer":
            self._code = PUSH_DIRECT_FRAGMENT.format(POINTER_LOC_MAP[index])

        
    @property
    def code(self):
        return self._code
    #
#
