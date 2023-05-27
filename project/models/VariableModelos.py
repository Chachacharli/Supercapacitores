from tkinter import StringVar, IntVar, DoubleVar

class VariableModelos: 
    def __init__(self) -> None:
        pass

    def float_variable(self, name) -> DoubleVar:
        floater = DoubleVar(master = None,name=name)
        return floater
    
    def string_variable(self,name) -> StringVar():
        stringer = StringVar(master = None,name=name)
        return stringer
    
    def int_variable(self, name) -> IntVar:
        integer = IntVar(master = None, name=name)

        return integer