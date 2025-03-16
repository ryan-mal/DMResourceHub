class Player:
    """Class representing a player in the DM Resource Hub"""
    
    def __init__(self, id=None, name="", discord_id="", discord_username="", 
                 campaigns=None, added_by="", added_at=None, notes=""):
        """Initialize a player object
        
        Args:
            id (str, optional): Player ID. Defaults to None.
            name (str, optional): Player name. Defaults to "".
            discord_id (str, optional): Discord ID. Defaults to "".
            discord_username (str, optional): Discord username. Defaults to "".
            campaigns (list, optional): List of campaign IDs. Defaults to empty list.
            added_by (str, optional): User ID who added the player. Defaults to "".
            added_at (datetime, optional): Addition timestamp. Defaults to None.
            notes (str, optional): Notes about the player. Defaults to "".
        """
        self.id = id
        self.name = name
        self.discord_id = discord_id
        self.discord_username = discord_username
        self.campaigns = campaigns or []
        self.added_by = added_by
        self.added_at = added_at
        self.notes = notes
    
    def to_dict(self):
        """Convert player object to dictionary for Firebase storage"""
        return {
            "name": self.name,
            "discordId": self.discord_id,
            "discordUsername": self.discord_username,
            "campaigns": self.campaigns,
            "addedBy": self.added_by,
            "addedAt": self.added_at,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, id, data):
        """Create a player object from a dictionary
        
        Args:
            id (str): Player ID
            data (dict): Player data from Firebase
            
        Returns:
            Player: A new Player object
        """
        return cls(
            id=id,
            name=data.get("name", ""),
            discord_id=data.get("discordId", ""),
            discord_username=data.get("discordUsername", ""),
            campaigns=data.get("campaigns", []),
            added_by=data.get("addedBy", ""),
            added_at=data.get("addedAt"),
            notes=data.get("notes", "")
        )
