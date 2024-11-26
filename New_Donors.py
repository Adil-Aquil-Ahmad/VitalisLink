import csv
import qrcode
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from flask import render_template, flash, redirect, url_for
from datetime import datetime
import io
from io import BytesIO
from PIL import Image
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

def Create_PDF(booking_id, booking_data, timeout=120):

    os.makedirs('tmp/Bookings/', exist_ok=True)
    pdf_filename = f"tmp/Bookings/{booking_id}_booking.pdf"
    
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(50, height - 40, "VitalisLink")
    
    c.drawImage("static/Images/VITALISLINK LOGO LIGHT2.png", 450, height - 55, width=100, height=30)

    c.setStrokeColor(colors.darkred)
    c.setLineWidth(2)
    c.line(50, height - 70, width - 50, height - 70)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 90, "Donor Booking Details")

    y_position = height - 120
    c.setFont("Helvetica", 12)

    c.drawString(50, y_position, f"Full Name: {booking_data['First Name']} {booking_data['Middle Name']} {booking_data['Last Name']}")
    y_position -= 20

    c.drawString(50, y_position, f"Age: {booking_data['Age']}")
    y_position -= 20

    c.drawString(50, y_position, f"Blood Group: {booking_data['Blood Group']}")
    y_position -= 20
    
    address = f"Address: {booking_data['Address']}, {booking_data['City']}"
    address_lines = address.split(" ")
    
    line = ""
    lines = []
    for word in address_lines:
        if len(line.split(" ")) <= 6:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())
    
    for line in lines:
        c.drawString(50, y_position, f"{line}")
        y_position -= 15
    
    c.drawString(50, y_position, f"{booking_data['State']} - {booking_data['Pin Code']}")
    y_position -= 25

    c.drawString(50, y_position, f"Time Slot: {booking_data['Preferred Slot']}")
    y_position -= 20

    c.drawString(50, y_position, f"Booking ID: {booking_data['Booking ID']}")
    y_position -= 20

    c.drawString(50, y_position, f"Date: {booking_data['Donation Date']}")
    y_position -= 20

    c.drawString(50, y_position, f"Status: {booking_data['Status']}")
    y_position += 210
    
    qr_base64 = booking_data['QR Code (Base64)']
    img_data = base64.b64decode(qr_base64)
    
    img = Image.open(BytesIO(img_data))
    img.save("temp_qr.png")

    box_x = width - 162
    box_y = y_position - 120
    box_size = 100
    c.setStrokeColor(colors.darkred)
    c.setLineWidth(2)
    c.rect(box_x - 10, box_y - 10, box_size + 20, box_size + 20)
    c.drawImage("temp_qr.png", box_x, box_y, width=box_size, height=box_size)

    c.save()

    os.remove("temp_qr.png")

    print(f"PDF generated: {pdf_filename}, Size: {os.path.getsize(pdf_filename)} bytes")

    return pdf_filename

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