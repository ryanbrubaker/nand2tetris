import os
import sys

from code_writer import CodeWriter
from parser import Parser

from command_type import CommandType


# Just assume we get a single command-line argument that is the file we need to parse
# and is named correctly with an 
source_file = sys.argv[1]
filepath = sys.argv[1]
base_file = os.path.basename(filepath)
base_file_name = base_file[:base_file.find(".")]

vm_parser = Parser(source_file)
writer = CodeWriter(base_file_name)

while vm_parser.has_more_lines():
    command_type = vm_parser.command_type()
    if command_type == CommandType.C_ARITHMETIC:
        writer.write_arithmetic(vm_parser.arg1())
    elif command_type == CommandType.C_POP or command_type == CommandType.C_PUSH:
        writer.write_push_pop(command_type, vm_parser.arg1(), vm_parser.arg2())
    
    vm_parser.advance()

#

writer.close()
