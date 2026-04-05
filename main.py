from flask import Flask, render_template,flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from form import FeedbackForm, LoginrForm, RegisterForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:iDiSTVicNDmtzLEghUfcLalxSMrJAHMJ@autorack.proxy.rlwy.net:24365/railway"
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "SECRET_KEY"
login_manager = LoginManager(app)
login_manager.login_view =  "login"
login_manager.login_message =  "info"

# ============ MODELS ===============

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='feedbacks')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    form= RegisterForm()

    if form.validate_on_submit():
        new_user= User(
            username= form.username.data,
            email= form.email.data,
            password= form.password.data
        )

        db.session.add(new_user)
        db.session.commit()

        flash(f"Account created succesfull, You can login now", "success")
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form= LoginrForm()
    
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()

        if user and user.password == form.password.data :
            login_user(user)
        
            flash("login succesfully", "success")

            if user.username == "admin":
                return redirect(url_for('admin'))
            
            return redirect(url_for("dashboard"))

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You hav been logout out")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    fb= Feedback.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", name=current_user.username, feedback=fb)

@app.route("/admin")
@login_required
def admin():
    if current_user.username != "admin" :
        return "access denied", 403
    
    users= User.query.all()
    feedbacks= Feedback.query.all()

    return render_template("admin.html", users=users, feedbacks=feedbacks)

@app.route("/add_feedback", methods=["GET","POST"])
@login_required
def add_feedback():
    form= FeedbackForm()

    if form.validate_on_submit():
        new_feedback= Feedback(
            title= form.title.data,
            content= form.content.data,
            user_id= current_user.id
        )
        db.session.add(new_feedback)
        db.session.commit()

        flash("feedback submited successfully", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_feedback.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)