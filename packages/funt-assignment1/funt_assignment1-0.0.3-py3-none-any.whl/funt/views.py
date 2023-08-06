from flask import render_template, request, redirect, Blueprint
import numpy as np
import sqlalchemy

from funt.model import Exam, db


bp = Blueprint('views', __name__)


@bp.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        exam_name = request.form['courseName']
        exam_grade = request.form['examMark']
        new_exam = Exam(name=exam_name, grade=exam_grade)
        try:
            db.session.add(new_exam)
            db.session.commit()
            db.session.close()
            return redirect('/')
        except sqlalchemy.exc.SQLAlchemyError:
            return 'There was an issue adding your exam'
    else:
        exams = db.session.query(Exam).order_by(Exam.date_created).all()
        return render_template("index.html", exams=exams)


@bp.route("/grades-mean", methods=['GET'])
def mean():
    exams = db.session.query(Exam).order_by(Exam.date_created).all()
    grades = []
    for e in exams:
        grades.append(int(e.grade))
    grades_mean = round(np.mean(grades), 2)
    return render_template("mean.html", mean=grades_mean)


@bp.route("/clear-db", methods=['GET'])
def clear_db():
    db.drop_all()
    db.create_all()
    return redirect('/')
