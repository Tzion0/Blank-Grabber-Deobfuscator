# Define functions for basic arithmetic operations
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Division by zero is not allowed"

# Main program
if __name__ == "__main__":
    num1 = 10
    num2 = 5

    print("Numbers: ", num1, num2)

    # Perform arithmetic operations using function calls
    print("Addition: ", add(num1, num2))
    print("Subtraction: ", subtract(num1, num2))
    print("Multiplication: ", multiply(num1, num2))
    print("Division: ", divide(num1, num2))

    # Edge case for division
    num3 = 0
    print("Division with zero: ", divide(num1, num3))
