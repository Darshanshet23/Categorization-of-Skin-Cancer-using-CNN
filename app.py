from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
import sys

# Ensure the default encoding is UTF-8
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Load the model
model = load_model('final_model03.keras')
class_names = ['Benign', 'Malignant']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('upload'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            if password == confirm_password:
                hashed_password = generate_password_hash(password)
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Signup successful! Please login.')
                return redirect(url_for('login'))
            else:
                flash('Passwords do not match!')
        else:
            flash('User already exists!')
    return render_template('signup.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            prediction = predict_image(filepath)
            return render_template('result.html', prediction=prediction, image_path=filename)
    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def predict_image(image_path):
    image = load_img(image_path, target_size=(180, 180))
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    pred_class_index = np.argmax(predictions, axis=1)[0]
    return class_names[pred_class_index]

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
