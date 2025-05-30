import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

users = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WRITE_CREDIT_PATH = os.path.join(BASE_DIR, 'c', 'write_credit')

@app.route('/')
def home():
    # Redirect to login page by default
    if 'user' in session:
        return redirect(url_for('login'))
    return redirect(url_for('deposit'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        user = users.get(phone)
        if user and user['password'] == password:
            session['user'] = phone
            flash("Logged in successfully!", "success")
            return redirect(url_for('deposit'))
        else:
            flash("Invalid phone number or password", "error")
    return render_template('login.html')

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        aadhar = request.form['aadhar']
        password = request.form['password']

        if phone in users:
            return render_template('create_account.html', error="User already exists")

        users[phone] = {"password": password}
        session['user'] = phone  # Log user in immediately

        # Call the C program using subprocess
        try:
            result = subprocess.run(
                ['./c/write_credit', firstname, lastname, phone, aadhar, password],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("C program output:", result.stdout)
            print("C program error output:", result.stderr)
        except subprocess.CalledProcessError as e:
            print("Error running C program:", e.stderr)
            return render_template('create_account.html', error="Internal error: Failed to write credit data.")

        return redirect(url_for('deposit'))  # Redirect to deposit page
    return render_template('create_account.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Deposit logic here
        flash("Deposit processed!", "success")
    return render_template('deposit.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
