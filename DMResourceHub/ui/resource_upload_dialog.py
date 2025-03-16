import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import datetime

from models.resource import Resource

class ResourceUploadDialog:
    """Dialog for uploading a new resource"""
    
    def __init__(self, parent, firebase_service, campaigns=None):
        """Initialize the upload dialog
        
        Args:
            parent: Parent window
            firebase_service: FirebaseService instance
            campaigns (list, optional): List of Campaign objects. Defaults to None.
        """
        self.parent = parent
        self.firebase_service = firebase_service
        self.campaigns = campaigns or []
        
        # Resource data
        self.resource = Resource()
        self.file_path = None
        self.thumbnail = None
        
        # Create the dialog window
        self.window = tk.Toplevel(parent)
        self.window.title("Upload New Resource")
        self.window.geometry("600x700")
        self.window.minsize(500, 600)
        self.window.grab_set()  # Make the dialog modal
        
        # Center the window
        self.center_window()
        
        # Create the form
        self.create_form()
    
    def center_window(self):
        """Center the dialog window on the parent window"""
        self.window.update_idletasks()
        
        # Get parent window dimensions and position
        parent_x = self.parent.winfo_rootx()
