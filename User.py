import csv
import hashlib

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
        fieldnames = [
            'username', 'email', 'password', 'First Name', 'Middle Name', 'Last Name', 
            'Age', 'Blood Group', 'Address', 'City', 'State', 'Pin Code', 'Latitude', 
            'Longitude'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow({'username': username, 'email': email, 'password': hash_password(password)})


def load_user_data(username):
    with open('User_Database.csv', mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username:
                return row
    return None

def save_user_data(updated_data):
    # Read the existing data into memory (excluding the header)
    with open('User_Database.csv', mode='r', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)  # Read all rows into memory
    
    # Flag to indicate whether we've updated the user data
    user_updated = False
    
    # Update the row for the specific username
    for row in rows:
        if row['username'] == updated_data['username']:
            row.update(updated_data)  # Update the row with the new data
            user_updated = True
            break  # Once we find and update the user, exit the loop
    
    # If the user was updated, write the modified data back to the file
    if user_updated:
        with open('User_Database.csv', mode='w', newline='') as f:
            fieldnames = [
                'username', 'email', 'password', 'First Name', 'Middle Name', 'Last Name', 
                'Age', 'Blood Group', 'Address', 'City', 'State', 'Pin Code', 'Latitude', 
                'Longitude'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row first
            writer.writerows(rows)  # Write all rows (including the updated one)
    else:
        print(f"User with username {updated_data['username']} not found.")

