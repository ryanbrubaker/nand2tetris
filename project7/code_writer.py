class CodeWriter:

    def __init__(self, filename):
        self._output_file = open(filename + ".asm", "w")
    #


    def write_arithmetic(self, command):
        self._output_file.write(command + "\n")
    #

    def write_push_pop(self, command):
        pass
    #

    def close(self):
        self._output_file.close()
    #


#