from app import create_app
from dotenv import load_dotenv
import os

print("Starting Flask application...")

load_dotenv()

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == "__main__":
    print("Flask app is running")
    app.run(host="0.0.0.0", port=5000, debug=True)