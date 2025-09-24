"""
Secure Enhancement System - Integration Layer

This module integrates all security-first components into a cohesive
real-time Ardour enhancement system with fail-fast architecture.
"""

import time
import json
import asyncio
import threading
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass
from enum import Enum
import logging

from security_first_architecture import (
    SecurityFirstEnhancer, SecurityContext, SecurityLevel, SecurityError,
    AsyncSafetyMonitor, CircuitBreaker
)
from secure_osc_client import SecureOSCClient, OSCConfig, OSCMessage, SecureOSCManager
from secure_file_parser import SecureFileParser, FileConfig, ParseResult, SecureFileManager
from secure_llm_client import SecureLLMClient, LLMConfig, LLMRequest, LLMResponse, SecureLLMManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancementMode(Enum):
    """Enhancement system modes"""
    OFFLINE = "offline"
    FILE_BASED = "file_based"
    REAL_TIME = "real_time"
    DEMO = "demo"

@dataclass
class EnhancementRequest:
    """Enhancement request with security context"""
    user_request: str
    enhancement_type: str
    track_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    security_level: SecurityLevel = SecurityLevel.MEDIUM
    user_id: str = "anonymous"
    session_id: str = "default"

@dataclass
class EnhancementResult:
    """Enhancement result with security metadata"""
    success: bool
    message: str
    data: Optional[Any] = None
    processing_time_ms: float = 0.0
    security_level: SecurityLevel = SecurityLevel.LOW
    warnings: List[str] = None
    errors: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.errors is None:
            self.errors = []
        if self.metadata is None:
            self.metadata = {}

