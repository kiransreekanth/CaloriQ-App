from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import gc

app = Flask(__name__)
CORS(app)

# ---------- Database Configuration ----------
db_config = {
    'host': 'localhost',
    'user': '', # replace with your username
    'password': '', # replace with your password
    'database': '' # replace with your database name
}

# ---------- Load ML Model ----------
model = tf.keras.models.load_model("best_food_model.h5")

# Clear any existing sessions and set memory growth
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

class_names = ['burger', 'butter_naan', 'chai', 'chapati', 'chole_bhature',
               'dal_makhani', 'dhokla', 'fried_rice', 'idli', 'jalebi',
               'kaathi_rolls', 'kadai_paneer', 'kulfi', 'masala_dosa', 'momos',
               'paani_puri', 'pakode', 'pav_bhaji', 'pizza', 'samosa']

# Add this after your class_names definition in app.py

# Food calorie database (calories per 100g serving)
food_calories = {
    'burger': 295,
    'butter_naan': 320,
    'chai': 37,  # per 100ml
    'chapati': 297,
    'chole_bhature': 320,
    'dal_makhani': 142,
    'dhokla': 160,
    'fried_rice': 163,
    'idli': 58,
    'jalebi': 495,
    'kaathi_rolls': 235,
    'kadai_paneer': 180,
    'kulfi': 223,
    'masala_dosa': 135,
    'momos': 154,
    'paani_puri': 329,
    'pakode': 285,
    'pav_bhaji': 105,
    'pizza': 266,
    'samosa': 308
}

# Typical serving sizes (in grams)
serving_sizes = {
    'burger': 150,
    'butter_naan': 80,
    'chai': 200,  # 200ml
    'chapati': 40,
    'chole_bhature': 200,
    'dal_makhani': 150,
    'dhokla': 100,
    'fried_rice': 200,
    'idli': 50,  # per piece
    'jalebi': 25,  # per piece
    'kaathi_rolls': 120,
    'kadai_paneer': 150,
    'kulfi': 100,
    'masala_dosa': 150,
    'momos': 25,  # per piece
    'paani_puri': 15,  # per piece
    'pakode': 30,  # per piece
    'pav_bhaji': 200,
    'pizza': 125,  # per slice
    'samosa': 50   # per piece
}

# New endpoint to get food calorie information
@app.route('/food-calories', methods=['POST'])
def get_food_calories():
    data = request.json
    food_name = data.get('food_name', '').lower()
    quantity = data.get('quantity', 1)  # Default to 1 serving
    
    if food_name not in food_calories:
        return jsonify({
            'statusCode': 'SC404',
            'statusDesc': 'Food item not found in database'
        })
    
    calories_per_100g = food_calories[food_name]
    typical_serving = serving_sizes[food_name]
    
    # Calculate calories for the specified quantity
    calories_per_serving = (calories_per_100g * typical_serving) / 100
    total_calories = calories_per_serving * quantity
    
    return jsonify({
        'statusCode': 'SC200',
        'statusDesc': 'Calorie information retrieved successfully',
        'food_name': food_name,
        'calories_per_100g': calories_per_100g,
        'typical_serving_size': typical_serving,
        'calories_per_serving': round(calories_per_serving, 2),
        'quantity': quantity,
        'total_calories': round(total_calories, 2),
        'unit': 'grams' if food_name != 'chai' else 'ml'
    })

# ---------- Authentication Routes ----------
# Replace your existing authentication routes in app.py with these updated versions

