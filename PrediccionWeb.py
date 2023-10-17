import os
import tempfile
from flask import Flask, request, redirect, render_template, url_for
from skimage import io
import base64
from skimage.transform import resize
import numpy as np
from tensorflow.keras.models import load_model
import cv2

model = load_model('modelo_entrenado.h5')
app = Flask(__name__, template_folder="templates/")

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("1!")
        img_data = request.form.get('myImage').replace("data:image/png;base64,","")
        img_binary = base64.b64decode(img_data)
        image = cv2.imdecode(np.frombuffer(img_binary, np.uint8), cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_resized = cv2.resize(img_gray, (28, 28))
        img_array = img_resized.reshape(1, 28, 28, 1)
        
        salida = model.predict(img_array)[0]
        print(salida)
        
        nums = salida*100
        print(nums)
        numeros_formateados = [f'{numero:.2f}' for numero in nums]
        print("13!")
        cadena_formateada = ', '.join(numeros_formateados)
        print("14!")
        return redirect(url_for('show_predictions', nums=cadena_formateada, img_data=img_data))
    except Exception as e:
        print("Error occurred: ", e)

    return redirect("/", code=302)

@app.route('/predicciones')
def show_predictions():
    nums = request.args.get('nums')
    img_data = request.args.get('img_data')
    componentes = nums.split(', ')
    nums = [float(componente) for componente in componentes]
    frutas = ["Platano", "Pera", "Manzana"]
    if img_data is not None:
        return render_template('Prediccion.html', nums=nums, frutas=frutas, img_data=img_data)
    else:
        return redirect("/", code=302)


if __name__ == "__main__":
    app.run()
