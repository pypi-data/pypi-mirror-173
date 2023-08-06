import json

class MessageProperty:

    def __init__(self):
        self.property1 = None
        self.property2 = None

    @property
    def property1(self) -> str:
        return self._property1
    
    @property1.setter
    def property1(self, property1: str):
        self._property1 = property1

    @property
    def property2(self) -> str:
        return self._property2
    
    @property1.setter
    def property2(self, property2: str):
        self._property2 = property2


    def __str__(self) -> str:
        return f'{"property1": {self.property1}, property2: {self.property2} }'

    