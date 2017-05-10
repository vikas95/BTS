import unicodedata
raw = open("Train_Fulloutput120", 'r').readlines()
all_x = []
point = []
for line in raw:
    stripped_line = line.strip().split(' ')
    for i in stripped_line:
        point.append(i)
print (len(point))

vocab = list(set(point))


File1=open("FullOutputvocab1",'w')
for i1 in vocab:
    File1.write("%s\n" % i1)
         


