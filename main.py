from flask import Flask, render_template
from Blood_Donation_Database import Person  

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/dashboard')
def dashboard():
    Person.instantiate_from_csv()  
    return render_template('Dashboard.html', people=Person.all)  

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/login')
def login():
    return render_template('Login.html')

if __name__ == "__main__":
    app.run(debug=True)
