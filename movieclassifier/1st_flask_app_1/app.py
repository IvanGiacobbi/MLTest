from flask import Flask, render_template
app=Flask(__name__)#troverà la cartella template nella stessa cartella dove risiede l'app
@app.route('/')#specifichiamo l'URL che lancia l'esecuzione della funzione index
def index(): #la  funzione index mostra firs_app.html
    return render_template('first_app.html')
if __name__=='__main__':
    app.run()#esegue l'app sul server quando lo script è lanciato da un interprete Python
