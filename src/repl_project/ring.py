import utils

class Ring:
    # Abstract class with static methods for ring operations
    @staticmethod
    def to_string(a): raise NotImplementedError("to_string method not implemented")
    @staticmethod    
    def add(a, b): raise NotImplementedError("Add method not implemented")
    @staticmethod
    def mul(a, b): raise NotImplementedError("Mul method not implemented")
    @staticmethod
    def neg(a): raise NotImplementedError("Neg method not implemented")
    @staticmethod
    def sub(a, b):
        return Ring.add(a, Ring.neg(b))
    @staticmethod
    def zero(): raise NotImplementedError("Zero method not implemented")
    @staticmethod
    def one(): raise NotImplementedError("One method not implemented")
    @staticmethod
    def div(a, b): raise NotImplementedError("Div method not implemented")

    @staticmethod
    def pow(a, n):
        if n < 0:
            a = Ring.div(Ring.one(), a)
            n = -n
        result = Ring.one()
        # Repeated squaring for efficient exponentiation
        while n > 0:
            if n % 2 == 1:
                result = Ring.mul(result, a)
            a = Ring.mul(a, a)
            n //= 2
        return result
    @staticmethod
    def eq(a, b):        return a == b

    # Atribute (ring name). This is used to choose the ring in which the operations will be performed. It can be overridden by subclasses to specify the ring type. 
    name = "Generic Ring"

class Integers(Ring):
    name = "Integers"

    @staticmethod
    def to_string(a):
        return str(a)

    @staticmethod
    def add(a, b):
        return str(a+b)

    @staticmethod
    def mul(a, b):
        return str(a*b)
    
    @staticmethod
    def neg(a):
        return -a


    @staticmethod
    def sub(a, b):
        return a - b
        
    @staticmethod
    def zero():
        return 0

    @staticmethod
    def one():
        return 1

    @staticmethod
    def div(a, b):
        if b not in {1, -1}:
            raise ValueError("Division by non-unit element is not defined in integers")
        return a // b

class Rationals(Ring):
    name = "Rationals"

    @staticmethod
    def to_string(a):
        num, denom = a
        if denom == 1:
            return str(num)
        return f"{num}:{denom}"

    @staticmethod
    def add(a, b):
        num_a, denom_a = a
        num_b, denom_b = b
        common_denom = denom_a * denom_b // utils.gcd(denom_a, denom_b) #LCM of denominators
        new_num_a = num_a * (common_denom // denom_a)
        new_num_b = num_b * (common_denom // denom_b)
        return Rationals.simplify(new_num_a + new_num_b, common_denom)
        
    @staticmethod
    def simplify(a):
        num, denom = a
        common_factor = utils.gcd(num, denom)
        if num == 0:
            return (0, 1)
        if denom < 0:
            num = -num
            denom = -denom
        return (num // common_factor, denom // common_factor)

    @staticmethod
    def mul(a, b):
        return Rationals.simplify((a[0] * b[0], a[1] * b[1]))

    @staticmethod
    def neg(a):
        return (-a[0], a[1])

    @staticmethod
    def zero():
        return (0, 1)

    @staticmethod
    def one():
        return (1, 1)

    @staticmethod
    def div(a, b):
        if b == Rationals.zero():
            raise ValueError("Division by zero is not defined in rationals")
        return Rationals.mul(a, (b[1], b[0])) # Multiply by reciprocal of b
    
    @staticmethod
    def eq(a, b):
        return a[0] * b[1] == b[0] * a[1] # Cross multiply to check equality
