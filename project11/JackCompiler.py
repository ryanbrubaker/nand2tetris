import os
import sys

from compilation_engine import CompilationEngine
from jack_token import JackToken


files_to_process = []
argument = sys.argv[1]
output_path = ""

if os.path.isfile(argument):
    files_to_process.append(argument)
else:
    base_dir = os.path.normpath(argument)
    for file in os.listdir(argument):
        if file.endswith(".jack"):
            files_to_process.append(base_dir + "/" + file)
        #
    #
#

for jack_file in files_to_process:
    input_file = open(jack_file)
    output_file = open(jack_file.replace(".jack", ".xml"), "w")

    compilation_engine = CompilationEngine(input_file, output_file)
    compilation_engine.compile_class()
#
