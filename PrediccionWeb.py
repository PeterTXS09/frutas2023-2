import os
import tempfile
from flask import Flask, request, redirect, render_template, url_for, flash
from skimage import io
import base64
from skimage.transform import resize
import numpy as np
from tensorflow.keras.models import load_model
import cv2

model = load_model('modelo_entrenado.h5')
app = Flask(__name__, template_folder="templates/")
app.secret_key = "super secret key"

@app.route("/")
def main():
    return render_template("index.html")


@app.route('/predict')
def predict_page():
    return render_template('predict.html')
    

@app.route('/predict', methods=['POST'])
def predict():
    try:
        img_data = request.form.get('myImage').replace("data:image/png;base64,","")
        img_binary = base64.b64decode(img_data)
        image = cv2.imdecode(np.frombuffer(img_binary, np.uint8), cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_resized = cv2.resize(img_gray, (28, 28))
        img_array = img_resized.reshape(1, 28, 28, 1)
        
        salida = model.predict(img_array)[0]

        etiquetas = {0: "Manzana", 1: "Pera", 2: "Platano"}

        valor = np.argmax(salida)

        if valor in etiquetas:
            kind = etiquetas[valor]
            print(f"Kind: {kind}")
        else:
            print("El valor predicho no tiene una etiqueta asociada.")
        return render_template('predict.html',value=kind)
        
    except Exception as e:
        print("Error occurred: ", e)

    return redirect("/")


if __name__ == "__main__":
    app.run()
