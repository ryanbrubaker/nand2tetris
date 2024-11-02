class AInstruction:
    def __init__(self, instruction_text):
        self._instruction_text = instruction_text
    #

    def compile(self, symbol_table, code_generator):
        value = self._instruction_text
        if not value.isnumeric():
            value = symbol_table.get_symbol(value)
        
        return '{0:016b}'.format(int(value))

    @property
    def text(self):
        return self._instruction_text

#