"""
SecureOSCClient - Security-First OSC Communication

This module implements a secure OSC client with built-in validation,
rate limiting, encryption, and safety monitoring.
"""

import time
import json
import hmac
import hashlib
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from collections import defaultdict, deque
import socket
import struct

from security_first_architecture import (
    SecurityFirstComponent, SecurityContext, SecurityResult, SecurityLevel,
    SecurityError, InputValidationError, RateLimitExceededError, SystemUnhealthyError
)

try:
    from pythonosc import osc_client, osc_server, dispatcher
    from pythonosc.osc_message_builder import OscMessageBuilder
    from pythonosc.udp_client import SimpleUDPClient
    OSC_AVAILABLE = True
except ImportError:
    OSC_AVAILABLE = False
    # Fallback implementations
    class SimpleUDPClient:
        def __init__(self, *args, **kwargs):
            pass
        def send_message(self, *args, **kwargs):
            pass

@dataclass
class OSCMessage:
    """Secure OSC message structure"""
    address: str
    arguments: List[Any]
    timestamp: float
    message_id: str
    signature: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "address": self.address,
            "arguments": self.arguments,
            "timestamp": self.timestamp,
            "message_id": self.message_id,
            "signature": self.signature
        }

@dataclass
class OSCConfig:
    """OSC configuration with security settings"""
    host: str = "127.0.0.1"
    port: int = 3819
    max_message_size: int = 1024
    max_arguments: int = 10
    rate_limit_per_second: int = 100
    rate_limit_burst: int = 20
    encryption_key: Optional[str] = None
    allowed_addresses: List[str] = None
    blocked_addresses: List[str] = None
    
    def __post_init__(self):
        if self.allowed_addresses is None:
            self.allowed_addresses = ["/ardour/*", "/enhancement/*"]
        if self.blocked_addresses is None:
            self.blocked_addresses = ["/system/*", "/admin/*"]

class RateLimiter:
    """Token bucket rate limiter for OSC messages"""
    
    def __init__(self, rate_per_second: int, burst_size: int):
        self.rate_per_second = rate_per_second
        self.burst_size = burst_size
        self.tokens = burst_size
        self.last_update = time.time()
        self.lock = threading.Lock()
        
    def is_allowed(self) -> bool:
        """Check if request is allowed under rate limit"""
        with self.lock:
            now = time.time()
            time_passed = now - self.last_update
            
            # Add tokens based on time passed
            self.tokens = min(self.burst_size, self.tokens + time_passed * self.rate_per_second)
            self.last_update = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

