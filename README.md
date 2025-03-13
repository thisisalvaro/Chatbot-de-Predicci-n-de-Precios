# Chatbot de Predicción de Precios de Viviendas
*Este es un chatbot interactivo que predice el precio de una vivienda basándose en las características que el usuario proporciona, como el número de habitaciones, baños, ubicación, entre otros. Utiliza un modelo de regresión entrenado previamente.*

## Requisitos
**Para ejecutar este proyecto, asegúrate de tener instaladas las siguientes dependencias:**

- Flask: Framework web para Python.
- Scikit-learn: Biblioteca para Machine Learning.
- NumPy: Biblioteca para cálculo numérico en Python.
*Puedes instalar las dependencias necesarias utilizando pip.*

## Dependencias
Puedes crear un entorno virtual y luego instalar las dependencias con:

```bash
pip install -r requirements.txt
```

**El archivo requirements.txt debe contener lo siguiente:**
```
Flask==2.1.2
scikit-learn==1.0.2
numpy==1.21.2
```
*O puedes instalar las dependencias de forma individual usando los siguientes comandos:*
``` bash
pip install Flask
pip install scikit-learn
pip install numpy
```
## Cómo ejecutar el proyecto
- Paso 1: Prepara el modelo
Asegúrate de tener el archivo model.pkl y scaler.pkl en el directorio raíz del proyecto. Estos archivos contienen el modelo entrenado y el escalador, respectivamente.
Si no tienes los archivos model.pkl y scaler.pkl, necesitarás entrenar un modelo de regresión, ajustarlo y guardarlo en un archivo con pickle.

- Paso 2: Inicia la aplicación
Una vez que tengas el modelo y las dependencias instaladas, puedes ejecutar el proyecto con el siguiente comando:
``` bash
python app.py
```
  *Esto iniciará el servidor de Flask en http://127.0.0.1:5000/.*
- Paso 3: Interactúa con el chatbot
1. Abre tu navegador y visita http://127.0.0.1:5000/.
2. El chatbot te hará una serie de preguntas relacionadas con la vivienda. Responde cada pregunta, y al final, el chatbot te dará una predicción del precio de la vivienda.

## Funciones del proyecto
- El chatbot hace preguntas sobre las características de la vivienda como área, habitaciones, baños, plantas, etc.
- Las respuestas se almacenan temporalmente en la sesión del navegador.
- Una vez que el usuario haya respondido todas las preguntas, el chatbot utiliza un modelo de Machine Learning entrenado para predecir el precio de la vivienda.
- El precio estimado se muestra al usuario.

## Estructura del proyecto
```bash
/proyecto-chatbot
│
├── app.py                # Archivo principal de la aplicación Flask
├── model.pkl             # Modelo de regresión entrenado (previamente generado)
├── scaler.pkl            # Escalador utilizado para normalizar los datos de entrada
├── templates/
│   └── index.html        # Plantilla HTML para la interfaz de usuario
├── requirements.txt      # Dependencias necesarias para el proyecto
└── README.md             # Documentación del proyecto
```

## Posibles errores y soluciones
- **Error**: `FileNotFoundError` al cargar el modelo
Asegúrate de que el archivo model.pkl y scaler.pkl estén en el directorio correcto. Si no los tienes, necesitarás entrenar el modelo y guardarlo.
- **Error**: `ModuleNotFoundError`
Si te falta alguna dependencia, ejecuta el comando:
`pip install -r requirements.txt`

# Licencia
Este proyecto está licenciado bajo la Licencia MIT.
