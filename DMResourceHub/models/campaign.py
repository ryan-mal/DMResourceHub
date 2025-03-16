class Campaign:
    """Class representing a campaign in the DM Resource Hub"""
    
    def __init__(self, id=None, name="", description="", created_by="", 
                 created_at=None, updated_at=None, cover_image="", tags=None):
        """Initialize a campaign object
        
        Args:
            id (str, optional): Campaign ID. Defaults to None.
            name (str, optional): Campaign name. Defaults to "".
            description (str, optional): Campaign description. Defaults to "".
            created_by (str, optional): User ID who created the campaign. Defaults to "".
            created_at (datetime, optional): Creation timestamp. Defaults to None.
            updated_at (datetime, optional): Last update timestamp. Defaults to None.
            cover_image (str, optional): Path to cover image. Defaults to "".
            tags (list, optional): List of tags. Defaults to empty list.
        """
        self.id = id
        self.name = name
        self.description = description
        self.created_by = created_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.cover_image = cover_image
        self.tags = tags or []
    
    def to_dict(self):
        """Convert campaign object to dictionary for Firebase storage"""
        return {
            "name": self.name,
            "description": self.description,
            "createdBy": self.created_by,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "coverImage": self.cover_image,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, id, data):
        """Create a campaign object from a dictionary
        
        Args:
            id (str): Campaign ID
            data (dict): Campaign data from Firebase
            
        Returns:
            Campaign: A new Campaign object
        """
        return cls(
            id=id,
            name=data.get("name", ""),
            description=data.get("description", ""),
            created_by=data.get("createdBy", ""),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
            cover_image=data.get("coverImage", ""),
            tags=data.get("tags", [])
        )
