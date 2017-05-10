from keras.models import Sequential
import numpy as np
from keras.layers.recurrent import LSTM
from keras.layers.core import TimeDistributedDense, Activation
from keras.preprocessing.sequence import pad_sequences
from keras.layers.embeddings import Embedding
from keras.layers import Merge
from keras.layers import Dropout
from keras.layers.wrappers import Bidirectional
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import seq2seq
import unicodedata

Train_file="ned.FullTrain"
Test_file="ned.testb"

#############################################################################################3
def Max_Val_Cal(Doc1):
    raw = open(Doc1, 'r',encoding="ISO-8859-1").readlines()
    all_x = []
    point = []
    for line in raw:
        stripped_line = line.strip().split(' ')
        point.append(stripped_line)
        if line == '\n':
           all_x.append(point[:-1])
           point = []
    lengths = [len(x) for x in all_x]
    return max(lengths)

Train_Max=Max_Val_Cal(Train_file)
Test_Max=Max_Val_Cal(Test_file)
maxlen=max(Train_Max,Test_Max)
#maxlen=250

#############################################################################################3
### TRAINING DATA   ### TRAINING DATA   ### TRAINING DATA  ### TRAINING DATA

raw = open(Train_file, 'r',encoding="ISO-8859-1").readlines()
all_x = []
point = []
for line in raw:
    stripped_line = line.strip().split(' ')
    point.append(stripped_line)
    if line == '\n':
       all_x.append(point[:-1])
       point = []    
    
X = [[c[0] for c in x] for x in all_x]
y = [[c[2] for c in y] for y in all_x]
POS_tags = [[c[1] for c in z] for z in all_x]

Letter_case=[[[unicodedata.category(c) for c in words1] for words1 in sent] for sent in X]
for ind0 in range(len(Letter_case)):
    for ind1 in range(len(Letter_case[ind0])):
        Letter_case[ind0][ind1]=''.join(Letter_case[ind0][ind1])

all_text = [c for x in X for c in x]
words = list(set(all_text))
word2ind = {word: index+1 for index, word in enumerate(words)}
ind2word = {index+1: word for index, word in enumerate(words)}

labels = list(set([c for x in y for c in x]))    
label2ind = {label: (index) for index, label in enumerate(labels)}
ind2label = {(index): label for index, label in enumerate(labels)}
    
POS_labels = list(set([c for x in POS_tags for c in x]))
POSlabel2ind = {label: (index) for index, label in enumerate(POS_labels)}
POSind2label = {(index): label for index, label in enumerate(POS_labels)}

Word_case = [c for x in Letter_case for c in x]
Case_labels = list(set(Word_case))
Caselabel2ind = {label: (index) for index, label in enumerate(Case_labels)}
Caseind2label = {(index): label for index, label in enumerate(Case_labels)}



def encode(x, n):
    result = np.zeros(n)
    result[x] = 1
    return result
X_enc = [[word2ind[c] for c in x] for x in X]
POS_enc=[[POSlabel2ind[c] for c in rand] for rand in POS_tags]

max_label = max(label2ind.values())+1
max_POS_label = max(POSlabel2ind.values())+1

X_enc_f = pad_sequences(X_enc, maxlen=maxlen)
POS_enc_M = pad_sequences(POS_enc, maxlen=maxlen)

Case_enc = [[Caselabel2ind[c] for c in rand] for rand in Letter_case]
Case_enc = pad_sequences(Case_enc, maxlen=maxlen)

y_enc = [[label2ind[c] for c in ey] for ey in y]
y_enc = [[encode(c, max_label) for c in ey] for ey in y_enc]
y_enc = pad_sequences(y_enc, maxlen=maxlen)

X_train_f=X_enc_f
y_train=y_enc
POS_enc_train=POS_enc_M
POSl2i_train=POSlabel2ind
Case_enc_train=Case_enc
Casel2i_train=Caselabel2ind

#############################################################################################3
### TESTING DATA   ### TESTING DATA   ### TESTING DATA  ### TESTING DATA
    
raw = open(Test_file, 'r',encoding="ISO-8859-1").readlines()
all_x = []
point = []
Words_inLines=[]
for line in raw:
    stripped_line = line.strip().split(' ')
    point.append(stripped_line)
    if line == '\n':
       Words_inLines.append(len(point)-1)  ## -1 because we are counting blank line as an element in the list. So for removing it, -1 is required.
       all_x.append(point[:-1])
       point = []    
    
X_t = [[c[0] for c in x] for x in all_x]
y_t = [[c[2] for c in y] for y in all_x]
POS_tags_test = [[c[1] for c in z] for z in all_x]
Testlabels = list(set([c for x in y for c in x]))

##############################################
Letter_case_t=[[[unicodedata.category(c) for c in words2] for words2 in sent] for sent in X_t]
for ind0 in range(len(Letter_case_t)):
    for ind1 in range(len(Letter_case_t[ind0])):
        Letter_case_t[ind0][ind1]=''.join(Letter_case_t[ind0][ind1])

