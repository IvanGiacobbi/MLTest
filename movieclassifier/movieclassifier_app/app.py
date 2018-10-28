import pickle
import re
import os
import numpy as np
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import sqlite3

from vectorizer import vect
from update import update_model

app=Flask(__name__)#troverà la cartella template nella stessa cartella dove risiede l'app

##Prepariamo il classificatore
#deserializziamo il classificatore
cur_dir=os.path.dirname('/home/ivan/data_science/ML/movieclassifier/moviclassifier_app')
clf=pickle.load(open(os.path.join(cur_dir,'pkl_objects','classifier.pkl'),'rb'))
#identifichiamo il database
db=os.path.join(cur_dir, 'reviews.sqlite')

#classificatore
def classify(document):
    label={0:'negativa', 1:'positiva'}
    #vettorizziamo il documento in modo da trasformarlo in un vettore di word
    X=vect.transform([document])
    #identifichiamo la classe
    y=clf.predict(X)[0]
    proba=np.max(clf.predict_proba(X))
    return label[y], proba

#apprendimento
def train(document, y):
    X=vect.transform([document])
    clf.partial_fit(X, [y])

#inserimento dati in database
def sqlite_entry(path, document, y):
    conn = sqlite3.connect('reviews.sqlite')
    c=conn.cursor()
    c.execute("INSERT INTO review_db"\
            "(review, sentiment, dateRev) VALUES"\
            "(?, ?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()

##Flask
class ReviewForm(Form):
    moviereview=TextAreaField('',[validators.DataRequired(), validators.length(min=15)]) #area di testo: viene controllato se un user introduce un valore valido

@app.route('/')#specifichiamo l'URL che lancia l'esecuzione della funzione index
def index(): #la  funzione index mostra firs_app.html
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)

@app.route('/results', methods=['POST']) #con POST il form viene portato dal server nel body
def results():
    form= ReviewForm(request.form)
    if request.method == 'POST' and form.validate(): #se nel form è inserito qualcosa si visualizza la pagina results
        review=request.form['moviereview']
        y, proba= classify(review)
        return render_template('results.html', content=review, prediction=y, probability=round(proba*100, 2))
    return render_template('reviewform.html', form=form)

@app.route('/thanks', methods=['POST']) #con POST il form viene portato dal server nel body
def feedback():
    feedback= request.form['feedback_button']
    review=request.form['review']
    prediction=request.form['prediction']
    inv_label={'negativa': 0, 'positiva': 1}
    y=inv_label[prediction]
    if feedback == "Sbagliata":
        y= int(not(y))
    train(review, y)
    sqlite_entry(db, review, y)
    return render_template('thanks.html')

if __name__=='__main__':
    # clf=update_model(db_path=db, model=clf, batch_size=10000) #per aggiornare ad ogni avvio dell'app il clf
    app.run(debug=True)#esegue l'app sul server quando lo script è lanciato da un interprete Python in modalità debug
