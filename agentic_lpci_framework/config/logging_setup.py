"""
Logging Setup for LPCI Framework
Configures structured logging with security considerations
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from .settings import LoggingConfig


class SecurityAwareFormatter(logging.Formatter):
    """
    Custom formatter that masks sensitive data in log messages
    """
    
    def __init__(self, *args, mask_sensitive=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.mask_sensitive = mask_sensitive
        
        # Patterns to mask
        self.sensitive_patterns = [
            ('api_key', r'(api_key["\']?\s*[:=]\s*["\']?)([^"\'\s]+)'),
            ('password', r'(password["\']?\s*[:=]\s*["\']?)([^"\'\s]+)'),
            ('token', r'(token["\']?\s*[:=]\s*["\']?)([^"\'\s]+)'),
            ('secret', r'(secret["\']?\s*[:=]\s*["\']?)([^"\'\s]+)'),
            ('auth', r'(authorization["\']?\s*[:=]\s*["\']?)([^"\'\s]+)'),
        ]
    
    def format(self, record):
        # First, apply standard formatting
        formatted_message = super().format(record)
        
        # Then mask sensitive data if enabled
        if self.mask_sensitive:
            formatted_message = self._mask_sensitive_data(formatted_message)
        
        return formatted_message
    
    def _mask_sensitive_data(self, message: str) -> str:
        """Mask sensitive data in log messages"""
        import re
        
        for pattern_name, pattern in self.sensitive_patterns:
            # Replace sensitive values with masked version
            def replace_func(match):
                prefix = match.group(1)
                value = match.group(2)
                if len(value) > 8:
                    masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:]
                else:
                    masked_value = '*' * len(value)
                return prefix + masked_value
            
            message = re.sub(pattern, replace_func, message, flags=re.IGNORECASE)
        
        return message

class AuditLogger:
    """
    Specialized logger for audit trail and security events
    """
    
    def __init__(self, name: str = "lpci_audit"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create audit-specific formatter
        audit_formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(levelname)s - %(message)s'
        )
        
        # Create file handler for audit logs
        audit_file = Path("lpci_audit.log")
        audit_handler = logging.handlers.RotatingFileHandler(
            audit_file, maxBytes=10*1024*1024, backupCount=10
        )
        audit_handler.setFormatter(audit_formatter)
        
        self.logger.addHandler(audit_handler)
    
    def log_test_execution(self, session_id: str, model_name: str, 
                         attack_vector: str, result: str, payload_id: str):
        """Log test execution for audit trail"""
        self.logger.info(
            f"TEST_EXECUTION - Session: {session_id}, Model: {model_name}, "
            f"Attack: {attack_vector}, Result: {result}, Payload: {payload_id}"
        )
    
    def log_payload_generation(self, payload_id: str, attack_vector: str, 
                             risk_level: str, agent_id: str):
        """Log payload generation for audit trail"""
        self.logger.info(
            f"PAYLOAD_GENERATED - ID: {payload_id}, Vector: {attack_vector}, "
            f"Risk: {risk_level}, Agent: {agent_id}"
        )
    
    def log_vulnerability_detected(self, session_id: str, model_name: str, 
                                 attack_vector: str, indicators: list):
        """Log vulnerability detection for audit trail"""
        self.logger.warning(
            f"VULNERABILITY_DETECTED - Session: {session_id}, Model: {model_name}, "
            f"Attack: {attack_vector}, Indicators: {indicators}"
        )
    
    def log_security_event(self, event_type: str, details: str, severity: str = "INFO"):
        """Log general security events"""
        log_method = getattr(self.logger, severity.lower(), self.logger.info)
        log_method(f"SECURITY_EVENT - Type: {event_type}, Details: {details}")

class LoggingManager:
    """
    Manages logging configuration and setup for the LPCI Framework
    """
    
    def __init__(self, config: LoggingConfig):
        self.config = config
        self.audit_logger = None
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        # Create logs directory if it doesn't exist
        if self.config.file_path:
            log_path = Path(self.config.file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.config.level.upper()))
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create formatter
        formatter = SecurityAwareFormatter(
            fmt=self.config.format,
            mask_sensitive=True
        )
        
        # Console handler
        if self.config.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, self.config.level.upper()))
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # File handler
        if self.config.file_path:
            file_handler = logging.handlers.RotatingFileHandler(
                self.config.file_path,
                maxBytes=self.config.max_file_size,
                backupCount=self.config.backup_count
            )
            file_handler.setLevel(getattr(logging, self.config.level.upper()))
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        # Setup audit logger
        self.audit_logger = AuditLogger()
        
        # Log initialization
        logger = logging.getLogger(__name__)
        logger.info("LPCI Framework logging initialized")
        logger.info(f"Log level: {self.config.level}")
        logger.info(f"Log file: {self.config.file_path}")
        logger.info(f"Console output: {self.config.console_output}")
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger with the specified name"""
        return logging.getLogger(name)
    
    def get_audit_logger(self) -> AuditLogger:
        """Get the audit logger"""
        return self.audit_logger
    
    def log_framework_start(self, version: str, config_path: str):
        """Log framework startup"""
        logger = logging.getLogger("lpci_framework")
        logger.info(f"Starting LPCI Framework v{version}")
        logger.info(f"Configuration loaded from: {config_path}")
        logger.info(f"Process ID: {os.getpid()}")
        logger.info(f"Start time: {datetime.now().isoformat()}")
    
    def log_framework_stop(self):
        """Log framework shutdown"""
        logger = logging.getLogger("lpci_framework")
        logger.info("LPCI Framework shutting down")
        logger.info(f"Stop time: {datetime.now().isoformat()}")
    
    def log_test_session_start(self, session_id: str, models: list, test_count: int):
        """Log test session start"""
        logger = logging.getLogger("lpci_testing")
        logger.info(f"Starting test session: {session_id}")
        logger.info(f"Target models: {models}")
        logger.info(f"Test count: {test_count}")
        
        # Audit log
        if self.audit_logger:
            self.audit_logger.logger.info(
                f"TEST_SESSION_START - Session: {session_id}, "
                f"Models: {models}, Tests: {test_count}"
            )
    
    def log_test_session_end(self, session_id: str, total_tests: int, 
                           vulnerabilities_found: int):
        """Log test session end"""
        logger = logging.getLogger("lpci_testing")
        logger.info(f"Test session completed: {session_id}")
        logger.info(f"Total tests: {total_tests}")
        logger.info(f"Vulnerabilities found: {vulnerabilities_found}")
        
        # Audit log
        if self.audit_logger:
            self.audit_logger.logger.info(
                f"TEST_SESSION_END - Session: {session_id}, "
                f"Total: {total_tests}, Vulnerabilities: {vulnerabilities_found}"
            )
    
    def log_model_interaction(self, model_name: str, request_size: int, 
                            response_size: int, execution_time: float):
        """Log model interaction metrics"""
        logger = logging.getLogger("lpci_models")
        logger.debug(
            f"Model interaction - {model_name}: "
            f"Request: {request_size} chars, Response: {response_size} chars, "
            f"Time: {execution_time:.2f}s"
        )
    
    def log_attack_result(self, attack_vector: str, model_name: str, 
                        result: str, indicators: list, session_id: str):
        """Log attack result"""
        logger = logging.getLogger("lpci_attacks")
        
        if result == "blocked":
            logger.info(f"Attack blocked - {attack_vector} on {model_name}")
        elif result == "executed":
            logger.warning(f"Attack succeeded - {attack_vector} on {model_name}")
            logger.warning(f"Indicators: {indicators}")
        else:
            logger.info(f"Attack result: {result} - {attack_vector} on {model_name}")
        
        # Audit log for successful attacks
        if self.audit_logger and result == "executed":
            self.audit_logger.log_vulnerability_detected(
                session_id, model_name, attack_vector, indicators
            )
    
    def log_error(self, component: str, error: Exception, context: dict = None):
        """Log errors with context"""
        logger = logging.getLogger(f"lpci_{component}")
        logger.error(f"Error in {component}: {str(error)}")
        if context:
            logger.error(f"Context: {context}")
        logger.exception("Exception details:")
    
    def log_performance_metrics(self, metrics: dict):
        """Log performance metrics"""
        logger = logging.getLogger("lpci_performance")
        for metric, value in metrics.items():
            logger.info(f"Performance metric - {metric}: {value}")
    
    def set_log_level(self, level: str):
        """Dynamically change log level"""
        new_level = getattr(logging, level.upper())
        root_logger = logging.getLogger()
        root_logger.setLevel(new_level)
        
        # Update all handlers
        for handler in root_logger.handlers:
            handler.setLevel(new_level)
        
        logger = logging.getLogger(__name__)
        logger.info(f"Log level changed to: {level}")
    
    def flush_logs(self):
        """Flush all log handlers"""
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            handler.flush()
        
        if self.audit_logger:
            for handler in self.audit_logger.logger.handlers:
                handler.flush()

def setup_logging(config: LoggingConfig) -> LoggingManager:
    """Setup logging with the given configuration"""
    return LoggingManager(config)

# Module level functions for convenience
def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)

def get_audit_logger() -> Optional[AuditLogger]:
    """Get the audit logger if available"""
    # This would be set by the framework initialization
    return getattr(setup_logging, '_audit_logger', None)