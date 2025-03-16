import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class MainWindow:
    def __init__(self, root):
        """Initialize the main application window"""
        self.root = root
        self.root.title("DM Resource Hub")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set up the menu
        self.create_menu()
        
        # Set up the main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure the main frame's grid
        self.main_frame.columnconfigure(0, weight=1)  # Left sidebar
        self.main_frame.columnconfigure(1, weight=3)  # Center panel
        self.main_frame.columnconfigure(2, weight=1)  # Right sidebar
        self.main_frame.rowconfigure(0, weight=1)
        
        # Create the UI sections
        self.create_left_sidebar()
        self.create_center_panel()
        self.create_right_sidebar()
        self.create_status_bar()
    
    def create_menu(self):
        """Create the main menu bar"""
        menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Resource", command=self.new_resource)
        file_menu.add_command(label="Import Resources", command=self.import_resources)
        file_menu.add_separator()
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Campaign menu
        campaign_menu = tk.Menu(menu_bar, tearoff=0)
        campaign_menu.add_command(label="New Campaign", command=self.new_campaign)
        campaign_menu.add_command(label="Manage Campaigns", command=self.manage_campaigns)
        menu_bar.add_cascade(label="Campaigns", menu=campaign_menu)
        
        # Players menu
        players_menu = tk.Menu(menu_bar, tearoff=0)
        players_menu.add_command(label="Add Player", command=self.add_player)
        players_menu.add_command(label="Manage Players", command=self.manage_players)
        players_menu.add_command(label="Create Group", command=self.create_group)
        menu_bar.add_cascade(label="Players", menu=players_menu)
        
        # Discord menu
        discord_menu = tk.Menu(menu_bar, tearoff=0)
        discord_menu.add_command(label="Connect to Discord", command=self.connect_discord)
        discord_menu.add_command(label="Bot Settings", command=self.bot_settings)
        menu_bar.add_cascade(label="Discord", menu=discord_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menu_bar)
    
    def create_left_sidebar(self):
        """Create the left sidebar with resource categories and filters"""
        sidebar = ttk.LabelFrame(self.main_frame, text="Resources")
        sidebar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create a frame for buttons at the top
        button_frame = ttk.Frame(sidebar)
        button_frame.pack(fill="x", pady=5)
        
        ttk.Button(button_frame, text="New", command=self.new_resource).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Import", command=self.import_resources).pack(side="left", padx=2)
        
        # Create a notebook for tabs
        notebook = ttk.Notebook(sidebar)
        notebook.pack(fill="both", expand=True, pady=5)
        
        # Folders tab
        folders_frame = ttk.Frame(notebook)
        notebook.add(folders_frame, text="Folders")
        
        # Will be replaced with actual treeview
        ttk.Label(folders_frame, text="Folder tree will go here").pack(pady=20)
        
        # Tags tab
        tags_frame = ttk.Frame(notebook)
        notebook.add(tags_frame, text="Tags")
        
        ttk.Label(tags_frame, text="Tags will go here").pack(pady=20)
        
        # Filters tab
        filters_frame = ttk.Frame(notebook)
        notebook.add(filters_frame, text="Filters")
        
        ttk.Label(filters_frame, text="Type:").pack(anchor="w", padx=5, pady=2)
        ttk.Checkbutton(filters_frame, text="Images").pack(anchor="w", padx=20, pady=2)
        ttk.Checkbutton(filters_frame, text="PDFs").pack(anchor="w", padx=20, pady=2)
        ttk.Checkbutton(filters_frame, text="Links").pack(anchor="w", padx=20, pady=2)
        ttk.Checkbutton(filters_frame, text="Text").pack(anchor="w", padx=20, pady=2)
        
        ttk.Label(filters_frame, text="Status:").pack(anchor="w", padx=5, pady=2)
        ttk.Checkbutton(filters_frame, text="Shared").pack(anchor="w", padx=20, pady=2)
        ttk.Checkbutton(filters_frame, text="Not shared").pack(anchor="w", padx=20, pady=2)
    
    def create_center_panel(self):
        """Create the center panel with resource list/grid"""
        center = ttk.LabelFrame(self.main_frame, text="Resource Browser")
        center.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Search bar at the top
        search_frame = ttk.Frame(center)
        search_frame.pack(fill="x", pady=5, padx=5)
        
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Search").pack(side="left", padx=5)
        
        # View options
        view_frame = ttk.Frame(center)
        view_frame.pack(fill="x", pady=5, padx=5)
        
        ttk.Label(view_frame, text="View:").pack(side="left", padx=5)
        ttk.Button(view_frame, text="Grid").pack(side="left", padx=2)
        ttk.Button(view_frame, text="List").pack(side="left", padx=2)
        
        # Resource display area - will be replaced with actual resource display
        display_frame = ttk.Frame(center)
        display_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Placeholder grid of example resources
        for i in range(3):
            for j in range(4):
                item_frame = ttk.Frame(display_frame, relief="solid", borderwidth=1)
                item_frame.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                
                ttk.Label(item_frame, text=f"Resource {i*4+j+1}").pack(pady=30, padx=30)
        
        # Configure grid weights for display_frame
        for i in range(3):
            display_frame.rowconfigure(i, weight=1)
        for j in range(4):
            display_frame.columnconfigure(j, weight=1)
    
    def create_right_sidebar(self):
        """Create the right sidebar with player selection and sharing options"""
        sidebar = ttk.LabelFrame(self.main_frame, text="Sharing")
        sidebar.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Resource preview area
        preview_frame = ttk.LabelFrame(sidebar, text="Preview")
        preview_frame.pack(fill="x", pady=5, padx=5)
        
        ttk.Label(preview_frame, text="Resource preview will appear here").pack(pady=50, padx=5)
        
        # Player selection area
        players_frame = ttk.LabelFrame(sidebar, text="Share with")
        players_frame.pack(fill="x", pady=5, padx=5)
        
        ttk.Checkbutton(players_frame, text="All Players").pack(anchor="w", padx=5, pady=2)
        ttk.Separator(players_frame, orient="horizontal").pack(fill="x", pady=5)
        
        # Example players
        ttk.Checkbutton(players_frame, text="Player 1").pack(anchor="w", padx=5, pady=2)
        ttk.Checkbutton(players_frame, text="Player 2").pack(anchor="w", padx=5, pady=2)
        ttk.Checkbutton(players_frame, text="Player 3").pack(anchor="w", padx=5, pady=2)
        
        # Discord channel selection
        discord_frame = ttk.LabelFrame(sidebar, text="Discord Channel")
        discord_frame.pack(fill="x", pady=5, padx=5)
        
        channel_combobox = ttk.Combobox(discord_frame, values=["#general", "#resources", "#player-handouts"])
        channel_combobox.pack(fill="x", padx=5, pady=5)
        channel_combobox.current(0)
        
        # Message field
        message_frame = ttk.LabelFrame(sidebar, text="Message (Optional)")
        message_frame.pack(fill="x", pady=5, padx=5)
        
        message_entry = tk.Text(message_frame, height=4)
        message_entry.pack(fill="x", padx=5, pady=5)
        
        # Share button
        ttk.Button(sidebar, text="Share Selected", command=self.share_selected).pack(fill="x", pady=10, padx=5)
    
    def create_status_bar(self):
        """Create a status bar at the bottom of the window"""
        status_frame = ttk.Frame(self.root, relief="sunken", borderwidth=1)
        status_frame.pack(side="bottom", fill="x")
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side="left", padx=5)
        
        version_label = ttk.Label(status_frame, text="v0.1")
        version_label.pack(side="right", padx=5)
    
    # Placeholder method implementations
    def new_resource(self):
        messagebox.showinfo("Info", "New Resource feature not implemented yet")
    
    def import_resources(self):
        messagebox.showinfo("Info", "Import Resources feature not implemented yet")
    
    def open_settings(self):
        messagebox.showinfo("Info", "Settings feature not implemented yet")
    
    def new_campaign(self):
        messagebox.showinfo("Info", "New Campaign feature not implemented yet")
    
    def manage_campaigns(self):
        messagebox.showinfo("Info", "Manage Campaigns feature not implemented yet")
    
    def add_player(self):
        messagebox.showinfo("Info", "Add Player feature not implemented yet")
    
    def manage_players(self):
        messagebox.showinfo("Info", "Manage Players feature not implemented yet")
    
    def create_group(self):
        messagebox.showinfo("Info", "Create Group feature not implemented yet")
    
    def connect_discord(self):
        messagebox.showinfo("Info", "Connect to Discord feature not implemented yet")
    
    def bot_settings(self):
        messagebox.showinfo("Info", "Bot Settings feature not implemented yet")
    
    def show_user_guide(self):
        messagebox.showinfo("User Guide", "User guide will be implemented in a future version")
    
    def show_about(self):
        messagebox.showinfo("About", "DM Resource Hub v0.1\nA tool for Dungeon Masters to organize and share resources")
    
    def share_selected(self):
        messagebox.showinfo("Info", "Share Selected feature not implemented yet")
