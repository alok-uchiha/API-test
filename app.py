from flask import Flask, render_template, flash, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from forms import RegisterForm, LoginForm, FeedbackForm


#configation

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/project_01'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#models

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(20), nullable=False, unique= True)
    email = db.Column(db.String(30), nullable=False, unique= True)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"user('{self.username}', '{self.email}')"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='feedbacks')

    def __repr__(self):
        return f"Feedback('{self.title}', by '{self.user.username}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#routes

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_passowrd= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    
        new_user= User(
            username= form.username.data,
            email= form.email.data,
            password = hashed_passowrd
        )

        db.session.add(new_user)
        db.session.commit()

        flash("account created successfully for {form.username.data}, you can login now!", "success")
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("login successfully", "success")
            return redirect(url_for('home'))

        else:
            flash("login failed!!. check your email and passowrd", "danger")

    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("your have been loged out", "info")
    return redirect(url_for('login'))


@app.route("/add_feedback", methods=["GET", "POST"])
@login_required
def add_feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        new_feedback= Feedback(
            title= form.title.data,
            content= form.content.data,
            user_id= current_user.id
        )
        db.session.add(new_feedback)
        db.session.commit()
        flash("Feedback added successfull", "success")
        return redirect(url_for('feedback'))
    return render_template("add_feedback.html", form=form)


@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    user_feedback= Feedback.query.filter_by(user_id=current_user.id).all()
    return render_template("feedback.html", name= current_user.username, fb=user_feedback)


@app.route("/api/feedback", methods= ["GET"])
@login_required
def get_feedback():
    fb = Feedback.query.filter_by(user_id=current_user.id).all()

    data =[]

    for f in fb:
        data.append({
            "id" : f.id,
            "title" : f.title,
            "content" : f.content
        })
    return jsonify({
        "user" : current_user.username,
        "feedback_count" : len(data),
        "feedback" : data
    }),200

 
# @app.route("/api/send_feedback", methods=["GET", "POST"])
# @login_required
# def send_feedback():

#     data= request.get_json()

#     if not data:
#         return jsonify({"error": "NO json data found"}),400

#     title= data.get('title')
#     content= data.get('content')

#     if not title or not content:
#         return jsonify({"error": "Missing title or content"}),400
    
#     feedback = {
#         "title": title,
#         "content": content
#         }
    
#     return jsonify({
#         "Message": "Feedback added Successfully",
#         "Feedback": feedback
#     }),201





if __name__ == "__main__":
    app.run(debug=True)