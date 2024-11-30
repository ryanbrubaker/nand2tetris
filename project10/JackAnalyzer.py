import os
import sys

from jack_token import JackToken
from jack_tokenizer import JackTokenizer


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
    output_file.write("<tokens>\n")


    tokenizer = JackTokenizer(input_file)
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        if tokenizer.token_type() == JackToken.IDENTIFIER:
            output_file.write(f"<identifier> {tokenizer.identifier()} </identifier>\n")
        elif tokenizer.token_type() == JackToken.KEYWORD:
            output_file.write(f"<keyword> {tokenizer.keyword()} </keyword>\n")
        elif tokenizer.token_type() == JackToken.SYMBOL:
            output_file.write(f"<symbol> {tokenizer.symbol()} </symbol>\n")
        elif tokenizer.token_type() == JackToken.INT_CONST:
            output_file.write(f"<integerConstant> {tokenizer.int_val()} </integerConstant>\n")
        elif tokenizer.token_type() == JackToken.STRING_CONST:
            output_file.write(f"<stringConstant> {tokenizer.string_val()} </stringConstant>\n")


    output_file.write("</tokens>")
    output_file.close()
#
