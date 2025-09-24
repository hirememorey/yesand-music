"""
SecureLLMClient - Security-First LLM Communication

This module implements secure LLM client with built-in request validation,
response sanitization, rate limiting, and safety monitoring.
"""

import time
import json
import hashlib
import re
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from collections import defaultdict, deque
import threading

from security_first_architecture import (
    SecurityFirstComponent, SecurityContext, SecurityResult, SecurityLevel,
    SecurityError, InputValidationError, RateLimitExceededError, SystemUnhealthyError
)

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    # Fallback for testing
    class OpenAI:
        class ChatCompletion:
            @staticmethod
            def create(*args, **kwargs):
                return {"choices": [{"message": {"content": "Test response"}}]}

@dataclass
class LLMRequest:
    """Secure LLM request structure"""
    prompt: str
    model: str
    max_tokens: int
    temperature: float
    request_id: str
    timestamp: float
    user_id: str
    session_id: str
    security_level: SecurityLevel
    metadata: Dict[str, Any]

@dataclass
class LLMResponse:
    """Secure LLM response structure"""
    content: str
    model: str
    request_id: str
    timestamp: float
    processing_time_ms: float
    token_count: int
    is_safe: bool
    confidence_score: float
    warnings: List[str]
    metadata: Dict[str, Any]

@dataclass
class LLMConfig:
    """LLM configuration with security settings"""
    api_key: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7
    rate_limit_per_minute: int = 60
    rate_limit_burst: int = 10
    max_prompt_length: int = 4000
    max_response_length: int = 2000
    enable_content_filtering: bool = True
    enable_response_validation: bool = True
    allowed_models: List[str] = None
    blocked_patterns: List[str] = None
    safe_response_patterns: List[str] = None
    
    def __post_init__(self):
        if self.allowed_models is None:
            self.allowed_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
        if self.blocked_patterns is None:
            self.blocked_patterns = [
                r"<script.*?>.*?</script>",
                r"javascript:",
                r"eval\s*\(",
                r"exec\s*\(",
                r"system\s*\(",
                r"shell\s*\(",
                r"rm\s+-rf",
                r"sudo\s+",
                r"chmod\s+777"
            ]
        if self.safe_response_patterns is None:
            self.safe_response_patterns = [
                r"^[A-Za-z0-9\s.,!?;:'\"()-]+$",  # Basic text
                r"^[0-9\s.,]+$",  # Numbers
                r"^[A-Za-z0-9\s]+$"  # Alphanumeric
            ]

class PromptValidator:
    """LLM prompt validation with security checks"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.blocked_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in config.blocked_patterns]
        
    def validate_prompt(self, prompt: str) -> SecurityResult:
        """Validate LLM prompt for security"""
        start_time = time.time()
        
        try:
            # Check prompt length
            if len(prompt) > self.config.max_prompt_length:
                return SecurityResult(
                    success=False,
                    message=f"Prompt too long: {len(prompt)} > {self.config.max_prompt_length}",
                    security_level=SecurityLevel.MEDIUM,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            # Check for blocked patterns
            for pattern in self.blocked_patterns:
                if pattern.search(prompt):
                    return SecurityResult(
                        success=False,
                        message=f"Blocked pattern detected: {pattern.pattern}",
                        security_level=SecurityLevel.HIGH,
                        processing_time_ms=(time.time() - start_time) * 1000
                    )
            
            # Check for suspicious content
            suspicious_indicators = [
                "ignore previous instructions",
                "you are now",
                "forget everything",
                "pretend to be",
                "act as if",
                "roleplay as"
            ]
            
            for indicator in suspicious_indicators:
                if indicator.lower() in prompt.lower():
                    return SecurityResult(
                        success=False,
                        message=f"Suspicious prompt pattern: {indicator}",
                        security_level=SecurityLevel.HIGH,
                        processing_time_ms=(time.time() - start_time) * 1000
                    )
            
            return SecurityResult(
                success=True,
                message="Prompt validation successful",
                security_level=SecurityLevel.LOW,
                processing_time_ms=(time.time() - start_time) * 1000
            )
            
        except Exception as e:
            return SecurityResult(
                success=False,
                message=f"Prompt validation error: {str(e)}",
                security_level=SecurityLevel.HIGH,
                processing_time_ms=(time.time() - start_time) * 1000
            )

class ResponseSanitizer:
    """LLM response sanitization and validation"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.blocked_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in config.blocked_patterns]
        self.safe_patterns = [re.compile(pattern) for pattern in config.safe_response_patterns]
        
    def sanitize_response(self, response: str) -> Dict[str, Any]:
        """Sanitize LLM response"""
        start_time = time.time()
        warnings = []
        is_safe = True
        confidence_score = 1.0
        
        try:
            # Check response length
            if len(response) > self.config.max_response_length:
                warnings.append(f"Response too long: {len(response)} > {self.config.max_response_length}")
                response = response[:self.config.max_response_length]
                confidence_score *= 0.8
            
            # Check for blocked patterns
            for pattern in self.blocked_patterns:
                if pattern.search(response):
                    warnings.append(f"Blocked pattern detected: {pattern.pattern}")
                    is_safe = False
                    confidence_score *= 0.3
                    # Remove the pattern
                    response = pattern.sub("[FILTERED]", response)
            
            # Check if response matches safe patterns
            if not any(pattern.match(response.strip()) for pattern in self.safe_patterns):
                warnings.append("Response doesn't match safe patterns")
                confidence_score *= 0.7
            
            # Additional safety checks
            if self._contains_suspicious_content(response):
                warnings.append("Suspicious content detected")
                is_safe = False
                confidence_score *= 0.5
            
            return {
                "sanitized_response": response,
                "is_safe": is_safe,
                "confidence_score": max(0.0, min(1.0, confidence_score)),
                "warnings": warnings,
                "processing_time_ms": (time.time() - start_time) * 1000
            }
            
        except Exception as e:
            return {
                "sanitized_response": "[ERROR]",
                "is_safe": False,
                "confidence_score": 0.0,
                "warnings": [f"Sanitization error: {str(e)}"],
                "processing_time_ms": (time.time() - start_time) * 1000
            }
    
    def _contains_suspicious_content(self, response: str) -> bool:
        """Check for suspicious content in response"""
        suspicious_indicators = [
            "execute",
            "run command",
            "system call",
            "file system",
            "network request",
            "database query",
            "admin access",
            "root privileges"
        ]
        
        response_lower = response.lower()
        return any(indicator in response_lower for indicator in suspicious_indicators)

