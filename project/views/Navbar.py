import customtkinter

class Navbar:
    def __init__(self, root) -> None:
        self.root = root
        nav = customtkinter.CTkFrame(self.root, height=100, fg_color='#1d3f60')
        nav.grid(row=0, column=1, columnspan=10, sticky= 'we')
