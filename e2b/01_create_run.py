# main.py
from dotenv import load_dotenv
load_dotenv()
from e2b_code_interpreter import Sandbox
sbx = Sandbox.create() # Creates a persistent sandbox session
execution = sbx.run_code("print('hello world')") # Execute Python inside the sandbox
print(execution.logs)
print("---------")
print(execution.results)
print("---------")
files = sbx.files.list("/project")
print(files)
