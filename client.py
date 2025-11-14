import requests
import json

# API endpoint
url = "http://localhost:5000/predict"

# Test patient data
patient_data = {
    "temperature": 103.5,
    "fever_days": 5,
    "headache": 1,
    "body_pain": 1,
    "eye_pain": 1,
    "nausea_vomiting": 0,
    "abdominal_pain": 0,
    "rash": 0,
    "bleeding": 0,
    "platelet_count": 120,
    "mosquito_exposure": 1,
    "travel": 0
}

# Make request
response = requests.post(url, json=patient_data)

# Print results
print("="*60)
print("🏥 FEVER DIAGNOSIS RESULT")
print("="*60)

if response.status_code == 200:
    result = response.json()
    print(f"\n✅ Status: {result['status']}")
    print(f"\n🎯 Prediction: {result['prediction']}")
    print(f"   Confidence: {result['confidence']:.1f}%")
    print(f"\n📊 Top 3 Predictions:")
    for pred in result['top_3_predictions']:
        print(f"   {pred['disease']:12s}: {pred['probability']:5.1f}%")
    print(f"\n📋 Input Summary:")
    print(f"   Temperature: {result['input_summary']['temperature']}°F")
    print(f"   Duration: {result['input_summary']['fever_days']} days")
    print(f"   Symptoms: {', '.join(result['input_summary']['key_symptoms'])}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.json())
