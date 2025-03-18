import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so Python can find your modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import your Firebase service
from services.firebase_service import FirebaseService

def test_firebase_connection():
    print("Testing Firebase connection...")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Create the Firebase service instance
    firebase = FirebaseService()
    
    try:
        # Try to initialize the connection
        firebase.initialize()
        print("✅ Firebase connection successful!")
        
        # Test getting a list of resources
        resources = firebase.get_resources(limit=10)
        print(f"✅ Successfully retrieved {len(resources)} resources from Firestore")
        
        return True
    except Exception as e:
        print(f"❌ Firebase connection failed: {e}")
        return False

if __name__ == "__main__":
    result = test_firebase_connection()
    print(f"Test completed with {'success' if result else 'failure'}")
