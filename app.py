# from flask import Flask,render_template
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db=SQLAlchemy(app)


# class Todo(db.Model):
#     sno=db.Column(db.Integer,primary_key=True)
#     title =db.Column(db.String(200),nullable=False)
#     desc =db.Column(db.String(500),nullable=False)
#     date_created=db.Column(db.DateTime,default=datetime.utcnow)

#     def __repr__(self)->str:
#         return f"{self.sno}-{self.title}"

# @app.route('/')
# def hello_world():
#     return render_template('index.html')
#     # return 'Hello, World!'

# @app.route('/products')
# def products():
#     return 'this is products page!'

# if __name__=="__main__":
#     app.run(debug=True)


from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"

# Define a function to create the database tables
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method =='POST':
        title=request.form['title']
        desc=request.form['desc']


        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltoDo=Todo.query.all()
    # print(alltoDo)
    return render_template('index.html',alltoDo=alltoDo)
   

@app.route('/show')
def products():
    alltoDo=Todo.query.all()
    print(alltoDo)
    return 'new'

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        toDo=Todo.query.filter_by(sno=sno).first()
        toDo.title=title
        toDo.desc=desc
        db.session.add(toDo)
        db.session.commit()
        return redirect("/")
    
    toDo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',toDo=toDo)

@app.route('/delete/<int:sno>')
def delete(sno):
    toDo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(toDo)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    # Create the database tables before running the app
    create_tables()
    app.run(debug=True)
