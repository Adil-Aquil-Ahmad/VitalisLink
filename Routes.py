from flask import render_template, request, redirect, url_for, flash, session
from User import load_users, save_user, hash_password, load_user_data, save_user_data
from New_Donors import register_donor, load_bookings, save_donor, load_booking, Create_PDF, getbookings
from Existing_Donors import Donors
import hashlib
import random
import csv
import os
from werkzeug.utils import secure_filename
import pdfkit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email_with_pdf(PDF_Filename):
    try:

        recipient_email = session.get('email')
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('EMAIL_PASSWORD')

        if not sender_email or not sender_password:
            raise ValueError("Environment variables SENDER_EMAIL or EMAIL_PASSWORD are not set.")
        if not recipient_email:
            raise ValueError("Recipient email not found in session.")

        subject = "Booking Confirmation - VitalisLink"
        body = "Hi! Please find your booking confirmation attached as a PDF."
        
        os.makedirs(os.path.dirname(PDF_Filename), exist_ok=True)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with open(PDF_Filename, 'rb') as attachment:
            part = MIMEBase('application', 'pdf')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(PDF_Filename)}')
            msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        return f"Booking confirmation PDF sent successfully to {recipient_email}."
    except Exception as e:
        return f"Error: {e}"

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
            Donors.instantiate_from_csv('Blood_Collection_Database.csv')
            return render_template('Dashboard.html', people=Donors.all, username=session['username'], latitude=session['latitude'], longitude=session['longitude'], blood_group=session['blood_group'])
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
            user_type = request.form.get('user_type')
            users = load_users()
            
            for user in users:
                if user['username'] == username and user['password'] == hash_password(password):
                    session['username'] = username
                    session['email'] = user['email']
                    session['user_type'] = user_type  
                    
                    user_data = load_user_data(username)
                    session['longitude'] = user_data.get('Longitude', None)
                    session['latitude'] = user_data.get('Latitude', None)
                    session['blood_group'] = user_data.get('Blood Group', None)
                    
                    flash("Login successful!", "success")
                    if user_type == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    else:
                        return redirect(url_for('my_profile'))
            
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
        booking_id = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100000000, 999999999)}"
        return register_donor(request, session, booking_id)

    @app.route('/my_bookings')
    def my_bookings():
        if 'username' in session and session.get('user_type') == 'admin':
            username = session['username']
            bookings = load_bookings(username)
            status="confirmed"
            return render_template('My_bookings.html', bookings=bookings, username=username, status=status)
        elif 'username' in session:
            username = session['username']
            bookings = load_bookings(username)
            status="confirmed"
            return render_template('My_bookings.html', bookings=bookings, username=username, status=status)
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

        return render_template('View_booking.html', booking=booking[0], username=session.get('username'),)
    
    @app.route('/send_email/<booking_id>')
    def send_email(booking_id):
        booking = load_booking(booking_id)
        if not booking:
            return "Booking not found", 404

        try:
            sender_email = os.getenv('SENDER_EMAIL')
            sender_password = os.getenv('EMAIL_PASSWORD')
            print(f"SENDER_EMAIL: {sender_email}, EMAIL_PASSWORD: {sender_password}")
            email = session.get('email')
            PDF_Filename = Create_PDF(booking_id, booking[0])
            send_email_with_pdf(PDF_Filename)
            return "Email sent successfully", 200
        except Exception as e:
            print(f"Error sending email: {e}")
            return "Failed to send email", 500

    @app.route('/myprofile', methods=['GET', 'POST'])
    def my_profile():
        if 'username' not in session:
            flash("You need to log in to view your profile.", "danger")
            return redirect(url_for('login'))

        username = session['username']
        user_data = load_user_data(username)
        if not user_data:
            flash("Profile not found.", "danger")
            return redirect(url_for('dashboard'))

        return render_template(
            'MyProfile.html',
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['First Name'],
            middle_name=user_data['Middle Name'],
            last_name=user_data['Last Name'],
            age=user_data['Age'],
            blood_group=user_data['Blood Group'],
            address=user_data['Address'],
            city=user_data['City'],
            state=user_data['State'],
            pin_code=user_data['Pin Code'],
        )
    
    @app.route('/update_profile', methods=['POST'])
    def update_profile():
        if 'username' not in session:
            flash("You need to log in to view your profile.", "danger")
            return redirect(url_for('login'))

        username = session['username']
        user_data = load_user_data(username)
        if not user_data:
            flash("Profile not found.", "danger")
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            user_data['First Name'] = request.form.get('first_name', user_data['First Name'])
            user_data['Middle Name'] = request.form.get('middle_name', user_data['First Name'])
            user_data['Last Name'] = request.form.get('last_name', user_data['First Name'])
            user_data['Age'] = request.form.get('age', user_data['First Name'])
            user_data['Address'] = request.form.get('address', user_data['Address'])
            user_data['City'] = request.form.get('city', user_data['City'])
            user_data['State'] = request.form.get('state', user_data['State'])
            user_data['Pin Code'] = request.form.get('pin_code', user_data['Pin Code'])
            user_data['Blood Group'] = request.form.get('blood_group', user_data['Blood Group'])
            user_data['Longitude'] = request.form.get('longitude', user_data['Longitude'])
            user_data['Latitude'] = request.form.get('latitude', user_data['Latitude'])

            save_user_data(user_data) 
            flash("Profile updated successfully!", "success")
            return redirect(url_for('my_profile'))

        return render_template(
            'MyProfile.html',
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['First Name'],
            middle_name=user_data['Middle Name'],
            last_name=user_data['Last Name'],
            age=user_data['Age'],
            blood_group=user_data['Blood Group'],
            address=user_data['Address'],
            city=user_data['City'],
            state=user_data['State'],
            pin_code=user_data['Pin Code'],
        )
    
    @app.route('/admin_dashboard')
    def admin_dashboard():
        getbookings()
        if session.get('user_type') == 'admin':
            New_Donors = Donors.new
            return render_template('Admin_Dashboard.html', people=New_Donors, username=session['username'], latitude=session['latitude'], longitude=session['longitude'], blood_group=session['blood_group'])
        else: 
            flash("Unauthorized access!", "danger")
            return redirect(url_for('login'))
        
    @app.route('/upload_csv', methods=['POST'])
    def upload_csv():
        if 'csv_file' not in request.files:
            flash("No file part", "danger")
            return redirect(url_for('dashboard'))
        
        file = request.files['csv_file']
        if file.filename == '':
            flash("No selected file", "danger")
            return redirect(url_for('dashboard'))
        
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)

                Donors.instantiate_from_admin(file_path, session['username'])
                flash("Records successfully added!", "success")
            except Exception as e:
                flash(f"Error processing file: {e}", "danger")
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
        else:
            flash("Invalid file format. Please upload a CSV file.", "danger")

        return redirect(url_for('dashboard'))
    
    # @app.route('/test_pdf')
    # def test_pdf():
    #     try:
    #         path_to_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
    #         config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    #         test_html = "<html><body><h1>Test PDF</h1></body></html>"
    #         pdf_filename = "test_output.pdf"
    #         sender_email = os.getenv('SENDER_EMAIL')
    #         sender_password = os.getenv('EMAIL_PASSWORD')
    #         send_email_with_pdf1()
    #         print(f"SENDER_EMAIL: {sender_email}, EMAIL_PASSWORD: {sender_password}")
    #         pdfkit.from_string(test_html, pdf_filename, configuration=config)
    #         return "PDF generated successfully."
    #     except Exception as e:
    #         return f"Error: {e}"
