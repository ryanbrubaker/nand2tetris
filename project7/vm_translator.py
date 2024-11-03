import os
import sys

from code_writer import CodeWriter
from parser import Parser


# Just assume we get a single command-line argument that is the file we need to parse
# and is named correctly with an 
source_file = sys.argv[1]
filepath = sys.argv[1]
base_file = os.path.basename(filepath)
base_file_name = base_file[:base_file.find(".")]

vm_parser = Parser(source_file)
writer = CodeWriter(base_file_name)

while vm_parser.has_more_lines():
    vm_parser.advance()
    command = vm_parser.arg1()
    writer.write_arithmetic(command)
#

writer.close()
