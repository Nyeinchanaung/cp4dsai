from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Result
import os
import pickle
import logging
import numpy as np

# Load the model and scaler from disk
category_encoder_path = './mlmodel/category_encoder.pkl'
k_mean_encoder_path = './mlmodel/k_mean_encoder.pkl'
payment_encoder_path = './mlmodel/payment_encoder.pkl'
percent_scaler_path = './mlmodel/percent_scaler.pkl'
recommender_model_path = './mlmodel/recommender_model.pkl'
state_encoder_path = './mlmodel/state_encoder.pkl'

with open(percent_scaler_path, 'rb') as percent_scaler_model:
    percent_scaler = pickle.load(percent_scaler_model)

with open(payment_encoder_path, 'rb') as payment_encoder_model:
    payment_encoder = pickle.load(payment_encoder_model)

with open(state_encoder_path, 'rb') as state_encoder_model:
    state_encoder = pickle.load(state_encoder_model)

with open(k_mean_encoder_path, 'rb') as k_mean_encoder_model:
    k_mean_encoder = pickle.load(k_mean_encoder_model)

with open(category_encoder_path, 'rb') as category_encoder_model:
    category_encoder = pickle.load(category_encoder_model)


with open(recommender_model_path, 'rb') as model:
    recommender_model = pickle.load(model)


def index(request):
    return render(request, "recommender/index.html")

def result(request):
    X = list()
    Category_list = dict()
    X.append(request.POST.get('age'))
    X.append(percent_scaler.transform([[request.POST.get('discount_percent')]]))
    X.append(payment_encoder.transform([[request.POST.get('payment_method')]]))
    X.append(state_encoder.transform([[request.POST.get('state')]]))
    X.append(k_mean_encoder.transform([[request.POST.get('customer_type')]]))

    for category in category_encoder.classes_:
        # Instead of adding the category as a feature,
        # create a separate model or adjust your existing model
        # to handle the category separately, perhaps as an input parameter
        # or by training the model on data that includes the category as a feature.

        # Here's an example of how to exclude the category from the features:
        #temp_X = X  # Use only the original 5 features

        # Reshape temp_X to a 2D array with one row and multiple columns
        temp_X = np.array(X, dtype="object").reshape(1, -1)

        # Pass temp_X to model.predict
        Category_list[category] = recommender_model.predict(temp_X)[0]
        recommended_product = sorted(Category_list.items(), key=lambda x:x[1], reverse=True)[:8]
        recommended_product_dict_array = [{"category": category, "value": value} for category, value in recommended_product]
        #recommended_product = sorted(Category_list.items(), key=lambda x:x[1], reverse=True)[:8]
        #print(recommended_product)
    return render(request, "recommender/detail.html", {"recommended_category": recommended_product_dict_array})
    #return render(request, "recommender/detail.html", {"recommended_product": Category_list})
    #return render(request, "recommender/detail.html", recommended_product)

def detail(request, result_id):
    result = get_object_or_404(Result, pk=result_id)
    return render(request, "risk_check/detail.html", {"result": result})

# def predict(request):

#     features = np.array([[request.POST.get('year'), request.POST.get('mileage'), request.POST.get('max_power')]])
#     #features = np.array([[2011, 100000, 64]])
#     # Predict the selling price
#     predicted_price_log = loaded_model.predict(features)

#     predicted_price = np.exp(predicted_price_log)

#     sms = "Predicted car price is:"+ str(int(predicted_price[0]))+"."
#     messages.info(request, sms)
#     return redirect('/')
