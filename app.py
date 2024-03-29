# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 15:23:32 2022

@author: Hema
"""
import requests
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from tensorflow.python.keras.backend import set_session

app = Flask(__name__)
 
#load both the vegetable and fruit models
model = load_model("vegetable.h5")
model1 = load_model("fruits.h5")
#home page
@app.route('/')
def home():
    return render_template("home.html")

#prediction page
@app.route('/prediction')
def prediction():
    return render_template("predict.html")

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        #get the file from post request
        f = request.files['image']
        #save the file to /uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        img = image.load_img(file_path, target_size=(128,128))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        plant=request.form['plant']
        print(plant)
        if(plant=="vegetable"):
            preds = model.predict_classes(x)
            print(preds)
            df=pd.read_excel('precautions - veg.xlsx')
            print(df.iloc[preds[0]]['caution'])
        else:
            preds = model.predict_classe(x)
            df=pd.read_excel('precautions - fruits.xlsx')
            print(df.iloc[preds[0]]['caution'])
        return df.iloc[preds[0]]['caution']
    
    if __name__ == '__main__':
        app.run(debug=False)
        

