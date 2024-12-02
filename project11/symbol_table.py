
class SymbolTable:

    STATIC = 0
    FIELD = 1
    ARG = 2
    VAR = 3

    def __init__(self):
        self._table = {}
        self._counts = {
            SymbolTable.STATIC: 0,
            SymbolTable.FIELD:  0,
            SymbolTable.ARG:    0,
            SymbolTable.VAR:    0
        }
    #

    def reset(self):
        self._table.clear()
    #

    ## Assumes no duplicate declarations
    def define(self, name, type, kind):
        self._table[name] = (type, kind, self._counts[kind])
        self._counts[kind] += 1
    #

    def varCount(self, kind):
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