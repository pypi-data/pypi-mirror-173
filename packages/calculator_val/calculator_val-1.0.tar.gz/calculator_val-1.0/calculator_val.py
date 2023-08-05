"""A simple calculator"""

__version__ = "1.0"


class Calculator:
    def __init__(self, memory: float) ->float:
        self.memory = memory

    def sum(self: float, arg1: float ) -> float:
        '''adds up the argument to the memory for example:
        >>> obj=Calculator(0.0)
        >>> obj.sum(2.0)
        2.0
        '''
        self.memory+= arg1
        return self.memory
    def sub(self: float, arg1: float) -> float:
        '''subtracts the input argument to the curent value in memory for example:
        2.0
        >>> obj.sub(1.0)
        1.0
        '''
        self.memory -= arg1
        return self.memory

    def nroot(self: float, root: float) -> float:
        '''returns n^th root of the value stored in memory for example
        27.0
        >>> obj.nroot(3.0)
        3.0
        '''
        self.memory = self.memory ** (1 / (root))
        return self.memory

    def div(self: float, arg2: float) -> float:
        '''divides the value stored in memory by the argument provided ex:
         3.0
         >>> obj.div(2.0)
         1.5
         '''
        self.memory = self.memory / arg2
        return self.memory

    def mult(self: float, arg1: float) -> float:
        '''it multiplies the value stored in memory by the imput given, ex.:
        1.0
        >>> obj.mult(27.0)
        27.0
        '''
        self.memory = self.memory * arg1
        return (self.memory)

    def delete(self):
        '''it resets the calculator by assigning 0 to the value in memory'''
        self.memory = 0
        return self.memory



