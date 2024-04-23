import subprocess
import time

count = 50
while count < 1563:
    count += 1 
    subprocess.run(["C:\\Users\\Whom\\Desktop\\Git\\next-writers-almanac\\python\\venv\\scripts\\python", "inference.py", str(count)])
    time.sleep(120)  


