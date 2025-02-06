from flask import Flask, render_template, request, jsonify, session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Add a secret key for secure sessions

# Load model and scaler once
def load_model():
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
            scaler = pickle.load(f)
        return model, scaler
    except Exception as e:
        raise Exception(f"Error loading model: {str(e)}")

# Process user data and make a prediction
def predict_price(user_data):
    try:
        model, scaler = load_model()
        features_scaled = scaler.transform([user_data])  # Standardize the user input
        prediction = model.predict(features_scaled)  # Predict price
        return prediction[0]
    except Exception as e:
        raise Exception(f"Error during prediction: {str(e)}")

# Variables to store user responses
questions = [
    "¿Cuál es el área de la vivienda en metros cuadrados? (por favor, introduce un número)",
    "¿Cuántas habitaciones tiene la vivienda?",
    "¿Cuántos baños tiene la vivienda?",
    "¿Cuántas plantas tiene la vivienda?",
    "¿Está en una calle principal? (sí/no)",
    "¿Tiene habitación de invitados? (sí/no)",
    "¿Tiene sótano? (sí/no)",
    "¿Cuenta con calefacción de agua caliente? (sí/no)",
    "¿Tiene aire acondicionado? (sí/no)",
    "¿Cuántas plazas de aparcamiento tiene la vivienda?",
    "¿Está en un área de preferencia? (sí/no)",
    "¿La vivienda está amueblada? (sí/no)"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/chatbot", methods=["POST"])
def chatbot():
    # Get user input and session data
    user_data = session.get(request.json["user_id"], [])
    last_response = request.json["message"].strip()

    # Determine the current question
    current_question_index = len(user_data)
    current_question = questions[current_question_index]

    # Validate and process the response
    if current_question_index < len(questions):
        expected_type = "numeric" if current_question_index in range(0, 3) else "boolean"

        if expected_type == "numeric":
            if not last_response.isdigit():
                return jsonify({"response": f"Por favor, introduce un número válido para la pregunta: {current_question}"})
            user_data.append(int(last_response))  # Store the numeric response
        elif expected_type == "boolean":
            if last_response.lower() not in ["sí", "no"]:
                return jsonify({"response": f"Por favor, responde 'sí' o 'no' a la pregunta: {current_question}"})
            user_data.append(1 if last_response.lower() == "sí" else 0)  # Store the boolean response as 1 or 0

        session[request.json["user_id"]] = user_data  # Save the user's answers

        # If all questions are answered, make the prediction
        if len(user_data) == len(questions):
            try:
                # Make a prediction with the model
                prediction = predict_price(user_data)
                response_text = f"El precio estimado de la vivienda es ${prediction:,.2f}"
                session.pop(request.json["user_id"], None)  # Reset session after prediction
            except Exception as e:
                response_text = f"Error al procesar la predicción: {str(e)}"
        else:
            # Send the next question to the user
            response_text = questions[len(user_data)]

        return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
