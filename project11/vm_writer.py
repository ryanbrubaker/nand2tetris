import segments as SEGMENTS
class VMWriter:


    SEGMENT_MAP = {
        SEGMENTS.CONSTANT:   "constant",
        SEGMENTS.ARGUMENT:   "argument",
        SEGMENTS.LOCAL:      "local",
        SEGMENTS.STATIC:     "static",
        SEGMENTS.THIS:       "this",
        SEGMENTS.THAT:       "that",
        SEGMENTS.POINTER:    "pointer",
        SEGMENTS.TEMP:       "temp"
    }


    ADD = 0
    SUB = 1
    EQ = 2
    GT = 3
    LT = 4
    AND = 5
    OR = 6
    NEG = 7
    NOT = 8


    OPERATOR_COMMANDS = {
        ADD:    "add",
        SUB:    "sub",
        EQ:     "eq",
        GT:     "gt",
        LT:     "lt",
        AND:    "and",
        OR:     "or",
        NEG:    "neg",
        NOT:    "not",
    }

    def __init__(self, output_file):
        self._output_file = output_file


    def write_push(self, segment, index):
        push_segment = VMWriter.SEGMENT_MAP[segment]
        self._output_file.write(f"push {push_segment} {index}\n")

    def write_pop(self, segment, index):
        push_segment = VMWriter.SEGMENT_MAP[segment]
        self._output_file.write(f"pop {push_segment} {index}\n")


    def write_arithmetic(self, command):
        self._output_file.write(VMWriter.OPERATOR_COMMANDS[command] + "\n")


    def write_label(self, label):
        self._output_file.write(f"label {label}\n")
        

    def write_goto(self, label):
        self._output_file.write(f"goto {label}\n")

    def write_if(self, label):
        self._output_file.write("not\n")
        self._output_file.write(f"if-goto {label}\n")

    def write_call(self, function_name, num_args):
        self._output_file.write(f"call {function_name} {num_args}\n")

    def write_function(self, function_name, num_vars):
        self._output_file.write(f"function {function_name} {num_vars}\n")

    def write_return(self):
        self._output_file.write("return\n")

