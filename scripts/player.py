class Player:
    def __init__(self, name, balance=100, auto_spin=0, current_bet=100):
        self._name = name
        self._auto_spin = auto_spin
        self._balance = balance
        self._current_bet = current_bet
    
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
    
    @property
    def current_bet(self):
        return self._current_bet
    
    @current_bet.setter
    def current_bet(self, amount):
        self._current_bet += amount
    
    def __str__(self) -> str:
        return f"{self.name} has ${self.balance} and is auto-spinning {self.auto_spin} times."