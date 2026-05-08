def is_even(n):
    return n%2
def validate(n):
    if(is_even(n) == 0):
        print(f"Yes,{n} is even")
    else:
        print(f"No,{n} is even")

def main():
    n = 12
    validate(n)
    
    n = "6" # as it is string and it doesn't satisfy the argument type of the function, it will throw an error
    validate(n)
    
    n = "nine" # as it is string and it doesn't satisfy the argument type of the function, it will throw an error
    validate(n)
    
if __name__ == "__main__":
    main()