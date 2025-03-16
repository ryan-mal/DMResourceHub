class Resource:
    """Class representing a resource in the DM Resource Hub"""
    
    RESOURCE_TYPES = ["image", "pdf", "link", "text"]
    
    def __init__(self, id=None, title="", description="", resource_type="", tags=None, 
                 folder="", campaigns=None, uploaded_by="", uploaded_at=None):
        """Initialize a resource object
        
        Args:
            id (str, optional): Resource ID. Defaults to None.
            title (str, optional): Resource title. Defaults to "".
            description (str, optional): Resource description. Defaults to "".
            resource_type (str, optional): Type of resource (image, pdf, link, text). Defaults to "".
            tags (list, optional): List of tags. Defaults to empty list.
            folder (str, optional): Folder path. Defaults to "".
            campaigns (list, optional): List of campaign IDs. Defaults to empty list.
            uploaded_by (str, optional): User ID who uploaded the resource. Defaults to "".
            uploaded_at (datetime, optional): Upload timestamp. Defaults to None.
        """
        self.id = id
        self.title = title
        self.description = description
        self.resource_type = resource_type if resource_type in self.RESOURCE_TYPES else ""
        self.tags = tags or []
        self.folder = folder
        self.campaigns = campaigns or []
        self.uploaded_by = uploaded_by
        self.uploaded_at = uploaded_at
        
        # Initialize sharing status
        self.sharing_status = {
            "has_been_shared": False,
            "last_shared": None,
            "shared_with": [],
            "times_shared": 0
        }
        
        # Type-specific data
        self.file_data = {}  # For images and PDFs
        self.link_data = {}  # For links
        self.text_data = {}  # For text notes
    
    def to_dict(self):
        """Convert resource object to dictionary for Firebase storage"""
        resource_dict = {
            "title": self.title,
            "description": self.description,
            "type": self.resource_type,
            "tags": self.tags,
            "folder": self.folder,
            "campaigns": self.campaigns,
            "uploadedBy": self.uploaded_by,
            "uploadedAt": self.uploaded_at,
            "sharingStatus": self.sharing_status
        }
        
        # Add type-specific data
        if self.resource_type in ["image", "pdf"]:
            resource_dict["fileData"] = self.file_data
        elif self.resource_type == "link":
            resource_dict["linkData"] = self.link_data
        elif self.resource_type == "text":
            resource_dict["textData"] = self.text_data
            
        return resource_dict
    
    @classmethod
    def from_dict(cls, id, data):
        """Create a resource object from a dictionary
        
        Args:
            id (str): Resource ID
            data (dict): Resource data from Firebase
            
        Returns:
            Resource: A new Resource object
        """
        resource = cls(
            id=id,
            title=data.get("title", ""),
            description=data.get("description", ""),
            resource_type=data.get("type", ""),
            tags=data.get("tags", []),
            folder=data.get("folder", ""),
            campaigns=data.get("campaigns", []),
            uploaded_by=data.get("uploadedBy", ""),
            uploaded_at=data.get("uploadedAt")
        )
        
        # Set sharing status
        if "sharingStatus" in data:
            resource.sharing_status = data["sharingStatus"]
            
        # Set type-specific data
        if "fileData" in data:
            resource.file_data = data["fileData"]
        if "linkData" in data:
            resource.link_data = data["linkData"]
        if "textData" in data:
            resource.text_data = data["textData"]
            
        return resource
