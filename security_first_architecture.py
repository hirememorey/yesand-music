"""
Security-First Real-Time Ardour Enhancement System

This module implements the core security-first architecture where security
is built into each component rather than added as an afterthought.
"""

import asyncio
import logging
import threading
import queue
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import json
import hashlib
import hmac
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels for different operations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityContext:
    """Security context for operations"""
    user_id: str
    session_id: str
    security_level: SecurityLevel
    timestamp: datetime
    request_id: str
    source_ip: Optional[str] = None
    user_agent: Optional[str] = None

@dataclass
class SecurityResult:
    """Result of security operations"""
    success: bool
    message: str
    security_level: SecurityLevel
    processing_time_ms: float
    additional_data: Optional[Dict[str, Any]] = None

class SecurityError(Exception):
    """Base security error"""
    def __init__(self, message: str, security_level: SecurityLevel = SecurityLevel.MEDIUM):
        self.message = message
        self.security_level = security_level
        super().__init__(message)

class InputValidationError(SecurityError):
    """Input validation failed"""
    pass

class RateLimitExceededError(SecurityError):
    """Rate limit exceeded"""
    pass

class SystemUnhealthyError(SecurityError):
    """System is unhealthy"""
    pass

class SecurityFirstComponent(ABC):
    """Base class for all security-first components"""
    
    def __init__(self, component_name: str, security_level: SecurityLevel = SecurityLevel.MEDIUM):
        self.component_name = component_name
        self.security_level = security_level
        self.logger = logging.getLogger(f"security.{component_name}")
        self.metrics = SecurityMetrics(component_name)
        self.health_checker = HealthChecker(component_name)
        
    @abstractmethod
    def _validate_input(self, data: Any, context: SecurityContext) -> SecurityResult:
        """Validate input data"""
        pass
    
    @abstractmethod
    def _process_secure(self, data: Any, context: SecurityContext) -> Any:
        """Process data securely"""
        pass
    
    def process(self, data: Any, context: SecurityContext) -> Any:
        """Main processing method with built-in security"""
        start_time = time.time()
        
        try:
            # Health check
            if not self.health_checker.is_healthy():
                raise SystemUnhealthyError(f"{self.component_name} is not healthy")
            
            # Input validation
            validation_result = self._validate_input(data, context)
            if not validation_result.success:
                raise InputValidationError(validation_result.message, validation_result.security_level)
            
            # Process securely
            result = self._process_secure(data, context)
            
            # Record metrics
            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_success(processing_time, context.security_level)
            
            self.logger.info(f"Successfully processed {self.component_name} request in {processing_time:.2f}ms")
            return result
            
        except SecurityError as e:
            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_security_error(e, processing_time)
            self.logger.error(f"Security error in {self.component_name}: {e.message}")
            raise
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_error(e, processing_time)
            self.logger.error(f"Unexpected error in {self.component_name}: {str(e)}")
            raise SecurityError(f"Unexpected error: {str(e)}", SecurityLevel.HIGH)

class SecurityMetrics:
    """Security metrics collection"""
    
    def __init__(self, component_name: str):
        self.component_name = component_name
        self.success_count = 0
        self.error_count = 0
        self.security_error_count = 0
        self.total_processing_time = 0.0
        self.by_security_level = {level: 0 for level in SecurityLevel}
        
    def record_success(self, processing_time_ms: float, security_level: SecurityLevel):
        """Record successful operation"""
        self.success_count += 1
        self.total_processing_time += processing_time_ms
        self.by_security_level[security_level] += 1
        
    def record_security_error(self, error: SecurityError, processing_time_ms: float):
        """Record security error"""
        self.security_error_count += 1
        self.total_processing_time += processing_time_ms
        self.by_security_level[error.security_level] += 1
        
    def record_error(self, error: Exception, processing_time_ms: float):
        """Record general error"""
        self.error_count += 1
        self.total_processing_time += processing_time_ms
        
    def get_stats(self) -> Dict[str, Any]:
        """Get current metrics"""
        total_operations = self.success_count + self.error_count + self.security_error_count
        avg_processing_time = self.total_processing_time / total_operations if total_operations > 0 else 0
        
        return {
            "component": self.component_name,
            "total_operations": total_operations,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "security_error_count": self.security_error_count,
            "success_rate": self.success_count / total_operations if total_operations > 0 else 0,
            "avg_processing_time_ms": avg_processing_time,
            "by_security_level": {level.value: count for level, count in self.by_security_level.items()}
        }

