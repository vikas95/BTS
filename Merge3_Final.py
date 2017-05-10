### Merging the results
lines=open("Test_Fullinput120",'r').readlines()
WordCountList=[]
for line1 in lines:
    TotWords=0
    words=line1.split()
    for word1 in words:
        if word1=="_":
           TotWords+=1
    WordCountList.append(TotWords)
    

####### Fusion1 output:

line2=open("new.testb_8",'r').readlines()
BinTags=[]
for line in line2:
    #Words=line.split()
    if line !="\n":
       BinTags.append(line[0]) ## taking just the first character
#print (BinTags[0:4])

line3=open("120_200K.txt","r").readlines()
ind=0
WordInd=0
PredTags=[]
for PredLines in line3:
    PredWords=PredLines.split()
    NumWords=WordCountList[ind]
    #print NumWords
    if len(PredWords)>1:   ## if it is equal to 1, then it is a STOP
       PredTags=PredWords[:-1]
       for tag1 in PredTags:
           # print (BinTags[WordInd:WordInd+NumWords])
           if 'S' in BinTags[WordInd:WordInd+NumWords]:
              # print (BinTags[WordInd:WordInd+NumWords])
              index=BinTags[WordInd:WordInd+NumWords].index('S')
              BinTags[WordInd+index]=tag1
       PredTags=[]
       PredWords=[]
    WordInd+=NumWords
    ind+=1

#### The remaining "S" is replaced by "O" and 1-7 are being replaced by B-PER and so on..

#ind2label = {(index): label for index, label in enumerate(labels)}
Ind2Label={1:"B-PER"}
Ind2Label.update({3:"B-LOC"})
Ind2Label.update({5:"B-ORG"})
Ind2Label.update({7:"B-MISC"})

Ind2Label.update({2:"I-PER"})
Ind2Label.update({4:"I-LOC"})
Ind2Label.update({6:"I-ORG"})
Ind2Label.update({8:"I-MISC"})

    
NewBinTags=[]
for tags2 in BinTags:
    if tags2=="S":
       NewBinTags.append("O")
    elif tags2=="O" : 
       NewBinTags.append("O")
    else:
       NewBinTags.append(Ind2Label[int(tags2)])

# print NewBinTags


Space=" "       
ind4=0
with open('ned.testb') as fileobject:
    for line in fileobject:                ## Spanish
        #print line + "\n"
        words = list(line.split())
        # print words
        if len(words)>1:
           new_line=words[0]+Space+words[1]+Space+words[2]+Space+str("".join(NewBinTags[ind4]))
           ind4=ind4+1
           with open("120_200K_8", "a") as myfile:
                myfile.write(new_line+"\n")
           new_line=[]
        else:
             
            with open("120_200K_8", "a") as myfile:
                 myfile.write("\n")
          



