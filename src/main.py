from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Simple user storage (phone -> user info)
users = {}

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('create_account'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        user = users.get(phone)
        if user and user['password'] == password:
            session['user'] = phone
            return redirect(url_for('deposit'))
        else:
            return render_template('login.html', error="Invalid phone number or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        if phone in users:
            return render_template('create_account.html', error="User already exists")
        users[phone] = {"password": password}
        session['user'] = phone  # Log user in immediately after registration
        return redirect(url_for('deposit'))  # Redirect to deposit page
    return render_template('create_account.html')

@app.route('/deposit')
def deposit():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('deposit.html')

if __name__ == '__main__':
    app.run(debug=True)
