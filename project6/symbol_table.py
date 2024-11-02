class SymbolTable:
    def __init__(self):
        self._current_open_address = 16  
        self._symbols = {
                "R0":     "0",
                "R1":     "1",
                "R2":     "2",
                "R3":     "3",
                "R4":     "4",
                "R5":     "5",
                "R6":     "6",
                "R7":     "7",
                "R8":     "8",
                "R9":     "9",
               "R10":    "10",
               "R11":    "11",
               "R12":    "12",
               "R13":    "13",
               "R14":    "14",
               "R15":    "15",
                "SP":     "0",
               "LCL":     "1",
               "ARG":     "2",
              "THIS":     "3",
              "THAT":     "4",
            "SCREEN": "16384",
               "KBD": "24576"
        }
    #

    @property
    def symbols(self):
        return self._symbols
    #

    def add_label(self, label, address):
        self._symbols[label] = address
    #


    def add_variable(self, variable_name):
        if not variable_name in self._symbols:
            self._symbols[variable_name] = str(self._current_open_address)
            self._current_open_address += 1
        #
    #

    
    def get_symbol(self, value):
        return self._symbols[value]

#