class RateLimiter:
    """Rate limiter for LLM requests"""
    
    def __init__(self, rate_per_minute: int, burst_size: int):
        self.rate_per_minute = rate_per_minute
        self.burst_size = burst_size
        self.requests = deque()
        self.lock = threading.Lock()
        
    def is_allowed(self) -> bool:
        """Check if request is allowed under rate limit"""
        with self.lock:
            now = time.time()
            
            # Remove old requests (older than 1 minute)
            while self.requests and now - self.requests[0] > 60:
                self.requests.popleft()
            
            # Check if we can make a request
            if len(self.requests) < self.rate_per_minute:
                self.requests.append(now)
                return True
            
            return False
    
    def get_wait_time(self) -> float:
        """Get time to wait before next request"""
        with self.lock:
            if not self.requests:
                return 0.0
            
            oldest_request = self.requests[0]
            wait_time = 60 - (time.time() - oldest_request)
            return max(0.0, wait_time)

class SecureLLMClient(SecurityFirstComponent):
    """Security-first LLM client with built-in validation and sanitization"""
    
    def __init__(self, config: LLMConfig, security_level: SecurityLevel = SecurityLevel.MEDIUM):
        super().__init__("secure_llm_client", security_level)
        self.config = config
        self.validator = PromptValidator(config)
        self.sanitizer = ResponseSanitizer(config)
        self.rate_limiter = RateLimiter(config.rate_limit_per_minute, config.rate_limit_burst)
        self.client = None
        self.request_history = deque(maxlen=1000)
        
        # Initialize OpenAI client if available
        if OPENAI_AVAILABLE:
            openai.api_key = config.api_key
            self.client = openai
        else:
            self.logger.warning("OpenAI library not available, using fallback implementation")
            self.client = OpenAI()
    
    def _validate_input(self, data: Any, context: SecurityContext) -> SecurityResult:
        """Validate LLM request input"""
        if not isinstance(data, LLMRequest):
            return SecurityResult(
                success=False,
                message="Input must be LLMRequest",
                security_level=SecurityLevel.MEDIUM,
                processing_time_ms=0
            )
        
        # Validate model
        if data.model not in self.config.allowed_models:
            return SecurityResult(
                success=False,
                message=f"Model not allowed: {data.model}",
                security_level=SecurityLevel.MEDIUM,
                processing_time_ms=0
            )
        
        # Validate prompt
        return self.validator.validate_prompt(data.prompt)
    
    def _process_secure(self, data: LLMRequest, context: SecurityContext) -> LLMResponse:
        """Process LLM request securely"""
        start_time = time.time()
        
        # Rate limiting
        if not self.rate_limiter.is_allowed():
            wait_time = self.rate_limiter.get_wait_time()
            raise RateLimitExceededError(f"Rate limit exceeded. Wait {wait_time:.1f} seconds")
        
        try:
            # Make LLM request
            if OPENAI_AVAILABLE:
                response = self.client.ChatCompletion.create(
                    model=data.model,
                    messages=[{"role": "user", "content": data.prompt}],
                    max_tokens=data.max_tokens,
                    temperature=data.temperature
                )
                content = response.choices[0].message.content
            else:
                # Fallback response
                content = f"Test response for: {data.prompt[:50]}..."
            
            # Sanitize response
            sanitization_result = self.sanitizer.sanitize_response(content)
            
            # Create response
            response = LLMResponse(
                content=sanitization_result["sanitized_response"],
                model=data.model,
                request_id=data.request_id,
                timestamp=time.time(),
                processing_time_ms=(time.time() - start_time) * 1000,
                token_count=len(content.split()),
                is_safe=sanitization_result["is_safe"],
                confidence_score=sanitization_result["confidence_score"],
                warnings=sanitization_result["warnings"],
                metadata={
                    "original_length": len(content),
                    "sanitized_length": len(sanitization_result["sanitized_response"]),
                    "security_level": context.security_level.value
                }
            )
            
            # Record request in history
            self.request_history.append({
                "request": data,
                "response": response,
                "timestamp": time.time(),
                "context": context.request_id
            })
            
            return response
            
        except Exception as e:
            self.logger.error(f"LLM request failed: {str(e)}")
            raise SecurityError(f"LLM request failed: {str(e)}", SecurityLevel.HIGH)
    
    def create_request(self, prompt: str, model: str = None, **kwargs) -> LLMRequest:
        """Create a new LLM request"""
        return LLMRequest(
            prompt=prompt,
            model=model or self.config.model,
            max_tokens=kwargs.get('max_tokens', self.config.max_tokens),
            temperature=kwargs.get('temperature', self.config.temperature),
            request_id=f"llm_{int(time.time() * 1000)}",
            timestamp=time.time(),
            user_id=kwargs.get('user_id', 'anonymous'),
            session_id=kwargs.get('session_id', 'default'),
            security_level=kwargs.get('security_level', SecurityLevel.MEDIUM),
            metadata=kwargs.get('metadata', {})
        )
    
    def get_request_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent request history"""
        return list(self.request_history)[-limit:]
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get current rate limit status"""
        with self.rate_limiter.lock:
            current_requests = len(self.rate_limiter.requests)
            return {
                "current_requests": current_requests,
                "rate_limit": self.config.rate_per_minute,
                "burst_limit": self.config.rate_limit_burst,
                "is_limited": current_requests >= self.config.rate_per_minute,
                "wait_time": self.rate_limiter.get_wait_time()
            }

