class CommandType:
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_IF = 4
    C_GOTO = 5,
    C_FUNCTION = 6,
    C_RETURN = 7,
    C_CALL = 8


    COMMAND_TYPE_MAP = {
         "add":     C_ARITHMETIC,
         "sub":     C_ARITHMETIC,
         "neg":     C_ARITHMETIC,
          "eq":     C_ARITHMETIC,
          "gt":     C_ARITHMETIC,
          "lt":     C_ARITHMETIC,
         "and":     C_ARITHMETIC,
          "or":     C_ARITHMETIC,
         "not":     C_ARITHMETIC,
        "push":     C_PUSH,
         "pop":     C_POP,
       "label":     C_LABEL,
     "if-goto":     C_IF,
        "goto":     C_GOTO,
    "function":     C_FUNCTION,
      "return":     C_RETURN,
        "call":     C_CALL
    }
#