import subprocess
import json
import random

count = 10

while count < 1583:
    count += 1
    poemNumber = str(random.randint(1, 6548))
    authorNumber = str(count) #str(random.randint(1, 1583))
    dayNumber = str(random.randint(1, 9098))
    subprocess.run(["/home/ec2-user/huggingface/venv/bin/python", "inference_biography_without_research.py" , str(count), poemNumber, authorNumber, dayNumber])