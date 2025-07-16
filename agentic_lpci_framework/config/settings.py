"""
Configuration and Settings Management for LPCI Framework
Handles configuration loading, validation, and environment setup
"""

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml


@dataclass
class ModelConfig:
    """Configuration for individual AI models"""
    name: str
    api_key: str
    api_url: Optional[str] = None
    max_tokens: int = 1024
    temperature: float = 0.7
    timeout: int = 30
    rate_limit: float = 1.0
    enabled: bool = True
    custom_headers: Dict[str, str] = field(default_factory=dict)

@dataclass
class DatabaseConfig:
    """Configuration for database connections"""
    type: str = "sqlite"
    path: str = "lpci_framework.db"
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    pool_size: int = 5

@dataclass
class LoggingConfig:
    """Configuration for logging"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = "lpci_framework.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    console_output: bool = True

@dataclass
class TestingConfig:
    """Configuration for testing parameters"""
    default_test_count: int = 100
    max_concurrent_tests: int = 10
    test_timeout: int = 60
    retry_attempts: int = 3
    enable_memory_tests: bool = True
    complexity_levels: List[str] = field(default_factory=lambda: ["simple", "intermediate", "advanced"])

@dataclass
class SecurityConfig:
    """Configuration for security settings"""
    enable_payload_logging: bool = True
    mask_sensitive_data: bool = True
    audit_trail: bool = True
    max_payload_size: int = 10000  # characters
    allowed_encodings: List[str] = field(default_factory=lambda: ["base64", "hex", "unicode"])

@dataclass
class VisualizationConfig:
    """Configuration for visualization settings"""
    output_directory: str = "lpci_reports"
    chart_format: str = "png"
    chart_dpi: int = 300
    enable_interactive: bool = True
    color_scheme: str = "default"

@dataclass
class LPCIFrameworkConfig:
    """Main configuration class for LPCI Framework"""
    models: Dict[str, ModelConfig] = field(default_factory=dict)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    testing: TestingConfig = field(default_factory=TestingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)
    
    # Framework settings
    framework_name: str = "LPCI Security Testing Framework"
    version: str = "1.0.0"
    author: str = "Security Research Team"
    debug_mode: bool = False
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        # Validate models
        if not self.models:
            errors.append("No models configured")
        
        for model_name, model_config in self.models.items():
            if not model_config.api_key:
                errors.append(f"No API key configured for model: {model_name}")
            if model_config.max_tokens <= 0:
                errors.append(f"Invalid max_tokens for model {model_name}: {model_config.max_tokens}")
            if not 0 <= model_config.temperature <= 2:
                errors.append(f"Invalid temperature for model {model_name}: {model_config.temperature}")
        
        # Validate database
        if self.database.type == "sqlite":
            if not self.database.path:
                errors.append("SQLite database path is required")
        elif self.database.type == "postgresql":
            if not all([self.database.host, self.database.username, self.database.database]):
                errors.append("PostgreSQL requires host, username, and database")
        
        # Validate logging
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.logging.level not in valid_log_levels:
            errors.append(f"Invalid log level: {self.logging.level}")
        
        # Validate testing
        if self.testing.default_test_count <= 0:
            errors.append("Default test count must be positive")
        if self.testing.max_concurrent_tests <= 0:
            errors.append("Max concurrent tests must be positive")
        
        return errors

class ConfigManager:
    """Manages configuration loading, validation, and environment setup"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config_file()
        self.config: Optional[LPCIFrameworkConfig] = None
        self.logger = logging.getLogger(__name__)
        
        # Environment variable prefixes
        self.env_prefix = "LPCI_"
        
    def _find_config_file(self) -> Optional[str]:
        """Find configuration file in standard locations"""
        possible_paths = [
            "lpci_config.yaml",
            "lpci_config.yml",
            "lpci_config.json",
            "config/lpci_config.yaml",
            "config/lpci_config.yml",
            "config/lpci_config.json",
            os.path.expanduser("~/.lpci/config.yaml"),
            "/etc/lpci/config.yaml"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def load_config(self) -> LPCIFrameworkConfig:
        """Load configuration from file and environment variables"""
        # Start with default configuration
        config = LPCIFrameworkConfig()
        
        # Load from file if exists
        if self.config_path and os.path.exists(self.config_path):
            try:
                config = self._load_from_file(self.config_path)
                print(f"Configuration loaded from: {self.config_path}")
            except Exception as e:
                print(f"Error loading configuration file: {e}")
                print("Using default configuration")
        else:
            print("No configuration file found, using defaults")
        
        # Override with environment variables
        config = self._apply_env_overrides(config)
        
        # Validate configuration
        errors = config.validate()
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            raise ValueError("Configuration validation failed")
        
        self.config = config
        return config
    
    def _load_from_file(self, file_path: str) -> LPCIFrameworkConfig:
        """Load configuration from YAML or JSON file"""
        path = Path(file_path)
        
        with open(path, 'r') as f:
            if path.suffix.lower() in ['.yaml', '.yml']:
                try:
                    import yaml
                    data = yaml.safe_load(f)
                except ImportError:
                    raise ImportError("PyYAML is required for YAML config files. Install with: pip install pyyaml")
            elif path.suffix.lower() == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported config file format: {path.suffix}")
        
        return self._dict_to_config(data)
    
    def _dict_to_config(self, data: dict) -> LPCIFrameworkConfig:
        """Convert dictionary to configuration object"""
        config = LPCIFrameworkConfig()
        
        # Framework settings
        if 'framework_name' in data:
            config.framework_name = data['framework_name']
        if 'version' in data:
            config.version = data['version']
        if 'author' in data:
            config.author = data['author']
        if 'debug_mode' in data:
            config.debug_mode = data['debug_mode']
        
        # Models
        if 'models' in data:
            for model_name, model_data in data['models'].items():
                config.models[model_name] = ModelConfig(
                    name=model_name,
                    api_key=model_data.get('api_key', ''),
                    api_url=model_data.get('api_url'),
                    max_tokens=model_data.get('max_tokens', 1024),
                    temperature=model_data.get('temperature', 0.7),
                    timeout=model_data.get('timeout', 30),
                    rate_limit=model_data.get('rate_limit', 1.0),
                    enabled=model_data.get('enabled', True),
                    custom_headers=model_data.get('custom_headers', {})
                )
        
        # Database
        if 'database' in data:
            db_data = data['database']
            config.database = DatabaseConfig(
                type=db_data.get('type', 'sqlite'),
                path=db_data.get('path', 'lpci_framework.db'),
                host=db_data.get('host'),
                port=db_data.get('port'),
                username=db_data.get('username'),
                password=db_data.get('password'),
                database=db_data.get('database'),
                pool_size=db_data.get('pool_size', 5)
            )
        
        # Logging
        if 'logging' in data:
            log_data = data['logging']
            config.logging = LoggingConfig(
                level=log_data.get('level', 'INFO'),
                format=log_data.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                file_path=log_data.get('file_path', 'lpci_framework.log'),
                max_file_size=log_data.get('max_file_size', 10 * 1024 * 1024),
                backup_count=log_data.get('backup_count', 5),
                console_output=log_data.get('console_output', True)
            )
        
        # Testing
        if 'testing' in data:
            test_data = data['testing']
            config.testing = TestingConfig(
                default_test_count=test_data.get('default_test_count', 100),
                max_concurrent_tests=test_data.get('max_concurrent_tests', 10),
                test_timeout=test_data.get('test_timeout', 60),
                retry_attempts=test_data.get('retry_attempts', 3),
                enable_memory_tests=test_data.get('enable_memory_tests', True),
                complexity_levels=test_data.get('complexity_levels', ['simple', 'intermediate', 'advanced'])
            )
        
        # Security
        if 'security' in data:
            sec_data = data['security']
            config.security = SecurityConfig(
                enable_payload_logging=sec_data.get('enable_payload_logging', True),
                mask_sensitive_data=sec_data.get('mask_sensitive_data', True),
                audit_trail=sec_data.get('audit_trail', True),
                max_payload_size=sec_data.get('max_payload_size', 10000),
                allowed_encodings=sec_data.get('allowed_encodings', ['base64', 'hex', 'unicode'])
            )
        
        # Visualization
        if 'visualization' in data:
            viz_data = data['visualization']
            config.visualization = VisualizationConfig(
                output_directory=viz_data.get('output_directory', 'lpci_reports'),
                chart_format=viz_data.get('chart_format', 'png'),
                chart_dpi=viz_data.get('chart_dpi', 300),
                enable_interactive=viz_data.get('enable_interactive', True),
                color_scheme=viz_data.get('color_scheme', 'default')
            )
        
        return config
    
    def _apply_env_overrides(self, config: LPCIFrameworkConfig) -> LPCIFrameworkConfig:
        """Apply environment variable overrides"""
        # Framework settings
        config.debug_mode = self._get_env_bool("DEBUG_MODE", config.debug_mode)
        
        # Model API keys from environment
        for model_name in config.models:
            env_key = f"{self.env_prefix}{model_name.upper()}_API_KEY"
            if env_key in os.environ:
                config.models[model_name].api_key = os.environ[env_key]
        
        # Database settings
        config.database.path = os.environ.get(f"{self.env_prefix}DB_PATH", config.database.path)
        config.database.host = os.environ.get(f"{self.env_prefix}DB_HOST", config.database.host)
        config.database.username = os.environ.get(f"{self.env_prefix}DB_USERNAME", config.database.username)
        config.database.password = os.environ.get(f"{self.env_prefix}DB_PASSWORD", config.database.password)
        
        # Logging settings
        config.logging.level = os.environ.get(f"{self.env_prefix}LOG_LEVEL", config.logging.level)
        config.logging.file_path = os.environ.get(f"{self.env_prefix}LOG_FILE", config.logging.file_path)
        
        return config
    
    def _get_env_bool(self, key: str, default: bool) -> bool:
        """Get boolean value from environment variable"""
        env_key = f"{self.env_prefix}{key}"
        if env_key in os.environ:
            return os.environ[env_key].lower() in ('true', '1', 'yes', 'on')
        return default
    
    def save_config(self, config: LPCIFrameworkConfig, file_path: str):
        """Save configuration to file"""
        config_dict = self._config_to_dict(config)
        
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            if path.suffix.lower() in ['.yaml', '.yml']:
                try:
                    import yaml
                    yaml.dump(config_dict, f, default_flow_style=False, indent=2)
                except ImportError:
                    raise ImportError("PyYAML is required for YAML config files. Install with: pip install pyyaml")
            elif path.suffix.lower() == '.json':
                json.dump(config_dict, f, indent=2)
            else:
                raise ValueError(f"Unsupported config file format: {path.suffix}")
    
    def _config_to_dict(self, config: LPCIFrameworkConfig) -> dict:
        """Convert configuration object to dictionary"""
        return {
            'framework_name': config.framework_name,
            'version': config.version,
            'author': config.author,
            'debug_mode': config.debug_mode,
            'models': {
                name: {
                    'api_key': model.api_key,
                    'api_url': model.api_url,
                    'max_tokens': model.max_tokens,
                    'temperature': model.temperature,
                    'timeout': model.timeout,
                    'rate_limit': model.rate_limit,
                    'enabled': model.enabled,
                    'custom_headers': model.custom_headers
                }
                for name, model in config.models.items()
            },
            'database': {
                'type': config.database.type,
                'path': config.database.path,
                'host': config.database.host,
                'port': config.database.port,
                'username': config.database.username,
                'password': config.database.password,
                'database': config.database.database,
                'pool_size': config.database.pool_size
            },
            'logging': {
                'level': config.logging.level,
                'format': config.logging.format,
                'file_path': config.logging.file_path,
                'max_file_size': config.logging.max_file_size,
                'backup_count': config.logging.backup_count,
                'console_output': config.logging.console_output
            },
            'testing': {
                'default_test_count': config.testing.default_test_count,
                'max_concurrent_tests': config.testing.max_concurrent_tests,
                'test_timeout': config.testing.test_timeout,
                'retry_attempts': config.testing.retry_attempts,
                'enable_memory_tests': config.testing.enable_memory_tests,
                'complexity_levels': config.testing.complexity_levels
            },
            'security': {
                'enable_payload_logging': config.security.enable_payload_logging,
                'mask_sensitive_data': config.security.mask_sensitive_data,
                'audit_trail': config.security.audit_trail,
                'max_payload_size': config.security.max_payload_size,
                'allowed_encodings': config.security.allowed_encodings
            },
            'visualization': {
                'output_directory': config.visualization.output_directory,
                'chart_format': config.visualization.chart_format,
                'chart_dpi': config.visualization.chart_dpi,
                'enable_interactive': config.visualization.enable_interactive,
                'color_scheme': config.visualization.color_scheme
            }
        }
    
    def create_sample_config(self, file_path: str):
        """Create a sample configuration file"""
        sample_config = LPCIFrameworkConfig()
        
        # Add sample models
        sample_config.models = {
            'chatgpt': ModelConfig(
                name='chatgpt',
                api_key='your-openai-api-key-here',
                max_tokens=2048,
                temperature=0.7,
                enabled=True
            ),
            'claude': ModelConfig(
                name='claude',
                api_key='your-anthropic-api-key-here',
                max_tokens=2048,
                temperature=0.7,
                enabled=True
            ),
            'gemini': ModelConfig(
                name='gemini',
                api_key='your-google-api-key-here',
                max_tokens=2048,
                temperature=0.7,
                enabled=True
            )
        }
        
        self.save_config(sample_config, file_path)
        print(f"Sample configuration created at: {file_path}")
        print("Please update the API keys before running the framework.")

# Global configuration instance
config_manager = ConfigManager()