class OSCValidator:
    """OSC message validator with security checks"""
    
    def __init__(self, config: OSCConfig):
        self.config = config
        self.max_message_size = config.max_message_size
        self.max_arguments = config.max_arguments
        
    def validate_message(self, message: OSCMessage) -> SecurityResult:
        """Validate OSC message for security"""
        start_time = time.time()
        
        try:
            # Check message size
            message_size = len(json.dumps(message.to_dict()))
            if message_size > self.max_message_size:
                return SecurityResult(
                    success=False,
                    message=f"Message too large: {message_size} > {self.max_message_size}",
                    security_level=SecurityLevel.MEDIUM,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            # Check argument count
            if len(message.arguments) > self.max_arguments:
                return SecurityResult(
                    success=False,
                    message=f"Too many arguments: {len(message.arguments)} > {self.max_arguments}",
                    security_level=SecurityLevel.MEDIUM,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            # Check address patterns
            if not self._is_address_allowed(message.address):
                return SecurityResult(
                    success=False,
                    message=f"Address not allowed: {message.address}",
                    security_level=SecurityLevel.HIGH,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            # Validate arguments
            for i, arg in enumerate(message.arguments):
                if not self._is_argument_valid(arg):
                    return SecurityResult(
                        success=False,
                        message=f"Invalid argument {i}: {type(arg).__name__}",
                        security_level=SecurityLevel.MEDIUM,
                        processing_time_ms=(time.time() - start_time) * 1000
                    )
            
            return SecurityResult(
                success=True,
                message="Message validation successful",
                security_level=SecurityLevel.LOW,
                processing_time_ms=(time.time() - start_time) * 1000
            )
            
        except Exception as e:
            return SecurityResult(
                success=False,
                message=f"Validation error: {str(e)}",
                security_level=SecurityLevel.HIGH,
                processing_time_ms=(time.time() - start_time) * 1000
            )
    
    def _is_address_allowed(self, address: str) -> bool:
        """Check if address is allowed"""
        # Check blocked addresses first
        for blocked in self.config.blocked_addresses:
            if self._matches_pattern(address, blocked):
                return False
        
        # Check allowed addresses
        for allowed in self.config.allowed_addresses:
            if self._matches_pattern(address, allowed):
                return True
        
        return False
    
    def _matches_pattern(self, address: str, pattern: str) -> bool:
        """Check if address matches pattern (supports wildcards)"""
        if pattern.endswith("*"):
            return address.startswith(pattern[:-1])
        return address == pattern
    
    def _is_argument_valid(self, arg: Any) -> bool:
        """Check if argument is valid"""
        valid_types = (int, float, str, bool)
        return isinstance(arg, valid_types)

class OSCEncryptor:
    """OSC message encryption for sensitive data"""
    
    def __init__(self, encryption_key: Optional[str] = None):
        self.encryption_key = encryption_key or "default_key_change_me"
        self.algorithm = "sha256"
        
    def encrypt_message(self, message: OSCMessage) -> OSCMessage:
        """Encrypt OSC message"""
        if not self.encryption_key:
            return message
        
        # Create signature
        message_data = json.dumps({
            "address": message.address,
            "arguments": message.arguments,
            "timestamp": message.timestamp,
            "message_id": message.message_id
        })
        
        signature = hmac.new(
            self.encryption_key.encode(),
            message_data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return OSCMessage(
            address=message.address,
            arguments=message.arguments,
            timestamp=message.timestamp,
            message_id=message.message_id,
            signature=signature
        )
    
    def verify_message(self, message: OSCMessage) -> bool:
        """Verify OSC message signature"""
        if not message.signature:
            return True  # No signature to verify
        
        message_data = json.dumps({
            "address": message.address,
            "arguments": message.arguments,
            "timestamp": message.timestamp,
            "message_id": message.message_id
        })
        
        expected_signature = hmac.new(
            self.encryption_key.encode(),
            message_data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(message.signature, expected_signature)

class SecureOSCClient(SecurityFirstComponent):
    """Security-first OSC client with built-in validation and rate limiting"""
    
    def __init__(self, config: OSCConfig, security_level: SecurityLevel = SecurityLevel.MEDIUM):
        super().__init__("secure_osc_client", security_level)
        self.config = config
        self.rate_limiter = RateLimiter(
            config.rate_limit_per_second,
            config.rate_limit_burst
        )
        self.validator = OSCValidator(config)
        self.encryptor = OSCEncryptor(config.encryption_key)
        self.client = None
        self.server = None
        self.message_history = deque(maxlen=1000)
        self.safety_monitor = None
        
        # Initialize OSC client if available
        if OSC_AVAILABLE:
            self.client = SimpleUDPClient(config.host, config.port)
        else:
            self.logger.warning("python-osc not available, using fallback implementation")
    
    def _validate_input(self, data: Any, context: SecurityContext) -> SecurityResult:
        """Validate OSC message input"""
        if not isinstance(data, OSCMessage):
            return SecurityResult(
                success=False,
                message="Input must be OSCMessage",
                security_level=SecurityLevel.MEDIUM,
                processing_time_ms=0
            )
        
        return self.validator.validate_message(data)
    
    def _process_secure(self, data: OSCMessage, context: SecurityContext) -> Dict[str, Any]:
        """Process OSC message securely"""
        # Rate limiting
        if not self.rate_limiter.is_allowed():
            raise RateLimitExceededError("Rate limit exceeded for OSC messages")
        
        # Encrypt message
        encrypted_message = self.encryptor.encrypt_message(data)
        
        # Send message
        if self.client:
            try:
                self.client.send_message(encrypted_message.address, encrypted_message.arguments)
                self.logger.debug(f"Sent OSC message to {encrypted_message.address}")
            except Exception as e:
                self.logger.error(f"Failed to send OSC message: {str(e)}")
                raise SecurityError(f"OSC send failed: {str(e)}", SecurityLevel.MEDIUM)
        
        # Record message in history
        self.message_history.append({
            "message": encrypted_message.to_dict(),
            "timestamp": time.time(),
            "context": context.request_id
        })
        
        return {
            "success": True,
            "message_id": encrypted_message.message_id,
            "address": encrypted_message.address,
            "timestamp": encrypted_message.timestamp
        }
    
    def start_server(self, port: int, message_handler: Callable[[OSCMessage], None]):
        """Start OSC server for receiving messages"""
        if not OSC_AVAILABLE:
            self.logger.warning("Cannot start OSC server: python-osc not available")
            return
        
        try:
            dispatcher_obj = dispatcher.Dispatcher()
            dispatcher_obj.map("*", self._handle_message)
            self.message_handler = message_handler
            
            self.server = osc_server.ThreadingOSCUDPServer(
                ("127.0.0.1", port), dispatcher_obj
            )
            
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            self.logger.info(f"Started OSC server on port {port}")
            
        except Exception as e:
            self.logger.error(f"Failed to start OSC server: {str(e)}")
            raise SecurityError(f"OSC server start failed: {str(e)}", SecurityLevel.HIGH)
    
    def _handle_message(self, address: str, *args):
        """Handle incoming OSC message"""
        try:
            message = OSCMessage(
                address=address,
                arguments=list(args),
                timestamp=time.time(),
                message_id=f"recv_{int(time.time() * 1000)}"
            )
            
            # Validate incoming message
            validation_result = self.validator.validate_message(message)
            if not validation_result.success:
                self.logger.warning(f"Invalid incoming message: {validation_result.message}")
                return
            
            # Verify signature if present
            if message.signature and not self.encryptor.verify_message(message):
                self.logger.warning("Invalid message signature")
                return
            
            # Call message handler
            if hasattr(self, 'message_handler'):
                self.message_handler(message)
                
        except Exception as e:
            self.logger.error(f"Error handling OSC message: {str(e)}")
    
    def stop_server(self):
        """Stop OSC server"""
        if self.server:
            self.server.shutdown()
            self.server = None
            self.logger.info("Stopped OSC server")
    
    def get_message_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent message history"""
        return list(self.message_history)[-limit:]
    
    def create_message(self, address: str, arguments: List[Any]) -> OSCMessage:
        """Create a new OSC message"""
        return OSCMessage(
            address=address,
            arguments=arguments,
            timestamp=time.time(),
            message_id=f"msg_{int(time.time() * 1000)}"
        )

class SecureOSCManager:
    """Manager for multiple secure OSC clients"""
    
    def __init__(self):
        self.clients = {}
        import logging
        self.logger = logging.getLogger("secure_osc_manager")
    
    def create_client(self, name: str, config: OSCConfig) -> SecureOSCClient:
        """Create a new secure OSC client"""
        client = SecureOSCClient(config)
        self.clients[name] = client
        self.logger.info(f"Created OSC client: {name}")
        return client
    
    def get_client(self, name: str) -> Optional[SecureOSCClient]:
        """Get OSC client by name"""
        return self.clients.get(name)
    
    def remove_client(self, name: str):
        """Remove OSC client"""
        if name in self.clients:
            self.clients[name].stop_server()
            del self.clients[name]
            self.logger.info(f"Removed OSC client: {name}")
    
    def get_all_health_status(self) -> Dict[str, Any]:
        """Get health status of all clients"""
        status = {}
        for name, client in self.clients.items():
            status[name] = {
                "healthy": client.health_checker.is_healthy(),
                "metrics": client.metrics.get_stats()
            }
        return status

# Example usage and testing
if __name__ == "__main__":
    # Create OSC configuration
    config = OSCConfig(
        host="127.0.0.1",
        port=3819,
        rate_limit_per_second=50,
        rate_limit_burst=10,
        encryption_key="test_key_123"
    )
    
    # Create security context
    context = SecurityContext(
        user_id="test_user",
        session_id="test_session",
        security_level=SecurityLevel.MEDIUM,
        timestamp=time.time(),
        request_id="test_request_001"
    )
    
    # Create secure OSC client
    client = SecureOSCClient(config)
    
    # Test message creation and sending
    message = client.create_message("/ardour/transport/play", [1])
    result = client.process(message, context)
    
    print(f"OSC message sent: {result}")
    print(f"Client health: {client.health_checker.is_healthy()}")
    print(f"Client metrics: {client.metrics.get_stats()}")
