from abc import ABC
from dataclasses import dataclass

"""
Esta es una interfaz hecha de fomra  
"""

class _ISetState(ABC):
    #Esta propiedad cambia el estado de el objeto para retornar un error si esa que el en algun momento ocurre un error.
    @property
    def change_state(self):
        return self.state
    
    @change_state.setter
    def change_state(self, newState: bool):
        self.state = newState

