class Player:
    def __init__(self, name):
        self._name = name
        self._auto_spin = 0
        self._balance = 10000000000000
    
    @property
    def name(self):
        return self._name
    
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, amount):
        self._balance += amount
    
    @property
    def auto_spin(self):
        return self._auto_spin
    
    @auto_spin.setter
    def auto_spin(self, amount):
        self._auto_spin += amount
    
    def __str__(self) -> str:
        return f"{self.name} has ${self.balance} and is auto-spinning {self.auto_spin} times."