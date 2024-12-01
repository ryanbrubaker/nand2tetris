
from jack_token import JackToken
from jack_tokenizer import JackTokenizer


class CompilationEngine:

    def __init__(self, input_file, output_file):
        self._input_file = input_file
        self._output_file = output_file

        self._tokenizer = JackTokenizer(input_file)
    #


    def compile_class(self):
        
        self._output_file.write("<class>\n")
        self.__get_next_token()

        self.__consume_expected_keyword(JackToken.CLASS)        
        self.__consume_expected_token(JackToken.IDENTIFIER)
        self.__consume_expected_symbol("{")
        
        self.compile_class_var_dec()
        self.compile_subroutine()
        
        while self._tokenizer.has_more_tokens():
            self._tokenizer.advance()
        #

        self.__consume_expected_symbol("}")
        self._output_file.write("</class>\n")

        if self._tokenizer.has_more_tokens():
            raise Exception("Expected end of input")
    #




    def compile_class_var_dec(self):

        while (self._tokenizer.token_type() == JackToken.KEYWORD and 
                    (self._tokenizer.keyword() == JackToken.STATIC or self._tokenizer.keyword() == JackToken.FIELD)):
            
            self._output_file.write("<classVarDec>\n")
            self.__consume_current_token();
        
            if self.__is_language_type():
                self.__consume_current_token()
            else:
                raise Exception("Unexpected token")
    
            self.__consume_expected_token(JackToken.IDENTIFIER)
            self.__compile_compound_var_decs()
            self.__consume_expected_symbol(";")
            self._output_file.write("</classVarDec>\n")
        #
    #


    def compile_subroutine(self):

        while (self._tokenizer.token_type() == JackToken.KEYWORD and
                    (self._tokenizer.keyword() == JackToken.CONSTRUCTOR or self._tokenizer.keyword() == JackToken.FUNCTION or
                        self._tokenizer.keyword() == JackToken.METHOD)):
            self._output_file.write("<subroutineDec>\n")
            self.__consume_current_token()
            
            if (self.__is_language_type() or 
                    (self._tokenizer.token_type() == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.VOID)):
                self.__consume_current_token()
            else:
                raise Exception("Unexpected token")

            self.__consume_expected_token(JackToken.IDENTIFIER)

            self.__consume_expected_symbol("(")
            self.compile_parameter_list()
            self.__consume_expected_symbol(")")

            self.compile_subroutine_body()
            self._output_file.write("</subroutineDec>\n")
        #
    #


    def compile_parameter_list(self):
        self._output_file.write("<parameterList>\n")
        if self.__is_language_type():
            self.__consume_current_token()
            self.__consume_expected_token(JackToken.IDENTIFIER)
            self.__compile_compound_param_list()
        #
        self._output_file.write("</parameterList>\n")
    #


    def compile_subroutine_body(self):
        self._output_file.write("<subroutineBody>\n")
        
        self.__consume_expected_symbol("{")
        self.compile_var_dec()
        self.compile_statements()
        self.__consume_expected_symbol("}")

        self._output_file.write("</subroutineBody>\n")
    #


    def compile_var_dec(self):

        while self._tokenizer.token_type() == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.VAR:
            self._output_file.write("<varDec>\n")
       
            self.__consume_expected_keyword(JackToken.VAR)

            if self.__is_language_type():
                self.__consume_current_token()
            else:
                raise Exception("Unexpected token")
            
            self.__consume_expected_token(JackToken.IDENTIFIER)
            self.__compile_compound_var_decs()
            self.__consume_expected_symbol(";")
            
            self._output_file.write("</varDec>\n")
        #
    #



    def compile_statements(self):
        self._output_file.write("<statements>\n")

        while self._tokenizer.token_type() == JackToken.KEYWORD:
            if self._tokenizer.keyword() == JackToken.LET:
                self.compile_let()
            elif self._tokenizer.keyword() == JackToken.IF:
                self.compile_if()
            elif self._tokenizer.keyword() == JackToken.WHILE:
                self.compile_while()
            elif self._tokenizer.keyword() == JackToken.DO:
                self.compile_do()
            elif self._tokenizer.keyword() == JackToken.RETURN:
                self.compile_return()
            else:
                raise Exception("Unexpected token")
            #
        #
        self._output_file.write("</statements>\n")
    #            

    def compile_let(self):
        self._output_file.write("<letStatement>\n")
        self.__consume_current_token()
        self.__consume_expected_token(JackToken.IDENTIFIER)
        self.__consume_expected_symbol("=")
        self.compile_expression()
        self.__consume_expected_symbol(";")
        self._output_file.write("</letStatement>\n")

    #

    def compile_if(self):
        self._output_file.write("<ifStatement>\n")
        self.__consume_current_token()
        self.__consume_expected_symbol("(")
        self.compile_expression()
        self.__consume_expected_symbol(")")
        self.__consume_expected_symbol("{")
        self.compile_statements()
        self.__consume_expected_symbol("}")

        if self._tokenizer.token_type() == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.ELSE:
            self.__consume_current_token()
            self.__consume_expected_symbol("{")
            self.compile_statements()
            self.__consume_expected_symbol("}")
        #
        self._output_file.write("</ifStatement>\n")
    #


    def compile_while(self):
        self._output_file.write("<whileStatement>\n")
        self.__consume_current_token()
        self.__consume_expected_symbol("(")
        self.compile_expression()
        self.__consume_expected_symbol(")")
        self.__consume_expected_symbol("{")
        self.compile_statements()
        self.__consume_expected_symbol("}")
        self._output_file.write("</whileStatement>\n")
    #


    def compile_do(self):
        self._output_file.write("<doStatement>\n")
        self.__consume_current_token()
        self.__consume_expected_token(JackToken.IDENTIFIER)

        if self._tokenizer.token_type() == JackToken.SYMBOL:
            if self._tokenizer.symbol() == ".":
                self.__consume_current_token()
                self.__consume_expected_token(JackToken.IDENTIFIER)
                self.__consume_expected_symbol("(")
                self.compile_expression_list()
                self.__consume_expected_symbol(")")
            elif self._tokenizer.symbol() == "(":
                self.__consume_current_token()
                self.compile_expression_list()
                self.__consume_expected_symbol(")")
            else:
                raise Exception("Unexpected token")
        else:
            raise Exception("Unexpected token")
        
        self.__consume_expected_symbol(";")
        self._output_file.write("</doStatement>\n")
    #


    def compile_return(self):
        self._output_file.write("<returnStatement>\n")
        self.__consume_current_token()
        
        if self._tokenizer.token_type() != JackToken.SYMBOL:
            self.compile_expression()

        self.__consume_expected_symbol(";")
        self._output_file.write("</returnStatement>\n")
    #s


    def compile_expression_list(self):
        self._output_file.write("<expressionList>\n")

        if self._tokenizer.token_type() != JackToken.SYMBOL:
            self.compile_expression()

            while self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ",":
                self.__consume_current_token()
                self.compile_expression()
            #
        #
        self._output_file.write("</expressionList>\n")
    #
            


    def compile_expression(self):
        self._output_file.write("<expression>\n")
        self.compile_term()
        self._output_file.write("</expression>\n")
    #


    def compile_term(self):
        self._output_file.write("<term>\n")

        token_type = self._tokenizer.token_type() 
        if (token_type == JackToken.INT_CONST or token_type == JackToken.STRING_CONST or
                token_type == JackToken.KEYWORD or token_type == JackToken.IDENTIFIER):
            self.__consume_current_token()
        #

        self._output_file.write("</term>\n")
    #

    
    def __is_language_type(self):
        return (self._tokenizer.token_type() == JackToken.IDENTIFIER or 
                    (self._tokenizer.token_type() == JackToken.KEYWORD and
                        (self._tokenizer.keyword() == JackToken.INT or
                            self._tokenizer.keyword() == JackToken.CHAR or
                            self._tokenizer.keyword() == JackToken.BOOLEAN)))
    #


    def __compile_compound_var_decs(self):
        while self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ",":
            self.__consume_current_token()
            self.__consume_expected_token(JackToken.IDENTIFIER)
        #
    #


    def __compile_compound_param_list(self):
        while self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ",":
            self.__consume_current_token()

            if self.__is_language_type():
                self.__consume_current_token()
            else:
                raise Exception("Unexpected token")
            
            self.__consume_expected_token(JackToken.IDENTIFIER)
        #
    #





    def __get_next_token(self):
        if self._tokenizer.has_more_tokens():
            self._tokenizer.advance()
        #
        #print(self._tokenizer.current_token.value)
    #
        

    ## Call when we know we have the expected token
    def __consume_current_token(self):
        self.__writeTokenToOutput()
        self.__get_next_token()
        

    ## Call when we need to verify the next token type
    def __consume_expected_token(self, token_type):
        if self._tokenizer.token_type() != token_type:
            raise Exception("Unexpected token")
        else:
            self.__writeTokenToOutput()
            self.__get_next_token()
        #
    #

    ## Call when we need to verify the next token is a specific keyword
    def __consume_expected_keyword(self, token_type):
        if self._tokenizer.keyword() != token_type:
            raise Exception("Unexpected token")
        else:
            self.__writeTokenToOutput()
            self.__get_next_token()
        #
    #

    ## Call when we need to verify the next token is a specific symbol
    def __consume_expected_symbol(self, text):
        if self._tokenizer.token_type() != JackToken.SYMBOL or self._tokenizer.symbol() != text:
            raise Exception("Unexpected token")
        else:
            self.__writeTokenToOutput()
            self.__get_next_token()
        #
    #


    def __writeTokenToOutput(self):
        self._output_file.write(self._tokenizer.current_token.to_string())
    #
#

        
