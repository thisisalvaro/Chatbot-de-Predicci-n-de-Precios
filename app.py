from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle
import os

app = Flask(__name__)

# Verifica si el modelo ya existe
MODEL_PATH = 'model.pkl'

if not os.path.exists(MODEL_PATH):
    # Cargar el dataset
    df = pd.read_csv('dataset_housing_price.csv')

    # Verificar las columnas del DataFrame
    print("Columnas del DataFrame:")
    print(df.columns)

    # Verificar los primeros registros
    print("Primeros registros del DataFrame:")
    print(df.head())

    # Eliminar la columna 'Unnamed: 0' si existe
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')

    # Convertir las variables categóricas a numéricas
    df['mainroad'] = df['mainroad'].map({'yes': 1, 'no': 0})
    df['guestroom'] = df['guestroom'].map({'yes': 1, 'no': 0})
    df['basement'] = df['basement'].map({'yes': 1, 'no': 0})
    df['hotwaterheating'] = df['hotwaterheating'].map({'yes': 1, 'no': 0})
    df['airconditioning'] = df['airconditioning'].map({'yes': 1, 'no': 0})
    df['prefarea'] = df['prefarea'].map({'yes': 1, 'no': 0})
    df['furnished'] = df['furnished'].map({'yes': 1, 'no': 0})

    # Imputar los valores NaN con valores predeterminados para categorías
    df.fillna({
        'mainroad': 0,
        'guestroom': 0,
        'basement': 0,
        'hotwaterheating': 0,
        'airconditioning': 0,
        'prefarea': 0,
        'furnished': 0
    }, inplace=True)

    # Eliminar filas si falta la etiqueta 'price'
    df.dropna(subset=['price'], inplace=True)

    # Validación después de la limpieza
    if df.empty:
        raise ValueError("El dataset está vacío después del preprocesamiento. Verifica los datos.")

    # Selección de características y etiqueta
    X = df.drop(columns=['price'])
    y = df['price']

    # Normalizar los datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Crear y entrenar el modelo
    model = LinearRegression()
    model.fit(X_scaled, y)

    # Guardar el modelo entrenado y el scaler
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
        pickle.dump(scaler, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()

    # Obtener los datos del formulario y convertirlos a formato adecuado
    features = [
        int(data['area']),
        int(data['bedrooms']),
        int(data['bathrooms']),
        int(data['stories']),
        int(data.get('mainroad', 0)),
        int(data.get('guestroom', 0)),
        int(data.get('basement', 0)),
        int(data.get('hotwaterheating', 0)),
        int(data.get('airconditioning', 0)),
        int(data['parking']),
        int(data.get('prefarea', 0)),
        int(data.get('furnished', 0))
    ]

    # Cargar el modelo y el scaler
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
        scaler = pickle.load(f)

    # Normalizar los datos de entrada
    features_scaled = scaler.transform([features])

    # Hacer la predicción
    prediction = model.predict(features_scaled)

    return jsonify({'price': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
