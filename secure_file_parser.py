"""
SecureFileParser - Security-First File Processing

This module implements secure file parsing with built-in validation,
sanitization, and safety monitoring for MIDI files and project data.
"""

import os
import json
import hashlib
import mimetypes
import tempfile
import shutil
from typing import Dict, List, Optional, Any, Union, BinaryIO
from dataclasses import dataclass
from pathlib import Path
import time

from security_first_architecture import (
    SecurityFirstComponent, SecurityContext, SecurityResult, SecurityLevel,
    SecurityError, InputValidationError, SystemUnhealthyError
)

try:
    import mido
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    # Fallback for basic file operations
    class MidiFile:
        def __init__(self, *args, **kwargs):
            pass
        def save(self, *args, **kwargs):
            pass

@dataclass
class FileInfo:
    """File information with security metadata"""
    path: str
    size: int
    mime_type: str
    hash: str
    created_time: float
    modified_time: float
    is_safe: bool
    security_level: SecurityLevel
    metadata: Dict[str, Any]

@dataclass
class ParseResult:
    """Result of file parsing operation"""
    success: bool
    data: Any
    file_info: FileInfo
    warnings: List[str]
    errors: List[str]
    processing_time_ms: float

@dataclass
class FileConfig:
    """File processing configuration with security settings"""
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: List[str] = None
    blocked_extensions: List[str] = None
    allowed_mime_types: List[str] = None
    blocked_mime_types: List[str] = None
    max_track_count: int = 64
    max_note_count: int = 10000
    temp_dir: Optional[str] = None
    enable_quarantine: bool = True
    quarantine_dir: Optional[str] = None
    
    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = ['.mid', '.midi', '.json', '.txt']
        if self.blocked_extensions is None:
            self.blocked_extensions = ['.exe', '.bat', '.cmd', '.scr', '.pif']
        if self.allowed_mime_types is None:
            self.allowed_mime_types = [
                'audio/midi', 'audio/mid', 'application/json', 'text/plain'
            ]
        if self.blocked_mime_types is None:
            self.blocked_mime_types = [
                'application/x-executable', 'application/x-msdownload'
            ]
        if self.temp_dir is None:
            self.temp_dir = tempfile.gettempdir()
        if self.quarantine_dir is None:
            self.quarantine_dir = os.path.join(self.temp_dir, "quarantine")

