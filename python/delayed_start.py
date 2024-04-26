import subprocess
import time

count = 0
while count < 100:
    count += 1 
    subprocess.run(["C:\\Users\\Whom\\Desktop\\Git\\next-writers-almanac\\python\\venv\\scripts\\python", "inference.py", str(count)])
     


