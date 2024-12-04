
class VMWriter:

    CONSTANT = 0
    ARGUMENT = 1
    LOCAL = 2
    STATIC = 3
    THIS = 4
    THAT = 5
    POINTER = 6
    TEMP = 7

    SEGMENT_MAP = {
        CONSTANT:   "constant",
        ARGUMENT:   "argument",
        LOCAL:      "static",
        STATIC:     "static",
        THIS:       "this",
        THAT:       "that",
        POINTER:    "pointer",
        TEMP:       "temp"
    }


    ADD = 0
    
    OPERATOR_COMMANDS = {
        ADD:    "add"
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


    def write_label(self):
        pass

    def write_goto(self):
        pass

    def write_if(self):
        pass

    def write_call(self, function_name, num_args):
        self._output_file.write(f"call {function_name} {num_args}\n")

    def write_function(self, function_name, num_vars):
        self._output_file.write(f"function {function_name} {num_vars}\n")

    def write_return(self):
        self._output_file.write("return\n")

