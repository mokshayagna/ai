from dotenv import load_dotenv
load_dotenv()
from e2b_code_interpreter import Sandbox

sdb = Sandbox.create()

code = """
print("Hello! This is a test file created by E2B")
"""
sdb.files.write(
    "/home/user/test.py",
    code.encode()
)
result = sdb.commands.run(
    "python /home/user/test.py"
)

print(result.stdout)