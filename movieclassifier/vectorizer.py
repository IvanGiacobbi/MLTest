from sklearn.feature_extraction.text import HashingVectorizer
import re
import os
import pickle
#deserializziamo e apriamo in binario le stopwords
cur_dir=os.path.dirname('/home/ivan/data_science/ML/movieclassifier/')
stop=pickle.load(open(os.path.join(cur_dir, 'pkl_objects', 'stopwords.pkl'), 'rb'))
#vettorizazione
def tokenizer(text):
    text=re.sub('<[^>]*>','',text)
    emoticons=re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    text=(re.sub('[\W]+', ' ',text.lower())+' '.join(emoticons).replace('-',''))
    tokenized=[w for w in text.split() if w not in stop]
    return tokenized
vect=HashingVectorizer(decode_error='ignore',
                      n_features=2**21,
                      preprocessor=None,
                      tokenizer=tokenizer)
