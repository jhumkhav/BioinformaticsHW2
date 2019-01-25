import re

file = open("reference.fasta", "r")
for line in file:
    line = line.split()
    if len(line) ==0:
        f.close()
    elif line[0][0] == ">":
        match = re.sub('\W', "", line[0][1:])
        f = open(match+".fasta", "w")
    else:
        f.write(line[0])
f.close()
