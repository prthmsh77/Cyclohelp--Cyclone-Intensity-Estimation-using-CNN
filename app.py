from flask import Flask, render_template, request, url_for
from PIL import Image,ImageOps
import alert
import numpy as np
import io
from tensorflow import keras
model = keras.models.load_model('cyclohelp_keras_model')
inform = "Cyclone intensity Estimation"
global output
output = "alert not raised"
global body
body = "This message is sent by cyclohelp alert system, an typhoon has been predicted by our system.Be aware\n"
extra = ""
emails = ['pdnigade77@gmail.com','shendagedipali73@gmail.com']
category = ""
damage = ""

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    # if request.method == "POST":
    #     print(request.form)
    #     inform = request.form.values
    return render_template("index.html")

@app.route("/emergency")
def show_alert():
    return render_template("emergency.html",alert_text=output)


@app.route('/predict',methods=['POST'])
def predict(): 
   extra = request.form['text']
   global body
   body += extra
   for email in emails:
        alert.email_alert("Cyclone Alert by CYCLOHELP ",body,email)
        
   
   output="Alert Raised !" 
   return render_template('emergency.html',alert_text=output)

@app.route("/about")
def show_about():
    return render_template("about.html")

@app.route('/upload', methods=['POST'])
def upload():
    image_file = request.files['upload_costum']
    image = Image.open(image_file)
    image = image.convert('L')
    image = ImageOps.fit(image,(201, 201), Image.ANTIALIAS)
    # image = np.invert(image)
    image = np.array(image) / 255
    image = np.expand_dims(image, axis=0)
    image = np.expand_dims(image, axis=3)
    prediction = model.predict(image)[0][0]
 
    if prediction< 20 :
        category = "No Cyclone Detected"
        damage = "None"
    elif prediction> 20 and prediction<=33:
        category = "Tropical Dispersion"
        damage = "Small"
    elif prediction>33 and prediction<=63:
        category = "Tropical storm"
        damage = "Significant"
    elif prediction> 63 and prediction<=82:
        category = "One(H1)"
        damage = "Significant"
    elif prediction> 82 and prediction<=95:
        category = "Two(H2)"
        damage = "Extensive"
    elif prediction> 95 and prediction<=112:
        category = "Three(H3)"
        damage = "Devastating"
    elif prediction> 112 and prediction<=136:
        category = "Four(H4)"
        damage = "Catastropic"
    elif prediction> 136:
        category = "Five(H5)"
        damage = "Catastropic"

    if prediction>50:
        global output
        output="Alert Raised !"
        for email in emails:
            alert.email_alert("Cyclone Alert by CYCLOHELP ",body,email)
    else:
        output="Alert Not Raised !"
    
    
    return render_template("index.html",pred = prediction,alert_text = output,Category = category,Damage = damage)


if __name__ == '__main__':
    app.run(debug=True)
