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



############
#  Building Vocab for the tag
################
raw = open("ned.testa", 'r').readlines()
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
label2ind = {label: (index) for index, label in enumerate(labels)}
ind2label = {(index): label for index, label in enumerate(labels)}


labels = list(set([c for x in y for c in x]))
labels2ind = {label: (index) for index,label in enumerate(labels)}
"""
    File2=open("Outputvocab",'w')
    for i in range(len(labels2ind)):
    File2.write("%s\n" % i)
    
    """
#####################################

ind=0
Start=0
Span=0
Curr_Pos=0
char=""
char1=""
Slid_Wind=30
SeqLen=60
NextLine=[]

# print str(Word_array[10])+str(Word_array[11])
with open('ned.testa') as fileobject:      ## This is for the 3rd model, when we are creating a multilingual dataset by combining Dutch and
    for ind4,line in enumerate(fileobject):
        #print line + "\n"
        words = list(line.split())
 
        
        if len(words)>0:
        # print words
        
           if Curr_Pos>Slid_Wind-1 and len(words[0])<SeqLen-Curr_Pos:    # This is if sliding window is 30
              NextLine.append(line)
           
                    

           if len(char)+len(words[0])<SeqLen:
              for ch in words[0]:
                  char=char+str(ord(ch))+space
              char=char+"_"+space
              if words[2]!='O':
                 tag= words[2]
                 Start=Curr_Pos
                 Span=len(words[0])+1
                 temp_tag=temp_tag+("S"+str(Start))+space+("L"+str(Span))+space+str(labels2ind[tag])+space
              Curr_Pos=Curr_Pos+len(words[0])+2
                  

    
           else:
               if ind4!=1:
                  for line1 in NextLine:
                      words1=list(line1.split())
                      for ch1 in words1[0]:
                          char1=char1+str(ord(ch1))+space
                      char1=char1+"_"+space
                   
                      if words1[2]!='O':
                         tag= words[2]
                         Start=Curr_Pos
                         Span=len(words1[0])+1
                         temp_tag=temp_tag+("S"+str(Start))+space+("L"+str(Span))+space+str(labels2ind[tag])+space
                      Curr_Pos=Curr_Pos+len(words1[0])+2
                  NextLine=[]
                  temp_line=temp_line+char1+char
               else:
                  temp_line=temp_line+char
        
               with open("Test_input5_60", "a") as myfile:
                    myfile.write(temp_line+"GO"+"\n")
            
               with open("Test_output5_60", "a") as myfile:
                   if len(temp_tag)<1:
                      temp_tag="STOP"
                      myfile.write(temp_tag+"\n")
                   else:
                      myfile.write(temp_tag+"STOP"+"\n")
            
               temp_line=""
               char=""
               char1=""
               temp_tag=""
               Curr_Pos=0


                          
               if len(words[0])<SeqLen-Curr_Pos:
                  for ch in words[0]:
                      char=char+str(ord(ch))+space
                  char=char+"_"+space
               
                  if words[2]!='O':
                     tag= words[2]
                     Start=Curr_Pos
                     Span=len(words[0])+1
                     temp_tag=temp_tag+("S"+str(Start))+space+("L"+str(Span))+space+str(labels2ind[tag])+space
                  Curr_Pos=Curr_Pos+len(words[0])+2
               else:
                   temp_line=temp_line+char
                   with open("Test_input5_60", "a") as myfile:
                        myfile.write(temp_line+"GO"+"\n")
                   with open("Test_output5_60", "a") as myfile:
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
                      temp_tag=temp_tag+("S"+str(Start))+space+("L"+str(Span))+space+str(labels2ind[tag])+space
                   Curr_Pos=Curr_Pos+len(words[0])+2
    
        else:
           char=char+"new"+space

            
          


