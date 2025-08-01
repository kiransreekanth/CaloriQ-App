# 🥗 CaloriQ - AI-Powered Food Calorie Predictor

**CaloriQ** is a full-stack AI-based mobile application that allows users to authenticate, upload food images, and get instant nutritional analysis. The app leverages a TensorFlow-trained model and provides calorie estimates per 100g and serving size. Built using **Flutter** for frontend and **Flask + MySQL + TensorFlow** for the backend.

---

## 🧰 Prerequisites

Ensure the following are installed on your system:

- Python 3.8+
- MySQL Server (local or remote)
- Flutter SDK (3.x recommended)
- Android Studio / Visual Studio Code (with Flutter and Dart plugins)
- Git

---

## 📦 Cloning the Repository

```bash
git clone https://github.com/kiransreekanth/CaloriQ-App.git
cd CaloriQ-App
````

---

## 🔧 Backend Setup (Flask + MySQL)

1. Navigate to the backend folder:

```bash
cd backend
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt  # (create this from your environment)
```

4. Configure your `.env` or update `db_config` in `app.py`:

```python
db_config = {
    'host': 'localhost',
    'user': 'your_mysql_user',
    'password': 'your_password',
    'database': 'your_db_name'
}
```

5. Run the backend:

```bash
python app.py
```

The Flask server will start at: `http://localhost:3000`

> ✅ The backend supports routes for authentication, calorie prediction, BMI calculation, and TDEE calorie estimation.

---

## 📱 Frontend Setup (Flutter)

1. Navigate to the Flutter frontend folder:

```bash
cd frontend_flutter
```

2. Install Flutter packages:

```bash
flutter pub get
```

3. Connect a device or start an emulator, then run:

```bash
flutter run
```

> 📷 Users can register, log in, and upload food images for analysis. The results show predicted food items, calories per 100g, serving size, and BMI/Calorie needs based on user profile.

---

## ✅ Key Features

* 👤 **User Registration & Login** with form validation
* 📸 **AI-Powered Food Recognition** via image upload
* 🔥 **Real-Time Calorie Prediction** with serving size calculator
* 📊 **BMI & Daily Calorie Estimator** based on user profile
* 📁 Integrated **TensorFlow Keras Model** for 20 Indian food classes
* 💾 Backend powered by **Flask, MySQL**, and **TensorFlow**
* 🎯 Flutter UI with clean modular structure (`pages`, `widgets`)

---

## ⚙️ Tech Stack

| Tech       | Purpose                        |
| ---------- | ------------------------------ |
| Flutter    | Cross-platform mobile frontend |
| Flask      | Backend API server             |
| MySQL      | User authentication storage    |
| TensorFlow | Food image classification      |
| PIL, NumPy | Image preprocessing            |
| CORS, JSON | Data handling & API flow       |

---

## 📝 Notes

* 🧠 Trained models (`.h5`) are located under `model_training/`
* 🍱 Images are processed and resized before prediction using Pillow (PIL)
* 🔐 Be sure to secure your MySQL credentials in production

---

## 📌 To-Do / Improvements

* ✅ Token-based auth (JWT)
* ⏳ Save prediction history
* ☁️ Host backend on Render/Heroku and frontend with Firebase
* 📈 Expand food dataset for higher accuracy

---

## 🧠 AI Model Details

* Model Input: 256x256 RGB images
* Output: Softmax probabilities over 20 Indian food classes
* Loss Function: Categorical Crossentropy
* Optimizer: Adam
* Accuracy: \~80% on validation set

---

<div style="display: flex; gap: 30px; margin-bottom: 40px;">

  <img width="400" height="800" alt="Screenshot (283)" src="https://github.com/user-attachments/assets/8b693af9-ef87-46d6-ac9b-7883cf43ad24" />
  <img width="400" height="800" alt="Screenshot (284)" src="https://github.com/user-attachments/assets/3b49b7ce-feda-4801-972c-41983d47bbb3" />

</div>

<div style="display: flex; gap: 30px; margin-bottom: 40px;">
  
  <img width="400" height="800" alt="Screenshot (285)" src="https://github.com/user-attachments/assets/449c272e-b222-4e85-80db-8e6a90f84733" />
  <img width="400" height="800" alt="Screenshot (286)" src="https://github.com/user-attachments/assets/bc6b5eab-8b1a-4922-8758-afb20f987398" />

</div>

<div style="display: flex; gap: 30px; margin-bottom: 40px;">
  
  <img width="400" height="800" alt="Screenshot (287)" src="https://github.com/user-attachments/assets/6dc09c34-7798-444d-8563-1dc4062554d2" />
  <img width="400" height="800" alt="Screenshot (289)" src="https://github.com/user-attachments/assets/8c40159e-33bd-44ff-afdb-23d824778218" />

</div>
