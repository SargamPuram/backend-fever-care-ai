from flask import Flask, request, jsonify
import pickle
import json
import numpy as np
import pandas as pd
from flask_cors import CORS
from sklearn.ensemble import GradientBoostingClassifier

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

print("="*80)
print("🏥 FEVER DIAGNOSIS API - LOADING MODEL")
print("="*80)

# Load the trained model
try:
    with open('fever_diagnosis_model_new.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Load label encoder
try:
    with open('label_encoder_new.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    print("✅ Label encoder loaded")
    print(f"   Classes: {list(label_encoder.classes_)}")
except Exception as e:
    print(f"❌ Error loading encoder: {e}")
    label_encoder = None

# Load feature info
try:
    with open('model_info_new.json', 'r') as f:
        model_info = json.load(f)
    feature_cols = model_info['feature_cols']
    print(f"✅ Feature info loaded")
    print(f"   Features: {len(feature_cols)}")
    print(f"   Model: {model_info['model_name']}")
    print(f"   CV Accuracy: {model_info['cv_accuracy']*100:.1f}%")
except Exception as e:
    print(f"❌ Error loading feature info: {e}")
    feature_cols = None

print("="*80)
print("🚀 API READY - Server starting...")
print("="*80)


@app.route('/', methods=['GET'])
def home():
    """API home page with info"""
    return jsonify({
        'status': 'online',
        'model': model_info.get('model_name', 'Unknown'),
        'accuracy': f"{model_info.get('cv_accuracy', 0)*100:.1f}%",
        'diseases': list(label_encoder.classes_) if label_encoder else [],
        'endpoints': {
            '/': 'GET - API info',
            '/predict': 'POST - Make prediction',
            '/health': 'GET - Health check'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    is_healthy = (model is not None and 
                  label_encoder is not None and 
                  feature_cols is not None)
    
    return jsonify({
        'status': 'healthy' if is_healthy else 'unhealthy',
        'model_loaded': model is not None,
        'encoder_loaded': label_encoder is not None,
        'features_loaded': feature_cols is not None
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict disease from patient symptoms
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'status': 'failed'
            }), 400
        
        # Extract basic features
        basic_features = {
            'temperature': float(data.get('temperature', 100)),
            'fever_days': int(data.get('fever_days', 3)),
            'headache': int(data.get('headache', 0)),
            'body_pain': int(data.get('body_pain', 0)),
            'eye_pain': int(data.get('eye_pain', 0)),
            'nausea_vomiting': int(data.get('nausea_vomiting', 0)),
            'abdominal_pain': int(data.get('abdominal_pain', 0)),
            'rash': int(data.get('rash', 0)),
            'bleeding': int(data.get('bleeding', 0)),
            'platelet_count': float(data.get('platelet_count', 200)),
            'mosquito_exposure': int(data.get('mosquito_exposure', 0)),
            'travel': int(data.get('travel', 0))
        }
        
        # Engineer features (same as training)
        engineered = {
            'temp_high': int(basic_features['temperature'] >= 103),
            'temp_very_high': int(basic_features['temperature'] >= 105),
            'duration_short': int(basic_features['fever_days'] <= 3),
            'duration_prolonged': int(basic_features['fever_days'] > 7),
            'platelet_low': int(basic_features['platelet_count'] < 150),
            'platelet_very_low': int(basic_features['platelet_count'] < 100),
            'dengue_triad': int(
                basic_features['headache'] == 1 and
                basic_features['body_pain'] == 1 and
                basic_features['eye_pain'] == 1
            ),
            'gi_symptoms': int(
                basic_features['nausea_vomiting'] == 1 or
                basic_features['abdominal_pain'] == 1
            )
        }
        
        # Combine all features
        all_features = {**basic_features, **engineered}
        
        # Create feature vector in correct order
        feature_vector = [all_features[col] for col in feature_cols]
        
        # ✅ FIX: Convert to DataFrame with proper feature names
        feature_df = pd.DataFrame([feature_vector], columns=feature_cols)
        
        # Make prediction
        prediction_encoded = model.predict(feature_df)[0]
        prediction_proba = model.predict_proba(feature_df)[0]
        
        # Decode prediction
        predicted_disease = label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Get confidence scores for all diseases
        confidence_scores = {}
        for idx, disease in enumerate(label_encoder.classes_):
            confidence_scores[disease] = float(prediction_proba[idx] * 100)
        
        # Sort by confidence
        sorted_predictions = sorted(
            confidence_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return jsonify({
            'status': 'success',
            'prediction': predicted_disease,
            'confidence': float(prediction_proba[prediction_encoded] * 100),
            'all_probabilities': confidence_scores,
            'top_3_predictions': [
                {'disease': disease, 'probability': prob}
                for disease, prob in sorted_predictions[:3]
            ],
            'input_summary': {
                'temperature': basic_features['temperature'],
                'fever_days': basic_features['fever_days'],
                'key_symptoms': [
                    symptom for symptom in ['headache', 'body_pain', 'eye_pain', 
                                           'nausea_vomiting', 'abdominal_pain', 
                                           'rash', 'bleeding']
                    if basic_features.get(symptom, 0) == 1
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500


if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
