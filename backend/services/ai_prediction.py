import numpy as np
from datetime import datetime
import json
import os

class HealthPredictionService:
    """AI-powered health risk prediction service"""

    def __init__(self):
        self.model = None
        self.scaler = None

    def load_model(self):
        """Load pre-trained ML model"""
        try:
            import joblib
            model_path = 'models/health_risk_model.pkl'
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print("Health prediction model loaded")
            else:
                print("Model not found - using rule-based prediction")
        except Exception as e:
            print(f"Model loading error: {e}")

    def predict_risk(self, health_record):
        """Predict health risk based on vital signs"""
        try:
            # Extract features from health record
            features = self._extract_features(health_record)

            # Use rule-based system (can be replaced with ML model)
            risk_score = self._rule_based_prediction(features)

            # Determine risk level
            risk_level = self._determine_risk_level(risk_score)

            # Generate recommendations
            recommendations = self._generate_recommendations(features, risk_level)

            return {
                'risk_score': float(risk_score),
                'risk_level': risk_level,
                'recommendations': recommendations,
                'prediction_timestamp': datetime.utcnow().isoformat()
            }

        except Exception as e:
            print(f"Prediction error: {e}")
            return {
                'risk_score': 0.5,
                'risk_level': 'medium',
                'recommendations': ['कृपया डॉक्टर से सलाह लें'],
                'error': str(e)
            }

    def _extract_features(self, health_record):
        """Extract and normalize features from health record"""
        features = {}

        # Age (estimated if not provided)
        features['age'] = getattr(health_record, 'age', 35)

        # Gender encoding (male=1, female=0)
        gender = getattr(health_record, 'gender', 'male')
        features['gender_encoded'] = 1 if gender.lower() == 'male' else 0

        # Vital signs
        features['bp_systolic'] = health_record.blood_pressure_systolic or 120
        features['bp_diastolic'] = health_record.blood_pressure_diastolic or 80
        features['heart_rate'] = health_record.heart_rate or 72
        features['temperature'] = health_record.temperature or 98.6
        features['weight'] = health_record.weight or 60

        # Calculate BMI (assuming height if not provided)
        height = getattr(health_record, 'height', 165) / 100  # Convert cm to m
        features['bmi'] = features['weight'] / (height * height)

        return features

    def _rule_based_prediction(self, features):
        """Rule-based health risk assessment"""
        risk_factors = 0

        # Blood pressure risk
        if features['bp_systolic'] > 140 or features['bp_diastolic'] > 90:
            risk_factors += 0.3
        elif features['bp_systolic'] > 130 or features['bp_diastolic'] > 85:
            risk_factors += 0.2

        # Heart rate risk
        if features['heart_rate'] > 100 or features['heart_rate'] < 60:
            risk_factors += 0.2

        # Temperature risk
        if features['temperature'] > 100.4 or features['temperature'] < 95:
            risk_factors += 0.25

        # BMI risk
        if features['bmi'] > 30:
            risk_factors += 0.15
        elif features['bmi'] > 25:
            risk_factors += 0.1

        # Age risk
        if features['age'] > 60:
            risk_factors += 0.1

        return min(risk_factors, 1.0)

    def _determine_risk_level(self, risk_score):
        """Convert risk score to categorical level"""
        if risk_score >= 0.8:
            return 'critical'
        elif risk_score >= 0.6:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        else:
            return 'low'

    def _generate_recommendations(self, features, risk_level):
        """Generate health recommendations based on risk factors"""
        recommendations = []

        # Blood pressure recommendations
        if features['bp_systolic'] > 140:
            recommendations.extend([
                "रक्तचाप अधिक है - तुरंत आराम करें",
                "नमक और तनाव कम करें",
                "डॉक्टर से तुरंत सलाह लें"
            ])

        # Heart rate recommendations
        if features['heart_rate'] > 100:
            recommendations.extend([
                "हृदय गति तेज़ है - शांत रहें",
                "गहरी सांस लें और आराम करें"
            ])

        # Temperature recommendations
        if features['temperature'] > 100.4:
            recommendations.extend([
                "बुखार है - तरल पदार्थ लें",
                "पैरासिटामोल ले सकते हैं",
                "यदि बुखार बना रहे तो डॉक्टर से मिलें"
            ])

        # BMI recommendations
        if features['bmi'] > 25:
            recommendations.extend([
                "वजन नियंत्रण की आवश्यकता",
                "संतुलित आहार और व्यायाम करें"
            ])

        # General recommendations by risk level
        if risk_level == 'critical':
            recommendations.insert(0, "🚨 तत्काल चिकित्सा सहायता लें")
        elif risk_level == 'high':
            recommendations.insert(0, "⚠️ 24 घंटे में डॉक्टर से मिलें")
        elif risk_level == 'medium':
            recommendations.append("📅 जल्द ही स्वास्थ्य जांच कराएं")
        else:
            recommendations.append("✅ स्वास्थ्य सामान्य है, नियमित जांच कराते रहें")

        return recommendations[:5]  # Return top 5 recommendations
