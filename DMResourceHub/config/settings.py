import os
import json
from pathlib import Path
from dotenv import load_dotenv

class Settings:
    """Class for managing application settings"""
    
    def __init__(self):
        """Initialize settings with default values"""
        # Load environment variables
        load_dotenv()
        
        # Default settings
        self.settings = {
            "app": {
                "name": "DM Resource Hub",
                "version": "0.1.0",
                "theme": "default",
                "window_size": (1200, 800),
                "show_thumbnails": True,
                "default_view": "grid"  # "grid" or "list"
            },
            "firebase": {
                "credentials_path": os.getenv("FIREBASE_CREDENTIALS_PATH", ""),
                "storage_bucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
                "offline_mode": False
            },
            "discord": {
                "bot_token": os.getenv("DISCORD_BOT_TOKEN", ""),
                "default_channel": "",
                "auto_connect": False
            },
            "resources": {
                "local_storage_path": os.getenv("LOCAL_STORAGE_PATH", "data/resources"),
                "max_thumbnail_size": (200, 200),
                "recent_resources_count": 10
            },
            "user": {
                "email": "",
                "display_name": "",
                "last_campaign": ""
            }
        }
        
        # Try to load settings from file
        self.settings_file = Path("config/settings.json")
        self.load()
    
    def get(self, section, key=None):
        """Get a setting value
        
        Args:
            section (str): Settings section (app, firebase, discord, etc.)
            key (str, optional): Setting key. If None, returns the entire section.
            
        Returns:
            The setting value, or None if not found
        """
        if section not in self.settings:
            return None
        
        if key is None:
            return self.settings[section]
        
        return self.settings[section].get(key)
    
    def set(self, section, key, value):
        """Set a setting value
        
        Args:
            section (str): Settings section
            key (str): Setting key
            value: Setting value
            
        Returns:
            bool: True if successful, False otherwise
        """
        if section not in self.settings:
            self.settings[section] = {}
        
        self.settings[section][key] = value
        return self.save()
    
    def update_section(self, section, values):
        """Update multiple settings in a section
        
        Args:
            section (str): Settings section
            values (dict): Dictionary of key-value pairs
            
        Returns:
            bool: True if successful, False otherwise
        """
        if section not in self.settings:
            self.settings[section] = {}
        
        self.settings[section].update(values)
        return self.save()
    
    def load(self):
        """Load settings from file
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.settings_file.exists():
            # Create settings directory if it doesn't exist
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            return False
        
        try:
            with open(self.settings_file, "r") as f:
                loaded_settings = json.load(f)
                
                # Update settings with loaded values (keeping defaults for missing values)
                for section, values in loaded_settings.items():
                    if section in self.settings:
                        self.settings[section].update(values)
                    else:
                        self.settings[section] = values
                
                return True
                
        except Exception as e:
            print(f"Error loading settings: {e}")
            return False
    
    def save(self):
        """Save settings to file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create settings directory if it doesn't exist
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=4)
                
            return True
                
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def reset_section(self, section):
        """Reset a section to default values
        
        Args:
            section (str): Settings section
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if section exists in defaults
        default_settings = Settings()
        if section not in default_settings.settings:
            return False
        
        # Reset section to defaults
        self.settings[section] = default_settings.settings[section].copy()
        return self.save()
    
    def reset_all(self):
        """Reset all settings to default values
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Create a new settings object with defaults
        default_settings = Settings()
        
        # Copy defaults
        self.settings = default_settings.settings.copy()
        
        return self.save()
