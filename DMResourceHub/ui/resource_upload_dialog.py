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
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate position
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        # Set position
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def create_form(self):
        """Create the upload form interface"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title and description at the top
        ttk.Label(main_frame, text="Upload New Resource", font=("Arial", 14, "bold")).pack(fill="x", pady=(0, 10))
        ttk.Label(main_frame, text="Add a new resource to your GM Resource Hub").pack(fill="x", pady=(0, 20))
        
        # Left side - form fields
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Resource type selection
        ttk.Label(form_frame, text="Resource Type:").pack(anchor="w", pady=(0, 5))
        
        type_frame = ttk.Frame(form_frame)
        type_frame.pack(fill="x", pady=(0, 10))
        
        resource_type = tk.StringVar(value="image")
        
        ttk.Radiobutton(type_frame, text="Image", variable=resource_type, value="image", 
                        command=lambda: self.update_resource_type("image")).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(type_frame, text="PDF", variable=resource_type, value="pdf",
                        command=lambda: self.update_resource_type("pdf")).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(type_frame, text="Link", variable=resource_type, value="link",
                        command=lambda: self.update_resource_type("link")).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(type_frame, text="Text", variable=resource_type, value="text",
                        command=lambda: self.update_resource_type("text")).pack(side="left")
        
        # Title and description
        ttk.Label(form_frame, text="Title:").pack(anchor="w", pady=(0, 5))
        self.title_entry = ttk.Entry(form_frame)
        self.title_entry.pack(fill="x", pady=(0, 10))
        
        ttk.Label(form_frame, text="Description:").pack(anchor="w", pady=(0, 5))
        self.description_entry = tk.Text(form_frame, height=4)
        self.description_entry.pack(fill="x", pady=(0, 10))
        
        # Tags
        ttk.Label(form_frame, text="Tags (comma separated):").pack(anchor="w", pady=(0, 5))
        self.tags_entry = ttk.Entry(form_frame)
        self.tags_entry.pack(fill="x", pady=(0, 10))
        
        # Folder
        ttk.Label(form_frame, text="Folder:").pack(anchor="w", pady=(0, 5))
        self.folder_entry = ttk.Entry(form_frame)
        self.folder_entry.pack(fill="x", pady=(0, 10))
        
        # Campaign selection
        ttk.Label(form_frame, text="Campaign:").pack(anchor="w", pady=(0, 5))
        self.campaign_combo = ttk.Combobox(form_frame)
        
        # Populate campaigns if available
        if self.campaigns:
            self.campaign_combo['values'] = [campaign.name for campaign in self.campaigns]
            self.campaign_combo.current(0)
        
        self.campaign_combo.pack(fill="x", pady=(0, 10))
        
        # Right side - file selection and preview
        preview_frame = ttk.LabelFrame(main_frame, text="Resource Preview")
        preview_frame.pack(side="right", fill="both", expand=True)
        
        # File selection for image/PDF
        self.file_frame = ttk.Frame(preview_frame)
        self.file_frame.pack(fill="x", pady=10, padx=10)
        
        self.file_label = ttk.Label(self.file_frame, text="No file selected")
        self.file_label.pack(side="left", fill="x", expand=True)
        
        ttk.Button(self.file_frame, text="Browse...", command=self.browse_file).pack(side="right")
        
        # URL field for links
        self.link_frame = ttk.Frame(preview_frame)
        self.url_entry = ttk.Entry(self.link_frame)
        self.url_entry.pack(fill="x", expand=True, pady=10, padx=10)
        ttk.Label(self.link_frame, text="Enter URL for link resource").pack(pady=(0, 10))
        
        # Text content field for text resources
        self.text_frame = ttk.Frame(preview_frame)
        self.text_content = tk.Text(self.text_frame, height=10)
        self.text_content.pack(fill="both", expand=True, pady=10, padx=10)
        ttk.Label(self.text_frame, text="Enter text content").pack(pady=(0, 10))
        
        # Preview area
        self.preview_area = ttk.Label(preview_frame, text="Preview will appear here")
        self.preview_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bottom buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Cancel", command=self.window.destroy).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Upload", command=self.upload_resource).pack(side="right")
        
        # Initialize UI based on default resource type
        self.update_resource_type("image")

    def update_resource_type(self, resource_type):
        """Update UI based on selected resource type"""
        self.resource.resource_type = resource_type
        
        # Hide all type-specific frames
        self.file_frame.pack_forget()
        self.link_frame.pack_forget()
        self.text_frame.pack_forget()
        
        # Show appropriate frame based on resource type
        if resource_type in ["image", "pdf"]:
            self.file_frame.pack(fill="x", pady=10, padx=10)
        elif resource_type == "link":
            self.link_frame.pack(fill="x", pady=10, padx=10)
        elif resource_type == "text":
            self.text_frame.pack(fill="both", expand=True, pady=10, padx=10)

    def browse_file(self):
        """Open file browser to select a file"""
        filetypes = []
        
        if self.resource.resource_type == "image":
            filetypes = [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        elif self.resource.resource_type == "pdf":
            filetypes = [("PDF files", "*.pdf")]
        
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            
            # Update preview if it's an image
            if self.resource.resource_type == "image":
                self.update_preview(file_path)

    def update_preview(self, file_path):
        """Update the preview area with an image"""
        try:
            # Open and resize image for preview
            img = Image.open(file_path)
            img.thumbnail((300, 300))  # Resize for preview
            
            # Convert to PhotoImage for Tkinter
            photo = ImageTk.PhotoImage(img)
            
            # Update preview label
            self.preview_area.config(image=photo)
            self.preview_area.image = photo  # Keep a reference
        except Exception as e:
            print(f"Error updating preview: {e}")
            self.preview_area.config(image=None, text="Error loading preview")

    def upload_resource(self):
        """Upload the resource to Cloudinary and save metadata to Firebase"""
        # Validate input
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Please enter a title for the resource")
            return
        
        # Get description
        description = self.description_entry.get("1.0", "end-1c").strip()
        
        # Get tags (split by comma and strip whitespace)
        tags = [tag.strip() for tag in self.tags_entry.get().split(",") if tag.strip()]
        
        # Get folder
        folder = self.folder_entry.get().strip()
        
        # Get campaign (if selected)
        campaign_index = self.campaign_combo.current()
        campaigns = []
        if campaign_index >= 0 and campaign_index < len(self.campaigns):
            campaigns = [self.campaigns[campaign_index].id]
        
        # Update resource object
        self.resource.title = title
        self.resource.description = description
        self.resource.tags = tags
        self.resource.folder = folder
        self.resource.campaigns = campaigns
        
        # Handle resource type-specific data
        try:
            if self.resource.resource_type == "image" or self.resource.resource_type == "pdf":
                if not self.file_path:
                    messagebox.showerror("Error", "Please select a file")
                    return
                
                # Upload to Cloudinary
                # Create cloudinary service instance
                from services.cloudinary_service import CloudinaryService
                cloudinary_service = CloudinaryService()
                
                # Determine folder in Cloudinary
                cloudinary_folder = "general"
                if campaigns and campaigns[0]:
                    cloudinary_folder = f"campaign_{campaigns[0]}"
                
                # Determine resource type for Cloudinary
                cloudinary_resource_type = "image" if self.resource.resource_type == "image" else "raw"
                
                # Show uploading progress
                self.window.config(cursor="wait")
                progress_window = tk.Toplevel(self.window)
                progress_window.title("Uploading")
                progress_window.geometry("300x100")
                ttk.Label(progress_window, text="Uploading resource...").pack(pady=20)
                progress_window.update()
                
                # Upload to Cloudinary
                result = cloudinary_service.upload_file(
                    self.file_path,
                    resource_type=cloudinary_resource_type,
                    folder=cloudinary_folder
                )
                
                progress_window.destroy()
                self.window.config(cursor="")
                
                if not result:
                    messagebox.showerror("Error", "Failed to upload file to Cloudinary")
                    return
                
                # Store Cloudinary data in resource
                self.resource.cloudinary_data = {
                    "public_id": result["public_id"],
                    "url": result["url"],
                    "secure_url": result["secure_url"],
                    "resource_type": result["resource_type"],
                    "format": result.get("format", ""),
                    "version": result.get("version", "")
                }
                
                # Store file info
                self.resource.file_data = {
                    "filename": os.path.basename(self.file_path),
                    "size": os.path.getsize(self.file_path),
                    "mime_type": result.get("mime_type", "")
                }
                
            elif self.resource.resource_type == "link":
                url = self.url_entry.get().strip()
                if not url:
                    messagebox.showerror("Error", "Please enter a URL")
                    return
                
                self.resource.link_data = {
                    "url": url,
                    "title": title,
                    "description": description
                }
                
            elif self.resource.resource_type == "text":
                content = self.text_content.get("1.0", "end-1c").strip()
                if not content:
                    messagebox.showerror("Error", "Please enter text content")
                    return
                
                self.resource.text_data = {
                    "content": content
                }
            
            # Add resource to Firebase
            resource_id = self.firebase_service.add_resource(self.resource)
            
            if resource_id:
                messagebox.showinfo("Success", "Resource uploaded successfully")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save resource metadata to Firebase")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(f"Error uploading resource: {e}")