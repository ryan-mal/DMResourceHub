import os
import asyncio
import threading
import discord
from discord import File
from dotenv import load_dotenv
from pathlib import Path

class DiscordService:
    """Service for interacting with Discord API"""
    
    def __init__(self):
        """Initialize the Discord service"""
        self.client = None
        self.token = None
        self.initialized = False
        self.connected = False
        
        # Lock for thread safety
        self._lock = threading.Lock()
        
        # Store the event loop for async operations
        self.loop = None
        self.thread = None
    
    def initialize(self):
        """Initialize Discord connection"""
        if self.initialized:
            return
        
        try:
            # Load environment variables from .env file
            load_dotenv()
            
            # Get Discord token
            self.token = os.getenv("DISCORD_BOT_TOKEN")
            if not self.token:
                raise ValueError("Discord bot token not found. Please set DISCORD_BOT_TOKEN in .env file.")
            
            # Create Discord client with required intents
            intents = discord.Intents.default()
            intents.message_content = True
            self.client = discord.Client(intents=intents)
            
            # Set up client event handlers
            @self.client.event
            async def on_ready():
                print(f"Discord bot connected as {self.client.user}")
                with self._lock:
                    self.connected = True
            
            # Set initialized flag
            self.initialized = True
            print("Discord service initialized")
            
        except Exception as e:
            print(f"Error initializing Discord service: {e}")
            raise
    
    def connect(self):
        """Connect to Discord in a separate thread
        
        Returns:
            bool: True if connection started, False otherwise
        """
        if not self.initialized:
            self.initialize()
        
        if self.connected:
            return True
        
        try:
            # Start the client in a separate thread
            self.thread = threading.Thread(target=self._run_discord_client)
            self.thread.daemon = True
            self.thread.start()
            
            # Give it a moment to connect
            for _ in range(10):
                with self._lock:
                    if self.connected:
                        return True
                # Wait a bit and check again
                threading.Event().wait(0.5)
            
            print("Discord connection timeout")
            return False
            
        except Exception as e:
            print(f"Error connecting to Discord: {e}")
            return False
    
    def _run_discord_client(self):
        """Run the Discord client in a new event loop"""
        try:
            # Create a new event loop for this thread
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            # Run the client
            self.loop.run_until_complete(self.client.start(self.token))
        except Exception as e:
            print(f"Error in Discord client thread: {e}")
        finally:
            # Clean up
            if self.loop:
                self.loop.close()
    
    def disconnect(self):
        """Disconnect from Discord
        
        Returns:
            bool: True if disconnected, False otherwise
        """
        if not self.connected:
            return True
        
        try:
            # Schedule the client to close
            if self.loop:
                asyncio.run_coroutine_threadsafe(self.client.close(), self.loop)
            
            # Wait for the thread to finish
            if self.thread:
                self.thread.join(timeout=5.0)
            
            with self._lock:
                self.connected = False
            
            return True
            
        except Exception as e:
            print(f"Error disconnecting from Discord: {e}")
            return False
    
    def get_channels(self):
        """Get a list of available text channels
        
        Returns:
            list: List of (channel_id, channel_name) tuples
        """
        if not self.connected:
            print("Not connected to Discord")
            return []
        
        channels = []
        
        try:
            # Create a future to hold the result
            future = asyncio.run_coroutine_threadsafe(self._get_channels_async(), self.loop)
            # Wait for the result with a timeout
            channels = future.result(timeout=5.0)
            
        except Exception as e:
            print(f"Error getting Discord channels: {e}")
        
        return channels
    
    async def _get_channels_async(self):
        """Async method to get channels"""
        channels = []
        for guild in self.client.guilds:
            for channel in guild.text_channels:
                channels.append((str(channel.id), f"#{channel.name} ({guild.name})"))
        return channels
    
    def send_message(self, channel_id, content, file_path=None):
        """Send a message to a Discord channel
        
        Args:
            channel_id (str): Discord channel ID
            content (str): Message content
            file_path (str, optional): Path to file to attach. Defaults to None.
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected:
            print("Not connected to Discord")
            return False
        
        try:
            # Create a future to hold the result
            future = asyncio.run_coroutine_threadsafe(
                self._send_message_async(channel_id, content, file_path), 
                self.loop
            )
            # Wait for the result with a timeout
            return future.result(timeout=10.0)
            
        except Exception as e:
            print(f"Error sending Discord message: {e}")
            return False
    
    async def _send_message_async(self, channel_id, content, file_path=None):
        """Async method to send a message"""
        try:
            # Get the channel
            channel = self.client.get_channel(int(channel_id))
            if not channel:
                print(f"Channel {channel_id} not found")
                return False
            
            # Send message with or without file
            if file_path and Path(file_path).exists():
                await channel.send(content=content, file=File(file_path))
            else:
                await channel.send(content=content)
            
            return True
            
        except Exception as e:
            print(f"Error in _send_message_async: {e}")
            return False
    
    def send_direct_message(self, user_id, content, file_path=None):
        """Send a direct message to a Discord user
        
        Args:
            user_id (str): Discord user ID
            content (str): Message content
            file_path (str, optional): Path to file to attach. Defaults to None.
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected:
            print("Not connected to Discord")
            return False
        
        try:
            # Create a future to hold the result
            future = asyncio.run_coroutine_threadsafe(
                self._send_dm_async(user_id, content, file_path), 
                self.loop
            )
            # Wait for the result with a timeout
            return future.result(timeout=10.0)
            
        except Exception as e:
            print(f"Error sending Discord DM: {e}")
            return False
    
    async def _send_dm_async(self, user_id, content, file_path=None):
        """Async method to send a direct message"""
        try:
            # Get the user
            user = await self.client.fetch_user(int(user_id))
            if not user:
                print(f"User {user_id} not found")
                return False
            
            # Send message with or without file
            if file_path and Path(file_path).exists():
                await user.send(content=content, file=File(file_path))
            else:
                await user.send(content=content)
            
            return True
            
        except Exception as e:
            print(f"Error in _send_dm_async: {e}")
            return False
