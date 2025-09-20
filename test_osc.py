#!/usr/bin/env python3
"""
Test script for OSC integration with StyleTransfer plugin.

This script sends OSC messages to test the plugin's OSC receiver.
"""

import socket
import time
import struct

def send_osc_message(host, port, address, value):
    """Send a single OSC message to the specified host and port."""
    
    # OSC message format: address, types, arguments
    # For simplicity, we'll send float32 values
    
    # Convert address to OSC format (null-terminated string)
    address_bytes = address.encode('utf-8') + b'\x00'
    # Pad to 4-byte boundary
    while len(address_bytes) % 4 != 0:
        address_bytes += b'\x00'
    
    # Type tag string (",f" for float32)
    type_tag = b',f\x00'
    # Pad to 4-byte boundary
    while len(type_tag) % 4 != 0:
        type_tag += b'\x00'
    
    # Value as float32 (big-endian)
    value_bytes = struct.pack('>f', value)
    
    # Combine all parts
    message = address_bytes + type_tag + value_bytes
    
    # Send via UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message, (host, port))
        print(f"Sent OSC message: {address} = {value}")
    finally:
        sock.close()

def main():
    """Test the OSC integration."""
    
    host = "localhost"
    port = 3819  # Default OSC port from the plugin
    
    print("Testing StyleTransfer Plugin OSC Integration")
    print("=" * 50)
    
    # Test messages
    test_cases = [
        ("/style/swing", 0.7),
        ("/style/accent", 25.0),
        ("/style/humanizeTiming", 0.3),
        ("/style/humanizeVelocity", 0.5),
        ("/style/swing", 0.5),  # Reset to straight
        ("/style/accent", 0.0),  # Reset accent
    ]
    
    for address, value in test_cases:
        send_osc_message(host, port, address, value)
        time.sleep(0.5)  # Wait between messages
    
    print("\nOSC test completed!")
    print("Check the plugin to see if parameters changed.")

if __name__ == "__main__":
    main()