@app.route('/authAdapter', methods=['POST'])
def register():
    data = request.json
    full_name = data.get('fullName')  # Updated field name
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')  # Updated field name

    print(f"Registration attempt: {data}")  # Debug log

    if not all([full_name, username, email, password, confirm_password]):
        return jsonify({'statusCode': 'SC400', 'statusDesc': 'All fields are required'}), 400
    if password != confirm_password:
        return jsonify({'statusCode': 'SC400', 'statusDesc': 'Passwords do not match'}), 400
    if len(password) < 6:
        return jsonify({'statusCode': 'SC400', 'statusDesc': 'Password must be at least 6 characters'}), 400

    hashed_password = generate_password_hash(password)

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Check if username or email already exists
        cursor.execute("SELECT username, email FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            connection.close()
            return jsonify({'statusCode': 'SC409', 'statusDesc': 'Username or Email already exists'}), 409
        
        cursor.execute("INSERT INTO users (full_name, username, email, password) VALUES (%s, %s, %s, %s)",
                       (full_name, username, email, hashed_password))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'statusCode': 'SC200', 'statusDesc': 'Registration successful! Please login.'}), 200
    except mysql.connector.IntegrityError as e:
        print(f"Integrity error: {e}")
        return jsonify({'statusCode': 'SC409', 'statusDesc': 'Username or Email already exists'}), 409
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'statusCode': 'SC500', 'statusDesc': 'Registration failed', 'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    print(f"Login attempt: username={username}")  # Debug log

    if not all([username, password]):
        return jsonify({'statusCode': 'SC400', 'statusDesc': 'Username and password are required'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and check_password_hash(user['password'], password):
            user_data = {
                'id': user['id'],
                'fullName': user['full_name'],
                'username': user['username'],
                'email': user['email']
            }
            print(f"Login successful for user: {user_data}")  # Debug log
            return jsonify({
                'statusCode': 'SC200', 
                'statusDesc': 'Login successful', 
                'user': user_data
            }), 200
        else:
            print("Invalid credentials")  # Debug log
            return jsonify({'statusCode': 'SC401', 'statusDesc': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'statusCode': 'SC500', 'statusDesc': 'Login failed', 'error': str(e)}), 500

# ---------- BMI Calculation ----------
@app.route('/bmi', methods=['POST'])
def calculate_bmi():
    data = request.json
    try:
        height = float(data['height']) / 100  # Convert cm to meters
        weight = float(data['weight'])
        if height <= 0 or weight <= 0:
            raise ValueError()

        bmi = weight / (height ** 2)
        if bmi < 18.5:
            status = 'Underweight'
        elif 18.5 <= bmi < 24.9:
            status = 'Normal'
        elif 25 <= bmi < 29.9:
            status = 'Overweight'
        else:
            status = 'Obese'

        return jsonify({
            'statusCode': 'SC200',
            'statusDesc': 'BMI calculated successfully',
            'bmi': round(bmi, 2),
            'status': status
        })
    except:
        return jsonify({'statusCode': 'SC400', 'statusDesc': 'Invalid height or weight'})

# ---------- Calorie Target Calculation ----------
@app.route('/calorie', methods=['POST'])
def calculate_calorie():
    data = request.json
    try:
        age = int(data['age'])
        gender = data['gender']
        height = float(data['height'])
        weight = float(data['weight'])
        activity_level = data['activity_level'].lower()

        bmr = (10 * weight + 6.25 * height - 5 * age + (5 if gender == 'male' else -161))
        activity_factors = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very active': 1.9
        }
        calorie_needs = bmr * activity_factors.get(activity_level, 1.2)

        return jsonify({
            'statusCode': 'SC200',
            'statusDesc': 'Calorie target calculated',
            'calories': round(calorie_needs, 2)
        })
    except:
        return jsonify({'statusCode': 'SC400', 'statusDesc': 'Invalid input data'})

# ---------- FIXED Food Prediction ----------
# Replace your existing /predict endpoint with this enhanced version
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'statusCode': 'SC400', 'statusDesc': 'No file uploaded'})

    file = request.files['file']
    try:
        # Read file into memory first
        file_bytes = file.read()
        
        # Reset file pointer and create new Image object
        img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        
        # Resize to 256x256 (same as training)
        img = img.resize((256, 256))
        
        # Convert to numpy array with proper dtype
        img_array = np.array(img, dtype=np.float32)
        
        # CRITICAL FIX: Normalize the image to 0-1 range
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # Force garbage collection to clear any cached data
        gc.collect()
        
        # Clear TensorFlow session to prevent caching issues
        tf.keras.backend.clear_session()
        
        # Debug: Print image statistics AFTER normalization
        print(f"Image shape: {img_array.shape}")
        print(f"Image min/max: {img_array.min():.3f}/{img_array.max():.3f}")
        print(f"Image mean: {img_array.mean():.3f}")

        # Make prediction with explicit steps
        with tf.device('/CPU:0'):  # Force CPU to avoid GPU memory issues
            prediction = model(img_array, training=False)
            prediction_numpy = prediction.numpy()
        
        # Apply softmax to get proper probabilities if model doesn't have it
        prediction_probs = tf.nn.softmax(prediction_numpy).numpy()
        
        predicted_index = int(np.argmax(prediction_probs))
        confidence = float(np.max(prediction_probs))
        predicted_label = class_names[predicted_index]
        
        # GET CALORIE INFORMATION FOR THE PREDICTED FOOD
        calories_per_100g = food_calories.get(predicted_label, 0)
        typical_serving = serving_sizes.get(predicted_label, 100)
        calories_per_serving = (calories_per_100g * typical_serving) / 100
        
        # Print all prediction probabilities for debugging
        print("All predictions (after softmax):")
        for i, prob in enumerate(prediction_probs[0]):
            print(f"  {class_names[i]}: {prob:.4f}")
        
        print(f"Final Predicted: {predicted_label} (index: {predicted_index}, confidence: {confidence:.3f})")

        # Clean up variables
        del img_array, prediction, prediction_numpy, prediction_probs
        gc.collect()

        return jsonify({
            'statusCode': 'SC200',
            'statusDesc': 'Prediction successful',
            'prediction': predicted_label,
            'confidence': round(confidence, 3),
            'predicted_index': predicted_index,
            # NEW: Calorie information included
            'calorie_info': {
                'calories_per_100g': calories_per_100g,
                'typical_serving_size': typical_serving,
                'calories_per_serving': round(calories_per_serving, 2),
                'unit': 'grams' if predicted_label != 'chai' else 'ml'
            }
        })

    except Exception as e:
        print(f"Prediction error: {str(e)}")
        # Clean up on error
        gc.collect()
        tf.keras.backend.clear_session()
        return jsonify({
            'statusCode': 'SC500',
            'statusDesc': 'Prediction failed',
            'error': str(e)
        })

