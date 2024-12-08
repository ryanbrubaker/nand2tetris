
import segments as SEGMENTS

from jack_token import JackToken
from jack_tokenizer import JackTokenizer
from symbol_table import SymbolTable
from vm_writer import VMWriter




class CompilationEngine:

    def __init__(self, input_file, output_file):
        self._input_file = input_file
        self._output_file = output_file

        self._tokenizer = JackTokenizer(input_file)
        self._class_symbol_table = SymbolTable()
        self._local_symbol_table = SymbolTable()
        self._vm_writer = VMWriter(output_file)

        self._current_class_name = ""
        self._file_label_num = 1
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
            
            self._local_symbol_table.reset()

            is_method = False
            is_constructor = self._tokenizer.keyword() == JackToken.CONSTRUCTOR

            if self._tokenizer.keyword() == JackToken.METHOD:
                is_method = True
                self._local_symbol_table.define("this", self._current_class_name, SymbolTable.ARG)

            self.__consume_current_token() 
            if (self.__is_language_type() or 
                    (self._tokenizer.token_type() == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.VOID)):
                self.__consume_current_token()
            else:
                raise Exception("Unexpected token")

            function_name = self._tokenizer.identifier()
            self.__consume_expected_token(JackToken.IDENTIFIER)

            self.__consume_expected_symbol("(")
            self.compile_parameter_list()
            self.__consume_expected_symbol(")")

            self.compile_subroutine_body(function_name, is_constructor, is_method)
        #
    #


    def compile_parameter_list(self):

        if self.__is_language_type():
            
            var_type = self._tokenizer.current_token.value
            self.__consume_current_token()

            var_name = self._tokenizer.current_token.value
            self.__consume_expected_token(JackToken.IDENTIFIER)

            self._local_symbol_table.define(var_name, var_type, SymbolTable.ARG)
            self.__compile_compound_param_list()
        #
    #


    def compile_subroutine_body(self, function_name, is_constructor, is_method):    
        #print(self._local_symbol_table.to_string())
   
        self.__consume_expected_symbol("{")
       
        num_vars = self.compile_var_dec()
        self._vm_writer.write_function(f"{self._current_class_name}.{function_name}", num_vars)

        if is_method:
            self._vm_writer.write_push(SEGMENTS.ARGUMENT, 0)
            self._vm_writer.write_pop(SEGMENTS.POINTER, 0)

        if is_constructor:
            self._vm_writer.write_push(SEGMENTS.CONSTANT, self._class_symbol_table.get_object_space_alloc())
            self._vm_writer.write_call("Memory.alloc", 1)
            self._vm_writer.write_pop(SEGMENTS.POINTER, 0)

        self.compile_statements()
        self.__consume_expected_symbol("}")
    #


    def compile_var_dec(self):
        
        num_vars = 0
        while self._tokenizer.token_type() == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.VAR:

            var_type = ""       
            self.__consume_expected_keyword(JackToken.VAR)

            if self.__is_language_type():
                var_type = self._tokenizer.current_token.value
                self.__consume_current_token()
            else:
                raise Exception("Unexpected token")
            
            var_name = self._tokenizer.current_token.value
            self._local_symbol_table.define(var_name, var_type, SymbolTable.VAR)
            #print(f"putting {var_name} into symbol table\n")
            num_vars += 1
            
            self.__consume_expected_token(JackToken.IDENTIFIER)
            num_vars += self.__compile_compound_var_decs(self._local_symbol_table, var_type, SymbolTable.VAR)
            self.__consume_expected_symbol(";")
        #
        return num_vars
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

        var_name = self._tokenizer.identifier()
        self.__consume_expected_token(JackToken.IDENTIFIER)

        if self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == "[":
            self.__consume_current_token()
            self.compile_expression()
            self.__consume_expected_symbol("]")
        #

        self.__consume_expected_symbol("=")
        self.compile_expression()

        var_info = self.__find_symbol(var_name)
        self._vm_writer.write_pop(var_info[0], var_info[1])

        self.__consume_expected_symbol(";")
    #

    def compile_if(self):
        self.__consume_current_token()
        self.__consume_expected_symbol("(")
        
        self.compile_expression()
        else_label = self.__generate_next_label()
        self._vm_writer.write_if(else_label)

        self.__consume_expected_symbol(")")
        self.__consume_expected_symbol("{")
        
        self.compile_statements()
        skip_else_label = self.__generate_next_label()
        self._vm_writer.write_goto(skip_else_label)

        self.__consume_expected_symbol("}")

        self._vm_writer.write_label(else_label)
        if self._tokenizer.token_type() == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.ELSE:    
            self.__consume_current_token()
            self.__consume_expected_symbol("{")
            self.compile_statements()
            self.__consume_expected_symbol("}")
        #
        self._vm_writer.write_label(skip_else_label)
    #


    def compile_while(self):
        while_label = self.__generate_next_label()
        self._vm_writer.write_label(while_label)

        self.__consume_current_token()
        self.__consume_expected_symbol("(")

        self.compile_expression()

        end_while_label = self.__generate_next_label()
        self._vm_writer.write_if(end_while_label)

        self.__consume_expected_symbol(")")
        self.__consume_expected_symbol("{")
        
        self.compile_statements()
        self._vm_writer.write_goto(while_label)

        self.__consume_expected_symbol("}")

        self._vm_writer.write_label(end_while_label)
    #


    def compile_do(self):
        self.__consume_current_token()

        num_args = 0
        function_name = self._tokenizer.identifier()
        self.__consume_expected_token(JackToken.IDENTIFIER)
        
        if self._tokenizer.token_type() == JackToken.SYMBOL:
            if self._tokenizer.symbol() == ".":
                self.__consume_current_token()
                
                if self._local_symbol_table.must_pass_this(function_name):
                    num_args += 1
                    self._vm_writer.write_push(self._local_symbol_table.kind_of(function_name),
                                               self._local_symbol_table.index_of(function_name))
                    function_name = self._local_symbol_table.type_of(function_name)
                #
                elif self._class_symbol_table.must_pass_this(function_name):
                    num_args += 1
                    self._vm_writer.write_push(self._class_symbol_table.kind_of(function_name),
                                               self._class_symbol_table.index_of(function_name))

                    function_name = self._class_symbol_table.type_of(function_name)
                #

                function_name += f".{self._tokenizer.identifier()}"
                self.__consume_expected_token(JackToken.IDENTIFIER)
                
                self.__consume_expected_symbol("(")
                num_args += self.compile_expression_list()
                self.__consume_expected_symbol(")")
            #
            elif self._tokenizer.symbol() == "(":
                function_name = f"{self._current_class_name}.{function_name}"
                self.__consume_current_token()
                num_args += 1
                self._vm_writer.write_push(SEGMENTS.POINTER, 0)
                num_args += self.compile_expression_list()
                self.__consume_expected_symbol(")")
            else:
                raise Exception("Unexpected token")
        else:
            raise Exception("Unexpected token")
        
        self._vm_writer.write_call(function_name, num_args)
        self._vm_writer.write_pop(SEGMENTS.TEMP, 0)
        self.__consume_expected_symbol(";")
    #


    def compile_return(self):
        self.__consume_current_token()

        has_return_val = False   
        if self._tokenizer.token_type() != JackToken.SYMBOL:
            has_return_val = True
            self.compile_expression()

        if not has_return_val:
            self._vm_writer.write_push(SEGMENTS.CONSTANT, 0)
        
        self._vm_writer.write_return()
        self.__consume_expected_symbol(";")
    #


    def compile_expression_list(self):

        num_expressions = 0
        if self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ")":
            pass
        else:
            self.compile_expression()
            num_expressions = 1
            while self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ",":
                self.__consume_current_token()
                self.compile_expression()
                num_expressions += 1
            #
        #
        return num_expressions
    #
            


    def compile_expression(self):
        self.compile_term()

        if self._tokenizer.token_type() == JackToken.SYMBOL:
            current_symbol = self._tokenizer.symbol()
            
            if current_symbol == "+":
                self.__consume_current_token()
                self.compile_term()
                self._vm_writer.write_arithmetic(VMWriter.ADD)
            elif current_symbol == "-":
                self.__consume_current_token()
                self.compile_term()
                self._vm_writer.write_arithmetic(VMWriter.SUB)
            elif current_symbol == '*':
                self.__consume_current_token()
                self.compile_term()
                self._vm_writer.write_call("Math.multiply", 2)
            elif current_symbol == '/':
                self.__consume_current_token()
                self.compile_term()
                self._vm_writer.write_call("Math.divide", 2)
            elif current_symbol == "=":
                self.__consume_current_token()
                self.compile_term()
                self._vm_writer.write_arithmetic(VMWriter.EQ)
            elif current_symbol == ">":
                self.__consume_current_token()
                self.compile_term()
                self._vm_writer.write_arithmetic(VMWriter.GT)
            elif current_symbol == "<":
                self.__consume_current_token()
                self.compile_term()
                self._vm_writer.write_arithmetic(VMWriter.LT)
            elif current_symbol == "&":
                self.__consume_current_token()
                self.compile_term()
                self._vm_writer.write_arithmetic(VMWriter.AND)
            elif current_symbol == "|":
                self.__consume_current_token()
                self.compile_term()
                self._vm_writer.write_arithmetic(VMWriter.OR)
            #
        #
    #


    def compile_term(self):
        token_type = self._tokenizer.token_type() 
        if token_type == JackToken.INT_CONST:
            self._vm_writer.write_push(SEGMENTS.CONSTANT, self._tokenizer.int_val())
            self.__consume_current_token()
        #
        elif token_type == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.TRUE:
            self._vm_writer.write_push(SEGMENTS.CONSTANT, 1)
            self._vm_writer.write_arithmetic(VMWriter.NEG)
            self.__consume_current_token()
        #
        elif token_type == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.FALSE:
            self._vm_writer.write_push(SEGMENTS.CONSTANT, 0)
            self.__consume_current_token()
        #
        elif token_type == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.THIS:
            self._vm_writer.write_push(SEGMENTS.POINTER, 0)
            self.__consume_current_token()
        #
        elif token_type == JackToken.KEYWORD and self._tokenizer.keyword() == JackToken.NULL:
            self._vm_writer.write_push(SEGMENTS.CONSTANT, 0)
            self.__consume_current_token()
        #
        elif token_type == JackToken.STRING_CONST:
            self.__consume_current_token()
        #
        elif token_type == JackToken.IDENTIFIER:
            identifier = self._tokenizer.identifier()
            self.__consume_current_token()
            num_args = 0

            if self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ".":
                self.__consume_current_token()

                if self._local_symbol_table.must_pass_this(identifier):
                    num_args += 1
                    self._vm_writer.write_push(self._local_symbol_table.kind_of(identifier),
                                               self._local_symbol_table.index_of(identifier))
                    function_name = self._local_symbol_table.type_of(identifier)
                #
                elif self._class_symbol_table.must_pass_this(identifier):
                    num_args += 1
                    self._vm_writer.write_push(self._class_symbol_table.kind_of(identifier),
                                               self._class_symbol_table.index_of(identifier))
                    function_name = self._local_symbol_table.type_of(identifier)
                #
                
                function_name = f"{identifier}.{self._tokenizer.identifier()}"
                self.__consume_expected_token(JackToken.IDENTIFIER)

                self.__consume_expected_symbol("(")
                num_args = self.compile_expression_list()
                self.__consume_expected_symbol(")")
                self._vm_writer.write_call(function_name, num_args)
            #
            elif self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == "(":
                self.__consume_current_token()
                num_args += 1
                self._vm_writer.write_push(SEGMENTS.POINTER, 0)
                num_args = self.compile_expression_list()                
                self.__consume_expected_symbol(")")
                self._vm_writer.write_call(function_name, num_args)
            #
            elif self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == "[":
                self.__consume_current_token()
                self.compile_expression()
                self.__consume_expected_symbol("]")
            else:
                var_info = self.__find_symbol(identifier)
                #print(f"var info for {identifier}: kind_of = {var_info[0]}, position = {var_info[1]}\n")
                self._vm_writer.write_push(var_info[0], var_info[1])
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
        elif token_type == JackToken.SYMBOL and self._tokenizer.symbol() == "~":
            self.__consume_current_token()
            self.compile_term()
            self._vm_writer.write_arithmetic(VMWriter.NOT)
        #
        elif token_type == JackToken.SYMBOL and self._tokenizer.symbol() == "-":
            self.__consume_current_token()
            self.compile_term()
            self._vm_writer.write_arithmetic(VMWriter.NEG)
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
        num_vars = 0
        while self._tokenizer.token_type() == JackToken.SYMBOL and self._tokenizer.symbol() == ",":
            self.__consume_current_token()

            symbol_table.define(self._tokenizer.current_token.value, current_type, current_kind)
            num_vars += 1
            self.__consume_expected_token(JackToken.IDENTIFIER)
        #
        return num_vars
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
            
            self._local_symbol_table.define(self._tokenizer.current_token.value, var_type, SymbolTable.ARG)
            
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


    ## Generate a unique label using the class name and counter
    def __generate_next_label(self):
        label = f"{self._current_class_name}.LABEL.{self._file_label_num}"
        self._file_label_num += 1
        return label
    

    # Find the given symbol in the two symbol tables
    def __find_symbol(self, var_name):
        if self._local_symbol_table.contains(var_name):
            return self._local_symbol_table.kind_of(var_name), self._local_symbol_table.index_of(var_name)
        elif self._class_symbol_table.contains(var_name):
            return self._class_symbol_table.kind_of(var_name), self._class_symbol_table.index_of(var_name)
        else:
            raise Exception("Undefined variable")
    


        