class FileValidator:
    """File validation with security checks"""
    
    def __init__(self, config: FileConfig):
        self.config = config
        
    def validate_file(self, file_path: str) -> SecurityResult:
        """Validate file for security"""
        start_time = time.time()
        
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return SecurityResult(
                    success=False,
                    message=f"File does not exist: {file_path}",
                    security_level=SecurityLevel.MEDIUM,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > self.config.max_file_size:
                return SecurityResult(
                    success=False,
                    message=f"File too large: {file_size} > {self.config.max_file_size}",
                    security_level=SecurityLevel.MEDIUM,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            # Check file extension
            file_ext = Path(file_path).suffix.lower()
            if file_ext in self.config.blocked_extensions:
                return SecurityResult(
                    success=False,
                    message=f"Blocked file extension: {file_ext}",
                    security_level=SecurityLevel.HIGH,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            if file_ext not in self.config.allowed_extensions:
                return SecurityResult(
                    success=False,
                    message=f"File extension not allowed: {file_ext}",
                    security_level=SecurityLevel.MEDIUM,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            # Check MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type in self.config.blocked_mime_types:
                return SecurityResult(
                    success=False,
                    message=f"Blocked MIME type: {mime_type}",
                    security_level=SecurityLevel.HIGH,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            if mime_type and mime_type not in self.config.allowed_mime_types:
                return SecurityResult(
                    success=False,
                    message=f"MIME type not allowed: {mime_type}",
                    security_level=SecurityLevel.MEDIUM,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            return SecurityResult(
                success=True,
                message="File validation successful",
                security_level=SecurityLevel.LOW,
                processing_time_ms=(time.time() - start_time) * 1000
            )
            
        except Exception as e:
            return SecurityResult(
                success=False,
                message=f"File validation error: {str(e)}",
                security_level=SecurityLevel.HIGH,
                processing_time_ms=(time.time() - start_time) * 1000
            )

class FileSanitizer:
    """File content sanitization"""
    
    def __init__(self, config: FileConfig):
        self.config = config
        
    def sanitize_midi_file(self, file_path: str) -> ParseResult:
        """Sanitize MIDI file content"""
        start_time = time.time()
        warnings = []
        errors = []
        
        try:
            if not MIDO_AVAILABLE:
                return ParseResult(
                    success=False,
                    data=None,
                    file_info=None,
                    warnings=warnings,
                    errors=["mido library not available"],
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            # Load MIDI file
            midi_file = mido.MidiFile(file_path)
            
            # Validate track count
            if len(midi_file.tracks) > self.config.max_track_count:
                warnings.append(f"Track count exceeds limit: {len(midi_file.tracks)} > {self.config.max_track_count}")
            
            # Count total notes
            total_notes = 0
            for track in midi_file.tracks:
                for msg in track:
                    if msg.type == 'note_on' and msg.velocity > 0:
                        total_notes += 1
            
            if total_notes > self.config.max_note_count:
                warnings.append(f"Note count exceeds limit: {total_notes} > {self.config.max_note_count}")
            
            # Sanitize track data
            sanitized_tracks = []
            for i, track in enumerate(midi_file.tracks):
                sanitized_track = self._sanitize_track(track, i)
                sanitized_tracks.append(sanitized_track)
            
            # Create sanitized MIDI file
            sanitized_midi = mido.MidiFile()
            sanitized_midi.ticks_per_beat = midi_file.ticks_per_beat
            sanitized_midi.tracks = sanitized_tracks
            
            # Get file info
            file_info = self._get_file_info(file_path)
            
            return ParseResult(
                success=True,
                data=sanitized_midi,
                file_info=file_info,
                warnings=warnings,
                errors=errors,
                processing_time_ms=(time.time() - start_time) * 1000
            )
            
        except Exception as e:
            return ParseResult(
                success=False,
                data=None,
                file_info=None,
                warnings=warnings,
                errors=[f"MIDI sanitization error: {str(e)}"],
                processing_time_ms=(time.time() - start_time) * 1000
            )
    
    def _sanitize_track(self, track, track_index: int):
        """Sanitize individual MIDI track"""
        sanitized_track = mido.MidiTrack()
        
        for msg in track:
            # Skip potentially dangerous messages
            if msg.type in ['sysex', 'unknown']:
                continue
            
            # Validate message parameters
            if hasattr(msg, 'channel') and not (0 <= msg.channel <= 15):
                continue
            
            if hasattr(msg, 'velocity') and not (0 <= msg.velocity <= 127):
                continue
            
            if hasattr(msg, 'note') and not (0 <= msg.note <= 127):
                continue
            
            sanitized_track.append(msg)
        
        return sanitized_track
    
    def _get_file_info(self, file_path: str) -> FileInfo:
        """Get file information with security metadata"""
        stat = os.stat(file_path)
        
        # Calculate file hash
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        return FileInfo(
            path=file_path,
            size=stat.st_size,
            mime_type=mime_type or "application/octet-stream",
            hash=file_hash,
            created_time=stat.st_ctime,
            modified_time=stat.st_mtime,
            is_safe=True,  # Will be updated based on validation
            security_level=SecurityLevel.LOW,
            metadata={}
        )

class QuarantineManager:
    """File quarantine management for suspicious files"""
    
    def __init__(self, quarantine_dir: str):
        self.quarantine_dir = quarantine_dir
        os.makedirs(quarantine_dir, exist_ok=True)
    
    def quarantine_file(self, file_path: str, reason: str) -> str:
        """Move file to quarantine"""
        filename = os.path.basename(file_path)
        quarantine_path = os.path.join(
            self.quarantine_dir,
            f"{int(time.time())}_{filename}"
        )
        
        try:
            shutil.move(file_path, quarantine_path)
            
            # Create quarantine log
            log_path = quarantine_path + ".log"
            with open(log_path, 'w') as f:
                f.write(f"Quarantined: {file_path}\n")
                f.write(f"Reason: {reason}\n")
                f.write(f"Time: {time.ctime()}\n")
            
            return quarantine_path
            
        except Exception as e:
            raise SecurityError(f"Failed to quarantine file: {str(e)}", SecurityLevel.HIGH)

class SecureFileParser(SecurityFirstComponent):
    """Security-first file parser with built-in validation and sanitization"""
    
    def __init__(self, config: FileConfig, security_level: SecurityLevel = SecurityLevel.MEDIUM):
        super().__init__("secure_file_parser", security_level)
        self.config = config
        self.validator = FileValidator(config)
        self.sanitizer = FileSanitizer(config)
        self.quarantine_manager = QuarantineManager(config.quarantine_dir)
        self.parsed_files = {}
        
    def _validate_input(self, data: Any, context: SecurityContext) -> SecurityResult:
        """Validate file input"""
        if not isinstance(data, (str, Path)):
            return SecurityResult(
                success=False,
                message="Input must be file path (str or Path)",
                security_level=SecurityLevel.MEDIUM,
                processing_time_ms=0
            )
        
        file_path = str(data)
        return self.validator.validate_file(file_path)
    
    def _process_secure(self, data: Any, context: SecurityContext) -> ParseResult:
        """Process file securely"""
        file_path = str(data)
        
        # Get file info
        file_info = self.sanitizer._get_file_info(file_path)
        
        # Determine file type and parse accordingly
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext in ['.mid', '.midi']:
            return self._parse_midi_file(file_path, file_info)
        elif file_ext == '.json':
            return self._parse_json_file(file_path, file_info)
        elif file_ext == '.txt':
            return self._parse_text_file(file_path, file_info)
        else:
            return ParseResult(
                success=False,
                data=None,
                file_info=file_info,
                warnings=[],
                errors=[f"Unsupported file type: {file_ext}"],
                processing_time_ms=0
            )
    
    def _parse_midi_file(self, file_path: str, file_info: FileInfo) -> ParseResult:
        """Parse MIDI file with sanitization"""
        return self.sanitizer.sanitize_midi_file(file_path)
    
    def _parse_json_file(self, file_path: str, file_info: FileInfo) -> ParseResult:
        """Parse JSON file with validation"""
        start_time = time.time()
        warnings = []
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Basic JSON validation
            if not isinstance(data, (dict, list)):
                errors.append("JSON root must be object or array")
            
            # Check for suspicious patterns
            if isinstance(data, dict):
                suspicious_keys = ['eval', 'exec', 'system', 'shell']
                for key in data.keys():
                    if any(sus in key.lower() for sus in suspicious_keys):
                        warnings.append(f"Suspicious key found: {key}")
            
            return ParseResult(
                success=len(errors) == 0,
                data=data,
                file_info=file_info,
                warnings=warnings,
                errors=errors,
                processing_time_ms=(time.time() - start_time) * 1000
            )
            
        except json.JSONDecodeError as e:
            return ParseResult(
                success=False,
                data=None,
                file_info=file_info,
                warnings=warnings,
                errors=[f"JSON decode error: {str(e)}"],
                processing_time_ms=(time.time() - start_time) * 1000
            )
        except Exception as e:
            return ParseResult(
                success=False,
                data=None,
                file_info=file_info,
                warnings=warnings,
                errors=[f"JSON parse error: {str(e)}"],
                processing_time_ms=(time.time() - start_time) * 1000
            )
    
    def _parse_text_file(self, file_path: str, file_info: FileInfo) -> ParseResult:
        """Parse text file with basic validation"""
        start_time = time.time()
        warnings = []
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for suspicious content
            suspicious_patterns = ['<script', 'javascript:', 'eval(', 'exec(']
            for pattern in suspicious_patterns:
                if pattern in content.lower():
                    warnings.append(f"Suspicious pattern found: {pattern}")
            
            return ParseResult(
                success=True,
                data=content,
                file_info=file_info,
                warnings=warnings,
                errors=errors,
                processing_time_ms=(time.time() - start_time) * 1000
            )
            
        except Exception as e:
            return ParseResult(
                success=False,
                data=None,
                file_info=file_info,
                warnings=warnings,
                errors=[f"Text parse error: {str(e)}"],
                processing_time_ms=(time.time() - start_time) * 1000
            )
    
    def quarantine_file(self, file_path: str, reason: str) -> str:
        """Quarantine a suspicious file"""
        return self.quarantine_manager.quarantine_file(file_path, reason)
    
    def get_parsed_files(self) -> Dict[str, ParseResult]:
        """Get all parsed files"""
        return self.parsed_files.copy()
    
    def clear_parsed_files(self):
        """Clear parsed files cache"""
        self.parsed_files.clear()

class SecureFileManager:
    """Manager for multiple secure file parsers"""
    
    def __init__(self):
        self.parsers = {}
        import logging
        self.logger = logging.getLogger("secure_file_manager")
    
    def create_parser(self, name: str, config: FileConfig) -> SecureFileParser:
        """Create a new secure file parser"""
        parser = SecureFileParser(config)
        self.parsers[name] = parser
        self.logger.info(f"Created file parser: {name}")
        return parser
    
    def get_parser(self, name: str) -> Optional[SecureFileParser]:
        """Get file parser by name"""
        return self.parsers.get(name)
    
    def remove_parser(self, name: str):
        """Remove file parser"""
        if name in self.parsers:
            del self.parsers[name]
            self.logger.info(f"Removed file parser: {name}")
    
    def get_all_health_status(self) -> Dict[str, Any]:
        """Get health status of all parsers"""
        status = {}
        for name, parser in self.parsers.items():
            status[name] = {
                "healthy": parser.health_checker.is_healthy(),
                "metrics": parser.metrics.get_stats()
            }
        return status

# Example usage and testing
if __name__ == "__main__":
    # Create file configuration
    config = FileConfig(
        max_file_size=5 * 1024 * 1024,  # 5MB
        allowed_extensions=['.mid', '.midi', '.json'],
        temp_dir="/tmp/secure_parsing"
    )
    
    # Create security context
    context = SecurityContext(
        user_id="test_user",
        session_id="test_session",
        security_level=SecurityLevel.MEDIUM,
        timestamp=time.time(),
        request_id="test_request_001"
    )
    
    # Create secure file parser
    parser = SecureFileParser(config)
    
    # Test file parsing (would need actual file)
    print("SecureFileParser initialized successfully")
    print(f"Parser health: {parser.health_checker.is_healthy()}")
    print(f"Parser metrics: {parser.metrics.get_stats()}")
