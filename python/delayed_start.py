import subprocess
import json
import random

count = 0

while count < 10000:
    count += 1
    poemNumber = str(random.randint(1, 6548))
    authorNumber = str(random.randint(1, 1583))
    dayNumber = str(random.randint(1, 9098))
    subprocess.run(["/home/ec2-user/huggingface/venv/scripts/python", "fine_tune_inference.py"] + [count, poemNumber, authorNumber, dayNumber])