# ---------- Alternative Prediction Method (use if above doesn't work) ----------
@app.route('/predict_alt', methods=['POST'])
def predict_alternative():
    """Alternative prediction method that reloads model for each prediction"""
    if 'file' not in request.files:
        return jsonify({'statusCode': 'SC400', 'statusDesc': 'No file uploaded'})

    file = request.files['file']
    try:
        # Read and process image
        file_bytes = file.read()
        img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        img = img.resize((256, 256))
        img_array = np.array(img, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Reload model for each prediction (slower but more reliable)
        temp_model = tf.keras.models.load_model("rawModelv1.h5")
        
        # Make prediction
        prediction = temp_model.predict(img_array, verbose=0)
        predicted_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction))
        predicted_label = class_names[predicted_index]
        
        # Clean up
        del temp_model
        gc.collect()
        
        return jsonify({
            'statusCode': 'SC200',
            'statusDesc': 'Prediction successful',
            'prediction': predicted_label,
            'confidence': round(confidence, 3),
            'predicted_index': predicted_index
        })

    except Exception as e:
        return jsonify({
            'statusCode': 'SC500',
            'statusDesc': 'Prediction failed',
            'error': str(e)
        })

# ---------- DB Initialization ----------
def init_db():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100),
                username VARCHAR(100) UNIQUE,
                email VARCHAR(100),
                password VARCHAR(255)
            )
        ''')
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized.")
    except Exception as e:
        print("Error initializing database:", str(e))

# ---------- Start App ----------
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=3000, debug=True)