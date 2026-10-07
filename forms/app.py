from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/formsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birthday = db.Column(db.Date, nullable=True)  # New birthday field

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all() 
    return render_template('home.html', users=users)

# CREATE - Add new user
@app.route('/add', methods=['GET', 'POST'])
def add_user():

    # TODO: Implement add user functionality
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        birthday = request.form.get('birthday')  # Get birthday from form

        if not username or not email:
            flash('Username and Email are required!', 'danger')
            return redirect(url_for('add_user'))

        new_user = User(username=username, email=email, birthday=birthday)
        db.session.add(new_user)
        db.session.commit()
        flash('User added succesfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_user.html')

# READ - View an individual user
@app.route('/view/<int:user_id>', methods=['GET'])
def view_user(user_id):
    user = User.query.get_or_404(user_id) 
    return render_template('view_user.html', user=user)

# UPDATE - Edit an individual user
@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)

    # TODO: Implement update user functionality
    user.username = request.form['username']
    user.email = request.form['email']
    db.session.commit()
    flash('User updated successfully!', 'success')

    return redirect(url_for('view_user', user_id=user_id))

# DELETE - Delete a user
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):

    # TODO: Implement delete user functionality
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))