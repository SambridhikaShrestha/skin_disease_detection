from django.shortcuts import render, HttpResponse
import keras
from PIL import Image
import numpy as np
import os
from django.core.files.storage import FileSystemStorage

# Load the model
model = keras.models.load_model('savedModel/model.h5')


def convertIMG(testing_img):
    img = Image.open(testing_img)
    img_resized = img.resize((28, 28))
    img_rgb = img_resized.convert('RGB')
    img_array = np.array(img_rgb)
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]  
    if img_array.shape[:2] != (28, 28):
        raise ValueError("Image size is not as expected")
    return img_array

def getPrediction(testing_img):
    img_input = np.expand_dims(convertIMG(testing_img), axis=0)
    res = np.argmax(model.predict(img_input))
    classes = ['Actinic Keratoses', 'Basal Cell Carcinoma', 'Benign Keratosis', 'Dermatolibroma', 'Melanacylic Nevi', 'Vascular Skin Lecione', 'Melanoma']  # Assuming you have these classes
    
    disease = classes[res]
    if disease == 'Actinic Keratoses':
        medicine_recommendation = 'Fluorouracil cream (5-FU), Imiquimod cream'
    elif disease == 'Basal Cell Carcinoma':
        medicine_recommendation = 'Imiquimod cream, 5% 5-fluorouracil cream'
    elif disease == 'Benign Keratosis':
        medicine_recommendation = 'Topical retinaide, Hydroquinone cream'
    elif disease == 'Dermatolibroma':
        medicine_recommendation = 'Topical corticosteroids'
    elif disease == 'Melanacylic Nevi':
        medicine_recommendation = 'No specific cream recommended, Kindly visit to the doctor'
    elif disease == 'Vascular Skin Lecione':
        medicine_recommendation = 'Topical corticosteroids, Calcineurin inhibitors'
    elif disease == 'Melanoma':
        medicine_recommendation = 'Kindly visit to the doctor'

    return disease, medicine_recommendation



def index(request):
    if request.method == "POST" and request.FILES.get('upload'):
        upload = request.FILES["upload"]
        if not upload:
            err = 'No image selected'
            return render(request, 'index.html', {'err': err})
        fss = FileSystemStorage()       
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        disease, medicine_recommendation = getPrediction(os.path.join('media', file))
        return render(request, 'index.html', {'disease': disease, 'medicine_recommendation': medicine_recommendation, 'file_url': file_url})
    else:
        return render(request, 'index.html')