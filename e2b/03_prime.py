from dotenv import load_dotenv
load_dotenv()
from e2b_code_interpreter import Sandbox

sdb = Sandbox.create() # Creates a persistent sandbox session

code = """
def is_prime(n):
    if n <= 1:
        print(f"{n} is not a prime number")
        return

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            print(f"{n} is not a prime number")
            return

    print(f"{n} is a prime number")

is_prime(17)
is_prime(18)
"""
sdb.files.write(
    "/home/user/prime.py",
    code.encode()
)
result = sdb.commands.run(
    "python /home/user/prime.py"
)   
print(result.stdout)
