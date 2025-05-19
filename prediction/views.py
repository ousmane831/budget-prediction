from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import joblib
import numpy as np

# Charger les modèles et l'encodeur
model_recettes = joblib.load("model_recettes.pkl")
model_depenses = joblib.load("model_depenses.pkl")
label_encoder = joblib.load("label_encoder.pkl")

@api_view(["POST"])
def predict_budget(request):
    try:
        commune = request.data.get("commune")
        annee = int(request.data.get("annee"))

        if commune is None or annee is None:
            return Response({"error": "Commune et année sont obligatoires"}, status=400)

        # Encoder la commune
        if commune not in label_encoder.classes_:
            return Response({"error": "Commune inconnue"}, status=400)
        
        commune_encoded = label_encoder.transform([commune])[0]

        X = np.array([[commune_encoded, annee]])

        recettes_pred = model_recettes.predict(X)[0]
        depenses_pred = model_depenses.predict(X)[0]

        return Response({
            "commune": commune,
            "annee": annee,
            "recettes": round(recettes_pred, 2),
            "depenses": round(depenses_pred, 2)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)


from django.shortcuts import render

def prediction_interface(request):
    return render(request, 'predict.html')  # Assure-toi que le fichier HTML est dans le dossier templates
