import ring

def controller(src: str, ring_active, globals = {}):
    """
    This is the main function of the REPL. 
    It takes the input src, checks for errors and then calls 
    the appropriate function to evaluate it.
    """
    for i in range(len(src)):
        char = src[i]
        if char not in "0123456789+-*/^=() " and not char.isalpha():
            print("Error: Invalid character '" + char + "'.")
            return
        if char == "-":
            if i==0 or src[i-1] == "(":
                src = src[:i] + "0" + src[i:] # This is to manage negative numbers. We replace -x by 0-x, which is equivalent but easier to manage.

    if "=" in src:
        return assignment(src, ring_active, globals)
    return eval_main(src, ring_active, globals)
    
def assignment(src: str, ring_active, globals = {}):
    """
    This function manages the assignment of a variable. 
    It takes the input src, checks for errors and then assigns 
    the value of the expression to the variable in the globals dictionary.
    """
    list = src.split("=")

    var = list[0].strip()
    expr = list[1].strip()

    # Error management ---------------------------------------
    if len(list)>2:
        print("Error: Too many = signs.")
        return
    if " " in var:
        print("Variable name invalid (has space).")
        return
    if var == "":
        print("Variable name invalid (empty).")
        return
    if "(" in var or ")" in var:
        print("Variable name invalid (has parenthesis).")
    if not var[0].isalnum():
        print("Variable name invalid (it is not alphanumeric)")
    if var[0].isnumeric():
        print("Variable name invalid (starts with number).")
        return
    
    # TODO: There may be some unmanaged errors. Verify.

    # End of error management --------------------------------
    globals[var] = eval_main(expr, ring_active, globals)
    return 

def eval_main(src: str, ring_active, globals = {}):
    """
    This function manages the evaluation of an expression.
    It takes the input src, checks for errors and then evaluates it using the eval function.
    """
    printable = eval(src, ring_active, globals)
    if printable is not None:
        printable.replace(":","/") # This is to manage the fact that we use : for rationals internally.

def eval(src: str, ring_active, globals = {}):
    """
    This function manages the evaluation of an expression.
    It takes the input src, checks for errors and then evaluates it.
    This is where the main parsing of the expression happens. 
    We look for the operators in the order of precedence and we evaluate 
    the left and right parts recursively.
    """
    try:
        src = src.strip()
        src = src.replace(" ", "")
        for c in "^*/+-":
            i = src.find(c)
            if i>=0:
                j = i-1
                if src[j] == ")":
                    open_needed = 1
                    while j>=0:
                        if src[j] == ")":
                            open_needed += 1
                        elif src[j] == "(":
                            open_needed -= 1
                        if open_needed == 0:
                            break
                        j -= 1
                    if j<0:
                        print("Error: Invalid syntax (missing parenthesis).")
                        return
                    left = src[j:i]
                    j -= 1
                else:
                    j = i-1
                    while j>=0 and src[j] not in "+-*/^()":
                        j -= 1
                    left = src[j+1:i]
                k = i+1
                if src[k] == "(":
                    close_needed = 1
                    while k<len(src):
                        if src[k] == "(":
                            close_needed += 1
                        elif src[k] == ")":
                            close_needed -= 1
                        if close_needed == 0:
                            break
                        k += 1
                    if k>=len(src):
                        print("Error: Invalid syntax (missing parenthesis).")
                        return
                    right = src[i+1:k]
                    k+=1
                else:
                    k = i+1
                    while k<len(src) and src[k] not in "+-*/^":
                        k += 1
                    right = src[i+1:k]
                left_val = eval(left, ring_active, globals)
                right_val = eval(right, ring_active, globals)
                return src[0:j] + operation(ring_active, left_val, c, right_val) + src[k:]
            
            
        # If we are here, it means that there is no operator in the src. It is either a variable or a number
        # or it has parenthesis around it or it has :. We manage parenthesis first.

        if src[0] == "(" and src[-1] == ")":
            return eval(src[1:-1], ring_active, globals)
        if all(c.isnumeric() or c==":" for c in src):
            return ring_active(int(src))            



            
    except Exception as e:
        print(e)
        # TODO: The previous printing is for debugging, for the product 
        # we want a custom print.
    

def operation(ring_active, left, op, right)-> str:
    if op == "+":
        return ring_active.add(left, right)
    elif op == "-":
        return ring_active.sub(left, right)
    elif op == "*":
        return ring_active.mul(left, right)
    elif op == "/":
        return ring_active.div(left, right)
    elif op == "^":
        return ring_active.pow(left, right)

class Repl:
    ring_active = ring.Integers
    def __init__(self, globals=None):
        self.globals = {} if globals is None else globals
    def run_once(self, ring_active, src: str):
        controller(src, ring_active, self.globals)
    def loop(self):
        try:
            while True:
                src = input(">>> ")
                if src.strip() in {"quit()"}:
                    break
                self.run_once(src)
        except (KeyboardInterrupt, EOFError):
            print("Fatal error. Exiting...")
            return

def main():
    repl = Repl()
    repl.loop()

if __name__ == "__main__":
    main()