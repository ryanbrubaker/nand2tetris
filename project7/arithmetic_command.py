BINARY_CODE_FRAGMENT = """@SP
A=M-1
D=M
A=A-1
D={}
M=D		
D=A
@SP
M=D+1
"""

NEG_CODE_FRAGMENT = """@SP
A=M-1
M=-M
"""


BINARY_CODE_MAP = {
    "add":  "D+M",
    "sub":  "M-D",
    "and":  "D&M",
    "or":   "D|M"
}


class ArithmeticCommand:
    def __init__(self, command):
        self._code = ""
        if command == "add" or command == "sub" or command == "and" or command == "or":
            self._code = BINARY_CODE_FRAGMENT.format(BINARY_CODE_MAP[command])
        elif command == "neg":
            self._code = NEG_CODE_FRAGMENT
        #

        
    @property
    def code(self):
        return self._code
    #
#