Word_case_t = [c for x in Letter_case_t for c in x]
Case_labels_t = list(set(Word_case_t))

LastCaseIndex=max(Caseind2label)
Test_Case2ind={}

for i in range(len(Case_labels_t)):
    if Case_labels_t[i] in Case_labels:
       Test_Case2ind.update({Case_labels_t[i]: Case_labels.index(Case_labels_t[i])})
    else:
       Test_Case2ind.update({Case_labels_t[i]: LastCaseIndex+1})
       LastCaseIndex=LastCaseIndex+1 
       

################################################
all_text = [c for x in X_t for c in x]
words1 = list(set(all_text))
LastIndex=max(ind2word)
words1_2ind={}
Dict_count=0
for i in range(len(words1)):
    if words1[i] in words:       
       words1_2ind.update({words1[i]: words.index(words1[i])+1})
       Dict_count=Dict_count+1
    else:
       words1_2ind.update({words1[i]: LastIndex+1})
       LastIndex=LastIndex+1  


##################################### Not used anywhere
LastLabelIndex=max(ind2label)
Test_label2ind=[]
for i in range(len(Testlabels)):
    if Testlabels[i] in labels:
       Test_label2ind.append({Testlabels[i]:labels.index(Testlabels[i])})
    else:
       Test_label2ind.append({Testlabels[i]:LastLabelIndex+1})
       LastLabelIndex=LastLabelIndex+1  
###########################################

POS_Test = list(set([c for x in POS_tags_test for c in x]))
LastPOSIndex=max(POSind2label)
Test_POS2ind={}

for i in range(len(POS_Test)):
    if POS_Test[i] in POS_labels:
       Test_POS2ind.update({POS_Test[i]: POS_labels.index(POS_Test[i])})
    else:
       Test_POS2ind.update({POS_Test[i]: LastPOSIndex+1})
       LastPOSIndex=LastPOSIndex+1 
###################################################


X_enc_test = [[words1_2ind[c] for c in x] for x in X_t]
POS_enc_test=[[Test_POS2ind[c] for c in rand] for rand in POS_tags_test]
Case_enc_test=[[Test_Case2ind[c] for c in rand] for rand in Letter_case_t]

y_enc_t = [[label2ind[c] for c in ey] for ey in y_t]
y_enc_t = [[encode(c, max_label) for c in ey] for ey in y_enc_t]
y_enc_t = pad_sequences(y_enc_t, maxlen=maxlen)


X_test_f = pad_sequences(X_enc_test, maxlen=maxlen)
POS_enc_test = pad_sequences(POS_enc_test, maxlen=maxlen)
Case_enc_test = pad_sequences(Case_enc_test, maxlen=maxlen)

######################################################################################################


max_features = 1+max(max(word2ind.values()),max(words1_2ind.values())) ## doubt - why maxfeatures is taken len of indices
max_features_POS = 2+max(POSl2i_train.values())  ## POSl2i will be same for train and test both. Worst cases- test data will contain lesser number of tags.
max_features_case = 2+max(max(Casel2i_train.values()),max(Test_Case2ind.values())) 

# max_features = len(word2ind)
# out_size = len(label2ind) + 1
embedding_size = 256
embedding_size_POS = 32
embedding_size_case = 128
inputdim=embedding_size+embedding_size_POS  #+embedding_size_case

hidden_size = 64
out_size = max(label2ind.values())+1

model_forward = Sequential()
model_forward.add(Embedding(max_features, embedding_size, input_length=maxlen, mask_zero=True))

model_POS = Sequential()
model_POS.add(Embedding(max_features_POS, embedding_size_POS, input_length=maxlen, mask_zero=True))

model_case= Sequential()
model_case.add(Embedding(max_features_case, embedding_size_case, input_length=maxlen, mask_zero=True))

Final_model = Sequential()
Final_model.add(Merge([model_forward, model_POS, model_case], mode='concat')) # 





Final_model.add(Bidirectional(LSTM(hidden_size, return_sequences=True)))

Final_model.add(Dropout(0.15))  
Final_model.add(TimeDistributedDense(out_size))

Final_model.add(Activation('softmax'))

#Final_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['precision', 'recall','fbeta_score','accuracy'])
Final_model.compile(loss='mse', optimizer='rmsprop')
batch_size = 32


# model.fit(X, Y, validation_split=0.33, nb_epoch=150, batch_size=10, validation_split=0.15, callbacks=callbacks_list, verbose=0)

Final_model.fit([X_train_f,POS_enc_train,Case_enc_train], y_train, batch_size=batch_size, nb_epoch=18) #5  #,Case_enc_train

# score1 = model_forward.evaluate(X_test_f, y_test, batch_size=batch_size)

pr = Final_model.predict_classes([X_test_f,POS_enc_test,Case_enc_test]) 

yh = y_enc_t.argmax(2)

thefile = open('PredFile_8tags_18', 'w')

for i in range(len(Words_inLines)):
    pred=pr[i][-Words_inLines[i]:]
    for pred_val in pred:
        thefile.write("%s\n" %ind2label[pred_val])
    thefile.write("\n")    


