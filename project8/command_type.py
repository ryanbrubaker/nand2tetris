class CommandType:
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_IF = 4


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
     "if-goto":     C_IF
    }
#