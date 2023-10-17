import os
import tempfile
from flask import Flask, request, redirect, render_template, url_for
from skimage import io
import base64
from skimage.transform import resize
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('modelo_entrenado.h5')
app = Flask(__name__, template_folder="templates/")

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("1!")
        img_data = request.form.get('myImage').replace("data:image/png;base64,", "")
        with tempfile.NamedTemporaryFile(delete=False, mode="w+b", suffix='.png', dir=str('prediccion')) as fh:
            fh.write(base64.b64decode(img_data))
            tmp_file_path = fh.name
        print("2!")
        imagen = io.imread(tmp_file_path)
        print("3!")
        imagen = imagen[:, :, 3]
        print("4!")
        size = (28, 28)
        print("5!")
        image = imagen / 255.0
        print("6!")
        im = resize(image, size)
        print("7!")
        im = im[:, :, np.newaxis]
        print("8!")
        im = im.reshape(1, *im.shape)
        print("9!")
        salida = model.predict(im)[0]
        print("10!")
        os.remove(tmp_file_path)
        print("11!")
        nums = salida*100
        print("12!")
        numeros_formateados = [f'{numero:.2f}' for numero in nums]
        print("13!")
        cadena_formateada = ', '.join(numeros_formateados)
        print("14!")
        return redirect(url_for('show_predictions', nums=cadena_formateada, img_data=img_data))
    except:
        print("Error occurred")

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
