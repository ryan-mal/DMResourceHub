import tkinter as tk
from tkinter import ttk
import os
import sys

class DMResourceHub:
    def __init__(self, root):
        self.root = root
        self.root.title("DM Resource Hub")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set application icon (once we have one)
        # self.root.iconbitmap("assets/icon.ico")
        
        # Configure the grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure the main frame's grid
        self.main_frame.columnconfigure(0, weight=1)  # Left sidebar
        self.main_frame.columnconfigure(1, weight=3)  # Center panel
        self.main_frame.columnconfigure(2, weight=1)  # Right sidebar
        self.main_frame.rowconfigure(0, weight=1)
        
        # Create three main sections
        self.create_left_sidebar()
        self.create_center_panel()
        self.create_right_sidebar()
        
        # Create status bar
        self.create_status_bar()
        
    def create_left_sidebar(self):
        """Create the left sidebar with resource categories and filters"""
        sidebar = ttk.Frame(self.main_frame, relief="ridge", padding=5)
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Header
        ttk.Label(sidebar, text="Resources", font=("Arial", 12, "bold")).pack(fill="x", pady=5)
        
        # Placeholder for folder tree
        ttk.Label(sidebar, text="Folders will go here").pack(fill="x", pady=10)
        
        # Placeholder for filters
        ttk.Label(sidebar, text="Filters will go here").pack(fill="x", pady=10)
        
    def create_center_panel(self):
        """Create the center panel with resource list/grid"""
        center = ttk.Frame(self.main_frame, relief="ridge", padding=5)
        center.grid(row=0, column=1, sticky="nsew")
        
        # Search bar at the top
        search_frame = ttk.Frame(center)
        search_frame.pack(fill="x", pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Search").pack(side="left", padx=5)
        
        # Placeholder for resource display
        ttk.Label(center, text="Resources will be displayed here").pack(expand=True)
        
    def create_right_sidebar(self):
        """Create the right sidebar with player selection and sharing options"""
        sidebar = ttk.Frame(self.main_frame, relief="ridge", padding=5)
        sidebar.grid(row=0, column=2, sticky="nsew")
        
        # Header
        ttk.Label(sidebar, text="Sharing", font=("Arial", 12, "bold")).pack(fill="x", pady=5)
        
        # Placeholder for player selection
        ttk.Label(sidebar, text="Player selection will go here").pack(fill="x", pady=10)
        
        # Placeholder for Discord channels
        ttk.Label(sidebar, text="Discord channels will go here").pack(fill="x", pady=10)
        
        # Share button
        ttk.Button(sidebar, text="Share Selected").pack(fill="x", pady=10)
        
    def create_status_bar(self):
        """Create a status bar at the bottom of the window"""
        status_bar = ttk.Frame(self.root, relief="sunken")
        status_bar.grid(row=1, column=0, sticky="ew")
        
        status_label = ttk.Label(status_bar, text="Ready")
        status_label.pack(side="left", padx=5)
        
        # Show a version number
        version_label = ttk.Label(status_bar, text="v0.1")
        version_label.pack(side="right", padx=5)

def main():
    root = tk.Tk()
    app = DMResourceHub(root)
    root.mainloop()

if __name__ == "__main__":
    main()
