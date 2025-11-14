#!/bin/bash

echo "========================================="
echo "🏥 FEVER DIAGNOSIS API - TEST SUITE"
echo "========================================="

# Test 1: Health Check
echo -e "\n1️⃣ Health Check:"
curl -X GET http://localhost:5000/health
echo -e "\n"

# Test 2: API Info
echo -e "\n2️⃣ API Info:"
curl -X GET http://localhost:5000/
echo -e "\n"

# Test 3: Dengue Case (High fever, headache, body pain, eye pain, low platelets)
echo -e "\n3️⃣ Test Case: Suspected Dengue"
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
echo -e "\n"

# Test 4: Typhoid Case (Prolonged fever, abdominal pain)
echo -e "\n4️⃣ Test Case: Suspected Typhoid"
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 101.5,
    "fever_days": 10,
    "headache": 1,
    "body_pain": 0,
    "eye_pain": 0,
    "nausea_vomiting": 1,
    "abdominal_pain": 1,
    "rash": 0,
    "bleeding": 0,
    "platelet_count": 180,
    "mosquito_exposure": 0,
    "travel": 0
  }'
echo -e "\n"

# Test 5: Malaria Case (High fever, travel history)
echo -e "\n5️⃣ Test Case: Suspected Malaria"
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 104.0,
    "fever_days": 4,
    "headache": 1,
    "body_pain": 1,
    "eye_pain": 0,
    "nausea_vomiting": 1,
    "abdominal_pain": 0,
    "rash": 0,
    "bleeding": 0,
    "platelet_count": 160,
    "mosquito_exposure": 0,
    "travel": 1
  }'
echo -e "\n"

# Test 6: Viral Fever (Short duration, mild)
echo -e "\n6️⃣ Test Case: Suspected Viral Fever"
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 100.5,
    "fever_days": 2,
    "headache": 1,
    "body_pain": 0,
    "eye_pain": 0,
    "nausea_vomiting": 0,
    "abdominal_pain": 0,
    "rash": 0,
    "bleeding": 0,
    "platelet_count": 230,
    "mosquito_exposure": 0,
    "travel": 0
  }'
echo -e "\n"

echo "========================================="
echo "✅ Test Suite Complete!"
echo "========================================="
