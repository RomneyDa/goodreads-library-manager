# OO Practice & notes
# https://www.youtube.com/watch?v=ZDa-Z5JzLYM

# data = attributes
# methods = functions

class Employee:
    # methods inside classes receive instance as first argument automatically
    # conventionally this is called self
    
    # __init__ is the built in "constructor"
    def __init__(self, first, last, pay):
        self.first = first
        self.last  = last
        self.pay   = pay
        
        self.email = first + '.' + last + '@company.com'
    
    def fn(self):
        print(self.first, self.last)
    
# emp1 and emp2 are "instances" of the employee class
emp1 = Employee('Dallin', 'Romney', 90000)
emp2 = Employee('Corey', 'Schafer', 20000)

emp1.fn()

print(emp1.email)