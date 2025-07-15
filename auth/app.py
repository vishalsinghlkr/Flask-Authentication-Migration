from flask import Flask,request,render_template,redirect, session
from flask_sqlalchemy import SQLAlchemy   #what is the error here?

import bcrypt # Import bcrypt for password hashing   

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db= SQLAlchemy(app)
app.secret_key= 'your_secret_key'  # Set a secret key for session management

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


    def __init__(self,email, password,name):

        self.name = name
        self.email = email
        self.password =bcrypt.hashpw( password.encode('utf-8'), bcrypt.gensalt()) # Hash the password
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
    
with app.app_context():
    db.create_all()  # Create database tables


@app.route('/')
def home():
    return "Welcome to the Auth App!"

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # Logic for user registration
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
        
    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return redirect('loin.html',error="invalid user")  # Redirect to login page if credentials are incorrect

       
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if session['name']:
        user= User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    return redirect('/login')
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')
if __name__ == '__main__':
    app.run(debug=True)