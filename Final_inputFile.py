# Dataset Conversion

space=' '
temp_line=""
temp_tag=""

ind=0
Start=0
Span=0
Curr_Pos=0
char=""
newchar=""
## if you want to train the first model, change the name if input file below to 'ned.train' or 'esp.train' and same goes with testing data.


InputFile="ned.FullTrain"
############
#  Building Vocab for the tag
################
raw = open(InputFile, 'r').readlines()
all_x = []
point = []
for line in raw:
    stripped_line = line.strip().split(' ')
    point.append(stripped_line)
    if line == '\n':
        all_x.append(point[:-1])
        point = []


y = [[c[2] for c in y] for y in all_x]

labels = list(set([c for x in y for c in x]))
LabInd={"B-PER":1}
LabInd.update({"I-PER":2})
LabInd.update({"B-LOC":3})
LabInd.update({"I-LOC":4})
LabInd.update({"B-ORG":5})
LabInd.update({"I-ORG":6})
LabInd.update({"B-MISC":7})
LabInd.update({"I-MISC":8})

Ind2Label={1:"B-PER"}
Ind2Label.update({2:"I-PER"})
Ind2Label.update({3:"B-LOC"})
Ind2Label.update({4:"I-LOC"})
Ind2Label.update({5:"B-ORG"})
Ind2Label.update({6:"I-ORG"})

Ind2Label.update({7:"B-MISC"})
Ind2Label.update({8:"I-MISC"})



#####################################

ind=0
Start=0
Span=0
Curr_Pos=0
char=""
LineNum=[]
LineInd=0
# print str(Word_array[10])+str(Word_array[11])
with open(InputFile) as fileobject:      ## This is for the 3rd model, when we are creating a multilingual dataset by combining Dutch and
    for line in fileobject:
        #print line + "\n"
        words = list(line.split())
        if len(words)>0:
            # print words
           if len(char)+len(words[0])<120:
              for ch in words[0]:
                  char=char+str(ord(ch))+space
              char=char+"_"+space
              if words[2]!='O':
                 tag= words[2]
                 Start=Curr_Pos
                 Span=len(words[0])+1
                 temp_tag=temp_tag+str(LabInd[tag])+space
           else:
               temp_line=temp_line+char
               with open("Train_Fullinput120", "a") as myfile:
                    myfile.write(temp_line+"GO"+"\n")
               with open("Train_Fulloutput120", "a") as myfile:
                   if len(temp_tag)<1:
                      temp_tag="STOP"
                      myfile.write(temp_tag+"\n")
                   else:
                      myfile.write(temp_tag+"STOP"+"\n")



               temp_line=""
               char=""
               temp_tag=""
               Curr_Pos=0

               for ch in words[0]:
                   char=char+str(ord(ch))+space
               char=char+"_"+space

               if words[2]!='O':
                  tag= words[2]
                  Start=Curr_Pos
                  Span=len(words[0])+1
                  temp_tag=temp_tag+str(LabInd[tag])+space
             
        else:
           char=char+"new"+space