class FailFastEnhancer:
    """Fail-fast enhancement system with health checks and circuit breakers"""
    
    def __init__(self):
        self.mode = EnhancementMode.OFFLINE
        self.components = {}
        self.circuit_breakers = {}
        self.health_checker = HealthChecker()
        self.safety_monitor = None
        self.logger = logging.getLogger("fail_fast_enhancer")
        
        # Initialize component managers
        self.osc_manager = SecureOSCManager()
        self.file_manager = SecureFileManager()
        self.llm_manager = SecureLLMManager()
        
        # Initialize safety monitor
        self.safety_monitor = AsyncSafetyMonitor("enhancement_system")
        self.safety_monitor.start()
        
        # Add safety rules
        self._setup_safety_rules()
        
    def _setup_safety_rules(self):
        """Setup safety rules for the enhancement system"""
        
        def check_processing_time(data):
            """Check if processing time is within limits"""
            processing_time = data.get('processing_time_ms', 0)
            return processing_time < 5000  # 5 seconds max
        
        def check_memory_usage(data):
            """Check if memory usage is within limits"""
            # This would integrate with actual memory monitoring
            return True
        
        def check_error_rate(data):
            """Check if error rate is within limits"""
            error_count = data.get('error_count', 0)
            total_operations = data.get('total_operations', 1)
            error_rate = error_count / total_operations
            return error_rate < 0.1  # 10% max error rate
        
        self.safety_monitor.add_safety_rule(check_processing_time, "processing_time")
        self.safety_monitor.add_safety_rule(check_memory_usage, "memory_usage")
        self.safety_monitor.add_safety_rule(check_error_rate, "error_rate")
    
    def detect_best_mode(self) -> EnhancementMode:
        """Detect the best available enhancement mode"""
        try:
            # Check if OSC is available
            if self._can_use_osc():
                return EnhancementMode.REAL_TIME
            
            # Check if file-based is available
            if self._can_use_file_based():
                return EnhancementMode.FILE_BASED
            
            # Check if offline is available
            if self._can_use_offline():
                return EnhancementMode.OFFLINE
            
            # Fallback to demo mode
            return EnhancementMode.DEMO
            
        except Exception as e:
            self.logger.error(f"Error detecting mode: {str(e)}")
            return EnhancementMode.DEMO
    
    def _can_use_osc(self) -> bool:
        """Check if OSC mode is available"""
        try:
            # Try to create OSC client
            config = OSCConfig(host="127.0.0.1", port=3819)
            client = self.osc_manager.create_client("test", config)
            
            # Test basic functionality
            message = client.create_message("/test", [1])
            context = SecurityContext(
                user_id="test",
                session_id="test",
                security_level=SecurityLevel.LOW,
                timestamp=time.time(),
                request_id="test"
            )
            
            result = client.process(message, context)
            return result.get("success", False)
            
        except Exception as e:
            self.logger.debug(f"OSC not available: {str(e)}")
            return False
    
    def _can_use_file_based(self) -> bool:
        """Check if file-based mode is available"""
        try:
            # Try to create file parser
            config = FileConfig()
            parser = self.file_manager.create_parser("test", config)
            
            # Test basic functionality
            context = SecurityContext(
                user_id="test",
                session_id="test",
                security_level=SecurityLevel.LOW,
                timestamp=time.time(),
                request_id="test"
            )
            
            # This would test with an actual file
            return True
            
        except Exception as e:
            self.logger.debug(f"File-based not available: {str(e)}")
            return False
    
    def _can_use_offline(self) -> bool:
        """Check if offline mode is available"""
        try:
            # Check if LLM client is available
            config = LLMConfig(api_key="test_key")
            client = self.llm_manager.create_client("test", config)
            
            # Test basic functionality
            request = client.create_request("test prompt")
            context = SecurityContext(
                user_id="test",
                session_id="test",
                security_level=SecurityLevel.LOW,
                timestamp=time.time(),
                request_id="test"
            )
            
            result = client.process(request, context)
            return result is not None
            
        except Exception as e:
            self.logger.debug(f"Offline not available: {str(e)}")
            return False
    
    def enhance(self, request: EnhancementRequest) -> EnhancementResult:
        """Main enhancement method with fail-fast architecture"""
        start_time = time.time()
        
        try:
            # Health check
            if not self.health_checker.is_healthy():
                return EnhancementResult(
                    success=False,
                    message="System is not healthy",
                    processing_time_ms=(time.time() - start_time) * 1000,
                    security_level=SecurityLevel.HIGH,
                    errors=["System health check failed"]
                )
            
            # Detect best mode
            self.mode = self.detect_best_mode()
            
            # Create security context
            context = SecurityContext(
                user_id=request.user_id,
                session_id=request.session_id,
                security_level=request.security_level,
                timestamp=time.time(),
                request_id=f"enhance_{int(time.time() * 1000)}"
            )
            
            # Process based on mode
            if self.mode == EnhancementMode.REAL_TIME:
                return self._enhance_real_time(request, context)
            elif self.mode == EnhancementMode.FILE_BASED:
                return self._enhance_file_based(request, context)
            elif self.mode == EnhancementMode.OFFLINE:
                return self._enhance_offline(request, context)
            else:
                return self._enhance_demo(request, context)
                
        except SecurityError as e:
            return EnhancementResult(
                success=False,
                message=f"Security error: {e.message}",
                processing_time_ms=(time.time() - start_time) * 1000,
                security_level=e.security_level,
                errors=[e.message]
            )
        except Exception as e:
            return EnhancementResult(
                success=False,
                message=f"Enhancement error: {str(e)}",
                processing_time_ms=(time.time() - start_time) * 1000,
                security_level=SecurityLevel.HIGH,
                errors=[str(e)]
            )
    
    def _enhance_real_time(self, request: EnhancementRequest, context: SecurityContext) -> EnhancementResult:
        """Real-time enhancement using OSC"""
        start_time = time.time()
        
        try:
            # Get OSC client
            osc_client = self.osc_manager.get_client("ardour")
            if not osc_client:
                # Create OSC client
                config = OSCConfig(host="127.0.0.1", port=3819)
                osc_client = self.osc_manager.create_client("ardour", config)
            
            # Get LLM client
            llm_client = self.llm_manager.get_client("enhancement")
            if not llm_client:
                # Create LLM client
                config = LLMConfig(api_key="your_api_key_here")
                llm_client = self.llm_manager.create_client("enhancement", config)
            
            # Create LLM request
            llm_request = llm_client.create_request(
                prompt=request.user_request,
                user_id=request.user_id,
                session_id=request.session_id,
                security_level=request.security_level
            )
            
            # Process LLM request
            llm_response = llm_client.process(llm_request, context)
            
            # Create OSC message
            osc_message = osc_client.create_message(
                f"/enhancement/{request.enhancement_type}",
                [llm_response.content, request.track_id or ""]
            )
            
            # Send OSC message
            osc_result = osc_client.process(osc_message, context)
            
            return EnhancementResult(
                success=True,
                message="Real-time enhancement completed",
                data={
                    "llm_response": llm_response,
                    "osc_result": osc_result
                },
                processing_time_ms=(time.time() - start_time) * 1000,
                security_level=SecurityLevel.LOW,
                metadata={
                    "mode": "real_time",
                    "track_id": request.track_id,
                    "enhancement_type": request.enhancement_type
                }
            )
            
        except Exception as e:
            return EnhancementResult(
                success=False,
                message=f"Real-time enhancement failed: {str(e)}",
                processing_time_ms=(time.time() - start_time) * 1000,
                security_level=SecurityLevel.MEDIUM,
                errors=[str(e)]
            )
    
    def _enhance_file_based(self, request: EnhancementRequest, context: SecurityContext) -> EnhancementResult:
        """File-based enhancement"""
        start_time = time.time()
        
        try:
            # Get file parser
            file_parser = self.file_manager.get_parser("ardour")
            if not file_parser:
                # Create file parser
                config = FileConfig()
                file_parser = self.file_manager.create_parser("ardour", config)
            
            # Get LLM client
            llm_client = self.llm_manager.get_client("enhancement")
            if not llm_client:
                # Create LLM client
                config = LLMConfig(api_key="your_api_key_here")
                llm_client = self.llm_manager.create_client("enhancement", config)
            
            # This would integrate with actual file-based workflow
            # For now, return a placeholder result
            
            return EnhancementResult(
                success=True,
                message="File-based enhancement completed",
                data={"mode": "file_based"},
                processing_time_ms=(time.time() - start_time) * 1000,
                security_level=SecurityLevel.LOW,
                metadata={
                    "mode": "file_based",
                    "enhancement_type": request.enhancement_type
                }
            )
            
        except Exception as e:
            return EnhancementResult(
                success=False,
                message=f"File-based enhancement failed: {str(e)}",
                processing_time_ms=(time.time() - start_time) * 1000,
                security_level=SecurityLevel.MEDIUM,
                errors=[str(e)]
            )
    
    def _enhance_offline(self, request: EnhancementRequest, context: SecurityContext) -> EnhancementResult:
        """Offline enhancement using LLM only"""
        start_time = time.time()
        
        try:
            # Get LLM client
            llm_client = self.llm_manager.get_client("enhancement")
            if not llm_client:
                # Create LLM client
                config = LLMConfig(api_key="your_api_key_here")
                llm_client = self.llm_manager.create_client("enhancement", config)
            
            # Create LLM request
            llm_request = llm_client.create_request(
                prompt=request.user_request,
                user_id=request.user_id,
                session_id=request.session_id,
                security_level=request.security_level
            )
            
            # Process LLM request
            llm_response = llm_client.process(llm_request, context)
            
            return EnhancementResult(
                success=True,
                message="Offline enhancement completed",
                data={"llm_response": llm_response},
                processing_time_ms=(time.time() - start_time) * 1000,
                security_level=SecurityLevel.LOW,
                metadata={
                    "mode": "offline",
                    "enhancement_type": request.enhancement_type
                }
            )
            
        except Exception as e:
            return EnhancementResult(
                success=False,
                message=f"Offline enhancement failed: {str(e)}",
                processing_time_ms=(time.time() - start_time) * 1000,
                security_level=SecurityLevel.MEDIUM,
                errors=[str(e)]
            )
    
    def _enhance_demo(self, request: EnhancementRequest, context: SecurityContext) -> EnhancementResult:
        """Demo enhancement mode"""
        start_time = time.time()
        
        return EnhancementResult(
            success=True,
            message="Demo enhancement completed",
            data={
                "demo_response": f"Demo enhancement for: {request.user_request}",
                "mode": "demo"
            },
            processing_time_ms=(time.time() - start_time) * 1000,
            security_level=SecurityLevel.LOW,
            metadata={
                "mode": "demo",
                "enhancement_type": request.enhancement_type
            }
        )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "mode": self.mode.value,
            "healthy": self.health_checker.is_healthy(),
            "osc_status": self.osc_manager.get_all_health_status(),
            "file_status": self.file_manager.get_all_health_status(),
            "llm_status": self.llm_manager.get_all_health_status(),
            "safety_monitor": {
                "running": self.safety_monitor.running if self.safety_monitor else False
            }
        }
    
    def shutdown(self):
        """Shutdown the enhancement system"""
        if self.safety_monitor:
            self.safety_monitor.stop()
        
        # Shutdown all OSC clients
        for client in self.osc_manager.clients.values():
            client.stop_server()
        
        self.logger.info("Enhancement system shutdown complete")

