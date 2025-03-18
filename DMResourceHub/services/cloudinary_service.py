import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
from pathlib import Path

class CloudinaryService:
    """Service for interacting with Cloudinary cloud storage"""
    
    def __init__(self):
        """Initialize the Cloudinary service"""
        self.initialized = False
    
    def initialize(self):
        """Initialize Cloudinary connection"""
        if self.initialized:
            return
        
        try:
            # Load environment variables
            load_dotenv()
            
            # Configure Cloudinary
            cloudinary.config(
                cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
                api_key=os.getenv("CLOUDINARY_API_KEY"),
                api_secret=os.getenv("CLOUDINARY_API_SECRET"),
                secure=True
            )
            
            self.initialized = True
            print("Cloudinary service initialized successfully")
            
        except Exception as e:
            print(f"Error initializing Cloudinary service: {e}")
            raise
    
    def _ensure_initialized(self):
        """Ensure that Cloudinary is initialized"""
        if not self.initialized:
            self.initialize()
    
    def upload_file(self, file_path, resource_type="auto", folder="general"):
        """Upload a file to Cloudinary
        
        Args:
            file_path (str): Local file path
            resource_type (str): Type of resource (auto, image, raw, video)
            folder (str): Folder to upload to
            
        Returns:
            dict: Upload result with URLs and metadata, or None if failed
        """
        self._ensure_initialized()
        
        try:
            # Verify file exists
            if not Path(file_path).exists():
                print(f"File not found: {file_path}")
                return None
                
            # Upload file to Cloudinary
            result = cloudinary.uploader.upload(
                file_path,
                resource_type=resource_type,
                folder=folder,
                use_filename=True,
                unique_filename=True,
                overwrite=True
            )
            
            return result
        except Exception as e:
            print(f"Error uploading file {file_path} to Cloudinary: {e}")
        
        return None
    
    def get_resource_url(self, public_id, resource_type="image", transformation=None):
        """Get URL for a Cloudinary resource
        
        Args:
            public_id (str): Public ID of the resource
            resource_type (str): Type of resource
            transformation (dict, optional): Transformation parameters
            
        Returns:
            str: URL of the resource
        """
        self._ensure_initialized()
        
        try:
            # Build URL for resource
            if resource_type == "image":
                # For images, we can apply transformations
                url = cloudinary.CloudinaryImage(public_id).build_url(transformation=transformation)
            else:
                # For other resources, just get the URL
                url = cloudinary.utils.cloudinary_url(public_id)[0]
            
            return url
        except Exception as e:
            print(f"Error getting URL for resource {public_id}: {e}")
        
        return None
    
    def get_thumbnail_url(self, public_id, width=200, height=200):
        """Get a thumbnail URL for an image resource
        
        Args:
            public_id (str): Public ID of the resource
            width (int): Thumbnail width
            height (int): Thumbnail height
            
        Returns:
            str: URL of the thumbnail
        """
        transformation = {
            'width': width,
            'height': height,
            'crop': 'fill'
        }
        
        return self.get_resource_url(public_id, transformation=transformation)
    
    def delete_resource(self, public_id, resource_type="image"):
        """Delete a resource from Cloudinary
        
        Args:
            public_id (str): Public ID of the resource
            resource_type (str): Type of resource
            
        Returns:
            bool: True if successful, False otherwise
        """
        self._ensure_initialized()
        
        try:
            # Delete resource from Cloudinary
            result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
            return result.get('result') == 'ok'
        except Exception as e:
            print(f"Error deleting resource {public_id}: {e}")
        
        return False
    
    def create_folder(self, folder_path):
        """Create a folder in Cloudinary
        
        Args:
            folder_path (str): Path of the folder to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        self._ensure_initialized()
        
        try:
            # Create folder in Cloudinary
            result = cloudinary.api.create_folder(folder_path)
            return True
        except Exception as e:
            # If error is that folder already exists, that's fine
            if "already exists" in str(e).lower():
                return True
            print(f"Error creating folder {folder_path}: {e}")
        
        return False
    
    def list_resources(self, folder=None, resource_type="image", max_results=100):
        """List resources in Cloudinary
        
        Args:
            folder (str, optional): Folder to list resources from
            resource_type (str): Type of resources to list
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of resources
        """
        self._ensure_initialized()
        
        try:
            # Set up parameters
            params = {
                'resource_type': resource_type,
                'max_results': max_results,
                'type': 'upload'
            }
            
            if folder:
                params['prefix'] = folder
            
            # Get resources from Cloudinary
            result = cloudinary.api.resources(**params)
            return result.get('resources', [])
        except Exception as e:
            print(f"Error listing resources: {e}")
        
        return []
