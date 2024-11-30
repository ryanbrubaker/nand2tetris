
class JackToken:
     
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4

    EOF = ''

    SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]
     
    CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT , BOOLEAN = 0, 1, 2, 3, 4, 5
    CHAR, VOID, VAR, STATIC, FIELD, LET, DO = 6, 7, 8, 9, 10, 11, 12
    IF, ELSE, WHILE, RETURN, TRUE, FALSE, NULL, THIS = 13, 14, 15, 16, 17, 18, 19, 20

    KEYWORDS = {
        "class":           CLASS,
        "method":          METHOD,
        "function":        FUNCTION,
        "constructor":     CONSTRUCTOR,
        "int":             INT,
        "boolean":         BOOLEAN,
        "char":            CHAR,
        "void":            VOID,
        "var":             VAR,
        "static":          STATIC,
        "field":           FIELD,
        "let":             LET,
        "do":              DO,
        "if":              IF,
        "else":            ELSE,
        "while":           WHILE,
        "return":          RETURN,
        "true":            TRUE,
        "false":           FALSE,
        "null":            NULL,
        "this":            THIS
    }

    def __init__(self, type, value):
        self._type = type
        self._value = value

        if self._type == JackToken.IDENTIFIER:
            if value in JackToken.KEYWORDS:
                self._type = JackToken.KEYWORD
            #
        #
    #

    @property
    def type(self):
        return self._type
    
    @property
    def value(self):
        if self._type == JackToken.IDENTIFIER:
            return self._value
        #
    #
#