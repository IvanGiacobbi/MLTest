from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators

app=Flask(__name__)#troverà la cartella template nella stessa cartella dove risiede l'app

class HelloForm(Form):
    sayhello=TextAreaField('',[validators.DataRequired()]) #area di testo: viene controllato se un user introduce un valore valido

@app.route('/')#specifichiamo l'URL che lancia l'esecuzione della funzione index
def index(): #la  funzione index mostra firs_app.html
    form = HelloForm(request.form)
    return render_template('first_app.html', form=form)

@app.route('/hello', methods=['POST']) #con POST il form viene portato dal server nel body
def hello():
    form= HelloForm(request.form)
    if request.method == 'POST' and form.validate(): #se nel form è inserito qualcosa si visualizza la pagina hello
        name=request.form['sayhello']
        return render_template('hello.html', name=name)
    return render_template('first_app.html', form=form)

if __name__=='__main__':
    app.run(debug=True)#esegue l'app sul server quando lo script è lanciato da un interprete Python in modalità debug
