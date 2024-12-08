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
        #print(f"adding {name} at index {self._counts[kind]}\n")
        self._table[name] = (type, kind, self._counts[kind])
        self._counts[kind] += 1
        #print(self.to_string())
    #

    def contains(self, var_name):
        return var_name in self._table
    
    def must_pass_this(self, var_name):
        return self.contains(var_name) and self.kind_of(var_name) != SymbolTable.STATIC


    def var_count(self, kind):
        return self._counts[kind]
    #

    def kind_of(self, name):
        return self._table[name][1]
    #

    def type_of(self, name):
        return self._table[name][0]
    #

    def index_of(self, name):
        return self._table[name][2]
    #

    def get_object_space_alloc(self):
        return self._counts[SymbolTable.FIELD]