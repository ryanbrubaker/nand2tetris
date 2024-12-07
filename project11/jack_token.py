
class JackToken:
     
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4

    TYPE_MAP = {
        KEYWORD:        "keyword",
        SYMBOL:         "symbol",
        IDENTIFIER:     "identifier",
        INT_CONST:      "integerConstant",
        STRING_CONST:   "stringConstant"
    }

    SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]
     
    CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT, BOOLEAN = 10, 11, 12, 13, 14, 15
    CHAR, VOID, VAR, STATIC, FIELD, LET, DO = 16, 17, 18, 19, 20, 21, 22
    IF, ELSE, WHILE, RETURN, TRUE, FALSE, NULL, THIS = 23, 24, 25, 26, 27, 28, 29, 30

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
        return self._value
    #

    def to_string(self):
        tag_name = JackToken.TYPE_MAP[self.type]
        return f"<{tag_name}> {self.value} </{tag_name}>\n"
    #
#