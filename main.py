from flask import Flask, render_template, request, redirect, url_for, flash, session
from Blood_Donation_Database import Person
import csv
import hashlib
import qrcode
from PIL import Image
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'adajsj435a$mKM%6mkls%mlamfo'

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

def save_donor(first_name, middle_name, last_name, age, blood_group, address, city, state, pin_code, donation_date, slot, username, booking_id):
    status = "Confirmed"
    
    with open('Blood_Donors_Database.csv', 'a', newline='') as f:
        fieldnames = [
            'username', 'Booking ID', 'First Name', 'Middle Name', 'Last Name', 
            'Age', 'Blood Group', 'Address', 'City', 'State', 'Pin Code', 
            'Preferred Slot', 'Donation Date', 'Status'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if f.tell() == 0:
            writer.writeheader()
        
        writer.writerow({
            'username': username,
            'Booking ID': booking_id,
            'First Name': first_name,
            'Middle Name': middle_name,
            'Last Name': last_name,
            'Age': age,
            'Blood Group': blood_group,
            'Address': address,
            'City': city,
            'State': state,
            'Pin Code': pin_code,
            'Preferred Slot': slot,
            'Donation Date': donation_date,
            'Status': status
        })

def load_bookings(username):
    bookings = []
    with open('Blood_Donors_Database.csv', newline='') as f:
        reader = csv.DictReader(f)
        for booking in reader:
            if booking['username'] == username:
                bookings.append(booking)
    return bookings

@app.route('/')
def home():
    if 'username' in session:
        return render_template('Home.html', username=session['username'])
    else:
        return render_template('Home.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        Person.instantiate_from_csv()
        return render_template('Dashboard.html', people=Person.all, username=session['username'])
    else:
        flash("Please log in to access the dashboard.")
        return redirect(url_for('login'))

@app.route('/about')
def about():
    if 'username' in session:
        return render_template('About.html', username=session['username'])
    else:
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

@app.route('/donor_register', methods=['GET', 'POST'])
def register_donor():
    if 'username' not in session:
        flash("Please log in to register as a donor.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name', '')
        last_name = request.form['last_name']
        age = request.form['age']
        blood_group = request.form['blood_group']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        pin_code = request.form['pin_code']
        slot = request.form['slot']
        donation_date = request.form['donation_date']
        username = session['username']
        booking_id = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100000000, 999999999)}"


        save_donor(first_name, middle_name, last_name, age, blood_group, address, city, state, pin_code, donation_date, slot, username, booking_id)
        
        status = "Confirmed"
        
        qr_data = f"{first_name} {middle_name} {last_name}, Age: {age}, Blood Group: {blood_group}, Address: {address}, {city}, {state}, {pin_code}, Slot: {slot}, Booking ID: {booking_id}, Date: {donation_date}, Status: {status}"
        qr = qrcode.make(qr_data)
        qr_filename = f"{first_name}_{last_name}_QR.png"
        qr_path = f"static/QR_Codes/{qr_filename}"
        os.makedirs("static/QR_Codes", exist_ok=True)
        qr.save(qr_path)

        booking_html = render_template('donor_booking.html',
                                       booking_id=booking_id, donation_date=donation_date, status=status,
                                       first_name=first_name, middle_name=middle_name, 
                                       last_name=last_name, age=age, blood_group=blood_group, 
                                       address=address, city=city, state=state, 
                                       pin_code=pin_code, slot=slot, qr_filename=qr_filename)
        
        booking_html_filename = f"{booking_id}.html"
        with open(os.path.join('static/Bookings', booking_html_filename), 'w') as f:
            f.write(booking_html)

        return redirect(url_for('view_booking', booking_id=booking_id))
    
    return render_template('Donor_register.html')

@app.route('/my_bookings')
def my_bookings():
    if 'username' in session:
        username = session['username']
        bookings = load_bookings(username)
        status="confirmed"
        return render_template('My_Bookings.html', bookings=bookings, username=username, status=status)
    else:
        flash("Please log in to view your bookings.")
        return redirect(url_for('login'))

@app.route('/view_booking/<booking_id>')
def view_booking(booking_id):
    try:
        return render_template(f"{booking_id}.html")
    except Exception as e:
        flash(f"Error loading booking: {str(e)}", "danger")
        return redirect(url_for('my_bookings'))

print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)
