from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask import abort

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.db'
db = SQLAlchemy(app)



# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(280), nullable=False)


# creates the sqlite database
with app.app_context():
    db.create_all()


@app.route('/profile/<username>')
def profile(username):
    user_data = User.query.filter_by(username=username).first()
    if user_data is None:
        return "User not found", 404
    user_posts = Post.query.filter_by(username=username).all()
    return render_template('profile.html', user=user_data, posts=user_posts)
    

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    users = User.query.filter(User.username.ilike(f"%{query}%")).all()
    return render_template('search_results.html', query=query, users=users)


def get_user_data(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404) 
    return user



@app.route('/')
def index():
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            flash('Login successful', 'success')
            session['username'] = username
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
        
        # Check if the username or email is already in use in the database
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already in use', 'error')
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)  # Add the new user to the database
            db.session.commit()
            flash('Registration successful', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('register.html')



@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        logged_in_username = session['username']
        posts = Post.query.all()  # Retrieve all posts

        return render_template("dashboard.html", username=logged_in_username, posts=posts)
    else:
        flash('Please log in first', 'error')
        return redirect(url_for('login'))


@app.route('/post', methods=['POST'])
def post_message():
    if 'username' in session:
        username = session['username']
        message = request.form['message']
        new_post = Post(username=username, message=message)
        db.session.add(new_post)
        db.session.commit()
        
        flash('Message posted successfully', 'success')
    else:
        flash('Please log in first', 'error')
    
    return redirect(url_for('dashboard'))


@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'username' in session:
        username = session['username']
        post = Post.query.filter_by(id=post_id, username=username).first()
        
        if post:
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted successfully', 'success')
        else:
            flash('Post not found or you do not have permission to delete it', 'error')
    else:
        flash('Please log in first', 'error')
    
    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    app.run(debug=True)