class HealthChecker:
    """Health checking for components"""
    
    def __init__(self, component_name: str):
        self.component_name = component_name
        self.last_health_check = time.time()
        self.health_status = True
        self.error_count = 0
        self.max_errors = 5
        self.error_window = 60  # seconds
        
    def is_healthy(self) -> bool:
        """Check if component is healthy"""
        current_time = time.time()
        
        # Reset error count if window has passed
        if current_time - self.last_health_check > self.error_window:
            self.error_count = 0
            self.last_health_check = current_time
            
        return self.health_status and self.error_count < self.max_errors
    
    def record_error(self):
        """Record an error"""
        self.error_count += 1
        if self.error_count >= self.max_errors:
            self.health_status = False
            
    def record_success(self):
        """Record a success"""
        self.error_count = max(0, self.error_count - 1)
        if self.error_count == 0:
            self.health_status = True

class AsyncSafetyMonitor:
    """Asynchronous safety monitoring that doesn't block main thread"""
    
    def __init__(self, component_name: str):
        self.component_name = component_name
        self.safety_queue = queue.Queue()
        self.monitor_thread = None
        self.running = False
        self.safety_rules = []
        self.logger = logging.getLogger(f"safety.{component_name}")
        
    def start(self):
        """Start the safety monitor"""
        if self.running:
            return
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info(f"Started safety monitor for {self.component_name}")
        
    def stop(self):
        """Stop the safety monitor"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info(f"Stopped safety monitor for {self.component_name}")
        
    def add_safety_rule(self, rule: Callable[[Dict[str, Any]], bool], name: str):
        """Add a safety rule"""
        self.safety_rules.append({"rule": rule, "name": name})
        
    def check_safety(self, data: Dict[str, Any]) -> bool:
        """Check safety rules asynchronously"""
        self.safety_queue.put(data)
        return True  # Always return True, actual checking happens async
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                # Get data from queue with timeout
                data = self.safety_queue.get(timeout=1.0)
                
                # Check all safety rules
                for rule_info in self.safety_rules:
                    try:
                        if not rule_info["rule"](data):
                            self.logger.warning(f"Safety rule '{rule_info['name']}' failed for {self.component_name}")
                    except Exception as e:
                        self.logger.error(f"Safety rule '{rule_info['name']}' error: {str(e)}")
                        
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Safety monitor error: {str(e)}")

class CircuitBreaker:
    """Circuit breaker pattern for external service calls"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.logger = logging.getLogger("circuit_breaker")
        
    def call(self, func: Callable, *args, **kwargs):
        """Call function through circuit breaker"""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                self.logger.info("Circuit breaker transitioning to HALF_OPEN")
            else:
                raise SecurityError("Circuit breaker is OPEN", SecurityLevel.HIGH)
                
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                self.logger.info("Circuit breaker transitioning to CLOSED")
            return result
            
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.logger.warning(f"Circuit breaker opened after {self.failure_count} failures")
                
            raise

class SecurityFirstEnhancer:
    """Main security-first enhancement orchestrator"""
    
    def __init__(self):
        self.components = {}
        self.security_context = None
        self.logger = logging.getLogger("security_first_enhancer")
        
    def register_component(self, name: str, component: SecurityFirstComponent):
        """Register a security-first component"""
        self.components[name] = component
        self.logger.info(f"Registered component: {name}")
        
    def set_security_context(self, context: SecurityContext):
        """Set security context for operations"""
        self.security_context = context
        
    def enhance(self, request: str) -> Dict[str, Any]:
        """Main enhancement method"""
        if not self.security_context:
            raise SecurityError("No security context set", SecurityLevel.HIGH)
            
        self.logger.info(f"Processing enhancement request: {request}")
        
        # Process through all registered components
        result = {"request": request, "components": {}}
        
        for name, component in self.components.items():
            try:
                component_result = component.process(request, self.security_context)
                result["components"][name] = component_result
            except SecurityError as e:
                self.logger.error(f"Component {name} failed: {e.message}")
                result["components"][name] = {"error": e.message, "security_level": e.security_level.value}
                
        return result
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of all components"""
        status = {}
        for name, component in self.components.items():
            status[name] = {
                "healthy": component.health_checker.is_healthy(),
                "metrics": component.metrics.get_stats()
            }
        return status

# Example usage and testing
if __name__ == "__main__":
    # Create security context
    context = SecurityContext(
        user_id="test_user",
        session_id="test_session",
        security_level=SecurityLevel.MEDIUM,
        timestamp=datetime.now(),
        request_id="test_request_001"
    )
    
    # Create enhancer
    enhancer = SecurityFirstEnhancer()
    enhancer.set_security_context(context)
    
    # Test basic functionality
    print("Security-First Architecture initialized successfully")
    print(f"Health status: {enhancer.get_health_status()}")
