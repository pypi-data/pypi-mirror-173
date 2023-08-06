class PyArithOps:
    def __init__(self, operand1, operand2):

        self.operand1 = operand1 
        self.operand2 = operand2 

    def addition(self):
        add = self.operand1 + self.operand2
        return add
    
    def subtraction(self):
        sub = self.operand1 - self.operand2
        return sub

    def multiplication(self):
        mul = self.operand1 * self.operand2
        return mul

    def division(self):
        div = self.operand1 / self.operand2
        return div