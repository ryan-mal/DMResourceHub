import os
import json
import datetime
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore, storage
from dotenv import load_dotenv

from models.resource import Resource
from models.campaign import Campaign
from models.player import Player

class FirebaseService:
    """Service for interacting with Firebase (Firestore and Storage)"""
    
    def __init__(self):
        """Initialize the Firebase service"""
        self.app = None
        self.db = None
        self.bucket = None
        self.initialized = False
    
    def initialize(self):
        """Initialize Firebase connection"""
        if self.initialized:
            return
    
        try:
            # Load environment variables from .env file
            load_dotenv()
        
            # Check for credentials file
            cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
            if not cred_path:
                # Check if credentials exist in the config directory
                default_path = Path("config/firebase-credentials.json")
                if default_path.exists():
                    cred_path = str(default_path)
                else:
                    raise ValueError("Firebase credentials not found. Please set FIREBASE_CREDENTIALS_PATH in .env file.")
        
            # Initialize Firebase app
            cred = credentials.Certificate(cred_path)
        
            # Check if storage bucket is specified
            storage_bucket = os.getenv("FIREBASE_STORAGE_BUCKET")
            if storage_bucket:
                self.app = firebase_admin.initialize_app(cred, {
                    'storageBucket': storage_bucket
                })
                # Initialize Storage only if bucket is specified
                self.bucket = storage.bucket()
            else:
                # Initialize without storage bucket
                self.app = firebase_admin.initialize_app(cred)
                self.bucket = None
        
            # Initialize Firestore
            self.db = firestore.client()
        
            self.initialized = True
            print("Firebase initialized successfully")
        
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            raise
    
    # Resource methods
    
    def get_resources(self, limit=50):
        """Get a list of resources
        
        Args:
            limit (int, optional): Maximum number of resources to return. Defaults to 50.
            
        Returns:
            list: List of Resource objects
        """
        self._ensure_initialized()
        
        resources = []
        try:
            resource_refs = self.db.collection('resources').limit(limit).get()
            for doc in resource_refs:
                resource = Resource.from_dict(doc.id, doc.to_dict())
                resources.append(resource)
        except Exception as e:
            print(f"Error getting resources: {e}")
        
        return resources
    
    def get_resource(self, resource_id):
        """Get a specific resource by ID
        
        Args:
            resource_id (str): Resource ID
            
        Returns:
            Resource: Resource object or None if not found
        """
        self._ensure_initialized()
        
        try:
            doc = self.db.collection('resources').document(resource_id).get()
            if doc.exists:
                return Resource.from_dict(doc.id, doc.to_dict())
        except Exception as e:
            print(f"Error getting resource {resource_id}: {e}")
        
        return None
    
    def add_resource(self, resource):
        """Add a new resource to Firestore
        
        Args:
            resource (Resource): Resource object
            
        Returns:
            str: ID of the created resource, or None if failed
        """
        self._ensure_initialized()
        
        try:
            # Set timestamps if not set
            if not resource.uploaded_at:
                resource.uploaded_at = firestore.SERVER_TIMESTAMP
            
            # Add resource to Firestore
            doc_ref = self.db.collection('resources').document()
            doc_ref.set(resource.to_dict())
            
            # Update resource ID and return it
            resource.id = doc_ref.id
            return doc_ref.id
        except Exception as e:
            print(f"Error adding resource: {e}")
        
        return None
    
    def update_resource(self, resource):
        """Update an existing resource in Firestore
        
        Args:
            resource (Resource): Resource object with updated values
            
        Returns:
            bool: True if successful, False otherwise
        """
        self._ensure_initialized()
        
        if not resource.id:
            print("Error updating resource: No resource ID provided")
            return False
        
        try:
            self.db.collection('resources').document(resource.id).update(resource.to_dict())
            return True
        except Exception as e:
            print(f"Error updating resource {resource.id}: {e}")
        
        return False
    
    def delete_resource(self, resource_id):
        """Delete a resource from Firestore
        
        Args:
            resource_id (str): Resource ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        self._ensure_initialized()
        
        try:
            self.db.collection('resources').document(resource_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting resource {resource_id}: {e}")
        
        return False
    
    # Campaign methods
    
    def get_campaigns(self):
        """Get a list of campaigns
        
        Returns:
            list: List of Campaign objects
        """
        self._ensure_initialized()
        
        campaigns = []
        try:
            campaign_refs = self.db.collection('campaigns').get()
            for doc in campaign_refs:
                campaign = Campaign.from_dict(doc.id, doc.to_dict())
                campaigns.append(campaign)
        except Exception as e:
            print(f"Error getting campaigns: {e}")
        
        return campaigns
    
    def get_campaign(self, campaign_id):
        """Get a specific campaign by ID
        
        Args:
            campaign_id (str): Campaign ID
            
        Returns:
            Campaign: Campaign object or None if not found
        """
        self._ensure_initialized()
        
        try:
            doc = self.db.collection('campaigns').document(campaign_id).get()
            if doc.exists:
                return Campaign.from_dict(doc.id, doc.to_dict())
        except Exception as e:
            print(f"Error getting campaign {campaign_id}: {e}")
        
        return None
    
    def add_campaign(self, campaign):
        """Add a new campaign to Firestore
        
        Args:
            campaign (Campaign): Campaign object
            
        Returns:
            str: ID of the created campaign, or None if failed
        """
        self._ensure_initialized()
        
        try:
            # Set timestamps if not set
            if not campaign.created_at:
                campaign.created_at = firestore.SERVER_TIMESTAMP
            if not campaign.updated_at:
                campaign.updated_at = firestore.SERVER_TIMESTAMP
            
            # Add campaign to Firestore
            doc_ref = self.db.collection('campaigns').document()
            doc_ref.set(campaign.to_dict())
            
            # Update campaign ID and return it
            campaign.id = doc_ref.id
            return doc_ref.id
        except Exception as e:
            print(f"Error adding campaign: {e}")
        
        return None
    
    # Player methods
    
    def get_players(self):
        """Get a list of players
        
        Returns:
            list: List of Player objects
        """
        self._ensure_initialized()
        
        players = []
        try:
            player_refs = self.db.collection('players').get()
            for doc in player_refs:
                player = Player.from_dict(doc.id, doc.to_dict())
                players.append(player)
        except Exception as e:
            print(f"Error getting players: {e}")
        
        return players
    
    def add_player(self, player):
        """Add a new player to Firestore
        
        Args:
            player (Player): Player object
            
        Returns:
            str: ID of the created player, or None if failed
        """
        self._ensure_initialized()
        
        try:
            # Set timestamps if not set
            if not player.added_at:
                player.added_at = firestore.SERVER_TIMESTAMP
            
            # Add player to Firestore
            doc_ref = self.db.collection('players').document()
            doc_ref.set(player.to_dict())
            
            # Update player ID and return it
            player.id = doc_ref.id
            return doc_ref.id
        except Exception as e:
            print(f"Error adding player: {e}")
        
        return None
    
    # Storage methods
    
    def upload_file(self, file_path, destination_path):
        """Upload a file to Firebase Storage
    
        Args:
            file_path (str): Local file path
            destination_path (str): Path in Firebase Storage
        
        Returns:
            str: Public URL of the uploaded file, or None if failed
        """
        self._ensure_initialized()
    
        # Check if storage bucket is available
        if not self.bucket:
            print("Firebase Storage not configured. Using Cloudinary instead.")
            return None
    
        try:
            blob = self.bucket.blob(destination_path)
            blob.upload_from_filename(file_path)
        
            # Make the file publicly accessible
            blob.make_public()
        
            # Return the public URL
            return blob.public_url
        except Exception as e:
            print(f"Error uploading file {file_path} to {destination_path}: {e}")
    
        return None
    
    def download_file(self, storage_path, destination_path):
        """Download a file from Firebase Storage
    
        Args:
            storage_path (str): Path in Firebase Storage
            destination_path (str): Local destination path
        
        Returns:
            bool: True if successful, False otherwise
        """
        self._ensure_initialized()
    
        # Check if storage bucket is available
        if not self.bucket:
            print("Firebase Storage not configured. Using Cloudinary instead.")
            return False
    
        try:
            blob = self.bucket.blob(storage_path)
            blob.download_to_filename(destination_path)
            return True
        except Exception as e:
            print(f"Error downloading file from {storage_path} to {destination_path}: {e}")
    
        return False
    
    def _ensure_initialized(self):
        """Ensure that Firebase is initialized"""
        if not self.initialized:
            self.initialize()
            

