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
    with open('User_Database.csv', mode='r', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    user_updated = False
    
    for row in rows:
        if row['username'] == updated_data['username']:
            row.update(updated_data)
            user_updated = True
            break
    
    if user_updated:
        with open('User_Database.csv', mode='w', newline='') as f:
            fieldnames = [
                'username', 'email', 'password', 'First Name', 'Middle Name', 'Last Name', 
                'Age', 'Blood Group', 'Address', 'City', 'State', 'Pin Code', 'Latitude', 
                'Longitude'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        print(f"User with username {updated_data['username']} not found.")

