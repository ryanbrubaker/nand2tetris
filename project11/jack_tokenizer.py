
from jack_token import JackToken


class JackTokenizer:

    def __init__(self, input_file):
        self._input_text = input_file.read().strip()
        self._input_length = len(self._input_text)
        self._char_index = 0
        self._current_char = None
        self._current_token_str = ''
        self._current_token = None
    #


    def has_more_tokens(self):
        return self._input_length > 0 and self._char_index < self._input_length
    #

    def advance(self):
       
        if self._current_char == None:
            self._current_char = self._input_text[self._char_index]

        self._current_token_str = ''
        self._current_token = None
        self.__skip_whistespace_and_comments()

        if self._current_char.isalpha() or self._current_char == "_":
            self.__parse_identifier()
        elif self._current_char.isdigit():
            self.__parse_int_literal()
        elif self._current_char == '"':
            self.__parse_string_literal()
        elif self._current_char in JackToken.SYMBOLS:
            self._current_token_str += self._current_char
            self._current_token = JackToken(JackToken.SYMBOL, self._current_token_str)
            self.__read_next_character()
        else:
            raise Exception("Unrecognized character")
        #
    #

    @property
    def current_token(self):
        return self._current_token
    
    
    def token_type(self):
        return self._current_token.type
    #

    def token_value(self):
        return self._current_token.value
    

    def keyword(self):
        return JackToken.KEYWORDS[self._current_token_str]

    def symbol(self):
        if self._current_token_str == "&":
            return "&amp;"
        elif self._current_token_str == "<":
            return "&lt;"
        elif self._current_token_str == ">":
            return "&gt;"
        elif self._current_token_str == '"':
            return "&quot;"
        else:
            return self._current_token_str

    def identifier(self):
        return self._current_token_str

    def int_val(self):
        return self._current_token_str

    def string_val(self):
        return self._current_token_str


    def __skip_whistespace_and_comments(self):

        while self.__is_whitespace(self._current_char) or self.__is_start_of_comment(self._current_char):
            if self.__is_whitespace(self._current_char):
                self.__read_next_character()
            else:
                self.__read_next_character()
                # Read single line comments started by //
                if self._current_char == '/':
                    while self._current_char != '\n':
                        self.__read_next_character()
                    self.__read_next_character()
                # Read multiline comments started by /* or /**
                elif self._current_char == '*':
                    prev_char = self._current_char
                    self.__read_next_character()
                    while prev_char != '*' or self._current_char != '/':
                        prev_char = self._current_char
                        self.__read_next_character()
                    self.__read_next_character()
                # we ran into the division sign so reset back to that character
                else:
                    self._char_index -= 1
                    self._current_char = self._input_text[self._char_index]
                    break
                #
            #
        #
    #

    def __parse_identifier(self):
        self._current_token_str += self._current_char
        self.__read_next_character()
        while self.__is_identifier_char(self._current_char):
            self._current_token_str += self._current_char
            self.__read_next_character()
        #
        self._current_token = JackToken(JackToken.IDENTIFIER, self._current_token_str)
    #


    def __parse_int_literal(self):
        self._current_token_str += self._current_char
        self.__read_next_character()
        while self._current_char.isdigit():
            self._current_token_str += self._current_char
            self.__read_next_character()
        #
        self._current_token = JackToken(JackToken.INT_CONST, self._current_token_str)
    #

                
    def __parse_string_literal(self):
        # Already read double quote so ignore and read next character
        self.__read_next_character()
        while self._current_char != '"':
            self._current_token_str += self._current_char
            self.__read_next_character()
        #

        # Ignore edning quote and move on to next character
        self.__read_next_character()
        self._current_token = JackToken(JackToken.STRING_CONST, self._current_token_str)
    #


    def __read_next_character(self):
        self._char_index += 1
        if self._char_index < self._input_length:
            self._current_char = self._input_text[self._char_index]

    def __is_whitespace(self, current_char):
        return current_char.isspace()
    
    def __is_start_of_comment(self, current_char):
        return current_char == '/'

    def __is_identifier_char(self, current_char):
        return current_char.isalpha() or current_char.isnumeric() or current_char == '_'

