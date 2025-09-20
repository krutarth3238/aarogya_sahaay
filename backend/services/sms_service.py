from flask import current_app
import logging

class SMSService:
    """SMS service for health communications using Twilio"""

    def __init__(self):
        self.client = None
        self.phone_number = None

    def init_app(self, app):
        try:
            from twilio.rest import Client
            account_sid = app.config.get('TWILIO_ACCOUNT_SID')
            auth_token = app.config.get('TWILIO_AUTH_TOKEN')
            self.phone_number = app.config.get('TWILIO_PHONE_NUMBER')

            if account_sid and auth_token:
                self.client = Client(account_sid, auth_token)
        except ImportError:
            print("Twilio not installed - SMS functionality disabled")

    def send_sms(self, phone_number, message):
        """Send SMS message"""
        try:
            if not self.client:
                print("Twilio SMS not configured - simulating SMS send")
                print(f"SMS to {phone_number}: {message}")
                return True

            # Format phone number for Indian numbers
            if not phone_number.startswith('+'):
                if phone_number.startswith('91'):
                    phone_number = '+' + phone_number
                else:
                    phone_number = '+91' + phone_number

            message_instance = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=phone_number
            )

            print(f"SMS sent to {phone_number}: {message_instance.sid}")
            return True

        except Exception as e:
            print(f"SMS send error: {e}")
            return False

    def send_otp(self, phone_number, otp):
        """Send OTP via SMS"""
        message = f"आरोग्य सहायक: आपका OTP {otp} है। यह 5 मिनट में समाप्त हो जाएगा। इसे किसी के साथ साझा न करें।"
        return self.send_sms(phone_number, message)

    def send_health_alert(self, phone_number, patient_name, alert_type):
        """Send health alert SMS"""
        try:
            alert_messages = {
                'emergency': f"🚨 आपातकाल: {patient_name} को तत्काल चिकित्सा सहायता चाहिए। तुरंत संपर्क करें।",
                'high_risk': f"⚠️ चेतावनी: {patient_name} का स्वास्थ्य जोखिम अधिक है। कृपया तुरंत जांच कराएं।",
                'medication': f"💊 याददाश्त: {patient_name}, यह आपकी दवा का समय है।",
                'appointment': f"📅 अपॉइंटमेंट: {patient_name}, आपकी कल स्वास्थ्य जांच है।"
            }

            message = alert_messages.get(alert_type, f"स्वास्थ्य अपडेट: {patient_name}, अपने स्वास्थ्य का ख्याल रखें।")
            return self.send_sms(phone_number, message)

        except Exception as e:
            print(f"Health alert SMS error: {e}")
            return False

    def send_bulk_sms(self, recipients, message):
        """Send bulk SMS messages"""
        results = []
        for phone in recipients:
            try:
                result = self.send_sms(phone, message)
                results.append({'phone': phone, 'success': result})
            except Exception as e:
                results.append({'phone': phone, 'success': False, 'error': str(e)})

        return results
