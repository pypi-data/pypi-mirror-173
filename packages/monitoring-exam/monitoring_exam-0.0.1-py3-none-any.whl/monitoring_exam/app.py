import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
test  = False
def is_test():
    global test
    test = True
    
class Exam(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Matricola = db.Column(db.String(7), nullable=False)
    Nome_esame = db.Column(db.String(100), nullable=False)
    Voto = db.Column(db.Integer, nullable=False)
    Data = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    #consente di assegnare a ciascun oggetto una rappresentazione di stringa per riconoscerlo a scopo di debug
    def __repr__(self):
        return f'<Exam {self.Matricola}>'

@app.route('/')
def index():
    exams = Exam.query.all()
    return render_template('index.html', exams=exams)


@app.route('/getexam/')
def get_exam(exam_id):
    with app.app_context(), app.test_request_context():
        return Exam.query.get(exam_id)


@app.route('/<int:exam_id>/')
def exam(exam_id):
    exam =  Exam.query.get_or_404(exam_id)
    return render_template('exam.html', exam=exam)


def check_voto(voto):
    if 17<voto<31:
        return True
    return False


@app.route('/create/', methods=('GET', 'POST'))
def create():
    global test
    if  test:
        if not (get_exam("0")):
            with app.app_context(), app.test_request_context():
                Id = "0"
                Matricola = "000"
                Nome_esame = "Test_esame"
                Voto = 0
                exam = Exam(Id = Id,
                            Matricola=Matricola,
                            Nome_esame=Nome_esame,
                            Voto=Voto)
                db.session.add(exam)
                db.session.commit()
                test = False
                return True
    elif request.method == 'POST':
        Matricola = request.form['Matricola']
        Nome_esame = request.form['Nome_esame']
        Voto = int(request.form['Voto'])
        if check_voto(Voto):
            exam = Exam(Matricola=Matricola,
                          Nome_esame=Nome_esame,
                          Voto=Voto)
        else:
            print("hai inserito un voto non valido, inserisco 0")
            exam = Exam(Matricola=Matricola,
                            Nome_esame=Nome_esame,
                            Voto=0)
        db.session.add(exam)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:exam_id>/edit/', methods=('GET', 'POST'))
def edit(exam_id):
    
    global test
    if  test:
        if get_exam("0"):
            print("ho trovato l'esame, lo modifico")
            with app.app_context(), app.test_request_context():
                exam = Exam.query.get_or_404(exam_id)
                Matricola = "000"
                Nome_esame = "Test_esame_modified"
                Voto = 0
                exam.Matricola = Matricola
                exam.Nome_esame = Nome_esame
                exam.Voto = Voto

                db.session.add(exam)
                db.session.commit()
                test = False
                return True
    elif request.method == 'POST':
        exam = Exam.query.get_or_404(exam_id)
        Matricola = request.form['Matricola']
        Nome_esame = request.form['Nome_esame']
        Voto = int(request.form['Voto'])

        exam.Matricola = Matricola
        exam.Nome_esame = Nome_esame
        if check_voto(Voto):
           
            exam.Voto = Voto
        else:
            print("hai inserito un voto non valido, inserisco 0")
            exam.voto = 0

        db.session.add(exam)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', exam=exam)


@app.route('/<int:exam_id>/delete/', methods=('GET', 'POST'))
def delete(exam_id):
    global test
    if  test:
        if get_exam("0"):
            with app.app_context(), app.test_request_context():
                exam = Exam.query.get_or_404(exam_id)
                db.session.delete(exam)
                db.session.commit()
                test = False
                return True
    elif request.method == 'POST':
        with app.app_context(), app.test_request_context():
            exam = Exam.query.get_or_404(exam_id)
            db.session.delete(exam)
            db.session.commit()
            return redirect(url_for('index'))
    return (url_for('index'))



if __name__ == "__main__":
    app.run()
    