class SecureLLMManager:
    """Manager for multiple secure LLM clients"""
    
    def __init__(self):
        self.clients = {}
        import logging
        self.logger = logging.getLogger("secure_llm_manager")
    
    def create_client(self, name: str, config: LLMConfig) -> SecureLLMClient:
        """Create a new secure LLM client"""
        client = SecureLLMClient(config)
        self.clients[name] = client
        self.logger.info(f"Created LLM client: {name}")
        return client
    
    def get_client(self, name: str) -> Optional[SecureLLMClient]:
        """Get LLM client by name"""
        return self.clients.get(name)
    
    def remove_client(self, name: str):
        """Remove LLM client"""
        if name in self.clients:
            del self.clients[name]
            self.logger.info(f"Removed LLM client: {name}")
    
    def get_all_health_status(self) -> Dict[str, Any]:
        """Get health status of all clients"""
        status = {}
        for name, client in self.clients.items():
            status[name] = {
                "healthy": client.health_checker.is_healthy(),
                "metrics": client.metrics.get_stats(),
                "rate_limit": client.get_rate_limit_status()
            }
        return status

# Example usage and testing
if __name__ == "__main__":
    # Create LLM configuration
    config = LLMConfig(
        api_key="test_key_123",
        model="gpt-3.5-turbo",
        max_tokens=500,
        rate_limit_per_minute=30
    )
    
    # Create security context
    context = SecurityContext(
        user_id="test_user",
        session_id="test_session",
        security_level=SecurityLevel.MEDIUM,
        timestamp=time.time(),
        request_id="test_request_001"
    )
    
    # Create secure LLM client
    client = SecureLLMClient(config)
    
    # Test request creation and processing
    request = client.create_request("Generate a funky bassline")
    result = client.process(request, context)
    
    print(f"LLM response: {result.content}")
    print(f"Response safe: {result.is_safe}")
    print(f"Confidence score: {result.confidence_score}")
    print(f"Client health: {client.health_checker.is_healthy()}")
    print(f"Rate limit status: {client.get_rate_limit_status()}")
