from flask import Flask, render_template, request, redirect, url_for, flash
import csv
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key in a production environment

# CSV file to store user data
CSV_FILE = 'user_data.csv'

# Check if the CSV file exists, and create it if not
try:
    with open(CSV_FILE, 'r') as file:
        pass
except FileNotFoundError:
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password'])
        
#########################################################       
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate_user(username, password):
            flash('Login successful', 'success')
           # return redirect(url_for('project'))
            return redirect(url_for('projectDetails'))
            
        else:
            flash('Login failed. Check your username and password.', 'error')

    return render_template('home.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not user_exists(username):
            hashed_password = generate_password_hash(password, method='sha256')
            add_user(username, hashed_password)
            flash('Registration successful. You can now login.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Username already exists. Choose a different username.', 'error')
         
    return render_template('register.html')

@app.route('/projectDetails')
def projectDetails():
    return render_template('projectDetails.html')

####################################################
@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/run_main', methods=['GET'])
def run_main():
    result = subprocess.run(['python', 'sample1\main1.py'], capture_output=True, text=True)
    return result.stdout

@app.route('/run_picker', methods=['GET'])
def run_picker():
    result = subprocess.run(['python', 'sample1\parkingspacepicker1.py'], capture_output=True, text=True)
    return result.stdout

######################################################
@app.route('/project1')
def project1():
    return render_template('project1.html')

@app.route('/run_main2', methods=['GET'])
def run_main2():
    result = subprocess.run(['python', 'sample2\main2.py'], capture_output=True, text=True)
    return result.stdout

@app.route('/run_picker2', methods=['GET'])
def run_picker2():
    result = subprocess.run(['python', 'sample2\parkingspacepicker2.py'], capture_output=True, text=True)
    return result.stdout

#####################################################

def read_csv():
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        return {rows[0]: rows[1] for rows in reader if len(rows) == 2}

def user_exists(username):
    existing_data = read_csv()
    return username in existing_data

def write_csv(data):
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def update_csv(data):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        for username, password in data.items():
            writer.writerow([username, password])


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = generate_password_hash(request.form['password'], method='sha256')

    existing_data = read_csv()

    if username in existing_data:
        return render_template('register.html', message='Username already exists. Please choose another username.')

    existing_data[username] = password
    update_csv(existing_data)

    return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    flash('Logout successful', 'success')
    return redirect(url_for('home'))

def authenticate_user(username, password):
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and check_password_hash(row['password'], password):
                return True
    return False

def user_exists(username):
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                return True
    return False

def add_user(username, password):
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

if __name__ == '__main__':
    app.run(debug=True)
