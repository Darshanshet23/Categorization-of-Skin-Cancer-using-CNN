# Categorization of Skin Cancer using CNN 🧠🩺

This project focuses on the detection and classification of skin cancer using Convolutional Neural Networks (CNN). It features both a deep learning model built with TensorFlow/Keras and a web-based application developed using Flask that allows users to upload skin lesion images and get predictions.

## 📝 Project Overview

Skin cancer is one of the most common types of cancer. Early detection can significantly improve survival rates. This project aims to classify skin lesions into categories (e.g., benign or malignant) using a CNN model trained on dermatological image data.

## 📂 Project Structure

```
├── Melanoma_SkinCancer_Detection.ipynb   # Main Jupyter notebook with model training
├── app.py                                # Flask app for the web interface
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── upload.html
│   └── result.html
├── static/
│   └── styles.css                        # CSS for styling
├── uploads/                              # Folder for uploaded images
├── doctor.png                            # Image used in UI
└── README.md                             # This file
```


3. Update paths in the notebook accordingly.

## 🧠 Model Details

- **Architecture**: CNN with Conv2D, MaxPooling2D, Dropout, Dense layers
- **Framework**: TensorFlow & Keras
- **Preprocessing**:
- Resizing images
- Normalizing pixel values
- **Metrics**: Accuracy, Confusion Matrix, Classification Report

## 🌐 Web Application

A Flask-based web app allows users to upload images and receive predictions from the trained model.

### To Run Locally:

1. **Clone the repository:**
```
git clone https://github.com/Darshanshet23/Categorization-of-Skin-Cancer-using-CNN.git
cd Categorization-of-Skin-Cancer-using-CNN
```
2. ** Install dependencies:**
```
pip install -r requirements.txt
```
3. ** Run the app:**
```
python app.py
```
4. **Visit in browser:**
```
http://localhost:5000
```
