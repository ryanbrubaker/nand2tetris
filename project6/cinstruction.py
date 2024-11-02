class CInstruction:
    def __init__(self, instruction_text):
        self._instruction_text = instruction_text
    #

    def compile(self, symbol_table, code_generator):
        return "111" + code_generator.translate_comp(self.comp) + code_generator.translate_dest(self.dest) + code_generator.translate_jump(self.jump)
        
    @property
    def text(self):
        return self._instruction_text
    

    @property
    def comp(self):
        comp = self._instruction_text

        index = comp.find("=")
        if index != -1:
            comp = comp[index+1:]

        index = comp.find(";")
        if index != -1:
            comp = comp[:index]
        
        return comp



    @property
    def dest(self):
        index = self._instruction_text.find("=")
        return None if index == -1 else self._instruction_text[:index]
    
    @property
    def jump(self):
        index = self._instruction_text.find(";")
        return None if index == -1 else self._instruction_text[index+1:]

#