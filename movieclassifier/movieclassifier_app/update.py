#il clf viene resettato ad ogni restart del web server. Per evitare questo e tenere traccia dei vari aggiornamenti,
#scarichiamo il database da PythonAnywhere poi con questo script aggiorniamo clf localmente ed eseguiamo il pickle su PythonAnywhere
import pickle
import re
import os
import numpy as np
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import sqlite3

from vectorizer import vect

def update_model (db_path, model, batch_size=10000):
    #identifichiamo il database
    conn = sqlite3.connect(db_path)
    c=conn.cursor()
    c.execute('SELECT * FROM review_db')
    results=c.fetchmany(batch_size)
    while results:
        data=np.array(results)
        X=data[:, 0]
        y=data[:, 1].astype(int)
        classes=np.array([0, 1])
        X_train=vect.transform(X)
        model.partial_fit(X_train, y, classes= classes)
        results= c.fetchmany(batch_size)
    conn.close()
    return model

cur_dir=os.path.dirname('/home/ivan/data_science/ML/movieclassifier/movieclassifier_app/') #probabilmente ci va il percorso di PythonAnywhere
clf=pickle.load(open(os.path.join(cur_dir,'pkl_objects','classifier.pkl'),'rb'))
#identifichiamo il database
db=os.path.join(cur_dir, 'reviews.sqlite')

clf=update_model(db_path=db, model=clf, batch_size=10000)

#decommentare per per eseguire l'update di classifier.plk permanentemente
#pickle.dump(clf, open(os.path.join(cur_dir, 'pkl_object', 'classifier.pkl'), 'wb'), protocol=4)
