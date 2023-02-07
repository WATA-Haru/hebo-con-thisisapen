import io
import os
import json
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

# Imports the Google Cloud client library
from google.cloud import vision

IMG_PATH = 'imgs'
header_img_path = "imgs/mannenhitsu.png" 

# Instantiates a client 
credentials_dict = json.loads(st.secrets["google_credentials"])
client = vision.ImageAnnotatorClient.from_service_account_info(info=credentials_dict)
# client = vision.ImageAnnotatorClient()

# introduce txt
st.write("## ペンの画像を入れてみよう！")
st.write(" *ペン以外をいれると．．．？ 試してみよう* ")

header_img = Image.open(header_img_path)
st.image(header_img, width=100)

# file upload
upload_file = st.file_uploader("", type=["png", "jpg", "jpeg"])
if upload_file is not None:
    # save image
    if "png" in upload_file.name:
        file_extentsion = "png"
    elif "jpg" in upload_file.name:
        file_extentsion = "jpg"
    elif "jpeg" in upload_file.name:
        file_extentsion = "jpeg"

    file_name = os.path.join(IMG_PATH, "upload_file" +"."+ file_extentsion)
    with open(file_name, 'wb') as f:
        f.write(upload_file.read())
    
    # show upload image
    img = Image.open(upload_file)
    st.image(img)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    is_pen = False
    for label in labels:
        # st.write(label.description)
        if label.description == "Pen":
            is_pen = True
    
    if is_pen:
        audio_file = open('audio/this_is_a_pen.wav', 'rb')
        audio_bytes = audio_file.read()
        st.write("# This is a Pen !!!!!")
        st.audio(audio_bytes, format="audio/wav")
    else:
        audio_file = open('audio/this_is_not_a_pen.wav', 'rb')
        audio_bytes = audio_file.read()
        st.write("# This is NOT a Pen .....")
        st.audio(audio_bytes, format="audio/wav")

st.write("TA_watahiki")
