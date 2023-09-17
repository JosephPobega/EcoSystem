from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secret key for session management

# Simulated database (you should use a real database)
users = []

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user exists (you should validate the credentials properly)
        user = next((user for user in users if user.username == username and user.password == password), None)
        if user:
            flash('Login successful', 'success')
            # Implement session management here (e.g., Flask-Session)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the username or email is already in use (you should validate this properly)
        if any(user.username == username or user.email == email for user in users):
            flash('Username or email already in use', 'error')
        else:
            new_user = User(username, email, password)
            users.append(new_user)
            flash('Registration successful', 'success')
            # Implement session management here (e.g., Flask-Session)
            return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    # Implement the dashboard logic here
    return "Welcome to the Dashboard"

if __name__ == '__main__':
    app.run(debug=True)
