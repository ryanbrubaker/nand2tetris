import os
import sys

from code_writer import CodeWriter
from parser import Parser

from command_type import CommandType


# Just assume we get a single command-line argument that is the file we need to parse
# and is named correctly with an


files_to_process = []
argument = sys.argv[1]
output_path = ""

if os.path.isfile(argument):
    files_to_process.append(argument)
    output_path = argument.replace(".vm", ".asm")
else:
    base_dir = os.path.normpath(argument)
    for file in os.listdir(argument):
        if file.endswith(".vm"):
            files_to_process.append(base_dir + "/" + file)
    output_path = base_dir + "/" + os.path.basename(base_dir) + ".asm"


writer = CodeWriter(output_path)    
for file in files_to_process:

    vm_parser = Parser(file)

    filename = os.path.basename(file)
    filename_no_ext = filename[:filename.index(".")]
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
        elif command_type == CommandType.C_CALL:
            writer.write_call(vm_parser.arg1(), vm_parser.arg2())
       
        vm_parser.advance()
    #
#

writer.close()
