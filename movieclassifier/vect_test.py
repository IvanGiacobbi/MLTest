import pickle
import re
import os
from vectorizer import vect
#deserializziamo il classificatore
cur_dir=os.path.dirname('/home/ivan/data_science/ML/movieclassifier/')
clf=pickle.load(open(os.path.join(cur_dir,'pkl_objects','classifier.pkl'),'rb'))
#testiamo il classificatore
import numpy as np
label={0:'negativa', 1:'positiva'}
example=['I love this movie']
#vettorizziamo il documento in modo da trasformarlo in un vettore di word
X=vect.transform(example)
#predict_proba restituisce un vettore di probabilità per ogni classe label quindi usiamo np.max per avere il valore massimo del vettore
print ('Predizione: %s\nProbabilità: %.2f%%' %\
        (label[clf.predict(X)[0]],
        np.max(clf.predict_proba(X))*100))
