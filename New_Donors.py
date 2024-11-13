import csv
import random
import qrcode
import os
from flask import render_template, flash, redirect, url_for
from datetime import datetime

def save_donor(first_name, middle_name, last_name, age, blood_group, address, city, state, pin_code, donation_date, slot, username, booking_id, qr_filename):
    status = "Confirmed"
    
    with open('Blood_Donors_Database.csv', 'a', newline='') as f:
        fieldnames = [
            'username', 'Booking ID', 'First Name', 'Middle Name', 'Last Name', 
            'Age', 'Blood Group', 'Address', 'City', 'State', 'Pin Code', 
            'Preferred Slot', 'Donation Date', 'Status', 'QR File Name'
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
            'Status': status,
            'QR File Name': qr_filename
        })

def load_bookings(username):
    bookings = []
    with open('Blood_Donors_Database.csv', newline='') as f:
        reader = csv.DictReader(f)
        for booking in reader:
            if booking['username'] == username:
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

def register_donor(request, session):
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
        status = "Confirmed"       
        qr_data = f"{first_name} {middle_name} {last_name}, Age: {age}, Blood Group: {blood_group}, Address: {address}, {city}, {state}, {pin_code}, Slot: {slot}, Booking ID: {booking_id}, Date: {donation_date}, Status: {status}"
        qr = qrcode.make(qr_data)
        qr_filename = f"{first_name}_{last_name}_QR.png"
        qr_path = f"static/QR_Codes/{qr_filename}"
        os.makedirs("static/QR_Codes", exist_ok=True)
        qr.save(qr_path)
        save_donor(first_name, middle_name, last_name, age, blood_group, address, city, state, pin_code, donation_date, slot, username, booking_id, qr_filename)
        

        # booking_html = render_template('donor_booking.html',
        #                                booking_id=booking_id, donation_date=donation_date, status=status,
        #                                first_name=first_name, middle_name=middle_name, 
        #                                last_name=last_name, age=age, blood_group=blood_group, 
        #                                address=address, city=city, state=state, 
        #                                pin_code=pin_code, slot=slot, qr_filename=qr_filename)
        
        # booking_html_filename = f"{booking_id}.html"
        # with open(os.path.join('static/Bookings', booking_html_filename), 'w') as f:
        #     f.write(booking_html)

        return redirect(url_for('view_booking', booking_id=booking_id))
    return render_template('Donor_register.html', username=session['username'])