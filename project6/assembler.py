from  parser import Parser
from symbol_table import SymbolTable
from code_generator import CodeGenerator

class Assembler:
    def __init__(self):
        self._symbol_table = SymbolTable()
        self._code_generator = CodeGenerator()
    #

    def process(self, filename):
        hack_parser = Parser()
        hack_parser.parse(filename, self._symbol_table)

        with open('./pong/PongL.hack', 'w') as output_file:
            for instruction in hack_parser.instructions:
                output_file.write(instruction.compile(self._symbol_table, self._code_generator) + "\n")


if __name__ == "__main__":
    assemb = Assembler()
    assemb.process("./pong/PongL.asm")