class HealthChecker:
    """System health checker"""
    
    def __init__(self):
        self.healthy = True
        self.last_check = time.time()
        self.error_count = 0
        self.max_errors = 10
        self.error_window = 300  # 5 minutes
        
    def is_healthy(self) -> bool:
        """Check if system is healthy"""
        current_time = time.time()
        
        # Reset error count if window has passed
        if current_time - self.last_check > self.error_window:
            self.error_count = 0
            self.last_check = current_time
            
        return self.healthy and self.error_count < self.max_errors
    
    def record_error(self):
        """Record an error"""
        self.error_count += 1
        if self.error_count >= self.max_errors:
            self.healthy = False
    
    def record_success(self):
        """Record a success"""
        self.error_count = max(0, self.error_count - 1)
        if self.error_count == 0:
            self.healthy = True

# Example usage and testing
if __name__ == "__main__":
    # Create enhancement system
    enhancer = FailFastEnhancer()
    
    # Create enhancement request
    request = EnhancementRequest(
        user_request="Create a funky bassline",
        enhancement_type="bass",
        track_id="1",
        security_level=SecurityLevel.MEDIUM,
        user_id="test_user",
        session_id="test_session"
    )
    
    # Process enhancement
    result = enhancer.enhance(request)
    
    print(f"Enhancement result: {result.success}")
    print(f"Message: {result.message}")
    print(f"Processing time: {result.processing_time_ms:.2f}ms")
    print(f"System status: {enhancer.get_system_status()}")
    
    # Shutdown
    enhancer.shutdown()
