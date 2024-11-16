import os
import sys

from code_writer import CodeWriter
from parser import Parser

from command_type import CommandType


# Just assume we get a single command-line argument that is the file we need to parse
# and is named correctly with an

if os.path.isfile(sys.argv[1]):
    source_path = sys.argv[1]
    output_path = source_path.replace(".vm", ".asm")

    filename = os.path.basename(source_path)
    filename_no_ext = filename[:filename.index(".")]

    vm_parser = Parser(source_path)
    writer = CodeWriter(output_path)
    writer.set_filename(filename_no_ext)

    while vm_parser.has_more_lines():
        command_type = vm_parser.command_type()
        if command_type == CommandType.C_ARITHMETIC:
            writer.write_arithmetic(vm_parser.arg1())
        elif command_type == CommandType.C_POP or command_type == CommandType.C_PUSH:
            writer.write_push_pop(command_type, vm_parser.arg1(), vm_parser.arg2())
        elif command_type == CommandType.C_LABEL:
            writer.write_label(vm_parser.arg1())
        elif command_type == CommandType.C_IF:
            writer.write_if(vm_parser.arg1())
        elif command_type == CommandType.C_GOTO:
            writer.write_goto(vm_parser.arg1())
        elif command_type == CommandType.C_FUNCTION:
            writer.write_function(vm_parser.arg1(), vm_parser.arg2())
        elif command_type == CommandType.C_RETURN:
            writer.write_return()

        
        vm_parser.advance()

    #

    writer.close()
else:
    print("directory")