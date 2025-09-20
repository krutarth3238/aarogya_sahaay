import requests
import json
from flask import current_app

class WhatsAppService:
    """WhatsApp Business API integration for health communications"""

    def __init__(self):
        self.api_url = None
        self.access_token = None
        self.phone_id = None

    def init_app(self, app):
        self.api_url = app.config.get('WHATSAPP_API_URL')
        self.access_token = app.config.get('WHATSAPP_ACCESS_TOKEN')
        self.phone_id = app.config.get('WHATSAPP_PHONE_ID')

    def send_message(self, phone_number, message, message_type='text'):
        """Send WhatsApp message"""
        try:
            if not all([self.api_url, self.access_token, self.phone_id]):
                print("WhatsApp API not configured - simulating message")
                print(f"WhatsApp to {phone_number}: {message}")
                return True

            # Format phone number (remove + and country code handling)
            if phone_number.startswith('+'):
                phone_number = phone_number[1:]
            if not phone_number.startswith('91'):
                phone_number = '91' + phone_number

            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }

            data = {
                'messaging_product': 'whatsapp',
                'to': phone_number,
                'type': message_type,
                'text': {
                    'body': message
                }
            }

            response = requests.post(
                f"{self.api_url}/{self.phone_id}/messages",
                headers=headers,
                json=data,
                timeout=10
            )

            if response.status_code == 200:
                print(f"WhatsApp message sent to {phone_number}")
                return True
            else:
                print(f"WhatsApp API error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"WhatsApp send error: {e}")
            return False

    def send_health_alert(self, phone_number, patient_name, alert_type, severity):
        """Send health-specific alert messages"""
        try:
            alert_messages = {
                'high_bp': f"🚨 {patient_name}, आपका रक्तचाप बहुत अधिक है ({severity})। कृपया तुरंत आराम करें और ASHA कार्यकर्ता से संपर्क करें।",
                'high_temperature': f"🌡️ {patient_name}, आपका बुखार खतरनाक स्तर पर है। तुरंत चिकित्सा सहायता लें।",
                'low_oxygen': f"⚠️ {patient_name}, ऑक्सीजन का स्तर कम है। गहरी सांस लें और तुरंत डॉक्टर से मिलें।",
                'emergency': f"🚨 आपातकाल: {patient_name} को तत्काल चिकित्सा सहायता की आवश्यकता है।",
                'medication_reminder': f"💊 {patient_name}, यह आपकी दवा का समय है। कृपया अपनी दवा लें।",
                'appointment_reminder': f"📅 {patient_name}, आपकी कल अपॉइंटमेंट है। कृपया समय पर पहुंचें।"
            }

            message = alert_messages.get(alert_type, f"स्वास्थ्य अलर्ट: {patient_name}, कृपया अपने स्वास्थ्य पर ध्यान दें।")
            return self.send_message(phone_number, message)

        except Exception as e:
            print(f"Health alert error: {e}")
            return False

    def send_bulk_message(self, phone_numbers, message):
        """Send bulk messages (for community health campaigns)"""
        results = []
        for phone in phone_numbers:
            try:
                result = self.send_message(phone, message)
                results.append({'phone': phone, 'success': result})
                # Rate limiting
                import time
                time.sleep(0.1)
            except Exception as e:
                results.append({'phone': phone, 'success': False, 'error': str(e)})

        return results
