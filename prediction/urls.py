from django.urls import path
from .views import predict_budget, prediction_interface

urlpatterns = [
    path('', prediction_interface, name='interface'),
    path('predict/', predict_budget, name='predict-budget'),
]
