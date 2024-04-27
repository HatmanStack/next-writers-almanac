import subprocess
import json

with open('new_data.json', 'r') as f:
    vs_data = json.load(f)

with open('poembyline.json', 'r') as f:
    poets = json.load(f)
    

new = ['Kristal Leebrick', 'Mary Logue', 'Henry King', 'Alan Feldman', 'Amy Fleury', 'Joan Seliger Sidney', 'John Wilmot', 'Mary K. Stillwell', 'Mary K. Stillwell', 'Bartholomew Griffin', 'Michael Lauchlan', 'Bill Mayer', 'Rosalind Brackenbury', 'Rosalind Brackenbury', 'Joseph Green', 'Maureen Ryan Griffin', 'Pauletta Hansel', 'Patrick Hicks', 'Lisa Erin Robertson', 'Jane Hoogestraat', 'Joseph Green', 'Claire Keyes', 'Sonia Greenfield', 'Noel Crook', 'Tony Morris', 'Jane Hoogestraat', 'Claire Keyes', 'Dana Robbins', 'Kareem Tayyar']
count = 0
with open('poembyline.json', 'r', encoding="utf-8") as f:
    poets = json.load(f)

for i in new:
    if poets[i]['poetry foundation'] != "NotAvailable":   
        subprocess.run(["C:\\Users\\Whom\\Desktop\\Git\\next-writers-almanac\\python\\venv\\scripts\\python", "inference.py", str(i)])
          

