"""
OSC Sender for JUCE Plugin Communication

This module provides a Python interface for sending OSC messages to the
StyleTransfer JUCE plugin, enabling remote control of style parameters.

Real-time safety: This module runs in the non-real-time thread and can safely
use blocking calls, memory allocation, and network operations.
"""

import logging
from typing import Optional, Union
from pythonosc import osc_message_builder, udp_client


class OSCSender:
    """
    OSC Sender for communicating with the StyleTransfer JUCE plugin.
    
    This class provides a thread-safe interface for sending OSC messages
    to control plugin parameters remotely. All operations are non-blocking
    and safe for use in the control plane.
    
    Thread Safety: This class is designed for use in the non-real-time thread
    and can safely use blocking calls and memory allocation.
    """
    
    def __init__(self, ip_address: str = '127.0.0.1', port: int = 3819):
        """
        Initialize the OSC sender.
        
        Args:
            ip_address: IP address of the JUCE plugin (default: localhost)
            port: OSC port number (default: 3819, matches JUCE plugin default)
        """
        self.ip_address = ip_address
        self.port = port
        self.client = None
        self.connected = False
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize OSC client
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """
        Initialize the OSC UDP client.
        
        This method creates the OSC client connection. It's safe to call
        multiple times and will reconnect if needed.
        """
        try:
            self.client = udp_client.SimpleUDPClient(self.ip_address, self.port)
            self.connected = True
            self.logger.info(f"OSC client initialized: {self.ip_address}:{self.port}")
        except Exception as e:
            self.logger.error(f"Failed to initialize OSC client: {e}")
            self.connected = False
            raise
    
    def _ensure_connected(self) -> None:
        """
        Ensure the OSC client is connected.
        
        Attempts to reconnect if the connection is lost.
        """
        if not self.connected or self.client is None:
            self.logger.warning("OSC client not connected, attempting to reconnect...")
            self._initialize_client()
    
    def send_message(self, address: str, value: Union[float, int, bool]) -> bool:
        """
        Send an OSC message to the plugin.
        
        Args:
            address: OSC address pattern (e.g., '/style/swing')
            value: Parameter value to send
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        try:
            self._ensure_connected()
            
            # Send the OSC message
            self.client.send_message(address, value)
            self.logger.debug(f"Sent OSC message: {address} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send OSC message {address}={value}: {e}")
            self.connected = False
            return False
    
    # ============================================================================
    # STYLE PARAMETER CONTROL METHODS
    # ============================================================================
    
    def set_swing_ratio(self, ratio: float) -> bool:
        """
        Set the swing ratio parameter.
        
        Args:
            ratio: Swing ratio (0.0 = straight, 1.0 = maximum swing)
            
        Returns:
            True if successful, False otherwise
        """
        # Clamp to valid range
        ratio = max(0.0, min(1.0, ratio))
        return self.send_message('/style/swing', ratio)
    
    def set_accent_amount(self, amount: float) -> bool:
        """
        Set the accent amount parameter.
        
        Args:
            amount: Accent amount (0.0-50.0 velocity boost)
            
        Returns:
            True if successful, False otherwise
        """
        # Clamp to valid range
        amount = max(0.0, min(50.0, amount))
        return self.send_message('/style/accent', amount)
    
    def set_humanize_timing(self, amount: float) -> bool:
        """
        Set the humanize timing parameter.
        
        Args:
            amount: Humanize timing amount (0.0 = no variation, 1.0 = maximum)
            
        Returns:
            True if successful, False otherwise
        """
        # Clamp to valid range
        amount = max(0.0, min(1.0, amount))
        return self.send_message('/style/humanizeTiming', amount)
    
    def set_humanize_velocity(self, amount: float) -> bool:
        """
        Set the humanize velocity parameter.
        
        Args:
            amount: Humanize velocity amount (0.0 = no variation, 1.0 = maximum)
            
        Returns:
            True if successful, False otherwise
        """
        # Clamp to valid range
        amount = max(0.0, min(1.0, amount))
        return self.send_message('/style/humanizeVelocity', amount)
    
    def set_osc_enabled(self, enabled: bool) -> bool:
        """
        Enable or disable OSC control.
        
        Args:
            enabled: True to enable OSC, False to disable
            
        Returns:
            True if successful, False otherwise
        """
        return self.send_message('/style/enable', enabled)
    
    def set_osc_port(self, port: int) -> bool:
        """
        Set the OSC port (if supported by plugin).
        
        Args:
            port: OSC port number (1000-65535)
            
        Returns:
            True if successful, False otherwise
        """
        # Clamp to valid range
        port = max(1000, min(65535, port))
        return self.send_message('/style/port', port)
    
    # ============================================================================
    # CONVENIENCE METHODS FOR COMMON OPERATIONS
    # ============================================================================
    
    def set_style_preset(self, preset_name: str) -> bool:
        """
        Set a style preset by name.
        
        Args:
            preset_name: Name of the preset ('jazz', 'classical', 'electronic', etc.)
            
        Returns:
            True if successful, False otherwise
        """
        presets = {
            'jazz': {'swing': 0.7, 'accent': 25.0, 'humanize_timing': 0.3, 'humanize_velocity': 0.4},
            'classical': {'swing': 0.5, 'accent': 15.0, 'humanize_timing': 0.2, 'humanize_velocity': 0.3},
            'electronic': {'swing': 0.5, 'accent': 5.0, 'humanize_timing': 0.0, 'humanize_velocity': 0.0},
            'blues': {'swing': 0.6, 'accent': 30.0, 'humanize_timing': 0.4, 'humanize_velocity': 0.5},
            'straight': {'swing': 0.5, 'accent': 0.0, 'humanize_timing': 0.0, 'humanize_velocity': 0.0}
        }
        
        if preset_name.lower() not in presets:
            self.logger.error(f"Unknown preset: {preset_name}")
            return False
        
        preset = presets[preset_name.lower()]
        success = True
        
        # Apply all preset parameters
        success &= self.set_swing_ratio(preset['swing'])
        success &= self.set_accent_amount(preset['accent'])
        success &= self.set_humanize_timing(preset['humanize_timing'])
        success &= self.set_humanize_velocity(preset['humanize_velocity'])
        
        if success:
            self.logger.info(f"Applied style preset: {preset_name}")
        else:
            self.logger.error(f"Failed to apply style preset: {preset_name}")
        
        return success
    
    def reset_to_defaults(self) -> bool:
        """
        Reset all parameters to default values.
        
        Returns:
            True if successful, False otherwise
        """
        success = True
        success &= self.set_swing_ratio(0.5)
        success &= self.set_accent_amount(20.0)
        success &= self.set_humanize_timing(0.0)
        success &= self.set_humanize_velocity(0.0)
        
        if success:
            self.logger.info("Reset all parameters to defaults")
        else:
            self.logger.error("Failed to reset parameters to defaults")
        
        return success
    
    # ============================================================================
    # STATUS AND DIAGNOSTIC METHODS
    # ============================================================================
    
    def is_connected(self) -> bool:
        """
        Check if the OSC client is connected.
        
        Returns:
            True if connected, False otherwise
        """
        return self.connected
    
    def get_connection_info(self) -> dict:
        """
        Get connection information.
        
        Returns:
            Dictionary with connection details
        """
        return {
            'ip_address': self.ip_address,
            'port': self.port,
            'connected': self.connected,
            'client_initialized': self.client is not None
        }
    
    def test_connection(self) -> bool:
        """
        Test the OSC connection by sending a ping message.
        
        Returns:
            True if connection is working, False otherwise
        """
        try:
            # Send a test message (plugin may not respond, but we can check if send succeeds)
            return self.send_message('/style/ping', 1.0)
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def __str__(self) -> str:
        """String representation of the OSC sender."""
        status = "connected" if self.connected else "disconnected"
        return f"OSCSender({self.ip_address}:{self.port}, {status})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the OSC sender."""
        return (f"OSCSender(ip_address='{self.ip_address}', port={self.port}, "
                f"connected={self.connected})")


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_osc_sender(ip_address: str = '127.0.0.1', port: int = 3819) -> OSCSender:
    """
    Create a new OSC sender instance.
    
    Args:
        ip_address: IP address of the JUCE plugin
        port: OSC port number
        
    Returns:
        New OSCSender instance
    """
    return OSCSender(ip_address, port)


def send_style_command(address: str, value: Union[float, int, bool], 
                      ip_address: str = '127.0.0.1', port: int = 3819) -> bool:
    """
    Send a single OSC style command.
    
    Args:
        address: OSC address pattern
        value: Parameter value
        ip_address: IP address of the plugin
        port: OSC port number
        
    Returns:
        True if successful, False otherwise
    """
    sender = OSCSender(ip_address, port)
    return sender.send_message(address, value)
