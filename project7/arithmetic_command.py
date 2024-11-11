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

LOGIC_CODE_FRAGMENT = """@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@{}
D;{}
@SP
A=M
M=0
@SP
M=M+1
@{}
0;JMP
{}
@SP
A=M
M=-1
@SP
M=M+1
{}
"""

NEG_CODE_FRAGMENT = """@SP
A=M-1
M=-M
"""

NOT_CODE_FRAGMENT = """@SP
A=M-1
M=!M
"""


BINARY_CODE_MAP = {
    "add":  "D+M",
    "sub":  "M-D",
    "and":  "D&M",
    "or":   "D|M"
}

LOGIC_CODE_MAP = {
    "eq":   "JEQ",
    "gt":   "JGT",
    "lt":   "JLT"
}



class ArithmeticCommand:
    LOGIC_COUNT = 0

    def __init__(self, command):
        self._code = ""
        if command == "add" or command == "sub" or command == "and" or command == "or":
            self._code = BINARY_CODE_FRAGMENT.format(BINARY_CODE_MAP[command])
        elif command == "neg":
            self._code = NEG_CODE_FRAGMENT
        elif command == "not":
            self._code = NOT_CODE_FRAGMENT
        elif command == "eq" or command == "gt" or command == "lt":
            count_str = str(ArithmeticCommand.LOGIC_COUNT)
            self._code = LOGIC_CODE_FRAGMENT.format(
                "TRUE_COND" + count_str,
                LOGIC_CODE_MAP[command],
                "END_COND" + count_str,
                "(TRUE_COND" + count_str + ")",
                "(END_COND" + count_str + ")"
            )
            ArithmeticCommand.LOGIC_COUNT += 1
        #

        
    @property
    def code(self):
        return self._code
    #
#