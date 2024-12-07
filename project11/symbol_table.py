import segments as SEGMENTS
class SymbolTable:

    STATIC = SEGMENTS.STATIC
    FIELD = SEGMENTS.THIS
    ARG = SEGMENTS.ARGUMENT
    VAR = SEGMENTS.LOCAL

    def __init__(self):
        self._table = {}
        self._counts = {
            SymbolTable.STATIC: 0,
            SymbolTable.FIELD:  0,
            SymbolTable.ARG:    0,
            SymbolTable.VAR:    0
        }
    #

    def to_string(self):
        return str(self._table)

    def reset(self):
        self._table.clear()
        self._counts[SymbolTable.STATIC] = 0
        self._counts[SymbolTable.FIELD] = 0
        self._counts[SymbolTable.ARG] = 0
        self._counts[SymbolTable.VAR] = 0

    #

    ## Assumes no duplicate declarations
    def define(self, name, type, kind):
        print(f"adding {name} at index {self._counts[kind]}\n")
        self._table[name] = (type, kind, self._counts[kind])
        self._counts[kind] += 1
    #

    def contains(self, var_name):
        return var_name in self._table

    def var_count(self, kind):
        return self._counts[kind]
    #

    def kindOf(self, name):
        return self._table[name][1]
    #

    def typeOf(self, name):
        return self._table[name][0]
    #

    def indexOf(self, name):
        return self._table[name][2]
    #