import random

#create a single string that is the kmer length
def create_string(length):
    string = ""
    for i in range(length):
        string += random.choice(['A','C','T','G'])
    return string

#initialize a dictionary that has length of kmer associated with list of seqs
seq = {}
for i in range(1,11):
    seq[i] = []

#makes all unique seqs for each kmer
def make_seq(num):
    while len(seq[item]) < num:
        string = create_string(item)
        if string not in seq[item]:
            seq[item].append(string)

#sets number of seqs per kmer
for item in seq:
    if item == 1:
        make_seq(4)
    else:
        make_seq(5)

#create string from file
fasta = open("Zmay_chr_9-P-94283818.fa")
string = ''
for line in fasta:
    line = line.strip()
    if line[0] == ">":
        pass
    else:
        for item in line:
            string += item

#find the number of occurrences of seq in fasta
def find_seq(string, substring, length):
    count = 0
    for index in range(len(string)):
        if substring == string[index:index+length]:
            count += 1
    return (count)

solution = {}

#find percentage per seq and percentage probability
for length in seq:
    for item in seq[length]:
        solution[item] = []
        percent = float(find_seq(string, item, length))/(len(string)-(length+1))
        solution[item].append((1/float(4**length)))
        solution[item].append(percent)

for seq in solution:
    print("Sequence: " + str(seq) + "\tProbability: " + str(solution[seq][0]) + "\tOccurrence: " + str(solution[seq][1]))
