import unicodedata

def Dict_develop(File):
    all_x = []
    point = []
    for line in File:
        stripped_line = line.strip().split(' ')
        for i in stripped_line:
            point.append(i)
    vocab = set(point)
    return vocab

# Dict from training file.
raw1 = open("Train_Fullinput120", 'r').readlines()
Dict1=Dict_develop(raw1)

# Dict from test file.
raw2 = open("Test_Fullinput120", 'r').readlines()
Dict2=Dict_develop(raw2)

print (len(Dict1))
print (len(Dict2))

vocab1=list(Dict1.union(Dict2))

File1=open("FullIntputvocab1",'w')
for i1 in vocab1:
    File1.write("%s\n" % i1)
         


