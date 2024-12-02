
from jack_token import JackToken
from jack_tokenizer import JackTokenizer
from symbol_table import SymbolTable


class CompilationEngine:

    def __init__(self, input_file, output_file):
        self._input_file = input_file
        self._output_file = output_file

        self._tokenizer = JackTokenizer(input_file)
        self._class_symbol_table = SymbolTable()
        self._subroutine_symbol_table = SymbolTable()

        self._current_class_name = ""
    #


    def compile_class(self):
        
        self.__get_next_token()

        self.__consume_expected_keyword(JackToken.CLASS)
        self._current_class_name = self._tokenizer.current_token.value     
        self.__consume_expected_token(JackToken.IDENTIFIER)
        self.__consume_expected_symbol("{")
        
        self.compile_class_var_dec()
        self.compile_subroutine()
        
        while self._tokenizer.has_more_tokens():
            self._tokenizer.advance()
        #

        self.__consume_expected_symbol("}")

        if self._tokenizer.has_more_tokens():
            raise Exception("Expected end of input")
    #




    def compile_class_var_dec(self):

        while (self._tokenizer.token_type() == JackToken.KEYWORD and 
                    (self._tokenizer.keyword() == JackToken.STATIC or self._tokenizer.keyword() == JackToken.FIELD)):
            
            var_type = ""
            var_kind = SymbolTable.STATIC if self._tokenizer.keyword() == JackToken.STATIC else SymbolTable.FIELD
            self.__consume_current_token();
        
            if self.__is_language_type():
                var_type = self._tokenizer.current_token.value
                self.__consume_current_token()
            else:
                raise Exception("Unexpected token")
            
            var_name = self._tokenizer.current_token.value
            self._class_symbol_table.define(var_name, var_type, var_kind)
    
            self.__consume_expected_token(JackToken.IDENTIFIER)
            self.__compile_compound_var_decs(self._class_symbol_table, var_type, var_kind)
            self.__consume_expected_symbol(";")
        #
    #


    def compile_subroutine(self):

        while (self._tokenizer.token_type() == JackToken.KEYWORD and
                    (self._tokenizer.keyword() == JackToken.CONSTRUCTOR or self._tokenizer.keyword() == JackToken.FUNCTION or
                        self._tokenizer.keyword() == JackToken.METHOD)):
            
            if self._subroutine_symbol_table.define("this", self._current_class_name, SymbolTable.ARG)
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
        #
    #


    def compile_parameter_list(self):
        if self.__is_language_type():
            var_type = self._tokenizer.current_token.value
            self.__consume_current_token()

            var_name = self._tokenizer.current_token.value
            self.__consume_expected_token(JackToken.IDENTIFIER)

            self._subroutine_symbol_table.define(var_name, var_type, SymbolTable.ARG)
            self.__compile_compound_param_list()
        #
    #


    def compile_subroutine_body(self):       
        self.__consume_expected_symbol("{")
        self.compile_var_dec()
        self.compile_statements()
        self.__consume_expected_symbol("}")
    #


    def compile_var_dec(self):

        while self._tokenizer.token_type() == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.VAR:

            var_type = ""       
            self.__consume_expected_keyword(JackToken.VAR)

            if self.__is_language_type():
                var_type = self._tokenizer.current_token.value
                self.__consume_current_token()
            else:
                raise Exception("Unexpected token")
            
            var_name = self._tokenizer.current_token.value
            self._class_symbol_table.define(var_name, var_type, SymbolTable.VAR)
    
            
            self.__consume_expected_token(JackToken.IDENTIFIER)
            self.__compile_compound_var_decs()
            self.__consume_expected_symbol(";")
        #
    #



    def compile_statements(self):
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
    #            

    def compile_let(self):
        self.__consume_current_token()
        self.__consume_expected_token(JackToken.IDENTIFIER)

        if self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == "[":
            self.__consume_current_token()
            self.compile_expression()
            self.__consume_expected_symbol("]")
        #

        self.__consume_expected_symbol("=")
        self.compile_expression()
        self.__consume_expected_symbol(";")
    #

    def compile_if(self):
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
    #


    def compile_while(self):
        self.__consume_current_token()
        self.__consume_expected_symbol("(")
        self.compile_expression()
        self.__consume_expected_symbol(")")
        self.__consume_expected_symbol("{")
        self.compile_statements()
        self.__consume_expected_symbol("}")
    #


    def compile_do(self):
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
    #


    def compile_return(self):
        self.__consume_current_token()
        
        if self._tokenizer.token_type() != JackToken.SYMBOL:
            self.compile_expression()

        self.__consume_expected_symbol(";")
    #s


    def compile_expression_list(self):

        if self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ")":
            pass
        else:
            self.compile_expression()
            while self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ",":
                self.__consume_current_token()
                self.compile_expression()
            #
        #
    #
            


    def compile_expression(self):
        self.compile_term()

        if self._tokenizer.token_type() == JackToken.SYMBOL:
            current_symbol = self._tokenizer.symbol()
            if (current_symbol == "+" or current_symbol == "-" or current_symbol == '*' or
                    current_symbol == "/" or current_symbol == "&amp;" or current_symbol == "|" or
                    current_symbol == "&lt;" or current_symbol == "&gt;" or current_symbol == "="):
                self.__consume_current_token()
                self.compile_term()
            #
        #
    #


    def compile_term(self):
        token_type = self._tokenizer.token_type() 
        if (token_type == JackToken.INT_CONST or token_type == JackToken.STRING_CONST or 
                (token_type == JackToken.KEYWORD and
                    (self._tokenizer.keyword() == JackToken.TRUE or self._tokenizer.keyword() == JackToken.FALSE or
                     self._tokenizer.keyword() == JackToken.NULL or self._tokenizer.keyword() == JackToken.THIS))):
            self.__consume_current_token()
        elif token_type == JackToken.IDENTIFIER:
            self.__consume_current_token()
            if self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ".":
                self.__consume_current_token()
                self.__consume_expected_token(JackToken.IDENTIFIER)
                self.__consume_expected_symbol("(")
                self.compile_expression_list()
                self.__consume_expected_symbol(")")
            elif self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == "(":
                self.__consume_current_token()
                self.compile_expression_list()                
                self.__consume_expected_symbol(")")
            elif self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == "[":
                self.__consume_current_token()
                self.compile_expression()
                self.__consume_expected_symbol("]")
            else:
                pass
            #
        #
        elif token_type == JackToken.SYMBOL and self._tokenizer.symbol() == "(":
            self.__consume_current_token()

            if self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.current_token.SYMBOL == ")":
                self.__consume_current_token()
            else:
                self.compile_expression()
                self.__consume_expected_symbol(")")
            #
        #
        elif token_type == JackToken.SYMBOL and (self._tokenizer.symbol() == "-" or self._tokenizer.symbol() == "~"):
            self.__consume_current_token()
            self.compile_term()
        #
    #

    
    def __is_language_type(self):
        return (self._tokenizer.token_type() == JackToken.IDENTIFIER or 
                    (self._tokenizer.token_type() == JackToken.KEYWORD and
                        (self._tokenizer.keyword() == JackToken.INT or
                            self._tokenizer.keyword() == JackToken.CHAR or
                            self._tokenizer.keyword() == JackToken.BOOLEAN)))
    #


    def __compile_compound_var_decs(self, symbol_table, current_type, current_kind):
        while self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ",":
            self.__consume_current_token()

            symbol_table.define(self._tokenizer.current_token.value, current_type, current_kind)
            self.__consume_expected_token(JackToken.IDENTIFIER)
        #
    #


    def __compile_compound_param_list(self):
        while self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ",":
            self.__consume_current_token()

            var_type = ""
            if self.__is_language_type():
                var_type = self._tokenizer.current_token.value
                self.__consume_current_token()
            else:
                raise Exception("Unexpected token")
            
            self._subroutine_symbol_table.define(self._tokenizer.current_token.value, var_type, SymbolTable.ARG)
            self.__consume_expected_token(JackToken.IDENTIFIER)
        #
    #





    def __get_next_token(self):
        if self._tokenizer.has_more_tokens():
            self._tokenizer.advance()
        #
    #
        

    ## Call when we know we have the expected token
    def __consume_current_token(self):    
        self.__get_next_token()
        

    ## Call when we need to verify the next token type
    def __consume_expected_token(self, token_type):
        if self._tokenizer.token_type() != token_type:
            raise Exception("Unexpected token")
        else:
            self.__get_next_token()
        #
    #

    ## Call when we need to verify the next token is a specific keyword
    def __consume_expected_keyword(self, token_type):
        if self._tokenizer.keyword() != token_type:
            raise Exception("Unexpected token")
        else:
            self.__get_next_token()
        #
    #

    ## Call when we need to verify the next token is a specific symbol
    def __consume_expected_symbol(self, text):
        if self._tokenizer.token_type() != JackToken.SYMBOL or self._tokenizer.symbol() != text:
            raise Exception("Unexpected token")
        else:
            self.__get_next_token()
        #
    #
#

        
