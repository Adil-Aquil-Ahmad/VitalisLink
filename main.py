from flask import Flask, render_template, request, redirect, url_for, flash, session
from Blood_Donation_Database import Person
import csv
import hashlib

app = Flask(__name__)
app.secret_key = 'adajsj435a$mKM%6mkls%mlamfo' #flash messages storing and session management

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    users = []
    with open('User_Database.csv', newline='') as f:
        reader = csv.DictReader(f)
        for user in reader:
            users.append(user)
    return users

def save_user(username, email, password):
    with open('User_Database.csv', 'a', newline='') as f:
        fieldnames = ['username', 'email', 'password']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow({'username': username, 'email': email, 'password': hash_password(password)})

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        Person.instantiate_from_csv()
        return render_template('Dashboard.html', people=Person.all)
    else:
        flash("Please log in to access the dashboard.")
        return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        
        for user in users:
            if user['username'] == username and user['password'] == hash_password(password):
                session['username'] = username
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
        
        flash("Invalid username or password.", "danger")
        return redirect(url_for('login'))
    
    return render_template('Login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        users = load_users()
        if any(user['username'] == username for user in users):
            flash("Username already taken.", "danger")
            return redirect(url_for('register'))
        
        save_user(username, email, password)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('Register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
