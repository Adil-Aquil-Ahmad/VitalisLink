from flask import render_template, request, redirect, url_for, flash, session
from User import load_users, save_user, hash_password
from New_Donors import register_donor, load_bookings, save_donor, load_booking
from Existing_Donors import Donors
import hashlib

def register_routes(app):

    @app.route('/')
    def home():
        if 'username' in session:
            return render_template('Home.html', username=session['username'])
        else:
            return render_template('Home.html')

    @app.route('/dashboard')
    def dashboard():
        if 'username' in session:
            Donors.instantiate_from_csv()
            return render_template('Dashboard.html', people=Donors.all, username=session['username'])
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
    def donor_register():
        return register_donor(request, session)

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
        if 'username' not in session:
            flash("You must be logged in to view booking details.", "warning")
            return redirect(url_for('login'))
        
        booking = load_booking(booking_id)
        if not booking:
            flash("Booking not found.", "danger")
            return redirect(url_for('my_bookings'))

        return render_template('view_booking.html', booking=booking[0], username=session.get('username'),)
