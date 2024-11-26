import csv
import random
import qrcode
import os
import pdfkit
import smtplib
from flask import render_template, flash, redirect, url_for
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io
import base64
from Existing_Donors import Donors

def save_donor(username, email, first_name, middle_name, last_name, age, blood_group, address, city, state, pin_code, latitude, longitude, donation_date, slot, booking_id, qr_binary):
    status = "Confirmed"
    
    with open('Blood_Donors_Database.csv', 'a', newline='') as f:
        fieldnames = [
            'username', 'email', 'Booking ID', 'First Name', 'Middle Name', 'Last Name', 
            'Age', 'Blood Group', 'Address', 'City', 'State', 'Pin Code', 'Latitude', 
            'Longitude', 'Preferred Slot', 'Donation Date', 'Status', 'QR Code (Base64)'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if f.tell() == 0:
            writer.writeheader()
        
        writer.writerow({
            'username': username,
            'email': email,
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
            'Latitude': latitude,
            'Longitude': longitude,
            'Preferred Slot': slot,
            'Donation Date': donation_date,
            'Status': status,
            'QR Code (Base64)': qr_binary
        })

def load_bookings(username):
    bookings = []
    with open('Blood_Donors_Database.csv', newline='') as f:
        reader = csv.DictReader(f)
        for booking in reader:
            if booking['username'] == username:
                bookings.append(booking)
            elif username == "admin":
                bookings.append(booking)
    return bookings

def load_booking(booking_id):
    bookings = []
    with open('Blood_Donors_Database.csv', newline='') as f:
        reader = csv.DictReader(f)
        for booking in reader:
            if booking['Booking ID'] == booking_id:
                bookings.append(booking)
    return bookings

def send_email_with_pdf(user_email, booking_id, booking_html):

    base_url = "http://127.0.0.1:5000"
    
    booking_html = booking_html.replace("../static/", f"{base_url}/static/")
    
    path_to_wkhtmltopdf = r'wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    
    pdf_filename = f"static/Bookings/{booking_id}_booking.pdf"
    options = {
    'quiet': '',
    'print-media-type': ''
     }

    pdfkit.from_string(booking_html, pdf_filename, options=options, configuration=config)

    sender_email = "adilaquil2005@gmail.com"
    sender_password = "aako ufhq wfvr psiz"
    receiver_email = user_email

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Booking Confirmation - VitalisLink'

    body = "Please find your booking confirmation attached as a PDF."
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_filename)}')
        msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def getbookings():
    Donors.new.clear()
    with open('Blood_Donors_Database.csv', 'r') as f:
            reader = csv.DictReader(f)
            New_Donors = list(reader)

            for donors in New_Donors:
                try:
                    Donors(
                        first_name=donors.get('First Name'),
                        middle_name=donors.get('Middle Name'),
                        last_name=donors.get('Last Name'),
                        age=int(donors.get('Age').strip()),
                        blood_group=donors.get('Blood Group').strip(),
                        address=donors.get('Address'),
                        city=donors.get('City'),
                        state=donors.get('State'),
                        pin_code=int(donors.get('Pin Code')),
                        latitude=float(donors.get('Latitude')),
                        longitude=float(donors.get('Longitude')),
                        status=donors.get('Status')
                    )
                    
                except (AssertionError, ValueError) as e:

                    print(f"Skipping invalid record: {donors}. Reason: {e}")


def register_donor(request, session, booking_id):
    if 'username' not in session:
        flash("Please log in to register as a donor.", "warning")
        return redirect(url_for('login'))
    
    Blood_Groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name', '')
        last_name = request.form['last_name']
        age = int(request.form['age'])
        if age < 18:
            flash('You must be at least 18 years old to donate blood.', 'error')
            return redirect('/donor_register')
        blood_group = request.form['blood_group'].upper()
        if blood_group not in Blood_Groups:
            flash('Please enter a valid blood group.', 'error')
            return redirect('/donor_register')
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        pin_code = request.form['pin_code']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        slot = request.form['slot']
        donation_date = request.form['donation_date']
        username = session['username']
        email = session['email']
        status = "Confirmed"

        qr_data = f"{first_name} {middle_name} {last_name}, Age: {age}, Blood Group: {blood_group}, Address: {address}, {city}, {state}, {pin_code}, Slot: {slot}, Booking ID: {booking_id}, Date: {donation_date}, Status: {status}"
        qr = qrcode.QRCode()
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        img_io = io.BytesIO()
        img.save(img_io, format="PNG")
        img_io.seek(0)
        qr_binary = base64.b64encode(img_io.getvalue()).decode('utf-8')

        save_donor(username, email, first_name, middle_name, last_name, age, blood_group, address, city, state, pin_code, latitude, longitude, donation_date, slot, booking_id, qr_binary)      

        # booking_html = render_template('donor_booking.html',
        #                                booking_id=booking_id, donation_date=donation_date, status=status,
        #                                first_name=first_name, middle_name=middle_name, 
        #                                last_name=last_name, age=age, blood_group=blood_group, 
        #                                address=address, city=city, state=state, 
        #                                pin_code=pin_code, slot=slot, qr_filename=qr_filename)
        
        # booking_html_filename = f"{booking_id}.html"
        # with open(os.path.join('static/Bookings', booking_html_filename), 'w') as f:
        #     f.write(booking_html)

        booking = load_booking(booking_id)
        booking_html = render_template('View_booking.html', booking=booking[0], username=session.get('username'),)

        return redirect(url_for('view_booking', booking_id=booking_id))
    return render_template('Donor_register.html', username=session['username'])

# getbookings()
# print(Donors.new)