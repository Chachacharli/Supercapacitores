import customtkinter



class MainInput:
    def __init__(self,master: customtkinter.CTkFrame, row: int , header: str, placeholder: str, unit_variables_asig: any) -> None:
    
        self.entrie_din = customtkinter.CTkEntry(master, 
                                            height=40, 
                                            corner_radius=5, 
                                            validate='focusout' , 
                                            placeholder_text=placeholder,
                                            textvariable=unit_variables_asig,
                                            border_color='#2CC985'
                                            )
        self.entrie_din.configure(validate="key",validatecommand=(self.entrie_din.register(self.valid_command),"%P",),)        
        self.entrie_din.grid(row=row+2, column=0, sticky="ew",padx=10, pady=15, columnspan=3)

        self.label_din = customtkinter.CTkLabel(master, text=header)
        self.label_din.grid(row=row+2,column = 3, sticky="ew",padx=15, pady=15)

    def valid_command(self, P):
        
        return P 
    
